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

## 🧠 完整理解

### 我会先这样理解

Request ID 是一次请求的唯一关联标识，用来把网关、API、数据库/下游调用相关日志串起来。客户端可传入可信格式的 id，也可以由服务端生成；随后通过中间件放入 request.state/contextvar，并在响应头和日志里传播。微服务环境还可以进一步使用 trace-id/span-id。

### 执行顺序 / 思考顺序

请求进入 → 中间件读取/生成 X-Request-ID → 存入上下文 → endpoint/service 日志自动带 id → 调下游时继续传 header → 响应返回同一 id → 出问题时按 id 搜索整条链路。

### 容易踩的坑

不要把用户任意超长 header 原样当 request-id 进入日志，需限制格式/长度。异步环境下全局变量存 request-id 会串请求，应该用 request.state 或 ContextVar。

### 面试时我会这样说

> Request ID 的价值就是把一堆分散日志串成“一次请求的故事”。我一般在 middleware 入口生成，然后所有日志自动带上，返回头也给客户端，用户报错时拿这个 id 就很好定位。

## 最小代码 / 场景

```python
request_id=request.headers.get('X-Request-ID') or str(uuid.uuid4())
```


## 🧪 简单例子与返回结果

### 例子

```python
request_id = "req-abc123"
print(f"[{request_id}] start")
print(f"[{request_id}] query db")
print(f"[{request_id}] done")
```

### 运行 / 返回结果

```text
[req-abc123] start
[req-abc123] query db
[req-abc123] done
```

**怎么理解：** 同一个 request-id 贯穿日志后，可以快速把一次请求的多条日志串起来。

## 🔗 关联知识

- [[../03-FastAPI/10-中间件]]
