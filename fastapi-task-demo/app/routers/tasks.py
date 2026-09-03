"""Task 相关 HTTP 路由：PostgreSQL + SQLAlchemy 异步版本。"""

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.dependencies.auth import verify_token
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
    },
)
async def get_tasks(
    # page 从 1 开始；page_size 最大限制 100，防止一次请求拉取过多数据。
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    # OFFSET = (页码 - 1) * 每页数量。
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
    """使用 LEFT OUTER JOIN 一次查询 Task 与 Category。

    使用 LEFT JOIN 而不是 INNER JOIN，是为了让没有分类的 Task 也能返回。
    """

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
        # mappings() 把每一行变成类似 dict 的映射，字段名与响应模型对应。
        "items": result.mappings().all(),
    }


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="查询单个任务",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        404: {
            "model": ErrorResponse,
            "description": "任务不存在",
        },
    },
)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    task = await db.get(Task, task_id)

    if task is None:
        raise task_not_found(task_id)

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
    },
)
async def create_task(
    data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_token),
):
    # async with db.begin() 就是明确的事务边界。
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

                # flush 会执行 INSERT 并拿到主键，但不会提交事务。
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

    # begin 正常结束后已经 COMMIT。
    await db.refresh(task)

    background_tasks.add_task(
        write_task_log,
        f"Created task: {task_id}",
    )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="更新任务",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        404: {
            "model": ErrorResponse,
            "description": "任务或分类不存在",
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

        # 如果客户端真的传了 category_id，并且不是 null，先检查外键目标是否存在。
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

    await db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="删除任务",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
        404: {
            "model": ErrorResponse,
            "description": "任务不存在",
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

    return {
        "message": "Task deleted"
    }
