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
