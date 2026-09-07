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
