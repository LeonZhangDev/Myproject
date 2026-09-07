---
tags: [week1]
difficulty: P0
status: learning
---

# FastAPI lifespan

## 一句话理解

管理应用级共享资源：启动时初始化，关闭时释放。

## 核心理解

连接池、Redis 客户端、模型、共享 HTTP Client 适合在 lifespan 管理。

## 最小代码 / 场景

```python
@asynccontextmanager
async def lifespan(app):
    app.state.redis=create_client(); yield; await app.state.redis.aclose()
```

## 🔗 关联知识

- [[../01-Python核心/09-上下文管理器]]
