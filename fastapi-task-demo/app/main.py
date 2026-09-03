"""FastAPI 应用入口。

main.py 只负责组装：创建 app、注册 CORS、中间件、异常处理器和 router。
数据库表结构由 Alembic 负责迁移，不在应用启动时偷偷 create_all。
"""

from fastapi import FastAPI

from app.core.cors import setup_cors
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_log import request_log_middleware
from app.routers import categories, chat, files, tasks


app = FastAPI(
    title="Task API",
    description="""
一个用于学习 FastAPI + PostgreSQL + SQLAlchemy 的任务管理项目。

## 功能

- PostgreSQL + SQLAlchemy 2.x AsyncSession
- Task CRUD
- Category 关联
- 数据库事务
- OFFSET / LIMIT 分页
- 数据库索引
- Task JOIN Category 查询
- Token 校验
- 全局异常处理
- PDF 上传
- BackgroundTasks
- SSE 流式聊天
""",
    version="2.0.0",
)

setup_cors(app)

app.middleware("http")(
    request_log_middleware
)

register_exception_handlers(app)

app.include_router(tasks.router)
app.include_router(categories.router)
app.include_router(files.router)
app.include_router(chat.router)
