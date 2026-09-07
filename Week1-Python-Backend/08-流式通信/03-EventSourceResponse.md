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


## 🧪 简单例子与返回结果

### 例子

```python
from sse_starlette.sse import EventSourceResponse

async def gen():
    yield {"data": "hello"}
    yield {"data": "world"}

# FastAPI 路由中：
# return EventSourceResponse(gen())
```

### 运行 / 返回结果

```text
客户端流式收到：
data: hello

data: world
```

## 🔗 关联知识

- [[04-ServerSentEvent]]
