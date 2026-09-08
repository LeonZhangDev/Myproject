---
tags: [week1]
difficulty: P0
status: learning
---

# model_validator

## 一句话理解

用于跨字段校验。

## 核心理解

例如 end >= start、确认密码一致等。

## 🧠 完整理解

### 我会先这样理解

`model_validator` 适合需要同时观察多个字段的规则，比如结束时间必须晚于开始时间、两种认证方式至少提供一种。它在整个模型层面校验，因此能表达单字段 Field 做不到的关系约束。Pydantic v2 可以选择 before/after 等模式。

### 执行顺序 / 思考顺序

各字段原始输入 → before model validator（如有）→ 字段级解析和校验 → 构成模型 → after model validator 检查字段间关系 → 返回模型或抛 ValidationError。

### 容易踩的坑

模型校验仍然只能保证当前输入内部一致，不能替代数据库唯一性和并发约束。不要在 validator 里偷偷开数据库 Session。

### 面试时我会这样说

> 比如 start_time 和 end_time，单独看两个字段都合法，但组合起来可能不合法，这就是 model_validator 的场景。我把它当成“跨字段的一致性校验”，数据库约束还是留给数据库。

## 最小代码 / 场景

```python
@model_validator(mode='after')
def check(self):
    if self.end<self.start: raise ValueError('bad range')
    return self
```


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel, model_validator

class Range(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def check_order(self):
        if self.end < self.start:
            raise ValueError("end must >= start")
        return self

print(Range(start=1, end=3))
```

### 运行 / 返回结果

```text
start=1 end=3
```

## 🔗 关联知识

- [[05-field-validator]]
