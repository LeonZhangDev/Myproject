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
