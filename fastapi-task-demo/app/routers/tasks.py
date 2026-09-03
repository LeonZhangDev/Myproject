"""Task 相关 HTTP 路由。

routers 层主要负责接收请求、调用公共依赖/业务逻辑并返回响应；Pydantic 模型、异常、数据和后台任务分别放在其他模块。
"""

from fastapi import APIRouter, BackgroundTasks, Depends

from app.data.task_store import tasks
from app.dependencies.auth import verify_token
from app.exceptions.app_exception import AppException
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.background import write_task_log


# prefix="/tasks" 表示：这个文件所有接口统一以 /tasks 开头。
#
# 所以：
# @router.get("")          -> GET /tasks
# @router.get("/{task_id}") -> GET /tasks/{task_id}
#
# 第一个参数写空字符串不是“没有路径”，
# 而是表示只使用 APIRouter 自己的 prefix。
router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
)


@router.get(
    "",

    # response_model 会校验并描述接口最终返回的数据结构。
    response_model=list[TaskResponse],

    # summary / responses 会显示在 /docs Swagger 文档里。
    summary="查询任务列表",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
    },
)
def get_tasks(
    # skip 和 limit 是查询参数：
    # GET /tasks?skip=0&limit=10
    skip: int = 0,
    limit: int = 10,

    # Depends(verify_token) 表示：
    # 在真正执行 get_tasks 前，FastAPI 先执行 verify_token。
    token: str = Depends(verify_token),
):
    # list[start:end] 是 Python 切片。
    # 例如 skip=10, limit=5 -> tasks[10:15]
    return tasks[skip:skip + limit]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="查询单个任务",
    description="""
根据任务 ID 查询任务。

- 需要提供合法 `X-Token`
- `task_id` 必须是整数
- 任务不存在返回 `404`
""",
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
def get_task(
    # 路由里写了 /{task_id}，函数参数里就接收 task_id。
    # int 会让 FastAPI 自动校验它必须是整数。
    task_id: int,
    token: str = Depends(verify_token),
):
    for task in tasks:
        if task["id"] == task_id:
            return task

    # 找完整个列表都没找到，抛出业务异常。
    raise AppException(
        status_code=404,
        code=40401,
        message="Task not found",
        data={
            "task_id": task_id,
        },
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=201,
    summary="创建任务",
    description="创建一个新的任务。",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
    },
)
def create_task(
    # data: TaskCreate 表示请求体必须符合 TaskCreate 模型。
    data: TaskCreate,

    # FastAPI 会自动给我们提供 BackgroundTasks 对象。
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    # 找当前最大的 id，再 +1，生成新任务 id。
    # default=0 解决 tasks 为空时 max() 无值的问题。
    next_id = max(
        [task["id"] for task in tasks],
        default=0,
    ) + 1

    # model_dump() 把 Pydantic 模型转换成普通 dict。
    # ** 是字典解包，把 title / description / completed 放进新字典。
    task = {
        "id": next_id,
        **data.model_dump(),
    }
    tasks.append(task)
    background_tasks.add_task(
        write_task_log,
        f"Created task: {next_id}",
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
            "description": "任务不存在",
        },
    },
)
def update_task(
    task_id: int,
    data: TaskUpdate,
    token: str = Depends(verify_token),
):
    for task in tasks:
        if task["id"] == task_id:
            # exclude_unset=True：
            # 只导出客户端“实际传进来”的字段。
            # 这样用户只传 title 时，不会把其他字段误更新成 None。
            update_data = data.model_dump(
                exclude_unset=True,
            )

            # dict.update() 用新字典里的键值更新原字典。
            task.update(update_data)
            return task

    raise AppException(
        status_code=404,
        code=40401,
        message="Task not found",
        data={
            "task_id": task_id,
        },
    )


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
def delete_task(
    task_id: int,
    token: str = Depends(verify_token),
):
    # enumerate(tasks) 同时拿到：
    # index = 列表位置；task = 当前任务字典。
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            # pop(index) 会直接从列表中删除该位置的完整任务对象。
            tasks.pop(index)
            return {
                "message": "Task deleted"
            }

    raise AppException(
        status_code=404,
        code=40401,
        message="Task not found",
        data={
            "task_id": task_id,
        },
    )
