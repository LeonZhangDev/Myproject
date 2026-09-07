---
tags: [week1]
difficulty: P0
status: learning
---

# Pydantic 与数据库约束

## 一句话理解

Pydantic 是应用入口校验；数据库约束是最终防线。

## 核心理解

唯一性、非空等关键规则常两层都要有。

## 最小代码 / 场景

```sql
ALTER TABLE users ADD CONSTRAINT uq_email UNIQUE(email);
```


## 🧪 简单例子与返回结果

### 例子

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str

print(UserCreate(email="a@test.com"))
print(UserCreate(email="a@test.com"))
```

### 运行 / 返回结果

```text
email='a@test.com'
email='a@test.com'
```

**怎么理解：** Pydantic 只校验单次输入格式，不知道数据库里是否已经存在该 email；唯一性仍应由数据库 UNIQUE 约束保证。

## 🔗 关联知识

- [[../05-数据库与SQLAlchemy/05-UNIQUE]]
