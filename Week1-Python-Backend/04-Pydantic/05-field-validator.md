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

## 最小代码 / 场景

```python
@field_validator('title')
@classmethod
def no_blank(cls,v):
    if not v.strip(): raise ValueError('blank')
    return v
```

## 🔗 关联知识

- [[06-model-validator]]
