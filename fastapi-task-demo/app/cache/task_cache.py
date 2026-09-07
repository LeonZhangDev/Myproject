"""Task 的 Cache-Aside 缓存封装。"""

import json
import logging
from typing import Any

from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import settings


logger = logging.getLogger(__name__)

CACHE_PREFIX = "task-api:task"
NULL_SENTINEL = "__NULL__"


def task_cache_key(task_id: int) -> str:
    """统一生成 Task 缓存 Key。"""

    return f"{CACHE_PREFIX}:{task_id}"


async def get_cached_task(
    task_id: int,
) -> tuple[bool, dict[str, Any] | None]:
    """读取 Task 缓存。

    返回值：
    - (False, None)：Redis 未命中，应该回源 PostgreSQL。
    - (True, None)：命中了空值缓存，数据库此前确认没有这个 Task。
    - (True, dict)：命中了正常 Task 缓存。

    Redis 在这里是加速层，所以 Redis 临时不可用时采用 fail-open：
    当作缓存未命中，继续访问 PostgreSQL，而不是让核心业务直接失败。
    """

    key = task_cache_key(task_id)

    try:
        cached = await redis_client.get(key)
    except RedisError:
        logger.exception("Redis GET failed for key=%s", key)
        return False, None

    if cached is None:
        return False, None

    if cached == NULL_SENTINEL:
        return True, None

    try:
        return True, json.loads(cached)
    except json.JSONDecodeError:
        # 缓存内容损坏时删除它并回源数据库，避免一直返回坏数据。
        logger.warning("Invalid JSON cache payload for key=%s", key)
        await delete_task_cache(task_id)
        return False, None


async def set_task_cache(
    task_id: int,
    task_data: dict[str, Any],
) -> None:
    """写入正常 Task 缓存，并设置 TTL。"""

    key = task_cache_key(task_id)

    try:
        await redis_client.set(
            key,
            json.dumps(
                task_data,
                ensure_ascii=False,
            ),
            ex=settings.task_cache_ttl_seconds,
        )
    except RedisError:
        # Cache-Aside 中缓存写失败不应该回滚已经成功的数据库读取。
        logger.exception("Redis SET failed for key=%s", key)


async def set_task_not_found_cache(
    task_id: int,
) -> None:
    """对不存在的 Task 写入短 TTL 空值缓存，降低缓存穿透。"""

    key = task_cache_key(task_id)

    try:
        await redis_client.set(
            key,
            NULL_SENTINEL,
            ex=settings.task_null_cache_ttl_seconds,
        )
    except RedisError:
        logger.exception("Redis negative-cache SET failed for key=%s", key)


async def delete_task_cache(task_id: int) -> None:
    """删除 Task 缓存。

    Task 在 PostgreSQL 中创建、更新或删除成功后主动失效缓存，下一次读取
    再回源数据库并重建缓存。这就是本项目采用的 Cache-Aside 写策略。
    """

    key = task_cache_key(task_id)

    try:
        await redis_client.delete(key)
    except RedisError:
        # 学习项目中采用 fail-open。生产环境可再加入重试/消息补偿。
        logger.exception("Redis DELETE failed for key=%s", key)
