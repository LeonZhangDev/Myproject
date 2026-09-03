"""全局异常处理器。

这里负责把 Python 异常统一转换成前端容易处理的 JSON 格式。
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.app_exception import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    """处理项目主动 raise 出来的 AppException。"""

    # exc 就是代码里 raise AppException(...) 创建出来的异常对象。
    # JSONResponse 用来手动控制 HTTP 状态码和返回 JSON 内容。
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """统一处理 Pydantic / FastAPI 的请求参数校验失败。"""

    # 例如：task_id 应该是 int，但客户端传了 abc；
    # 或 TaskCreate.title 不满足 Field(min_length=1)。
    return JSONResponse(
        status_code=422,
        content={
            "code": 42201,
            "message": "Request validation failed",
            "data": exc.errors(),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """把异常类型和对应处理函数注册到 FastAPI。"""

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
