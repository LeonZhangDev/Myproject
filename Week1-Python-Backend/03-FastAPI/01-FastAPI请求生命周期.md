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

## 🧠 完整理解

### 我会先这样理解

一次 FastAPI 请求不是“直接调用路由函数”这么简单。请求先由 ASGI server 接收，依次经过中间件、路由匹配、参数提取、依赖解析、Pydantic 校验，再执行 endpoint，随后响应模型做序列化/过滤，最后响应再穿过中间件返回。把这条链搞清楚，排查 422、依赖异常、响应慢、日志位置都会容易很多。

### 执行顺序 / 思考顺序

Client → Uvicorn/ASGI → middleware 前半段 → router 匹配 → Depends 递归求值 → 参数/Pydantic 校验 → endpoint → response_model 序列化 → middleware 后半段 → Client。异常会在相应层被 exception handler 捕获和转换。

### 容易踩的坑

性能问题不一定在 endpoint 本身。依赖里查数据库、中间件里做同步 I/O、响应序列化过重都可能成为瓶颈。

### 面试时我会这样说

> 我排 FastAPI 问题时会先按请求生命周期定位：是还没进路由就失败，还是依赖失败，还是 endpoint 慢，还是响应序列化慢。这样比只盯着接口函数本身更容易找到根因。

## 最小代码 / 场景

```text
Request -> Middleware -> Route -> Depends -> Pydantic -> Business -> Response
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "hello"}
```

### 运行 / 返回结果

```text
GET /hello
→ 路由匹配
→ 参数/依赖处理
→ 执行 hello()
→ 序列化响应
→ 200 {"message":"hello"}
```

## 🔗 关联知识

- [[05-依赖注入]]
- [[10-中间件]]
