---
tags: [week1]
difficulty: P0
status: learning
---

# AsyncSession

## 一句话理解

异步 Session 仍是可变、有状态的事务上下文。

## 核心理解

多个并发 Task 共享会让连接、事务、ORM 状态互相干扰。

## 🧠 完整理解

### 我会先这样理解

AsyncSession 是 SQLAlchemy 异步 ORM 的事务/工作单元对象，搭配异步数据库驱动使用。它允许数据库 I/O 在 await 时让出事件循环，但它仍然是有事务状态的对象，不应该被多个并发 Task 同时共享使用。异步只是改变 I/O 调度方式，不改变 Session 需要独立生命周期这个事实。

### 执行顺序 / 思考顺序

请求创建 AsyncSession → `await session.execute(...)` → 驱动异步等待数据库 → 当前 Task 让出 event loop → 结果回来继续 → flush/commit/rollback → close。一个 Session 的事务操作应由单个逻辑任务有序推进。

### 容易踩的坑

不要在 `asyncio.gather` 里让多个 Task 共用同一个 AsyncSession 并发执行。需要真正并发数据库操作时应评估独立 Session/连接以及事务语义。

### 面试时我会这样说

> 我会说 AsyncSession 的“async”只说明数据库 I/O 可以 await，不代表 Session 本身可以并发共享。Session 有事务和 identity map 状态，所以还是一个请求/一个工作单元独立使用最稳。

## 最小代码 / 场景

```python
# avoid: gather(do_a(session), do_b(session))
```


## 🧪 简单例子与返回结果

### 例子

```python
result = await db.execute(
    select(User).where(User.id == 1)
)
user = result.scalar_one()
print(user.id)
```

### 运行 / 返回结果

```text
1
```

## 🔗 关联知识

- [[12-Session生命周期]]
- [[../02-Asyncio与并发/13-竞态条件]]
