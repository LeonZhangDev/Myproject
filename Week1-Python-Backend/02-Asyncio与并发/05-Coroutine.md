---
tags: [week1]
difficulty: P0
status: learning
---

# Coroutine

## 一句话理解

调用 async 函数得到协程对象。

## 核心理解

它描述将要执行的异步计算，通常被 await 或包装成 Task。

## 🧠 完整理解

### 我会先这样理解

Coroutine（协程对象）表示一段可以暂停和恢复的异步执行过程。调用 `async def` 并不会立即把函数完整执行，而是返回 coroutine；它必须被 await、包装成 Task，或者交给事件循环运行，否则就可能出现 “coroutine was never awaited” 警告。协程描述的是“要做的工作”，Task 才更像“已经被调度去做的工作”。

### 执行顺序 / 思考顺序

`coro = foo()` 只是创建协程对象 → `await coro` 时当前任务负责推进它，或 `create_task(coro)` 把它注册到事件循环 → 协程在 await 点暂停/恢复 → 最终返回值或抛异常。

### 容易踩的坑

同一个 coroutine 对象通常不能被重复 await；需要再次执行时应该重新调用协程函数创建新的对象。

### 面试时我会这样说

> 我会区分 coroutine 和 Task：调用 async 函数拿到的 coroutine 更像一份“待执行说明”，它自己不会凭空在后台跑；交给 await 或 create_task 以后，事件循环才真正推进它。

## 最小代码 / 场景

```python
async def hello(): return 'hi'
coro=hello(); result=await coro
```


## 🧪 简单例子与返回结果

### 例子

```python
async def hello():
    return "hello"

coro = hello()
print(type(coro).__name__)
coro.close()
```

### 运行 / 返回结果

```text
coroutine
```

**怎么理解：** 调用 async def 不会立刻执行函数体，而是先得到 coroutine 对象；需要 await 或交给事件循环运行。

## 🔗 关联知识

- [[06-Task]]
