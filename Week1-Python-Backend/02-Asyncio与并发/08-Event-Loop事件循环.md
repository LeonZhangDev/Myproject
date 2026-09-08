---
tags: [week1]
difficulty: P0
status: learning
---

# Event Loop 事件循环

## 一句话理解

事件循环调度 Task、定时器和 I/O 就绪事件。

## 核心理解

协程在未完成 await 处让出；普通 CPU 计算/阻塞调用不会自动让出。

## 🧠 完整理解

### 我会先这样理解

Event Loop 是 asyncio 的调度核心：它维护可运行任务、定时器以及 I/O 就绪事件，反复选择“现在可以继续执行”的协程推进。协程必须在 await 点主动让出，事件循环才能去运行其他任务，因此它是协作式调度。高性能来自一个线程可以管理大量等待中的 I/O，而不是事件循环本身会把 CPU 计算并行化。

### 执行顺序 / 思考顺序

loop 取就绪 Task → 执行到 await → 注册等待的 I/O/Future → Task 挂起 → loop 去跑别的任务 → 操作系统通知 I/O 就绪 → Future 完成 → Task 回到 ready 队列 → 继续执行。

### 容易踩的坑

不要在事件循环线程里做长时间 CPU 循环、`time.sleep()`、同步 requests 等阻塞操作，否则其他所有协程都得等它让出。

### 面试时我会这样说

> 我把事件循环想成一个调度台。哪个协程现在能跑就让它跑，跑到 await 等外部结果时就先放一边，再去服务别人。所以它特别适合大量 I/O；但如果某个协程一直算不让权，整个调度台就卡住了。

## 最小代码 / 场景

```text
Task A --await--> Loop --> Task B
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def main():
    print("事件循环正在运行")

asyncio.run(main())
```

### 运行 / 返回结果

```text
事件循环正在运行
```

**怎么理解：** asyncio.run() 会创建并驱动事件循环，直到 main() 完成。

## 🔗 关联知识

- [[09-阻塞调用]]
- [[../03-FastAPI/17-ASGI与WSGI]]
