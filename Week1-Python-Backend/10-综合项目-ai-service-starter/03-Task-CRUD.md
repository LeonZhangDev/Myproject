---
tags: [week1, project]
difficulty: P0
status: learning
---
# Task CRUD
```python
@router.post("")
async def create_task(data:TaskCreate, session=Depends(get_session)):
    task=Task(title=data.title)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

关联：[[../03-FastAPI/02-路由]]、[[../05-数据库与SQLAlchemy/11-数据库Session]]。
