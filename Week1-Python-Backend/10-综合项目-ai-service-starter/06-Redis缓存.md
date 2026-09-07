---
tags: [week1, project]
difficulty: P0
status: learning
---
# Redis 缓存
```text
GET cache -> hit return
          -> miss SELECT DB -> SET EX 300 -> return
UPDATE DB -> COMMIT -> DELETE cache
```

关联：[[../06-Redis与缓存/02-Cache-Aside]]、[[../06-Redis与缓存/03-缓存一致性]]。
