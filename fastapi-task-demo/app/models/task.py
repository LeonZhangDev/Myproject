"""Task 数据库表模型。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.category import Category


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    priority: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )

    # 外键把 tasks 与 categories 关联起来。
    # index=True 便于按分类过滤，也有利于常见的关联查询。
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="SET NULL",
        ),
        index=True,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    category: Mapped[Category | None] = relationship(
        back_populates="tasks",
    )

    # 复合索引：适合“按完成状态筛选，并结合优先级处理”的查询方向。
    __table_args__ = (
        Index(
            "ix_tasks_completed_priority",
            "completed",
            "priority",
        ),
    )
