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

## 🧠 完整理解

### 我会先这样理解

SSE（Server-Sent Events）是基于 HTTP 的服务器单向推送协议，响应类型通常是 `text/event-stream`，每个事件由 `data:`、`event:`、`id:` 等字段按文本格式分隔。浏览器原生 EventSource 支持断线重连，特别适合通知、日志、LLM token 等“服务器持续推给客户端”的场景。

### 执行顺序 / 思考顺序

客户端建立 GET 长连接 → 服务端返回 event-stream 响应 → 持续写 `data: ...

` → 浏览器每收到完整事件就触发 message/event 回调 → 断开时 EventSource 可按 retry/Last-Event-ID 机制重连。

### 容易踩的坑

SSE 是单向服务器→客户端，客户端要发送复杂实时消息仍需普通 HTTP 或 WebSocket。代理缓冲、超时、心跳和客户端断开后的任务取消都要处理。

### 面试时我会这样说

> LLM 输出我很喜欢 SSE，因为需求本来就是服务端不断往前端推 token，不需要双向实时通信。协议又是普通 HTTP，部署比 WebSocket 简单；但我会配心跳和代理禁缓冲。

## 最小代码 / 场景

```text
event: token
data: {"content":"你"}

```


## 🧪 简单例子与返回结果

### 例子

```text
data: hello

data: world
```

### 运行 / 返回结果

```text
浏览器依次收到两个 SSE 消息：
hello
world
```

**怎么理解：** SSE 每条事件以空行分隔，典型字段是 data:。

## 🔗 关联知识

- [[03-EventSourceResponse]]
- [[07-SSE-vs-WebSocket]]
