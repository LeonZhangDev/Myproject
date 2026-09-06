---
tags: [week1]
difficulty: P0
status: learning
---

# Cache-Aside

## 一句话理解

读：先缓存，miss 查 DB 并回填；写：更新 DB 后删除缓存。

## 核心理解

让下一次读重新从数据库构建缓存。

## 最小代码 / 场景

```python
cached=await redis.get(key)
if not cached:
    task=await session.get(Task,id)
    await redis.set(key,json,ex=300)
```

## 🔗 关联知识

- [[03-缓存一致性]]
