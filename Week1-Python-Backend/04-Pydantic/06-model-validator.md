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
