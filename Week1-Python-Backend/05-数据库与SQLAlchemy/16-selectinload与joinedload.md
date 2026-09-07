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
