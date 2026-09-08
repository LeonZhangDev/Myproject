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

## 🧠 完整理解

### 我会先这样理解

SSE 和 WebSocket 的核心选择标准是通信方向和系统复杂度，而不是谁“更高级”。SSE 基于 HTTP、单向服务端推送、浏览器原生重连，适合通知和 LLM 流；WebSocket 全双工、协议更灵活，适合频繁双向实时交互。部署环境、鉴权方式、代理支持和消息规模也要一起评估。

### 执行顺序 / 思考顺序

先问业务是否需要客户端在同一长连接上持续主动发消息 → 不需要时优先 SSE/HTTP streaming → 需要双向实时则 WebSocket → 再评估断线恢复、水平扩展、网关支持和可靠性。

### 容易踩的坑

不要把“聊天”两个字就自动等同 WebSocket。很多 LLM 聊天其实是一次 POST 用户消息 + 一条 SSE 响应流，完全够用。

### 面试时我会这样说

> 我的判断很直接：服务端单向推送就先 SSE，双向实时才考虑 WebSocket。像 ChatGPT 这种“用户发一次、模型持续回”其实 POST + SSE 就能做得很好，没必要为了技术感增加复杂度。

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
