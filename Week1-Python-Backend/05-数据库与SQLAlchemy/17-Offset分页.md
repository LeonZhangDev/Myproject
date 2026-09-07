---
tags: [week1]
difficulty: P0
status: learning
---

# Offset 分页

## 一句话理解

LIMIT/OFFSET 简单且支持跳页。

## 核心理解

深分页扫描成本高，数据并发变化可能重复/遗漏。

## 最小代码 / 场景

```sql
SELECT * FROM tasks ORDER BY id DESC LIMIT 20 OFFSET 10000;
```


## 🧪 简单例子与返回结果

### 例子

```sql
SELECT id, title
FROM tasks
ORDER BY id
LIMIT 10 OFFSET 20;
```

### 运行 / 返回结果

```text
返回排序后的第 21～30 条记录。
```

## 🔗 关联知识

- [[18-游标分页]]
