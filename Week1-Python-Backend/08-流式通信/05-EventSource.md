---
tags: [week1]
difficulty: P0
status: learning
---

# EventSource

## 一句话理解

浏览器连接 SSE 的客户端 API。

## 核心理解

`event.data` 是服务端发送的 data 字段。

## 🧠 完整理解

### 我会先这样理解

EventSource 是浏览器原生的 SSE 客户端 API，给一个 URL 后会维护 HTTP 长连接，接收 message/自定义事件，并在非主动关闭时自动重连。它使用起来简单，但原生 API 对自定义请求 header 支持有限，因此带 Bearer Authorization 的场景常需要 Cookie、query token（需谨慎）或改用 fetch streaming。

### 执行顺序 / 思考顺序

`new EventSource(url)` → 浏览器发 GET → 收到 text/event-stream → 逐事件解析 → 调 onmessage/addEventListener → 连接异常自动重试并可能携带 Last-Event-ID → 调 close 才主动停止。

### 容易踩的坑

EventSource 不能像 fetch 那样自由设置所有 headers；跨域还要正确 CORS。页面卸载、切换会话时记得 close，避免留下无用连接。

### 面试时我会这样说

> 前端如果只是接 SSE，EventSource 非常省事，还自带重连。但它的 header 控制比较弱，所以鉴权设计要提前考虑；如果必须自定义 Authorization，我可能会用 fetch 读流。

## 最小代码 / 场景

```javascript
const source=new EventSource('/stream')
source.onmessage=(event)=>console.log(event.data)
```


## 🧪 简单例子与返回结果

### 例子

```javascript
const es = new EventSource("/events");
es.onmessage = (event) => {
  console.log(event.data);
};
```

### 运行 / 返回结果

```text
服务器发送 data: hello
浏览器控制台：
hello
```

## 🔗 关联知识

- [[02-SSE]]
