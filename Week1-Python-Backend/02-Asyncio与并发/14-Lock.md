---
tags: [week1]
difficulty: P0
status: learning
---

# Lock

## 一句话理解

Lock 保护临界区，同一时刻只允许一个协程进入。

## 核心理解

它解决互斥，不是跨机器分布式锁。

## 最小代码 / 场景

```python
lock=asyncio.Lock()
async with lock:
    ...
```

## 🔗 关联知识

- [[13-竞态条件]]
- [[../06-Redis与缓存/15-分布式锁]]
