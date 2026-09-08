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

## 🧠 完整理解

### 我会先这样理解

BaseModel 是 Pydantic 的数据模型基础，用类型注解声明字段后，它负责把外部数据解析成受约束的 Python 对象，并给出结构化校验错误。它特别适合 API 边界，因为客户端传进来的 JSON 永远不能默认可信。模型同时也能提供序列化、JSON Schema 和 FastAPI 文档信息。

### 执行顺序 / 思考顺序

原始 dict/JSON → BaseModel 读取字段 → 类型解析/转换 → 字段和模型级 validator → 成功得到模型实例，失败得到 ValidationError → 之后可 `model_dump` 输出。

### 容易踩的坑

不要把 Pydantic 模型当 ORM 实体长期持有数据库状态。它更适合数据传输/边界校验；数据库唯一性、外键等约束仍应由数据库兜底。

### 面试时我会这样说

> 我把 BaseModel 当成 API 边界的“结构化门卫”。外部 JSON 进来先按类型和规则校验，业务代码拿到的是相对干净的数据，不需要每个字段自己 if 判断一遍。

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
