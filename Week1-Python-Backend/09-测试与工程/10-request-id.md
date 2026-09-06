---
tags: [week1]
difficulty: P0
status: learning
---

# request_id

## 一句话理解

一次请求的唯一关联标识。

## 核心理解

把中间件、DB、Redis、异常日志串成一条链。

## 最小代码 / 场景

```python
request_id=request.headers.get('X-Request-ID') or str(uuid.uuid4())
```

## 🔗 关联知识

- [[../03-FastAPI/10-中间件]]
