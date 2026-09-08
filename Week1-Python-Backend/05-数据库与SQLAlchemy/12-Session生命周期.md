---
tags: [week1]
difficulty: P0
status: learning
---

# Session 生命周期

## 一句话理解

Web 中通常每请求一个 Session，请求结束提交/回滚/关闭。

## 核心理解

不要把一个 Session 作为跨请求全局对象。

## 🧠 完整理解

### 我会先这样理解

Web 服务里最常见的 Session 生命周期是“请求级”：请求开始获取 Session，请求内所有数据库操作共享这个事务上下文，请求成功按业务显式 commit，请求失败 rollback，最后一定 close。这样事务状态不会串到其他请求，也便于依赖注入和测试。

### 执行顺序 / 思考顺序

请求进入 → Depends/get_db 创建 Session → service/repository 共用它 → 执行查询/flush/commit → 异常则 rollback → finally close → 连接归还池 → 响应结束。

### 容易踩的坑

“一个请求一个 Session”不等于“一个请求一个物理连接始终占着”。Session 可能按需获取连接；另一方面，一个请求里也不要随意创建很多独立 Session 破坏同一事务语义。

### 面试时我会这样说

> 我的默认做法就是 request-scoped Session。请求之间一定隔离，同一请求的 service 可以共享一个 Session，这样事务边界也好控制；最后无论成功失败都要 close/rollback 干净。

## 最小代码 / 场景

```python
async def get_session():
    async with SessionLocal() as s:
        try: yield s
        except: await s.rollback(); raise
```


## 🧪 简单例子与返回结果

### 例子

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 运行 / 返回结果

```text
请求 A -> 创建 Session A -> 使用 -> close
请求 B -> 创建 Session B -> 使用 -> close
```

**怎么理解：** Web 请求通常一请求一个 Session，避免不同请求共享事务状态和 ORM 对象状态。

## 🔗 关联知识

- [[../03-FastAPI/05-依赖注入]]
- [[13-AsyncSession]]
