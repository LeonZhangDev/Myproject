"""Task 的 Pydantic 请求/响应模型。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """POST /tasks 创建任务。"""

    title: str = Field(
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )
    completed: bool = False
    priority: int = Field(
        default=1,
        ge=1,
        le=5,
    )

    # 可选分类名。
    # 如果分类不存在，创建任务时会在同一个事务里先创建分类。
    category_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )


class TaskUpdate(BaseModel):
    """PUT /tasks/{task_id} 更新任务。"""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )
    completed: bool | None = None
    priority: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )
    category_id: int | None = Field(
        default=None,
        ge=1,
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    priority: int
    category_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class TaskPageResponse(BaseModel):
    """普通任务列表的分页响应。"""

    page: int
    page_size: int
    total: int
    items: list[TaskResponse]


class TaskWithCategoryResponse(BaseModel):
    """JOIN 查询结果。"""

    id: int
    title: str
    description: str | None = None
    completed: bool
    priority: int
    category_id: int | None = None
    category_name: str | None = None
    created_at: datetime


class TaskWithCategoryPageResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[TaskWithCategoryResponse]
