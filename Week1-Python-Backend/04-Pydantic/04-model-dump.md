---
tags: [week1]
difficulty: P0
status: learning
---

# model_dump

## 一句话理解

把 Pydantic 模型转换成普通字典。

## 核心理解

JSON 可用 `model_dump_json()`。

## 最小代码 / 场景

```python
data=task.model_dump()
```

## 🔗 关联知识

- [[08-字典解包]]
