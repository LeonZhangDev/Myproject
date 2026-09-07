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

## 🔗 关联知识

- [[../02-Asyncio与并发/08-Event-Loop事件循环]]
