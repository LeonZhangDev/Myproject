---
tags: [week1]
difficulty: P0
status: learning
---

# selectinload 与 joinedload

## 一句话理解

selectinload 用额外批量查询；joinedload 用 JOIN 一次带出关联。

## 核心理解

选择要看一对多数据量、行膨胀、查询次数和执行计划。

## 🧠 完整理解

### 我会先这样理解

`selectinload` 和 `joinedload` 都是 SQLAlchemy 的 eager loading 策略。selectinload 通常先查父表，再用父键集合发第二条 `WHERE ... IN (...)` 查子表；joinedload 则在主查询中直接 JOIN。前者常适合一对多集合，避免主结果行爆炸；后者常适合多对一/一对一或子关系很小的情况。

### 执行顺序 / 思考顺序

selectinload：父查询 → 收集 parent ids → 第二条 IN 查询子表 → ORM 组装关系。joinedload：单条 JOIN → 数据库返回重复父列的组合行 → ORM 去重并组装对象图。

### 容易踩的坑

joinedload 一对多时行数可能大幅膨胀，还会影响分页思考；selectinload 的 IN 列表也不是无限免费。SQLAlchemy 结果去重/API 细节要按版本正确使用。

### 面试时我会这样说

> 我不会简单背“哪个更快”。一对多而且子项不少时我通常先考虑 selectinload，两条 SQL 但结果更干净；多对一或关联很小，joinedload 一条 JOIN 往往很合适，最后还是看实际 SQL 和数据量。

## 最小代码 / 场景

```python
select(User).options(joinedload(User.tasks))
```


## 🧪 简单例子与返回结果

### 例子

```python
stmt = select(User).options(selectinload(User.tasks))
users = (await db.execute(stmt)).scalars().all()
```

### 运行 / 返回结果

```text
典型 selectinload：
第 1 条 SQL 查 users
第 2 条 SQL 用 IN (...) 批量查 tasks
避免 1 + N 次逐条查询。
```

## 🔗 关联知识

- [[15-N加1问题]]
