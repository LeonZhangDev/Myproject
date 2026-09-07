"""FastAPI 应用入口。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.cache.redis import close_redis
from app.core.cors import setup_cors
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_log import request_log_middleware
from app.routers import categories, chat, files, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：关闭时释放 Redis 客户端连接池。"""

    yield
    await close_redis()


app = FastAPI(
    title="Task API",
    description="""
一个用于学习 FastAPI + PostgreSQL + SQLAlchemy + Redis 的任务管理项目。

## PostgreSQL / SQLAlchemy

- SQLAlchemy 2.x AsyncSession
- Task CRUD
- Category 外键关联
- 数据库事务
- OFFSET / LIMIT 分页
- 数据库索引
- Task LEFT JOIN Category
- 每个请求独立 AsyncSession

## Redis

- `GET /tasks/{task_id}` Cache-Aside 单条缓存
- `__NULL__` 短 TTL 空值缓存，降低缓存穿透
- Task 创建 / 更新 / 删除后主动失效对应缓存
- Redis Lua 脚本实现 `/tasks` 固定窗口限流
- Redis 故障时缓存与限流 fail-open，PostgreSQL 核心 CRUD 仍可工作

## 其他

- Token 校验
- 全局异常处理
- PDF 上传
- BackgroundTasks
- SSE 流式聊天
""",
    version="3.0.0",
    lifespan=lifespan,
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
