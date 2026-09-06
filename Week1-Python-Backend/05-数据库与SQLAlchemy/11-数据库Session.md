---
tags: [week1]
difficulty: P0
status: learning
---

# 数据库 Session

## 一句话理解

SQLAlchemy Session 是 ORM 工作单元/事务上下文。

## 核心理解

它跟踪 ORM 对象状态、事务和连接使用，不等于数据库本身。

## 最小代码 / 场景

```python
session.add(task); await session.flush(); await session.commit()
```

## 🔗 关联知识

- [[12-Session生命周期]]
- [[13-AsyncSession]]
