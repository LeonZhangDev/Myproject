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
