---
tags: [week1]
difficulty: P0
status: learning
---

# Task

## 一句话理解

Task 是注册到事件循环中的协程执行单元。

## 核心理解

用 `create_task()` 可以让协程开始被调度，然后稍后 await 结果。

## 最小代码 / 场景

```python
t=asyncio.create_task(work()); r=await t
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def work():
    await asyncio.sleep(0.1)
    return 42

async def main():
    task = asyncio.create_task(work())
    print(await task)

asyncio.run(main())
```

### 运行 / 返回结果

```text
42
```

## 🔗 关联知识

- [[05-Coroutine]]
- [[07-Future]]
