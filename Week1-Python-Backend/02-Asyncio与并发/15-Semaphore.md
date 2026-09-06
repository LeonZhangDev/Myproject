---
tags: [week1]
difficulty: P0
status: learning
---

# Semaphore

## 一句话理解

Semaphore 限制最多 N 个任务同时进入。

## 核心理解

适合下游 API 限并发、限制 DB 并发、保护资源。

## 最小代码 / 场景

```python
sem=asyncio.Semaphore(3)
async with sem:
    await remote_call()
```

## 🔗 关联知识

- [[14-Lock]]
- [[../05-数据库与SQLAlchemy/19-连接池]]
