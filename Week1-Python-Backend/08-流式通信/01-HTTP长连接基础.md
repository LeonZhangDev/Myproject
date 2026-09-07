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

## 最小代码 / 场景

```text
request -> chunk -> chunk -> chunk -> done
```

## 🔗 关联知识

- [[02-SSE]]
- [[06-WebSocket]]
