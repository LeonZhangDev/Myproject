---
tags: [week1]
difficulty: P0
status: learning
---

# WebSocket

## 一句话理解

全双工长连接，客户端和服务端都能主动发消息。

## 核心理解

适合实时协作、游戏、双向高频消息。

## 最小代码 / 场景

```text
Client <====> Server
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI, WebSocket
app = FastAPI()

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    msg = await websocket.receive_text()
    await websocket.send_text("echo:" + msg)
```

### 运行 / 返回结果

```text
客户端发送：ping
客户端收到：echo:ping
```

## 🔗 关联知识

- [[07-SSE-vs-WebSocket]]
