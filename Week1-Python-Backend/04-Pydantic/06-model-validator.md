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

## 最小代码 / 场景

```python
@model_validator(mode='after')
def check(self):
    if self.end<self.start: raise ValueError('bad range')
    return self
```

## 🔗 关联知识

- [[05-field-validator]]
