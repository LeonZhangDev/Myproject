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
