"""可复用的 FastAPI 依赖。

认证逻辑放在 dependencies 中后，多个接口都可以通过 Depends(verify_token) 复用，而不用重复写 Token 判断。
"""

from fastapi import Header

from app.exceptions.app_exception import AppException


def verify_token(
    x_token: str | None = Header(default=None),
):
    """读取请求头 X-Token，并做最简单的身份校验。"""

    # Header(default=None) 告诉 FastAPI：
    # 从 HTTP Header 中读取 x-token / X-Token。
    # 如果没有传，则值为 None。
    if x_token != "dev-token":
        raise AppException(
            status_code=401,
            code=40101,
            message="Invalid token",
        )

    # Depends(verify_token) 的接口会拿到这里的返回值。
    return x_token
