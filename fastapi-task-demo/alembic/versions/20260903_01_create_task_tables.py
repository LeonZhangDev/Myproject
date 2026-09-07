"""create categories and tasks tables

Revision ID: 20260903_01
Revises:
Create Date: 2026-09-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260903_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_categories_name",
        "categories",
        ["name"],
        unique=True,
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tasks_category_id",
        "tasks",
        ["category_id"],
        unique=False,
    )
    op.create_index(
        "ix_tasks_completed_priority",
        "tasks",
        ["completed", "priority"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_tasks_completed_priority",
        table_name="tasks",
    )
    op.drop_index(
        "ix_tasks_category_id",
        table_name="tasks",
    )
    op.drop_table("tasks")

    op.drop_index(
        "ix_categories_name",
        table_name="categories",
    )
    op.drop_table("categories")
