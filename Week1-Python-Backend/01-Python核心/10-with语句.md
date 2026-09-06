---
tags: [week1]
difficulty: P0
status: learning
---

# with 语句

## 一句话理解

`with` 是使用上下文管理器的语法。

## 核心理解

异步资源对应 `async with`，如 asyncio Lock、异步事务。

## 最小代码 / 场景

```python
async with lock:
    ...
```

## 🔗 关联知识

- [[09-上下文管理器]]
- [[../02-Asyncio与并发/14-Lock]]
