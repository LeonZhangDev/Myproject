---
tags: [week1]
difficulty: P0
status: learning
---

# BackgroundTasks

## 一句话理解

响应返回后执行轻量、短时、允许偶尔失败的同进程任务。

## 核心理解

没有持久队列、跨进程协调、可靠重试，不应当可靠任务队列。

## 最小代码 / 场景

```python
background_tasks.add_task(write_log, 'created')
```

## 🔗 关联知识

- [[../02-Asyncio与并发/16-CPU密集任务]]
