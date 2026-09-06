---
tags: [week1]
difficulty: P0
status: learning
---

# UNIQUE

## 一句话理解

数据库唯一约束保证指定列/组合不重复。

## 核心理解

它首先是正确性约束，其次常通过唯一索引实现。

## 最小代码 / 场景

```sql
CREATE UNIQUE INDEX uq_users_email ON users(email);
```

## 🔗 关联知识

- [[../04-Pydantic/10-Pydantic与数据库约束]]
- [[../06-Redis与缓存/14-幂等键]]
