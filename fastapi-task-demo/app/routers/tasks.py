"""Task 路由：PostgreSQL 持久化 + Redis Cache-Aside / 限流。"""

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.task_cache import (
    delete_task_cache,
    get_cached_task,
    set_task_cache,
    set_task_not_found_cache,
)
from app.database.session import get_db
from app.dependencies.auth import verify_token
from app.dependencies.rate_limit import rate_limit
from app.exceptions.app_exception import AppException
from app.models.category import Category
from app.models.task import Task
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.task import (
    TaskCreate,
    TaskPageResponse,
    TaskResponse,
    TaskUpdate,
    TaskWithCategoryPageResponse,
)
from app.services.background import write_task_log


router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
    # 所有 /tasks 接口统一经过 Redis 限流。
    dependencies=[Depends(rate_limit)],
)


def task_not_found(task_id: int) -> AppException:
    """统一构造任务不存在异常。"""

    return AppException(
        status_code=404,
        code=40401,
        message="Task not found",
        data={"task_id": task_id},
    )


@router.get(
    "",
    response_model=TaskPageResponse,
    summary="分页查询任务列表",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        429: {
            "model": ErrorResponse,
            "description": "Redis 限流触发",
        },
    },
)
async def get_tasks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    """使用 PostgreSQL OFFSET / LIMIT 分页。

    第一版不缓存分页列表，因为创建/更新任务后需要失效大量不同分页 Key，
    缓存一致性成本明显高于单条 Task 缓存。
    """

    offset = (page - 1) * page_size

    total = await db.scalar(
        select(func.count(Task.id))
    )

    result = await db.execute(
        select(Task)
        .order_by(Task.id)
        .offset(offset)
        .limit(page_size)
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total or 0,
        "items": result.scalars().all(),
    }


@router.get(
    "/with-category",
    response_model=TaskWithCategoryPageResponse,
    summary="分页查询任务与分类（JOIN）",
)
async def get_tasks_with_category(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    """使用 LEFT OUTER JOIN 一次查询 Task 与 Category。"""

    offset = (page - 1) * page_size

    total = await db.scalar(
        select(func.count(Task.id))
    )

    statement = (
        select(
            Task.id,
            Task.title,
            Task.description,
            Task.completed,
            Task.priority,
            Task.category_id,
            Category.name.label("category_name"),
            Task.created_at,
        )
        .outerjoin(
            Category,
            Task.category_id == Category.id,
        )
        .order_by(Task.id)
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(statement)

    return {
        "page": page,
        "page_size": page_size,
        "total": total or 0,
        "items": result.mappings().all(),
    }


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="查询单个任务（Redis Cache-Aside）",
    description=(
        "先查 Redis；未命中再回源 PostgreSQL 并写回缓存。"
        "数据库不存在时写入短 TTL 的 __NULL__ 空值缓存以降低缓存穿透。"
    ),
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        404: {
            "model": ErrorResponse,
            "description": "任务不存在",
        },
        429: {
            "model": ErrorResponse,
            "description": "Redis 限流触发",
        },
    },
)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    # 1. 先查 Redis。
    cache_hit, cached_task = await get_cached_task(task_id)

    if cache_hit:
        # 命中 __NULL__：此前数据库已经确认不存在，无需再次访问 PostgreSQL。
        if cached_task is None:
            raise task_not_found(task_id)

        return cached_task

    # 2. Redis miss，再查 PostgreSQL。
    task = await db.get(Task, task_id)

    if task is None:
        # 3. 数据库也 miss：短 TTL 空值缓存，降低恶意/重复不存在 ID 的穿透。
        await set_task_not_found_cache(task_id)
        raise task_not_found(task_id)

    # 4. 数据库命中：把响应模型转换成 JSON 可序列化 dict 写回 Redis。
    task_data = TaskResponse.model_validate(task).model_dump(
        mode="json"
    )

    await set_task_cache(
        task_id,
        task_data,
    )

    return task


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201,
    summary="创建任务（事务）",
    description=(
        "如果 category_name 不存在，会先创建分类，再创建任务。"
        "两个数据库操作属于同一个事务：全部成功才提交，任何一步失败都会回滚。"
    ),
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        429: {
            "model": ErrorResponse,
            "description": "Redis 限流触发",
        },
    },
)
async def create_task(
    data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    async with db.begin():
        category_id: int | None = None

        if data.category_name is not None:
            category = await db.scalar(
                select(Category).where(
                    Category.name == data.category_name
                )
            )

            if category is None:
                category = Category(
                    name=data.category_name,
                )
                db.add(category)

                # flush 执行 INSERT 并拿到主键，但仍处于事务中，可以回滚。
                await db.flush()

            category_id = category.id

        task = Task(
            title=data.title,
            description=data.description,
            completed=data.completed,
            priority=data.priority,
            category_id=category_id,
        )
        db.add(task)
        await db.flush()

        task_id = task.id

    # begin 正常退出后 PostgreSQL 已 COMMIT。
    await db.refresh(task)

    # 如果这个未来 ID 曾被恶意请求并写成 __NULL__，创建成功后主动清掉。
    await delete_task_cache(task_id)

    background_tasks.add_task(
        write_task_log,
        f"Created task: {task_id}",
    )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="更新任务并失效 Redis 缓存",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        404: {
            "model": ErrorResponse,
            "description": "任务或分类不存在",
        },
        429: {
            "model": ErrorResponse,
            "description": "Redis 限流触发",
        },
    },
)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    async with db.begin():
        task = await db.get(Task, task_id)

        if task is None:
            raise task_not_found(task_id)

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if "category_id" in update_data:
            category_id = update_data["category_id"]

            if category_id is not None:
                category = await db.get(
                    Category,
                    category_id,
                )

                if category is None:
                    raise AppException(
                        status_code=404,
                        code=40402,
                        message="Category not found",
                        data={"category_id": category_id},
                    )

        for field_name, value in update_data.items():
            setattr(task, field_name, value)

        await db.flush()

    # 先保证 PostgreSQL COMMIT，再删除 Redis；下次 GET 会回源并重建缓存。
    await delete_task_cache(task_id)

    await db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="删除任务并失效 Redis 缓存",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        404: {
            "model": ErrorResponse,
            "description": "任务不存在",
        },
        429: {
            "model": ErrorResponse,
            "description": "Redis 限流触发",
        },
    },
)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    async with db.begin():
        task = await db.get(Task, task_id)

        if task is None:
            raise task_not_found(task_id)

        await db.delete(task)

    # 数据库删除已经提交，再删除缓存，避免继续读到旧 Task。
    await delete_task_cache(task_id)

    return {
        "message": "Task deleted"
    }
