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

## 🧠 完整理解

### 我会先这样理解

EXPLAIN 用来查看数据库“准备怎么执行”一条 SQL，包括扫描方式、连接顺序、估算行数和成本。它是性能排查的入口，能告诉你是否全表扫描、是否走索引、JOIN 使用了什么策略。普通 EXPLAIN 通常不真正完整执行查询，因此展示的是估算计划。

### 执行顺序 / 思考顺序

SQL → 解析/重写 → 优化器根据统计信息生成候选计划并估算成本 → 选出计划 → EXPLAIN 把 plan tree 展示出来。阅读时通常从最底层扫描节点向上看数据如何被过滤和连接。

### 容易踩的坑

只看到 `Index Scan` 就宣布“优化完成”不够。还要看估算行数、过滤掉多少、是否额外 Sort、JOIN 是否膨胀；估算严重不准还可能说明统计信息过旧。

### 面试时我会这样说

> 我查慢 SQL 第一反应一般是 EXPLAIN。先看从哪张表开始、有没有 Seq Scan、预计扫多少行、JOIN 怎么做，再决定是索引问题、SQL 写法问题还是数据分布问题。

## 最小代码 / 场景

```sql
EXPLAIN SELECT * FROM tasks WHERE user_id=123;
```


## 🧪 简单例子与返回结果

### 例子

```sql
EXPLAIN
SELECT * FROM users WHERE email = 'a@test.com';
```

### 运行 / 返回结果

```text
简化理解：
Index Scan using users_email_key on users
  Index Cond: (email = 'a@test.com')
```

**怎么理解：** 真实输出会因 PostgreSQL 版本、数据量和统计信息而不同。

## 🔗 关联知识

- [[09-EXPLAIN-ANALYZE]]
