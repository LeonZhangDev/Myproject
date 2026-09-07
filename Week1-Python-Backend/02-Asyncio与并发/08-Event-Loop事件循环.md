---
tags: [week1]
difficulty: P0
status: learning
---

# Event Loop 事件循环

## 一句话理解

事件循环调度 Task、定时器和 I/O 就绪事件。

## 核心理解

协程在未完成 await 处让出；普通 CPU 计算/阻塞调用不会自动让出。

## 最小代码 / 场景

```text
Task A --await--> Loop --> Task B
```

## 🔗 关联知识

- [[09-阻塞调用]]
- [[../03-FastAPI/17-ASGI与WSGI]]
