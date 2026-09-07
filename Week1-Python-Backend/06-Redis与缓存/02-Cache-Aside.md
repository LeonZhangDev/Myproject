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


## 🧪 简单例子与返回结果

### 例子

```python
cached = r.get("user:1")
if cached:
    print("Redis命中")
else:
    print("查数据库")
    r.set("user:1", '{"id":1}', ex=300)
```

### 运行 / 返回结果

```text
首次：查数据库
后续缓存未过期时：Redis命中
```

## 🔗 关联知识

- [[03-缓存一致性]]
