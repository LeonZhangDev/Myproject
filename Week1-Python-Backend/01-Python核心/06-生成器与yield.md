---
tags: [week1]
difficulty: P0
status: learning
---

# 生成器与 yield

## 一句话理解

生成器用 `yield` 简洁地创建惰性迭代器。

## 核心理解

适合大文件、流式数据、SSE token；数据按需生成，不必一次性占满内存。

## 最小代码 / 场景

```python
def nums():
    yield 1
    yield 2
for x in nums(): print(x)
```

## 🔗 关联知识

- [[05-迭代器]]
- [[../08-流式通信/02-SSE]]
