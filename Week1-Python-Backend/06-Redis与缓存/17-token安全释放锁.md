---
tags: [week1]
difficulty: P0
status: learning
---

# token 安全释放锁

## 一句话理解

释放前必须确认锁仍属于自己。

## 核心理解

否则旧持有者可能误删已经被新持有者获得的锁；实际用 Lua 保证比较+删除原子。

## 最小代码 / 场景

```text
if redis_token == my_token: delete lock
```

## 🔗 关联知识

- [[15-分布式锁]]
