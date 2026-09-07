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

## 最小代码 / 场景

```redis
INCR page:view
SET request:123 done NX EX 60
```

## 🔗 关联知识

- [[14-幂等键]]
