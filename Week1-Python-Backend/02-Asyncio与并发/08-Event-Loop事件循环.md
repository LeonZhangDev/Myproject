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


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def main():
    print("事件循环正在运行")

asyncio.run(main())
```

### 运行 / 返回结果

```text
事件循环正在运行
```

**怎么理解：** asyncio.run() 会创建并驱动事件循环，直到 main() 完成。

## 🔗 关联知识

- [[09-阻塞调用]]
- [[../03-FastAPI/17-ASGI与WSGI]]
