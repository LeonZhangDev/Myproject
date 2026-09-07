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
