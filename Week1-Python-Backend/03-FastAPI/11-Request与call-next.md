---
tags: [week1]
difficulty: P0
status: learning
---

# Request 与 call_next

## 一句话理解

Request 表示当前请求；`call_next(request)` 把请求交给后续路由。

## 核心理解

`call_next` 由框架传给中间件。

## 最小代码 / 场景

```python
response=await call_next(request)
```

## 🔗 关联知识

- [[10-中间件]]
