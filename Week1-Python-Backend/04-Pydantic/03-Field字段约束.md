---
tags: [week1]
difficulty: P0
status: learning
---

# Field 字段约束

## 一句话理解

`Field()` 添加长度、范围、描述等约束。

## 核心理解

让接口在进入业务逻辑前就拒绝非法输入。

## 🧠 完整理解

### 我会先这样理解

`Field` 用来在类型之外补充约束和元数据，例如最小/最大值、长度、正则 pattern、描述、别名、示例。类型告诉我们“它是什么”，Field 进一步表达“什么范围才算合法”。这些约束既参与运行时校验，也能进入 JSON Schema/OpenAPI。

### 执行顺序 / 思考顺序

模型声明 `Field(...)` → Pydantic 生成字段 schema → 输入经过类型解析后检查约束 → 不满足则产生带字段路径的 ValidationError → FastAPI 通常转为 422。

### 容易踩的坑

不要把所有业务规则都塞 Field。跨字段约束更适合 model_validator，依赖数据库状态的规则更不能只靠 Pydantic。

### 面试时我会这样说

> 我一般用 Field 表达单字段、确定性的规则，比如 price 必须大于 0、name 最长 100。它的好处是校验和 OpenAPI 文档一起生成；跨字段或者要查数据库的规则我会放别的层。

## 最小代码 / 场景

```python
title:str=Field(min_length=1,max_length=100)
priority:int=Field(ge=1,le=5)
```


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    age: int = Field(ge=0, le=120)

try:
    User(age=-1)
except ValidationError as e:
    print(e.errors()[0]["type"])
```

### 运行 / 返回结果

```text
greater_than_equal
```

## 🔗 关联知识

- [[05-field-validator]]
