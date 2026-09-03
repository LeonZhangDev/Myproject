"""Category 数据库表模型。"""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # 分类名经常用于查找，并且不能重复，因此建立唯一索引。
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    # 一个 Category 可以对应多个 Task。
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="category",
    )
