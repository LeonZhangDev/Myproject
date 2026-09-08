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

## 🧠 完整理解

### 我会先这样理解

Task 是事件循环对 coroutine 的调度包装。创建 Task 后，它会在事件循环获得执行机会，而当前协程可以继续做别的事情，因此适合并发启动多个相互独立的异步操作。Task 还保存最终结果、异常、取消状态，方便上层管理生命周期。

### 执行顺序 / 思考顺序

coroutine → `asyncio.create_task()` → 注册到当前 event loop → loop 在合适时机推进 Task → Task 遇 await 挂起 → 完成后保存 result 或 exception → await Task 的代码取得结果。

### 容易踩的坑

“创建 Task 后不管它”很危险。后台 Task 的异常可能没人消费，程序退出时也可能被直接取消。生产代码应该有明确的所有权、等待或取消策略。

### 面试时我会这样说

> 我把 Task 理解成“已经放进事件循环执行队列里的协程”。coroutine 只是描述任务，Task 才开始被调度。工程里如果我 create_task，通常也会想清楚谁负责 await、谁负责取消、异常谁来收。

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
