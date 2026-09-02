import time
from typing import Any
from pathlib import Path
from fastapi import (
    FastAPI,
    Request,
    Header,
    Depends,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from fastapi import UploadFile

app = FastAPI(
    title="Task API",
    description="""
一个用于学习 FastAPI 的任务管理项目。

## 功能

- 创建任务
- 查询任务
- 更新任务
- 删除任务
- Token 校验
- 全局异常处理
""",
    version="1.0.0",
)

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MAX_FILE_SIZE = 5 * 1024 * 1024

# ==========================
# CORS
# ==========================

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,

    # 哪些前端地址允许访问
    allow_origins=origins,

    # 是否允许 Cookie、Authorization 等凭证
    allow_credentials=True,

    # 允许哪些 HTTP 方法
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],

    # 前端允许发送哪些 Header
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Token",
    ],

    # 前端 JS 可以读取哪些响应 Header
    expose_headers=[
        "X-Process-Time",
    ],
)


# ==========================
# 请求日志 Middleware
# ==========================

@app.middleware("http")
async def request_log_middleware(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    )

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time:.4f}s"
    )

    response.headers["X-Process-Time"] = (
        f"{process_time:.4f}"
    )

    return response


# ==========================
# Pydantic 模型
# ==========================

class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    completed: bool | None = None

class TaskResponse(BaseModel):

    id: int

    title: str

    description: str | None = None

    completed: bool


class ErrorResponse(BaseModel):

    code: int

    message: str

    data: Any = None

# ==========================
# 模拟数据库
# ==========================

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "学习 FastAPI",
        "completed": False,
    },
    {
        "id": 2,
        "title": "Learn Pydantic",
        "description": "学习 Pydantic",
        "completed": True,
    },
]


# ==========================
# 通用业务异常
# ==========================

class AppException(Exception):

    def __init__(
        self,
        status_code: int,
        code: int,
        message: str,
        data: Any = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.data = data


# ==========================
# 业务异常处理器
# ==========================

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
        },
    )


# ==========================
# 参数校验异常
# ==========================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "code": 42201,
            "message": "Request validation failed",
            "data": exc.errors(),
        },
    )


# ==========================
# Token 依赖
# ==========================

def verify_token(
    x_token: str | None = Header(
        default=None
    ),
):
    if x_token != "dev-token":

        raise AppException(
            status_code=401,
            code=40101,
            message="Invalid token",
        )

    return x_token


# ==========================
# 查询任务
# ==========================

@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    summary="查询任务列表",
    tags=["Task"],
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
    },
)
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    token: str = Depends(verify_token),
):
    return tasks[skip:skip + limit]


@app.get(
    "/tasks/{task_id}",

    response_model=TaskResponse,

    summary="查询单个任务",

    description="""
根据任务 ID 查询任务。

- 需要提供合法 `X-Token`
- `task_id` 必须是整数
- 任务不存在返回 `404`
""",

    tags=["Task"],

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
    task_id: int,
    token: str = Depends(verify_token),
):
    for task in tasks:

        if task["id"] == task_id:
            return task

    raise AppException(
        status_code=404,
        code=40401,
        message="Task not found",
        data={
            "task_id": task_id,
        },
    )


# ==========================
# 创建任务
# ==========================

@app.post(
    "/tasks",

    response_model=TaskResponse,

    status_code=201,

    summary="创建任务",

    description="创建一个新的任务。",

    tags=["Task"],

    responses={
        401: {
            "model": ErrorResponse,
            "description": "Token 无效",
        },
    },
)
def create_task(
    data: TaskCreate,
    token: str = Depends(verify_token),
):

    next_id = max(
        [task["id"] for task in tasks],
        default=0,
    ) + 1

    task = {
        "id": next_id,
        **data.model_dump(),
    }

    tasks.append(task)

    return task


# ==========================
# 更新任务
# ==========================

@app.put(
    "/tasks/{task_id}",

    response_model=TaskResponse,

    summary="更新任务",

    tags=["Task"],

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

            update_data = data.model_dump(
                exclude_unset=True
            )

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


# ==========================
# 删除任务
# ==========================
class MessageResponse(BaseModel):
    message: str
@app.delete(
    "/tasks/{task_id}",

    response_model=MessageResponse,

    summary="删除任务",

    tags=["Task"],

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
    for index, task in enumerate(tasks):

        if task["id"] == task_id:

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
    
@app.post(
    "/upload/pdf",
    summary="上传 PDF",
    tags=["File"],
)
async def upload_pdf(
    file: UploadFile,
):
    if file.content_type != "application/pdf":

        raise AppException(
            status_code=400,
            code=40001,
            message="Only PDF files are allowed",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:

        raise AppException(
            status_code=413,
            code=41301,
            message="File is too large",
            data={
                "max_size_mb": 5,
            },
        )

    safe_filename = Path(
        file.filename or "upload.pdf"
    ).name

    file_path = (
        UPLOAD_DIR / safe_filename
    )

    with open(
        file_path,
        "wb",
    ) as f:
        f.write(content)

    return {
        "filename": safe_filename,
        "content_type": file.content_type,
        "size": len(content),
        "path": str(file_path),
    }