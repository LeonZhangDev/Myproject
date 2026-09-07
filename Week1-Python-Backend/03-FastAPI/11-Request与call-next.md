---
tags: [week1]
difficulty: P0
status: learning
---

# Request 与 call_next

## 一句话理解

Request 表示当前请求；`call_next(request)` 把请求交给后续路由。

## 核心理解

`call_next` 由框架传给中间件。

## 最小代码 / 场景

```python
response=await call_next(request)
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI, Request
app = FastAPI()

@app.middleware("http")
async def log_path(request: Request, call_next):
    print("path:", request.url.path)
    response = await call_next(request)
    return response

@app.get("/ping")
def ping():
    return {"pong": True}
```

### 运行 / 返回结果

```text
控制台：
path: /ping

客户端：
200 {"pong":true}
```

## 🔗 关联知识

- [[10-中间件]]
