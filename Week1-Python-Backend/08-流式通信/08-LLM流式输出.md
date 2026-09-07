---
tags: [week1]
difficulty: P0
status: learning
---

# LLM 流式输出

## 一句话理解

模型不断产生 token/chunk，服务端持续推送给前端。

## 核心理解

SSE 能很好承载这种 Server -> Client 流。

## 最小代码 / 场景

```python
async for token in llm_stream():
    yield ServerSentEvent(event='token', data=token)
```

## 🔗 关联知识

- [[02-SSE]]
