---
tags: [week1]
difficulty: P0
status: learning
---

# Redis Stream

## 一句话理解

追加式消息流，支持消息 ID 和消费组。

## 核心理解

适合轻量事件流，但不要自动等同于完整企业消息队列。

## 最小代码 / 场景

```redis
XADD events * type task_created task_id 123
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli XADD events 1-0 type login user 42
redis-cli XRANGE events - +
```

### 运行 / 返回结果

```text
1) 1-0
2) 1) "type"
   2) "login"
   3) "user"
   4) "42"
```

## 🔗 关联知识

- [[18-延迟双删与消息同步]]
