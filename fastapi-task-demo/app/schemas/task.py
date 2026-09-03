"""Task 的 Pydantic 数据模型。

Schema 用来定义“客户端可以传什么”和“接口应该返回什么”，它不是数据库表本身。
"""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """POST /tasks 创建任务时，客户端需要提交的数据。"""

    # Field 不只是写类型，还可以附加长度、范围等校验规则。
    title: str = Field(
        min_length=1,
        max_length=100,
    )

    # str | None 表示既可以是字符串，也可以是 None。
    # default=None 表示这个字段不传也可以。
    description: str | None = Field(
        default=None,
        max_length=500,
    )

    completed: bool = False


class TaskUpdate(BaseModel):
    """PUT /tasks/{task_id} 更新任务时使用。"""

    # 更新接口里的字段都允许不传，
    # 因为用户可能只想更新 title，而不是整个对象。
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


class TaskResponse(BaseModel):
    """任务接口返回给客户端的数据结构。"""

    id: int
    title: str
    description: str | None = None
    completed: bool
