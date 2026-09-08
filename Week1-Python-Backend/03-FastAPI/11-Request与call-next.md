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

## 🧠 完整理解

### 我会先这样理解

`Request` 提供当前 HTTP 请求的上下文，包括 method、url、headers、client、state、body 等；`call_next` 常见于 HTTP middleware，用来把请求继续传给下游并等待响应。中间件里可以在调用前记录开始时间，在调用后补响应头或记录耗时。

### 执行顺序 / 思考顺序

middleware 接到 Request → 读取不破坏流的元数据 → `response = await call_next(request)` → 下游路由完整执行 → response 返回中间件 → 修改 header/记录日志 → return response。

### 容易踩的坑

请求 body 通常是流，重复读取要非常小心；大文件和流式请求更不能在中间件里无脑全部加载。`request.state` 适合放 request-id 等请求级上下文，但不要当全局存储。

### 面试时我会这样说

> 我最常见的用法就是中间件里拿 Request 生成 request-id，然后 `await call_next` 让真正接口执行，回来以后把耗时和状态码记日志。关键是别在这里把 request body 全读一遍。

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
