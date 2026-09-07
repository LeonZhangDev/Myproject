"""项目自定义业务异常。

业务代码只负责 raise AppException(...)，具体如何转成 HTTP JSON 响应由 handlers.py 统一处理。
"""

from typing import Any


class AppException(Exception):
    """
    项目统一业务异常。

    status_code: HTTP 状态码，例如 404、401。
    code:        项目自己的业务错误码，例如 40401。
    message:     给客户端看的错误说明。
    data:        可选的额外错误信息。
    """

    def __init__(
        self,
        status_code: int,
        code: int,
        message: str,
        data: Any = None,
    ):
        # 这些属性会在全局异常处理器里通过 exc.xxx 读取。
        self.status_code = status_code
        self.code = code
        self.message = message
        self.data = data
