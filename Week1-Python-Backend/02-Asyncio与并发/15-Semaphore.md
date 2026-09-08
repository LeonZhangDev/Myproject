---
tags: [week1]
difficulty: P0
status: learning
---

# Semaphore

## 一句话理解

Semaphore 限制最多 N 个任务同时进入。

## 核心理解

适合下游 API 限并发、限制 DB 并发、保护资源。

## 🧠 完整理解

### 我会先这样理解

Semaphore 与 Lock 的区别是它允许固定数量的任务同时进入，而不是只允许一个。它特别适合并发限流，比如最多同时调用 20 个外部 API、最多同时做 5 个昂贵任务。这样可以保护连接池、第三方服务和本机资源，避免瞬时并发把系统拖垮。

### 执行顺序 / 思考顺序

初始化计数 N → 每个任务 acquire 时计数减一 → 计数为 0 的任务排队 → 已进入的任务完成后 release → 计数加一并唤醒等待者。它限制的是同时在临界区域里的数量。

### 容易踩的坑

Semaphore 只是进程内并发门槛，不等于全局 QPS 限流；多实例部署需要 Redis/网关等全局限流方案。还要避免 acquire 后异常却没有 release，最好使用 `async with`。

### 面试时我会这样说

> 我把 Semaphore 理解成“有 N 个许可证的门”。比如下游只扛得住 20 个并发，我就不会 gather 1000 个请求一起砸过去，而是用 Semaphore 把同时在飞的请求控制在 20 左右。

## 最小代码 / 场景

```python
sem=asyncio.Semaphore(3)
async with sem:
    await remote_call()
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

running = 0
max_running = 0
sem = asyncio.Semaphore(2)

async def job():
    global running, max_running
    async with sem:
        running += 1
        max_running = max(max_running, running)
        await asyncio.sleep(0.05)
        running -= 1

async def main():
    await asyncio.gather(*(job() for _ in range(5)))
    print(max_running)

asyncio.run(main())
```

### 运行 / 返回结果

```text
2
```

**怎么理解：** Semaphore(2) 把同时进入关键区域的协程数量限制为 2。

## 🔗 关联知识

- [[14-Lock]]
- [[../05-数据库与SQLAlchemy/19-连接池]]
