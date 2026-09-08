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

## 🧠 完整理解

### 我会先这样理解

`EventSourceResponse` 是一些 ASGI/SSE 库提供的响应封装，用来把异步生成器产生的事件按 SSE 协议持续发送。相比手工拼 StreamingResponse，它通常会处理 content-type、事件编码、断连/心跳等常见细节。应用代码只需要 yield 字符串或结构化事件。

### 执行顺序 / 思考顺序

endpoint 返回 EventSourceResponse(generator) → ASGI 开始发送 SSE headers → 迭代 async generator → 每次 yield 转换成 SSE frame 并 send → 客户端断开或生成器结束 → 清理资源并结束响应。

### 容易踩的坑

不同库对 yield 的 dict 格式、ping、断连检测支持不同，不能只凭类名假设 API。生成器内部也要处理 CancelledError/finally，确保上游 LLM/DB 资源释放。

### 面试时我会这样说

> 我把 EventSourceResponse 看成 SSE 的协议适配层。业务生成器负责产生事件，它负责按 event-stream 正确发出去。这样我不需要每次自己拼 `data:

`，但断连和清理我还是会认真处理。

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
