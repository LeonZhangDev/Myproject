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
