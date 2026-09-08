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

## 🧠 完整理解

### 我会先这样理解

SQL 是声明式语言，重点不是告诉数据库“每一步怎么做”，而是描述“我要什么结果”。数据库优化器会根据统计信息、索引和成本模型选择执行计划。后端工程里最重要的是能把业务需求翻译成正确的 SELECT/INSERT/UPDATE/DELETE，并理解过滤、连接、排序、聚合、事务这些操作对性能和一致性的影响。

### 执行顺序 / 思考顺序

应用构造 SQL → 数据库解析语法 → 绑定参数 → 优化器选择执行计划 → 执行器访问表/索引 → 产生结果集 → 驱动把结果映射回 Python。参数化查询还能把数据与 SQL 结构分离，降低注入风险。

### 容易踩的坑

不要把 ORM 当成“不需要懂 SQL”。ORM 最终仍然会生成 SQL；不会看 SQL 和执行计划，就很难排查慢查询、N+1、索引失效。字符串拼接 SQL 还会带来注入风险。

### 面试时我会这样说

> 我理解 SQL 的重点是：我写的是结果要求，真正怎么扫表、走哪个索引是数据库优化器决定的。所以我用 ORM 时也会关注最终 SQL，尤其是慢查询一定会回到 SQL 和执行计划上看。

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
