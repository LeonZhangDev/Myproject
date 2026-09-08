---
tags: [week1]
difficulty: P0
status: learning
---

# Redis Hash

## 一句话理解

适合对象的多个字段，可单独读写字段。

## 核心理解

避免为一个简单对象拆太多独立 Key。

## 🧠 完整理解

### 我会先这样理解

Hash 适合一个 key 下保存多个字段，例如 `user:1` 下有 name、age、status。与把整个对象序列化成 String 相比，它可以单独读取/更新字段，适合字段级操作；但是否更省内存取决于对象大小和 Redis 内部编码，不应机械认为 Hash 永远更优。

### 执行顺序 / 思考顺序

HSET key field value → Redis 在一个 hash 对象中维护多个 field → HGET/HMGET 读取需要字段 → 可对单字段修改而不重写整个对象。TTL 通常作用在整个 key 上，而不是单个 field。

### 容易踩的坑

如果需要每个字段独立过期，普通 Hash 语义并不直接满足。超大 Hash 也可能形成热点 key；对象结构经常整体读写时 String JSON 反而更简单。

### 面试时我会这样说

> 我一般把 Hash 用在“一个对象很多字段，而且经常只改单个字段”的场景。比如用户状态。但 TTL 通常是整个 user key 一起过期，所以如果字段生命周期完全不同，我就不会硬塞一个 Hash。

## 最小代码 / 场景

```redis
HSET user:1 name Leon age 30
HGET user:1 name
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli HSET user:1 name Leon age 25
redis-cli HGET user:1 name
```

### 运行 / 返回结果

```text
(integer) 2
"Leon"
```

## 🔗 关联知识

- [[09-String]]
