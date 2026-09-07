---
tags: [week1]
difficulty: P0
status: learning
---

# EventSourceResponse

## 一句话理解

表示整条 SSE HTTP 响应。

## 核心理解

它负责保持流并把生成器中的事件持续发送给客户端。

## 最小代码 / 场景

```python
@app.get('/stream', response_class=EventSourceResponse)
```

## 🔗 关联知识

- [[04-ServerSentEvent]]
