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
