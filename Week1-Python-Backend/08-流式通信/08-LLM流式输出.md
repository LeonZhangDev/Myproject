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


## 🧪 简单例子与返回结果

### 例子

```python
async def fake_llm():
    for token in ["你", "好", "！"]:
        yield token

async for token in fake_llm():
    print(token, end="", flush=True)
```

### 运行 / 返回结果

```text
你好！
```

**怎么理解：** 真实 LLM 接口也是不断产出 token/chunk，再通过 SSE 或 WebSocket 推给前端。

## 🔗 关联知识

- [[02-SSE]]
