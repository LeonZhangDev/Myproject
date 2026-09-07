"""基于 Redis 的固定窗口 API 限流。"""

import logging

from fastapi import Request
from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import settings
from app.exceptions.app_exception import AppException


logger = logging.getLogger(__name__)

# Lua 脚本在 Redis 服务端一次执行完 INCR + EXPIRE，因此两个操作具有原子性。
# 返回：当前窗口计数、Key 剩余 TTL。
_RATE_LIMIT_SCRIPT = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
local ttl = redis.call('TTL', KEYS[1])
return {current, ttl}
"""


async def rate_limit(request: Request) -> None:
    """限制同一客户端对 Task API 的请求频率。

    Redis 只是辅助基础设施，因此 Redis 临时故障时选择 fail-open：
    记录日志但放行请求，保证 PostgreSQL 核心 CRUD 仍可使用。
    """

    client_host = (
        request.client.host
        if request.client is not None
        else "unknown"
    )

    # 对整个 tasks 资源共享一个计数窗口，而不是按 /tasks/1、/tasks/2 分开计数。
    key = f"task-api:rate-limit:tasks:{client_host}"

    try:
        result = await redis_client.eval(
            _RATE_LIMIT_SCRIPT,
            1,
            key,
            settings.rate_limit_window_seconds,
        )
    except RedisError:
        logger.exception("Redis rate-limit check failed for key=%s", key)
        return

    current = int(result[0])
    ttl = max(int(result[1]), 1)

    if current > settings.rate_limit_requests:
        raise AppException(
            status_code=429,
            code=42901,
            message="Too many requests",
            data={
                "limit": settings.rate_limit_requests,
                "window_seconds": settings.rate_limit_window_seconds,
                "retry_after_seconds": ttl,
            },
        )
