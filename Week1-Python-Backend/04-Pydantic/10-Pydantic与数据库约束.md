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

## 🔗 关联知识

- [[../05-数据库与SQLAlchemy/05-UNIQUE]]
