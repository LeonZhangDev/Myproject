---
tags: [week1]
difficulty: P0
status: learning
---

# TTL

## 一句话理解

TTL 决定某个 Key 什么时候过期。

## 核心理解

它不同于内存达到上限时“删谁”的淘汰策略。

## 最小代码 / 场景

```redis
SET task:1 value EX 300
TTL task:1
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli SET session:1 abc EX 60
redis-cli GET session:1
```

### 运行 / 返回结果

```text
OK
"abc"

60 秒后再次 GET：
(nil)
```

## 🔗 关联知识

- [[08-内存淘汰策略]]
