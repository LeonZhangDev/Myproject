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

## 🧠 完整理解

### 我会先这样理解

字段类型决定 Pydantic 如何解析和校验输入。`Optional[T]` 的语义是 `T | None`，也就是值可以为 None；但“是否可以不传”还取决于有没有默认值。Pydantic v2 里 `name: str | None` 没有默认值时通常仍然是必填字段，只是允许显式传 null；`= None` 才表示可以缺省。

### 执行顺序 / 思考顺序

读取字段定义 → 判断 required/default → 输入缺失时按 required 规则处理 → 输入存在时再按 union/type 解析 → 允许 None 则接受 null，否则报验证错误。

### 容易踩的坑

最常见误区就是把 Optional 直接理解成“可不传”。另外 bool/int 等类型可能存在自动转换，严格输入场景可以考虑 strict 模式。

### 面试时我会这样说

> 我会把“可为空”和“可不传”分开说。`str | None` 只说明值允许是 None；如果没有默认值，字段可能还是必须出现。这个细节在 PATCH 接口里特别重要，因为“没传”和“明确传 null”语义不一样。

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
