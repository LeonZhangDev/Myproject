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
