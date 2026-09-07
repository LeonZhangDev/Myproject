---
tags: [week1]
difficulty: P0
status: learning
---

# Coroutine

## 一句话理解

调用 async 函数得到协程对象。

## 核心理解

它描述将要执行的异步计算，通常被 await 或包装成 Task。

## 最小代码 / 场景

```python
async def hello(): return 'hi'
coro=hello(); result=await coro
```

## 🔗 关联知识

- [[06-Task]]
