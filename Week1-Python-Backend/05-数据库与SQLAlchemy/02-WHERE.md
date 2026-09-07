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


## 🧪 简单例子与返回结果

### 例子

```sql
SELECT id, name
FROM users
WHERE age >= 18;
```

### 运行 / 返回结果

```text
假设数据为：Leon(25)、Tom(16)
返回：
1 | Leon
```

## 🔗 关联知识

- [[06-数据库索引]]
