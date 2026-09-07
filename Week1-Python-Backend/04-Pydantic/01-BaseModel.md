---
tags: [week1]
difficulty: P0
status: learning
---

# BaseModel

## 一句话理解

声明数据结构并完成解析、校验、序列化。

## 核心理解

FastAPI 请求/响应模型主要基于 BaseModel。

## 最小代码 / 场景

```python
class TaskCreate(BaseModel):
    title:str
    priority:int=1
```

## 🔗 关联知识

- [[03-Field字段约束]]
