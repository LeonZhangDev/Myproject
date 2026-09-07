---
tags: [week1]
difficulty: P0
status: learning
---

# EXPLAIN ANALYZE

## 一句话理解

真实执行 SQL 并显示实际耗时/实际行数。

## 核心理解

比 EXPLAIN 更接近真实性能；生产写语句要谨慎。

## 最小代码 / 场景

```sql
EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id=123;
```

## 🔗 关联知识

- [[08-EXPLAIN]]
