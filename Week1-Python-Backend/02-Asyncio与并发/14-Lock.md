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
