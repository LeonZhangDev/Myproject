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

## 🧠 完整理解

### 我会先这样理解

lifespan 用来管理应用级资源的启动与关闭生命周期，例如初始化数据库连接池、Redis 客户端、HTTP client、模型对象，关闭时统一释放。它和请求级 Depends 不同：lifespan 通常是整个进程只初始化一次，Depends 更常按请求获取/释放资源。

### 执行顺序 / 思考顺序

应用进程启动 → 进入 lifespan startup 部分 → 创建共享客户端/加载模型 → 开始接收请求 → 关闭信号到来 → 停止接收新请求并等待 → 进入 lifespan teardown → close/dispose 资源。

### 容易踩的坑

不要把每个请求独立的 Session 放成一个全局 lifespan 对象；共享的是 engine/client/pool，事务状态通常仍应请求隔离。多 worker 时每个进程都会各自执行 lifespan。

### 面试时我会这样说

> 我会把 lifespan 当成“应用进程的构造和析构”。像 Redis client、HTTP client、模型这种重资源启动一次就行；数据库 Session 这种带请求事务状态的东西仍然按请求创建，不能全局共用。

## 最小代码 / 场景

```python
@asynccontextmanager
async def lifespan(app):
    app.state.redis=create_client(); yield; await app.state.redis.aclose()
```


## 🧪 简单例子与返回结果

### 例子

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    yield
    print("shutdown")

app = FastAPI(lifespan=lifespan)
```

### 运行 / 返回结果

```text
服务启动：startup
...
服务关闭：shutdown
```

## 🔗 关联知识

- [[../01-Python核心/09-上下文管理器]]
