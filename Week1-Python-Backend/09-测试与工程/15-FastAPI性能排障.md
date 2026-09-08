---
tags: [week1]
difficulty: P0
status: learning
---

# FastAPI 性能排障

## 一句话理解

慢接口先分段定位，不要第一反应就加缓存/加机器。

## 核心理解

顺序：首字节/总耗时 → request_id/trace → 外部 API → DB/池 → Redis → Event Loop → CPU/内存 → 最近发布 → 回归压测。

## 🧠 完整理解

### 我会先这样理解

FastAPI 性能排障应该按链路分层，而不是一慢就加 worker。先确认症状是延迟、吞吐还是错误率，再用 access log、request-id、APM/trace 拆出中间件、依赖、数据库、Redis、外部 HTTP、序列化各段耗时。找到主瓶颈后再针对性优化，并用同一压测条件回归。

### 执行顺序 / 思考顺序

建立基线 p50/p95/p99/QPS/错误率 → trace 一个慢请求 → 判断 CPU 还是 I/O → 看 event loop 是否被阻塞 → 查看 DB SQL/连接池、外部 API、Redis、响应大小 → 修复 → 重新压测 → 对比前后指标。

### 容易踩的坑

不要只看平均延迟；p99 才常暴露连接池耗尽、GC、慢 SQL。盲目增加并发/worker 可能让数据库更糟。压测必须固定数据、并发、机器和预热条件。

### 面试时我会这样说

> 我不会先猜“FastAPI 不够快”。我先看 p95/p99，再用 trace 判断时间到底花在数据库、外部接口、event loop 阻塞还是序列化。比如发现 Async endpoint 里用了 requests，那就先修这个，再用同一套压测验证收益。

## 最小代码 / 场景

```text
request -> route -> external API / DB / Redis -> response
```


## 🧪 简单例子与返回结果

### 例子

```text
现象：/chat P95 从 200ms 变成 2s
排查：request-id 日志 -> DB 慢查询 -> EXPLAIN ANALYZE
```

### 运行 / 返回结果

```text
定位到：某 SQL 发生 Seq Scan，耗时占大头
优化索引/查询后再 benchmark，确认 P95 是否下降。
```

## 🔗 关联知识

- [[09-日志]]
- [[../05-数据库与SQLAlchemy/19-连接池]]
- [[../02-Asyncio与并发/09-阻塞调用]]
