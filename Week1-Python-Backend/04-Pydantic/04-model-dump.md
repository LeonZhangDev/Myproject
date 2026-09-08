---
tags: [week1]
difficulty: P0
status: learning
---

# model_dump

## 一句话理解

把 Pydantic 模型转换成普通字典。

## 核心理解

JSON 可用 `model_dump_json()`。

## 🧠 完整理解

### 我会先这样理解

Pydantic v2 的 `model_dump()` 把模型实例转换成 Python 字典，并可控制 include/exclude、exclude_none、exclude_unset、by_alias 等。它常用于把验证后的数据传给 ORM 或构造响应。特别是 PATCH 更新时，`exclude_unset=True` 能区分用户没传的字段和用户显式传入的字段。

### 执行顺序 / 思考顺序

模型实例保存已验证字段与 fields_set → 调 model_dump → 根据参数筛选字段 → 返回普通 dict；如需 JSON 兼容字符串则可用 model_dump_json 或框架序列化。

### 容易踩的坑

不要不加区分地把 `model_dump()` 全量结果直接用于更新数据库，可能把未提供字段覆盖成默认值/None。也要留意 secret 字段是否应该被导出。

### 面试时我会这样说

> 我最常用 model_dump 的场景就是把请求模型转成字典。创建接口全量 dump 问题不大，但 PATCH 我通常加 `exclude_unset=True`，否则用户没传的字段也可能被错误覆盖。

## 最小代码 / 场景

```python
data=task.model_dump()
```


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

u = User(id=1, name="Leon")
print(u.model_dump())
```

### 运行 / 返回结果

```text
{'id': 1, 'name': 'Leon'}
```

## 🔗 关联知识

- [[08-字典解包]]
