---
tags: [week1, project]
difficulty: P0
status: learning
---
# Pydantic 校验
```python
class TaskCreate(BaseModel):
    title:str=Field(min_length=1,max_length=100)
    priority:int=Field(default=1,ge=1,le=5)
```

关联：[[../04-Pydantic/00-Pydantic-MOC]]。
