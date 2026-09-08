---
tags: [week1]
difficulty: P0
status: learning
---

# ServerSentEvent

## 一句话理解

表示 SSE 流中的一条事件。

## 核心理解

EventSourceResponse 是整条流，ServerSentEvent 是流中的一条消息。

## 🧠 完整理解

### 我会先这样理解

ServerSentEvent 通常表示一条结构化 SSE 事件，可以包含 data、event、id、retry、comment 等字段。它比直接 yield 一段字符串更明确，尤其当客户端需要区分 `token`、`done`、`error` 等事件类型时。id 还能帮助断线重连后恢复事件位置。

### 执行顺序 / 思考顺序

业务创建事件对象 → 序列化为多行 SSE 字段 → 每个事件以空行结束 → EventSource 解析 event 类型和 data → 分发到对应监听器。若设置 id，浏览器会记录 Last-Event-ID 用于重连。

### 容易踩的坑

data 内有换行时必须按 SSE 规范逐行编码；不要把任意异常堆栈直接塞进 error event 给前端。事件 schema 也需要版本和兼容思维。

### 面试时我会这样说

> 我更愿意把 LLM 流式协议做成明确事件，比如 `event: token`、`event: done`、`event: error`。前端就不用通过字符串内容猜“是不是结束了”，后续协议也好扩展。

## 最小代码 / 场景

```python
yield ServerSentEvent(event='token', data='hi')
```


## 🧪 简单例子与返回结果

### 例子

```python
from sse_starlette import ServerSentEvent

event = ServerSentEvent(data="hello", event="message", id="1")
print(str(event))
```

### 运行 / 返回结果

```text
id: 1
event: message
data: hello
```

**怎么理解：** 实际库版本的字符串格式细节可能略有差异，但核心字段就是 id/event/data。

## 🔗 关联知识

- [[../01-Python核心/06-生成器与yield]]
