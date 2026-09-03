"""项目公共配置。"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从 .env 读取数据库与开发环境配置。"""

    database_url: str = (
        "postgresql+asyncpg://task_user:task_password@127.0.0.1:5432/task_db"
    )
    sql_echo: bool = True

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
