---
tags: [week1]
difficulty: P0
status: learning
---

# EXPLAIN

## 一句话理解

查看数据库计划如何执行 SQL。

## 核心理解

关注 Seq Scan/Index Scan、估算行数、Join 类型、Sort。

## 最小代码 / 场景

```sql
EXPLAIN SELECT * FROM tasks WHERE user_id=123;
```

## 🔗 关联知识

- [[09-EXPLAIN-ANALYZE]]
