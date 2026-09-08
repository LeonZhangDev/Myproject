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

## 🧠 完整理解

### 我会先这样理解

Pydantic 校验发生在应用层，适合格式、类型和业务输入友好提示；数据库约束发生在持久化层，是最终一致性底线。比如 email 格式可以 Pydantic 校验，但 email 唯一必须依靠 UNIQUE 约束，因为两个并发请求都可能先通过应用层“查无重复”，然后同时插入。两层不是重复，而是防守位置不同。

### 执行顺序 / 思考顺序

请求先经 Pydantic 快速拒绝明显非法输入 → 业务逻辑执行 → 数据库 INSERT/UPDATE → 数据库再检查 UNIQUE/FK/CHECK/NOT NULL → 违反约束时事务失败并由应用转换错误。

### 容易踩的坑

“我已经在代码里查过了，所以不用 UNIQUE”是典型并发 bug。相反，只靠数据库报错也会让用户体验和错误信息很差，因此两层通常配合。

### 面试时我会这样说

> 我会说 Pydantic 是第一道门，数据库约束是最后一道门。比如注册邮箱，我可以先查一次给用户友好提示，但最终一定要有 UNIQUE，因为并发条件下应用层先查再插并不原子。

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
