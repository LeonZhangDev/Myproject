---
tags: [week1, interview, e]
difficulty: P0
status: learning
---

# E｜Redis与缓存


## W1-Q31｜缓存与数据库数据不一致时，你会怎样处理？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
先确认一致性要求，再选 Cache-Aside、写后失效、版本号、消息同步；设置 TTL 并处理删除失败。关键数据以数据库为准。

### 最小代码 / 场景
```text
UPDATE DB -> COMMIT -> DELETE CACHE
```

### 关联知识
- [[../06-Redis与缓存/03-缓存一致性]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q32｜Cache-Aside 模式的基本读写流程是什么？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
读：先缓存，miss 查数据库并回填；写：通常更新数据库成功后删除缓存，让下一次读重建。

### 最小代码 / 场景
```python
cached=await redis.get(key)
if not cached:
    obj=await session.get(Task,id)
    await redis.set(key,obj_json,ex=300)
```

### 关联知识
- [[../06-Redis与缓存/02-Cache-Aside]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q33｜缓存穿透、缓存击穿和缓存雪崩分别是什么？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
穿透：查不存在数据；击穿：热点 Key 失效大量回源；雪崩：大量 Key 同时失效。分别用空值短缓存/布隆、互斥重建、TTL 打散/限流降级。

### 最小代码 / 场景
```text
穿透: cache miss + DB miss
击穿: hot key expired
雪崩: many keys expired
```

### 关联知识
- [[../06-Redis与缓存/04-缓存穿透]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q34｜使用 Redis 实现分布式锁时需要注意哪些问题？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
至少用 SET key token NX PX 原子加锁；合理过期；唯一 token；比较 token 后删除；长任务考虑续期。不能替代数据库唯一约束和业务幂等。

### 最小代码 / 场景
```redis
SET lock:1 token-abc NX PX 10000
```

### 关联知识
- [[../06-Redis与缓存/15-分布式锁]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q35｜Redis 的 TTL 和内存淘汰策略有什么区别？常见数据结构怎样选择？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
TTL 决定某 Key 何时过期；淘汰策略决定内存上限时删谁。String 计数/幂等，Hash 对象字段，Set 去重，Sorted Set 排序，Stream 消息流。

### 最小代码 / 场景
```redis
INCR counter
HSET user:1 name Leon
SADD tags python
ZADD rank 100 alice
XADD events * type created
```

### 关联知识
- [[../06-Redis与缓存/07-TTL]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？
