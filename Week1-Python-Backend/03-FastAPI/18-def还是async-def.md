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

## 🔗 关联知识

- [[../02-Asyncio与并发/09-阻塞调用]]
