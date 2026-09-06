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

## 🔗 关联知识

- [[15-N加1问题]]
