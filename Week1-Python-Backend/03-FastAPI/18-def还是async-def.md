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
