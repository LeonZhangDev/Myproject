---
tags: [week1]
difficulty: P0
status: learning
---

# FastAPI 请求生命周期

## 一句话理解

一次请求会经过中间件、路由、依赖、校验、业务和响应。

## 核心理解

理解这条链后，Session、request_id、异常处理为什么放在不同位置就更清楚。

## 最小代码 / 场景

```text
Request -> Middleware -> Route -> Depends -> Pydantic -> Business -> Response
```

## 🔗 关联知识

- [[05-依赖注入]]
- [[10-中间件]]
