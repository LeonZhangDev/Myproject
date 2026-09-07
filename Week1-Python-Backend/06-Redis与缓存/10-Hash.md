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

## 最小代码 / 场景

```redis
HSET user:1 name Leon age 30
HGET user:1 name
```

## 🔗 关联知识

- [[09-String]]
