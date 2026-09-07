"""所有 SQLAlchemy ORM 模型共同继承的 Base。"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy 2.x 声明式模型基类。"""

    pass
