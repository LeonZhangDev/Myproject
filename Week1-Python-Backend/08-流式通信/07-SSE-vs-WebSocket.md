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


## 🧪 简单例子与返回结果

### 例子

```text
需求 A：LLM 只需要服务器持续把 token 推给浏览器
需求 B：在线聊天双方都要随时主动发消息
```

### 运行 / 返回结果

```text
需求 A：SSE 往往更简单
需求 B：WebSocket 更合适，因为它是双向通信
```

## 🔗 关联知识

- [[08-LLM流式输出]]
