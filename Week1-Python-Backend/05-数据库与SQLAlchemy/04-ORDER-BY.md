---
tags: [week1]
difficulty: P0
status: learning
---

# ORDER BY

## 一句话理解

指定结果排序规则。

## 核心理解

分页必须使用稳定排序，常加唯一键作为最终排序条件。

## 最小代码 / 场景

```sql
ORDER BY created_at DESC,id DESC
```

## 🔗 关联知识

- [[17-Offset分页]]
- [[18-游标分页]]
