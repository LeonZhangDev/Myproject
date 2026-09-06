---
tags: [week1, interview, b]
difficulty: P0
status: learning
---

# B｜asyncio与并发


## W1-Q8｜Coroutine、Task 和 Future 分别是什么？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
调用 async 函数得到 Coroutine；Task 把协程注册到事件循环并调度；Future 表示未来结果，Task 属于 Future 体系的高级封装。

### 最小代码 / 场景
```python
task=asyncio.create_task(work())
result=await task
```

### 关联知识
- [[../02-Asyncio与并发/05-Coroutine]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q9｜事件循环的作用是什么？协程在什么时候让出执行权？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
Event Loop 调度 Task、定时器和 I/O 就绪事件。协程遇到尚未完成的 await 时让出；普通计算和阻塞调用不会自动让出。

### 最小代码 / 场景
```python
await asyncio.sleep(1)  # 让出
time.sleep(1)           # 阻塞
```

### 关联知识
- [[../02-Asyncio与并发/08-Event-Loop事件循环]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q10｜在 async def 中调用阻塞函数会发生什么？应该怎样处理？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
阻塞函数会占住事件循环线程，让其他请求一起变慢。优先换异步库；无法替换的阻塞 I/O 可用 asyncio.to_thread；CPU 重任务用进程池或独立服务。

### 最小代码 / 场景
```python
result=await asyncio.to_thread(blocking_io)
```

### 关联知识
- [[../02-Asyncio与并发/09-阻塞调用]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q11｜asyncio.gather 和 TaskGroup 有什么主要区别？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
gather 适合并发等待一组任务并收集结果；TaskGroup 提供结构化并发，组内任务失败传播和生命周期管理更清晰。

### 最小代码 / 场景
```python
async with asyncio.TaskGroup() as tg:
    t1=tg.create_task(a())
    t2=tg.create_task(b())
```

### 关联知识
- [[../02-Asyncio与并发/11-TaskGroup]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q12｜异步任务如何设置超时和正确处理取消？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
用 asyncio.timeout 或 wait_for 设置超时；取消会触发 CancelledError，应在 finally 清理资源，通常继续传播取消。

### 最小代码 / 场景
```python
async with asyncio.timeout(2):
    await work()
```

### 关联知识
- [[../02-Asyncio与并发/12-超时与取消]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q13｜单线程协程为什么仍可能发生竞态条件？Lock 和 Semaphore 分别解决什么问题？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
协程会在 await 处交错执行；共享状态的读改写跨越 await 时会竞态。Lock 保护临界区；Semaphore 限制同时进入的任务数量。

### 最小代码 / 场景
```python
lock=asyncio.Lock()
async with lock:
    tmp=count
    count=tmp+1
```

### 关联知识
- [[../02-Asyncio与并发/13-竞态条件]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q14｜CPU 密集任务为什么不适合直接放在事件循环中？有哪些处理方式？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
CPU 长计算不 await，会阻塞事件循环。可用多进程、ProcessPool、原生扩展、任务队列或独立计算服务。

### 最小代码 / 场景
```python
from concurrent.futures import ProcessPoolExecutor
```

### 关联知识
- [[../02-Asyncio与并发/16-CPU密集任务]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？
