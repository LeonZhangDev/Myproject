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
