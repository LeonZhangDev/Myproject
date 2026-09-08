---
tags: [week1]
difficulty: P0
status: learning
---

# FastAPI 路由用 def 还是 async def

## 一句话理解

异步库用 async def；阻塞库可用普通 def；最危险是 async def 内直接阻塞。

## 核心理解

FastAPI 会在线程池处理普通 def 路由；async def 则运行在事件循环。

## 🧠 完整理解

### 我会先这样理解

FastAPI 里 `async def` 适合调用异步数据库、异步 HTTP 客户端等可 await I/O；普通 `def` 适合同步库，FastAPI 会把同步 endpoint 放到线程池执行，避免直接卡住事件循环。真正的选型依据是你里面调用的依赖是什么，而不是“async 看起来更高级”。

### 执行顺序 / 思考顺序

async endpoint 直接在 event loop 运行 → await 时让出；sync endpoint 通常由 Starlette/AnyIO offload 到线程池 → 完成后把结果交回事件循环。async endpoint 里如果直接调用长时间同步阻塞函数，反而最危险。

### 容易踩的坑

不要为了统一风格全部写 async def。如果数据库驱动和 SDK 都是同步的，贸然 async 只会制造假异步；反过来，真正 async 驱动也不要被同步 wrapper 阻塞。

### 面试时我会这样说

> 我不会看到 FastAPI 就所有接口都写 async。我会看调用链：如果里面是 AsyncSession、httpx AsyncClient，我写 async；如果主要是同步 SDK，我宁愿用 def 让框架放线程池，也不在 async def 里直接阻塞 event loop。

## 最小代码 / 场景

```python
@app.get('/bad')
async def bad():
    time.sleep(5)
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI
import asyncio
app = FastAPI()

@app.get("/io")
async def io_task():
    await asyncio.sleep(0.1)
    return {"type": "async"}

@app.get("/sync")
def sync_task():
    return {"type": "sync"}
```

### 运行 / 返回结果

```text
GET /io   -> {"type":"async"}
GET /sync -> {"type":"sync"}
```

**怎么理解：** 需要 await 异步 I/O 时用 async def；纯同步阻塞库可以使用 def，让 FastAPI 在线程池中执行。

## 🔗 关联知识

- [[../02-Asyncio与并发/09-阻塞调用]]
