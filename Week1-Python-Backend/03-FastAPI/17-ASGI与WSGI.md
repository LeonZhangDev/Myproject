---
tags: [week1]
difficulty: P0
status: learning
---

# ASGI 与 WSGI

## 一句话理解

WSGI 偏同步 HTTP；ASGI 支持异步、WebSocket、长连接事件。

## 核心理解

FastAPI 是 ASGI 应用，通常由 Uvicorn 等 ASGI Server 运行。

## 🧠 完整理解

### 我会先这样理解

WSGI 是传统 Python Web 的同步接口规范，一个请求调用一个同步应用；ASGI 在此基础上支持异步调用模型和多种连接类型，因此可以自然处理 HTTP、WebSocket、长连接。FastAPI 基于 ASGI，Uvicorn/Hypercorn 是常见 ASGI server。ASGI 的优势只有在你的应用和依赖链真正非阻塞时才能体现。

### 执行顺序 / 思考顺序

ASGI server 接收连接 → 以 `scope + receive + send` 调用应用 → 应用可以多次 await receive/send，因此能处理流式和长连接。WSGI 更接近一次 environ/start_response 的同步调用模型。

### 容易踩的坑

ASGI 不是“自动让所有同步代码高并发”。同步阻塞库仍然要交给线程池或替换成异步客户端。部署时也不要把 ASGI app 直接交给不兼容的 WSGI server。

### 面试时我会这样说

> 我会说 FastAPI 能很好支持 async、SSE、WebSocket，底层很大一部分就是因为它跑在 ASGI 模型上。但 ASGI 只是提供能力，业务里如果还是一堆同步阻塞调用，性能不会凭空变好。

## 最小代码 / 场景

```text
Client -> Uvicorn -> ASGI -> FastAPI -> asyncio
```


## 🧪 简单例子与返回结果

### 例子

```text
WSGI：一次请求 -> 一个同步调用
ASGI：支持 async/await、WebSocket、长连接等异步场景

FastAPI -> ASGI
Flask 传统模式 -> WSGI
```

### 运行 / 返回结果

```text
FastAPI + Uvicorn 可以直接处理 async 路由和 WebSocket；
传统 WSGI 接口本身不提供同样的异步长连接模型。
```

## 🔗 关联知识

- [[../02-Asyncio与并发/08-Event-Loop事件循环]]
