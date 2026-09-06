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

## 🔗 关联知识

- [[09-日志]]
- [[../05-数据库与SQLAlchemy/19-连接池]]
- [[../02-Asyncio与并发/09-阻塞调用]]
