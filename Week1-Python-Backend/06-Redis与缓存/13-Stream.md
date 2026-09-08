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

## 🧠 完整理解

### 我会先这样理解

Redis Stream 是面向消息流的数据结构，每条消息有递增 ID 和字段内容，支持消费组、pending list、ack，因此比简单 Pub/Sub 更适合需要“消息被消费过没有”这类可靠消费语义。它可以用于轻量队列和事件流，但在超大规模消息系统中仍要和 Kafka/RabbitMQ 等做能力对比。

### 执行顺序 / 思考顺序

XADD 写入 Stream → 消费组 XREADGROUP 获取未投递/新消息 → 消息进入 PEL → 消费者处理成功 XACK → 失败消息仍可被追踪/claim；同时通过 MAXLEN 等控制流长度。

### 容易踩的坑

Stream 有消息确认不等于业务 exactly-once。消费者处理后在 ACK 前崩溃可能重复消费，所以业务仍然要幂等。长期不清理 PEL/Stream 会占内存。

### 面试时我会这样说

> 我会把 Redis Stream 看成“带消费进度和确认机制的 Redis 消息流”。比 Pub/Sub 靠谱，但消费者仍然可能收到重复消息，所以订单之类的处理我还是会做幂等。

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
