---
tags: [week1]
difficulty: P0
status: learning
---

# ServerSentEvent

## 一句话理解

表示 SSE 流中的一条事件。

## 核心理解

EventSourceResponse 是整条流，ServerSentEvent 是流中的一条消息。

## 最小代码 / 场景

```python
yield ServerSentEvent(event='token', data='hi')
```

## 🔗 关联知识

- [[../01-Python核心/06-生成器与yield]]
