---
tags: [week1]
difficulty: P0
status: learning
---

# WebSocket

## 一句话理解

全双工长连接，客户端和服务端都能主动发消息。

## 核心理解

适合实时协作、游戏、双向高频消息。

## 🧠 完整理解

### 我会先这样理解

WebSocket 在一次 HTTP Upgrade 握手后建立全双工长连接，客户端和服务器都可以随时发送消息。它适合聊天、协同编辑、游戏状态等真正需要双向低延迟通信的场景。相比 SSE，它协议状态更强，连接管理、心跳、扩容和消息可靠性也更复杂。

### 执行顺序 / 思考顺序

HTTP Upgrade 请求 → 服务端返回 101 → TCP 连接进入 WebSocket frame 模式 → 双方独立 send/receive → 心跳/业务消息持续 → 任一方 close → 清理连接状态。多实例部署时还要处理连接落在哪台机器。

### 容易踩的坑

WebSocket 本身不保证业务消息持久可靠，断线期间消息可能丢。大规模连接要考虑 sticky session、broker/pubsub、背压和连接数。

### 面试时我会这样说

> 如果只是 LLM 单向吐 token，我不会因为“实时”就上 WebSocket，SSE 更简单。只有前后端都需要随时主动发消息，比如实时协作，我才更倾向 WebSocket，因为它的运维和状态管理成本更高。

## 最小代码 / 场景

```text
Client <====> Server
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI, WebSocket
app = FastAPI()

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    msg = await websocket.receive_text()
    await websocket.send_text("echo:" + msg)
```

### 运行 / 返回结果

```text
客户端发送：ping
客户端收到：echo:ping
```

## 🔗 关联知识

- [[07-SSE-vs-WebSocket]]
