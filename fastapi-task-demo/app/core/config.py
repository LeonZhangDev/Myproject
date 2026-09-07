"""项目公共配置。"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从 .env 读取 PostgreSQL、Redis 与开发环境配置。"""

    database_url: str = (
        "postgresql+asyncpg://task_user:task_password@127.0.0.1:5432/task_db"
    )
    sql_echo: bool = True

    redis_url: str = "redis://127.0.0.1:6379/0"

    # 正常 Task 缓存 5 分钟；不存在的数据只缓存 60 秒。
    task_cache_ttl_seconds: int = 300
    task_null_cache_ttl_seconds: int = 60

    # 固定窗口限流：默认每个客户端每 60 秒最多 60 次 /tasks 请求。
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MAX_FILE_SIZE = 5 * 1024 * 1024

ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
