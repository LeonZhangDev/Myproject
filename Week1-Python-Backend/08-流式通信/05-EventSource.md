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

## 最小代码 / 场景

```javascript
const source=new EventSource('/stream')
source.onmessage=(event)=>console.log(event.data)
```

## 🔗 关联知识

- [[02-SSE]]
