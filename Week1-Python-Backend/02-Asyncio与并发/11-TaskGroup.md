---
tags: [week1]
difficulty: P0
status: learning
---

# TaskGroup

## 一句话理解

TaskGroup 用作用域管理一组并发任务。

## 核心理解

组内失败会协调取消其他任务，并统一等待/汇总异常，结构化并发更清晰。

## 最小代码 / 场景

```python
async with asyncio.TaskGroup() as tg:
    t1=tg.create_task(a())
    t2=tg.create_task(b())
```

## 🔗 关联知识

- [[10-asyncio-gather]]
- [[12-超时与取消]]
