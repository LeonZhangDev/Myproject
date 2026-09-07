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
