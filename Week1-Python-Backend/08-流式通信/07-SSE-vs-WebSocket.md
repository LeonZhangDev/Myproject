---
tags: [week1]
difficulty: P0
status: learning
---

# SSE vs WebSocket

## 一句话理解

单向服务器推送优先 SSE；双向高频实时通信选 WebSocket。

## 核心理解

LLM 文本生成通常服务器单向输出，因此 SSE 更简单。

## 最小代码 / 场景

```text
SSE: Server -> Client
WS : Client <-> Server
```

## 🔗 关联知识

- [[08-LLM流式输出]]
