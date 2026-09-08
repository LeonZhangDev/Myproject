---
tags: [week1]
difficulty: P0
status: learning
---

# Redis String

## 一句话理解

适合普通值、计数器、幂等键、锁 token。

## 核心理解

Redis 的 INCR 是原子计数操作。

## 🧠 完整理解

### 我会先这样理解

String 是 Redis 最基础的数据类型，值可以是字符串、数字或二进制内容。缓存 JSON、计数器、token、分布式锁 key 都经常用它。`INCR`、`SET NX EX/PX` 等命令之所以实用，是因为单条 Redis 命令具有原子执行语义。

### 执行顺序 / 思考顺序

客户端发 SET/GET/INCR → Redis 单线程命令执行路径按顺序处理核心数据结构 → 更新/读取 key → 返回结果。String 本身可以配 TTL，也可以做条件写入。

### 容易踩的坑

不要把巨大 JSON 无限制塞进单个 String；修改其中一个字段也要整块重写。计数器还要考虑溢出、key 生命周期和持久化需求。

### 面试时我会这样说

> String 我用得最多，因为很多缓存其实就是 key → 一段值。除了普通 JSON，像计数器用 INCR、锁用 SET NX PX 都是基于 String，但复杂对象频繁改单字段时 Hash 可能更合适。

## 最小代码 / 场景

```redis
INCR page:view
SET request:123 done NX EX 60
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli SET counter 10
redis-cli INCR counter
redis-cli GET counter
```

### 运行 / 返回结果

```text
OK
(integer) 11
"11"
```

## 🔗 关联知识

- [[14-幂等键]]
