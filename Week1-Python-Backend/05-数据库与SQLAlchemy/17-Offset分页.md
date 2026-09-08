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

## 🧠 完整理解

### 我会先这样理解

Offset 分页用 `LIMIT size OFFSET n` 跳过前面若干行，优点是简单、可以直接跳页，也很好和页码 UI 对接。缺点是 offset 很大时数据库通常仍需要找到/扫描前面那些行再丢掉，而且数据在翻页过程中新增或删除还可能造成重复/遗漏。

### 执行顺序 / 思考顺序

按稳定 ORDER BY 获取候选结果 → 跳过 offset 行 → 返回 limit 行 → 下一页 offset 增大。越往后跳过的行越多，成本可能越来越高。

### 容易踩的坑

没有稳定 ORDER BY 的 offset 分页结果不可靠；深分页性能差。后台管理页、小数据集通常没问题，大型时间流列表更适合游标分页。

### 面试时我会这样说

> Offset 分页我会用在需要“第几页”而且数据量不太大的后台列表，因为实现最简单。但如果是几百万行还要一直往后翻，OFFSET 1000000 会越来越慢，我会换 cursor/keyset。

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
