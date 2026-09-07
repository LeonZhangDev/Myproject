---
tags: [week1]
difficulty: P0
status: learning
---

# asyncio.gather

## 一句话理解

`gather` 并发等待一组 awaitable，并按输入顺序返回结果。

## 核心理解

适合“全部完成后一起拿结果”；异常传播策略要明确。

## 最小代码 / 场景

```python
r=await asyncio.gather(a(),b(),c())
```

## 🔗 关联知识

- [[11-TaskGroup]]
