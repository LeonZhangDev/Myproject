---
tags: [week1]
difficulty: P0
status: learning
---

# SQL 基础

## 一句话理解

SQL 声明你要读写关系数据库中的什么数据。

## 核心理解

先掌握 SELECT/INSERT/UPDATE/DELETE/WHERE/JOIN/ORDER BY。

## 最小代码 / 场景

```sql
SELECT id,title FROM tasks WHERE done=false ORDER BY id DESC;
```


## 🧪 简单例子与返回结果

### 例子

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name VARCHAR(50)
);

INSERT INTO users(id, name) VALUES (1, 'Leon');
SELECT * FROM users;
```

### 运行 / 返回结果

```text
id | name
----+------
  1 | Leon
```

## 🔗 关联知识

- [[02-WHERE]]
- [[03-JOIN]]
