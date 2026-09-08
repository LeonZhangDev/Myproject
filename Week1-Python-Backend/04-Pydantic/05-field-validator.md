---
tags: [week1]
difficulty: P0
status: learning
---

# field_validator

## 一句话理解

对某个字段执行自定义校验。

## 核心理解

适合 trim、格式检查、单字段业务规则。

## 🧠 完整理解

### 我会先这样理解

`field_validator` 用于对单个字段做自定义校验或规范化，例如去空格、检查枚举之外的业务格式、统一大小写。它可以在类型解析前或后执行，具体取决于 mode。能用标准类型/Field 表达的规则优先用标准约束，自定义 validator 留给真正的特殊规则。

### 执行顺序 / 思考顺序

输入字段 → before validator（若配置）→ Pydantic 类型解析 → after validator/默认模式 → 返回处理后的字段值 → 任何阶段抛 ValueError 等都会变成 ValidationError。

### 容易踩的坑

validator 不适合做慢 I/O 或查数据库；Pydantic 校验通常是同步纯函数式过程。校验器里偷偷修改外部状态也会让行为难测试。

### 面试时我会这样说

> 我把 field_validator 用在“这个字段自己就能判断”的规则上，比如用户名 trim 后不能为空。能用 Field 写我先用 Field，因为更直观；真的有自定义逻辑再上 validator。

## 最小代码 / 场景

```python
@field_validator('title')
@classmethod
def no_blank(cls,v):
    if not v.strip(): raise ValueError('blank')
    return v
```


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def clean_name(cls, v):
        return v.strip()

print(User(name="  Leon  ").name)
```

### 运行 / 返回结果

```text
Leon
```

## 🔗 关联知识

- [[06-model-validator]]
