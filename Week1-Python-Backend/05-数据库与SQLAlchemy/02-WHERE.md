---
tags: [week1]
difficulty: P0
status: learning
---

# WHERE

## 一句话理解

`WHERE` 用条件过滤行。

## 核心理解

WHERE 字段常影响索引设计。

## 最小代码 / 场景

```sql
SELECT * FROM tasks WHERE user_id=10 AND done=false;
```

## 🔗 关联知识

- [[06-数据库索引]]
