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
