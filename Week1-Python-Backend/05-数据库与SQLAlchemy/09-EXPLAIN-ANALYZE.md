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

## 🧠 完整理解

### 我会先这样理解

EXPLAIN ANALYZE 不只展示估算计划，还会实际执行 SQL 并记录真实耗时和真实行数，因此能直接比较“优化器以为会有多少行”和“实际上有多少行”。这对发现统计信息错误、某一步骤真实特别慢非常有用，但因为它会真的执行，生产环境尤其对写操作必须谨慎。

### 执行顺序 / 思考顺序

优化器先生成执行计划 → 数据库真实执行每个节点 → 采集 actual time/rows/loops 等 → 输出估算值与实际值 → 通过差异定位成本估算或执行瓶颈。

### 容易踩的坑

对 UPDATE/DELETE/INSERT 跑 EXPLAIN ANALYZE 会真的修改数据，除非在可回滚事务或安全环境中操作。耗时数据也会受到缓存、并发和机器状态影响。

### 面试时我会这样说

> EXPLAIN 是“计划怎么跑”，ANALYZE 是“真的跑一次看看”。我重点会对比 estimated rows 和 actual rows，如果差几个数量级，优化器很可能因为统计信息不准选错了计划。

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
