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
