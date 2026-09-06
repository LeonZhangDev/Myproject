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

## 🔗 关联知识

- [[../03-FastAPI/05-依赖注入]]
- [[13-AsyncSession]]
