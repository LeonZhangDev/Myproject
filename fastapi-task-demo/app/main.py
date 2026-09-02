from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Task API",
    description="用于学习 FastAPI 的任务管理 API",
    version="0.1.0",
)

class TaskCreate(BaseModel):
    title: str =Field(
        min_length=1,
        max_length=100
    )
    description: str | None = Field(
        default=None,
        max_length=500
    )
    priority: int = Field(
        default=1,
        ge=1,
        le=5
    )
tasks = []

next_id = 1
    
@app.get(
    "/",
    summary="首页",
    tags=["Common"],
)
def root():
    return {
        "message": "Hello FastAPI"
    }



@app.get(
    "/tasks",
    summary="查询任务列表",
    tags=["Task"],
)
def get_tasks():
    return {
        "tasks": [
            {
                "id": 1,
                "title": "学习 FastAPI",
            },
            {
                "id": 2,
                "title": "学习 Pydantic",
            },
        ]
    }
    

@app.get(
    "/tasks/{task_id}",
    summary="查询单个任务",
    tags=["Task"],
)
def get_task(task_id: int):
    return {
        "task_id": task_id
    }


@app.get(
    "/tasks/{task_id}/detail",
    summary="查询任务详细信息",
    tags=["Task"],
)
def get_task_detail(
    task_id: int,
    verbose: bool = False,
):
    return {
        "task_id": task_id,
        "verbose": verbose,
    }

@app.get(
    "/search",
    summary="搜索任务",
    tags=["Task"],
)
def search_tasks(
    keyword: str,
    limit: int = 20,
):
    return {
        "keyword": keyword,
        "limit": limit,
    }

@app.post(
    "/tasks",
    status_code=201,
    summary="创建任务",
    tags=["Task"],
)
def create_task(task: TaskCreate):
    return {
        "title": task.title,
        "description": task.description,
    }