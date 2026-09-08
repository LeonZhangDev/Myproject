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

## 🧠 完整理解

### 我会先这样理解

Lock 用来保证同一时间只有一个执行单元进入临界区。asyncio.Lock 保护的是同一个事件循环中的协程，不是跨进程分布式锁。它适合保护进程内共享状态，但临界区应该尽量短，尤其不要拿着锁去做无关的慢 I/O，否则并发会退化成排队。

### 执行顺序 / 思考顺序

任务尝试 `async with lock` → 锁空闲则获取 → 执行临界区 → 退出自动 release → 等待队列中的下一个任务获得。锁能保证这段代码互斥，但不能自动保证业务跨数据库/跨服务的一致性。

### 容易踩的坑

不要把 asyncio.Lock 当成数据库锁或 Redis 分布式锁。多 worker 部署时，每个进程都有自己的 Lock，彼此根本看不到。

### 面试时我会这样说

> 我一般只用 Lock 保护“当前进程内”的共享状态，而且锁住的范围越小越好。如果数据真正共享在数据库里，我更愿意把一致性放在数据库事务、条件更新或行锁里解决。

## 最小代码 / 场景

```python
lock=asyncio.Lock()
async with lock:
    ...
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

counter = 0
lock = asyncio.Lock()

async def add_one():
    global counter
    async with lock:
        old = counter
        await asyncio.sleep(0)
        counter = old + 1

async def main():
    await asyncio.gather(*(add_one() for _ in range(100)))
    print(counter)

asyncio.run(main())
```

### 运行 / 返回结果

```text
100
```

**怎么理解：** Lock 保证同一时刻只有一个协程进入临界区。

## 🔗 关联知识

- [[13-竞态条件]]
- [[../06-Redis与缓存/15-分布式锁]]
