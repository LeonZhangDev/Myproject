---
tags: [week1]
difficulty: P0
status: learning
---

# async 与 await

## 一句话理解

`async def` 定义协程函数；`await` 等待异步操作并可能让出控制权。

## 核心理解

只有遇到未完成的 await 才会让 Event Loop 调度其他 Task；阻塞调用不会自动让出。

## 🧠 完整理解

### 我会先这样理解

`async def` 定义协程函数，调用它得到协程对象；`await` 则是在当前协程里等待另一个可等待对象，并在等待期间把控制权交还事件循环。真正的并发来自“等待时让出”，不是写了 async 关键字就自动变快。整条 I/O 调用链最好都使用异步兼容库，否则一个同步阻塞调用就可能卡住整个事件循环。

### 执行顺序 / 思考顺序

调用 async 函数 → 得到 coroutine → 事件循环开始执行 → 遇到 await 未完成 I/O → 当前 coroutine 挂起并让出 → loop 执行其他就绪任务 → I/O 完成 → 原 coroutine 恢复并拿到结果。

### 容易踩的坑

`await` 不是“创建并发任务”的同义词。连续 `await f1(); await f2()` 仍然可能是串行；如果两件事相互独立，通常要先创建 Task 或用 gather/TaskGroup。

### 面试时我会这样说

> 我把 async/await 理解成“遇到等待别占着线程”。但我要特别看调用链是不是全异步，比如 async 接口里用 requests 去请求外部服务，照样会阻塞。还有连续 await 只是异步写法，不代表两个任务会同时跑。

## 最小代码 / 场景

```python
async def work():
    await asyncio.sleep(1)
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def get_data():
    await asyncio.sleep(0.1)
    return "data"

async def main():
    result = await get_data()
    print(result)

asyncio.run(main())
```

### 运行 / 返回结果

```text
data
```

## 🔗 关联知识

- [[05-Coroutine]]
- [[08-Event-Loop事件循环]]
- [[09-阻塞调用]]
