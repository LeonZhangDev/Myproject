---
tags: [week1]
difficulty: P0
status: learning
---

# HTTP 长连接基础

## 一句话理解

流式响应在连接保持期间持续发送数据块/事件。

## 核心理解

和一次性返回完整 JSON 的普通响应不同。

## 🧠 完整理解

### 我会先这样理解

HTTP 长连接要区分两个概念：TCP 连接复用（keep-alive）和“一个 HTTP 响应持续很久不断发送数据”。前者减少反复握手，后者用于 streaming/SSE。LLM 流式输出通常是服务器先发送响应头，然后分块持续发送 token，连接在生成结束后才关闭。

### 执行顺序 / 思考顺序

客户端建立 TCP/TLS → 发 HTTP 请求 → 服务端返回响应头 → 普通响应一次/有限 body 后结束；流式响应则 body 分多次 send → 客户端边到边消费 → 完成后响应结束，TCP 是否继续复用取决于协议/连接管理。

### 容易踩的坑

代理、负载均衡、CDN 可能有 idle timeout 或 buffering，导致本地能流式、线上却攒成一坨才返回。需要同时配置应用和基础设施。

### 面试时我会这样说

> 我会先区分 keep-alive 和 streaming。keep-alive 是多个请求复用连接；SSE/LLM 流式是同一个响应一直没结束，服务端持续往 body 里推数据。线上还要特别看 Nginx 是否缓冲。

## 最小代码 / 场景

```text
request -> chunk -> chunk -> chunk -> done
```


## 🧪 简单例子与返回结果

### 例子

```text
普通响应：请求 -> 等全部完成 -> 一次返回
流式响应：请求 -> chunk1 -> chunk2 -> chunk3 -> 连接结束
```

### 运行 / 返回结果

```text
客户端可以在服务器尚未生成全部内容时，先看到前面的 chunk。
```

## 🔗 关联知识

- [[02-SSE]]
- [[06-WebSocket]]
