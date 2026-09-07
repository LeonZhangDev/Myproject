"""多个接口共用的响应模型。"""

from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Swagger 中描述统一错误返回格式。"""

    code: int
    message: str
    data: Any = None


class MessageResponse(BaseModel):
    """用于只需要返回 message 的简单接口，例如 DELETE。"""

    message: str
