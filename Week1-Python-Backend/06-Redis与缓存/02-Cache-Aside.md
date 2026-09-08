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

## 🧠 完整理解

### 我会先这样理解

Cache-Aside 是最常见的缓存模式：应用自己负责读缓存、miss 时查数据库并回填；更新时通常先更新数据库，再删除缓存，让下一次读取重新加载。数据库仍是事实来源，缓存是可丢弃副本，因此逻辑直观、容错性好。

### 执行顺序 / 思考顺序

读：GET cache → hit 返回 → miss 查 DB → SET cache + TTL → 返回。写：UPDATE DB 成功 → DEL cache → 下一次读 miss → 从 DB 重建最新缓存。

### 容易踩的坑

“更新数据库再删缓存”仍存在很小并发窗口，极端一致性要求需要版本号、消息同步等更强方案。先删缓存再更新 DB 更容易被并发旧读回填脏值。

### 面试时我会这样说

> 我项目里默认会从 Cache-Aside 开始，因为数据库是主数据，Redis 丢了也能重建。读 miss 就回源，写我通常先改 DB 再删缓存，不直接同时更新两份，减少双写一致性复杂度。

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
