---
tags: [week1]
difficulty: P0
status: learning
---

# SSE

## 一句话理解

服务器到客户端的单向 HTTP 事件流。

## 核心理解

浏览器支持 EventSource 和自动重连，特别适合 LLM token 输出。

## 最小代码 / 场景

```text
event: token
data: {"content":"你"}

```

## 🔗 关联知识

- [[03-EventSourceResponse]]
- [[07-SSE-vs-WebSocket]]
