---
tags: [week1]
difficulty: P0
status: learning
---

# async 与 await

## 一句话理解

`async def` 定义协程函数；`await` 等待异步操作并可能让出控制权。

## 核心理解

只有遇到未完成的 await 才会让 Event Loop 调度其他 Task；阻塞调用不会自动让出。

## 最小代码 / 场景

```python
async def work():
    await asyncio.sleep(1)
```

## 🔗 关联知识

- [[05-Coroutine]]
- [[08-Event-Loop事件循环]]
- [[09-阻塞调用]]
