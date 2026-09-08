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

## 🧠 完整理解

### 我会先这样理解

JOIN 用来根据关联条件把多张表组合起来。INNER JOIN 只保留能匹配的行，LEFT JOIN 会保留左表全部行，右表匹配不到时补 NULL。真正需要理解的是连接基数：一对多连接会把左表一行扩成多行，既影响结果正确性，也影响排序、分页和聚合。

### 执行顺序 / 思考顺序

优化器选择一张表作为驱动输入 → 根据 join condition 去另一张表找匹配行 → 可能使用 nested loop、hash join、merge join 等算法 → 输出组合行 → 再执行后续过滤/聚合/排序。

### 容易踩的坑

JOIN 条件漏写可能造成笛卡尔积；一对多 JOIN 后直接 count(*) 可能把主表重复计算。用于连接的外键/关联列通常值得评估索引。

### 面试时我会这样说

> 我做 JOIN 时会先明确关系是一对一、一对多还是多对多，因为这决定结果行数会不会膨胀。很多分页和 count 出错，不是 SQL 语法错，而是 JOIN 以后同一个主记录被展开成多行。

## 最小代码 / 场景

```sql
SELECT users.name,tasks.title
FROM users LEFT JOIN tasks ON users.id=tasks.user_id;
```


## 🧪 简单例子与返回结果

### 例子

```sql
SELECT u.name, t.title
FROM users u
JOIN tasks t ON t.user_id = u.id;
```

### 运行 / 返回结果

```text
假设 Leon 有任务 "Learn FastAPI"：
Leon | Learn FastAPI
```

## 🔗 关联知识

- [[15-N加1问题]]
