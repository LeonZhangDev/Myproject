"""SQLAlchemy 异步 Engine 与每请求 Session 依赖。"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


# Engine 是应用级对象，内部负责维护数据库连接池。
# 它可以被整个 FastAPI 应用共享。
engine = create_async_engine(
    settings.database_url,
    echo=settings.sql_echo,
    pool_pre_ping=True,
)


# Session 工厂本身也可以全局共享；真正的 AsyncSession 会按请求创建。
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """为一次 HTTP 请求提供一个独立 AsyncSession。

    FastAPI 执行到 yield 时把 session 注入路由；请求结束后退出
    async with，Session 自动关闭并把连接归还 Engine 的连接池。
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            # 如果路由中有尚未结束的事务，发生异常时确保回滚。
            await session.rollback()
            raise
