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


## 🧪 简单例子与返回结果

### 例子

```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'a@test.com';
```

### 运行 / 返回结果

```text
简化理解：
Index Scan ...
(actual time=... rows=1 loops=1)
Planning Time: ...
Execution Time: ...
```

**怎么理解：** EXPLAIN ANALYZE 会真的执行 SQL，因此能看到实际耗时与实际行数。

## 🔗 关联知识

- [[08-EXPLAIN]]
