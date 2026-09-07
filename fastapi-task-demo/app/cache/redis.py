"""应用级 Redis 客户端。

Redis 客户端内部维护连接池，因此它和 SQLAlchemy Engine 一样可以全局共享；
不要像数据库 AsyncSession 那样为每个 HTTP 请求重新创建 Redis 客户端。
"""

from redis.asyncio import Redis

from app.core.config import settings


redis_client = Redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)


async def close_redis() -> None:
    """应用关闭时释放 Redis 客户端连接池。"""

    await redis_client.aclose()
