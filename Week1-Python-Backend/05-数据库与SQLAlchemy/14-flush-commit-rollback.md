---
tags: [week1]
difficulty: P0
status: learning
---

# flush、commit、rollback

## 一句话理解

flush 发 SQL 但不结束事务；commit 提交；rollback 撤销未提交事务。

## 核心理解

flush 后常能拿到数据库生成主键，但其他事务未必可见。

## 最小代码 / 场景

```python
await session.flush(); await session.commit()
```

## 🔗 关联知识

- [[10-事务]]
