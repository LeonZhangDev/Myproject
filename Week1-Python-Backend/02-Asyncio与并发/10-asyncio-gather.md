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

## 🧠 完整理解

### 我会先这样理解

`asyncio.gather` 用来同时等待多个 awaitable，并按传入顺序汇总结果。它非常适合“几个相互独立的 I/O 都必须完成，然后才能继续”的场景。默认情况下某个任务异常会向调用方传播，但其他任务的生命周期细节要理解清楚；如果需要更结构化的错误和取消语义，Python 3.11+ 常优先考虑 TaskGroup。

### 执行顺序 / 思考顺序

构造多个 coroutine/Task → gather 把它们并发推进 → 每个任务独立等待 I/O → 全部完成后按原输入顺序返回结果列表。总耗时通常接近最慢的那个任务，而不是简单相加。

### 容易踩的坑

并发启动数量过大也会压垮下游。gather 10000 个 HTTP 请求不代表更快，常常还需要 Semaphore 限流。`return_exceptions=True` 也要谨慎，否则异常会变成普通返回值，容易被忽略。

### 面试时我会这样说

> 如果三个接口互相没依赖，我不会一个一个 await，而会 gather 一起等，这样总时间更接近最慢的那个。但我也不会无脑 gather 几千个任务，下游连接池和限流都要一起考虑。

## 最小代码 / 场景

```python
r=await asyncio.gather(a(),b(),c())
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def double(x):
    await asyncio.sleep(0.1)
    return x * 2

async def main():
    result = await asyncio.gather(double(1), double(2), double(3))
    print(result)

asyncio.run(main())
```

### 运行 / 返回结果

```text
[2, 4, 6]
```

**怎么理解：** gather 会并发等待多个 awaitable，并按传入顺序返回结果。

## 🔗 关联知识

- [[11-TaskGroup]]
