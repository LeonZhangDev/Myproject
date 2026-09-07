---
tags: [week1]
difficulty: P0
status: learning
---

# 字段类型与 Optional

## 一句话理解

`str | None` 表示值可为 None；是否可省略还看默认值。

## 核心理解

`nickname: str | None = None` 才能在输入中省略。

## 最小代码 / 场景

```python
nickname:str|None=None
```


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int | None = None

print(User(name="Leon"))
```

### 运行 / 返回结果

```text
name='Leon' age=None
```

## 🔗 关联知识

- [[01-BaseModel]]
