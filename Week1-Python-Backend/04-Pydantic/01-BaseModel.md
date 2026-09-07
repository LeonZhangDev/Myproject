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


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

u = User(id="1", name="Leon")
print(u)
print(type(u.id))
```

### 运行 / 返回结果

```text
id=1 name='Leon'
<class 'int'>
```

**怎么理解：** Pydantic 会按模型规则解析和校验输入。

## 🔗 关联知识

- [[03-Field字段约束]]
