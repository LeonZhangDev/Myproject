"""Category 的 Pydantic 请求/响应模型。"""

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )


class CategoryResponse(BaseModel):
    id: int
    name: str

    # 允许 Pydantic 直接读取 SQLAlchemy ORM 对象属性。
    model_config = ConfigDict(
        from_attributes=True,
    )
