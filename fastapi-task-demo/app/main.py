"""FastAPI 应用入口。

这个文件尽量只负责“组装”：创建 app、注册 CORS、中间件、异常处理器和各个 router。
具体业务逻辑放到其他模块，避免 main.py 再次变成几百行的大文件。
"""

from fastapi import FastAPI

from app.core.cors import setup_cors
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_log import request_log_middleware
from app.routers import chat, files, tasks


# FastAPI(...) 会创建整个 Web 应用对象。
# 后续的路由、中间件、异常处理器、CORS 都要注册到这个 app 上。
#
# title / description / version 不只是“说明文字”，
# 它们还会自动出现在 Swagger 文档：/docs 中。
#
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
- PDF 上传
- BackgroundTasks
- SSE 流式聊天
""",
    version="1.0.0",
)


# 真正的 CORS 细节拆到了 app/core/cors.py。
# main.py 这里只负责“把它装到 app 上”。
setup_cors(app)


# 每个 HTTP 请求都会先经过 request_log_middleware。
# 它会统计处理耗时，并在响应头中加入 X-Process-Time。
app.middleware("http")(
    request_log_middleware
)


# 把 AppException 和 Pydantic 参数校验异常统一注册到 FastAPI。
# 真正的处理逻辑在 app/exceptions/handlers.py。
register_exception_handlers(app)


# include_router 的作用可以理解成：
# “把另一个文件里的路由，挂到主 app 上”。
#
app.include_router(tasks.router)
app.include_router(files.router)
app.include_router(chat.router)
