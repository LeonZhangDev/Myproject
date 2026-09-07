---
tags: [week1]
difficulty: P0
status: learning
---

# JOIN

## 一句话理解

按关联条件把多张表的数据组合起来。

## 核心理解

LEFT JOIN 会保留左表所有记录，即使右表没有匹配。

## 最小代码 / 场景

```sql
SELECT users.name,tasks.title
FROM users LEFT JOIN tasks ON users.id=tasks.user_id;
```

## 🔗 关联知识

- [[15-N加1问题]]
