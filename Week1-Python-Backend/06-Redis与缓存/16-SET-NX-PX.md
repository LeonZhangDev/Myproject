---
tags: [week1]
difficulty: P0
status: learning
---

# SET NX PX

## 一句话理解

NX=不存在才写；PX=毫秒级过期。

## 核心理解

组合在同一条 SET 中实现原子“抢锁+过期”。

## 🧠 完整理解

### 我会先这样理解

`SET key value NX PX ttl` 把“key 不存在才写入”和“设置过期时间”合并成一条原子命令，是 Redis 简单分布式锁的基础。NX 保证同一时刻只有一个竞争者创建锁 key，PX 给锁设置毫秒级租约，value 则应该放唯一 token 标识锁的所有者。

### 执行顺序 / 思考顺序

竞争者发送 SET lock token NX PX 10000 → Redis 原子检查 key 是否存在 → 不存在则写 token+TTL 并返回 OK → 已存在返回空/失败 → 获锁者进入临界区。

### 容易踩的坑

不要用 `SETNX` 成功后再单独 `EXPIRE`，两条命令中间进程崩溃可能留下永不过期的锁。TTL 也不能随便拍脑袋，要覆盖合理执行时间或配合续租。

### 面试时我会这样说

> 我会强调为什么是 SET NX PX 一条命令：因为“抢锁”和“设过期”必须原子。如果分成 SETNX 再 EXPIRE，刚抢到锁进程就挂了，可能留下死锁。

## 最小代码 / 场景

```redis
SET lock:1 random-token NX PX 10000
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli SET lock:job abc NX PX 10000
redis-cli SET lock:job xyz NX PX 10000
```

### 运行 / 返回结果

```text
OK
(nil)
```

**怎么理解：** NX=key 不存在才写入；PX=毫秒 TTL。第二次因为锁已存在而失败。

## 🔗 关联知识

- [[15-分布式锁]]
