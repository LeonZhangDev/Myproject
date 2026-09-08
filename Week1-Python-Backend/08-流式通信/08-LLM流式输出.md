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

## 🧠 完整理解

### 我会先这样理解

LLM 流式输出的目标不是让模型总计算时间一定变短，而是降低用户感知的首 token 延迟，让生成中的内容持续可见。后端通常从模型 API/vLLM 收到增量 token，再立即转成 SSE/chunk 发给前端。完整链路还要处理客户端断开、上游取消、usage、finish_reason 和最终落库。

### 执行顺序 / 思考顺序

用户请求 → 后端调用 LLM stream=true → 上游返回增量 chunk → 后端解析 delta → 立即 yield SSE token → 前端追加渲染 → finish_reason/done → 后端汇总完整答案、记录 usage/落库 → 关闭流。

### 容易踩的坑

不要每个 token 都同步写一次数据库，会严重放大 I/O；通常内存累积后结束时落一次。客户端断开后如果不取消上游生成，会浪费 GPU/token 成本。

### 面试时我会这样说

> 我做 LLM stream 会分两条线：一条是 token 尽快往前端发，另一条是后台累积完整回答，结束后一次落库。客户端如果断开，我还会尽量把上游生成一起取消，不让 GPU 继续白算。

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
