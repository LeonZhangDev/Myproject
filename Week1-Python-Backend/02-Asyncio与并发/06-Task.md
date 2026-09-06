---
tags: [week1]
difficulty: P0
status: learning
---

# Task

## 一句话理解

Task 是注册到事件循环中的协程执行单元。

## 核心理解

用 `create_task()` 可以让协程开始被调度，然后稍后 await 结果。

## 最小代码 / 场景

```python
t=asyncio.create_task(work()); r=await t
```

## 🔗 关联知识

- [[05-Coroutine]]
- [[07-Future]]
