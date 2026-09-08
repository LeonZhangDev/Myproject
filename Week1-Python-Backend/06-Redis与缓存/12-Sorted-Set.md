---
tags: [week1]
difficulty: P0
status: learning
---

# Redis Sorted Set

## 一句话理解

成员有 score，并按 score 排序。

## 核心理解

适合排行榜、时间排序。

## 🧠 完整理解

### 我会先这样理解

Sorted Set（ZSet）在不重复 member 的基础上给每个 member 一个 score，并按 score 排序。它很适合排行榜、延迟队列时间索引、按权重/时间取范围。score 相同的成员还会按规则继续排序。关键优势是能高效地按排名和分数范围查询。

### 执行顺序 / 思考顺序

ZADD member score → Redis 同时维护成员唯一性和有序结构 → ZRANGE/ZREVRANGE 按排名取 → ZRANGEBYSCORE 按分数区间取 → 更新同一 member 的 score 会改变其位置。

### 容易踩的坑

score 是双精度浮点语义，大整数时间戳/精度边界要留意。超大排行榜频繁范围查询也要评估内存和热点。

### 面试时我会这样说

> 排行榜我第一反应就是 ZSet，因为 member 天然唯一，score 决定排序。比如分数变化只要 ZADD 更新 score，然后直接按排名取前 100，不需要应用层每次重新排序。

## 最小代码 / 场景

```redis
ZADD rank 100 alice
ZADD rank 80 bob
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli ZADD rank 100 Alice 80 Bob
redis-cli ZREVRANGE rank 0 -1 WITHSCORES
```

### 运行 / 返回结果

```text
1) "Alice"
2) "100"
3) "Bob"
4) "80"
```

## 🔗 关联知识

- [[11-Set]]
