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

## 🧠 完整理解

### 我会先这样理解

ORDER BY 要求数据库按照一个或多个键返回稳定顺序。小数据排序很简单，但大结果集排序可能需要额外内存甚至落盘；如果排序字段和过滤条件能匹配合适的复合索引，数据库有机会直接按索引顺序读取，省掉显式 sort。分页场景还需要稳定的唯一排序键，否则翻页期间容易重复或漏数据。

### 执行顺序 / 思考顺序

先得到满足过滤/连接条件的候选行 → 若执行计划不能直接提供所需顺序，则做 sort → 按 ASC/DESC 和多个键比较 → LIMIT/OFFSET 再截取所需部分。

### 容易踩的坑

只按 `created_at` 排序但它不是唯一值时，很多行同时间戳，分页顺序可能不稳定。常用 `ORDER BY created_at DESC, id DESC` 增加确定性。

### 面试时我会这样说

> 我会把 ORDER BY 和分页一起看。比如按创建时间翻页，我通常再带一个 id 做稳定排序；数据量大时还会看复合索引能不能同时服务 WHERE 和 ORDER BY，避免每次大排序。

## 最小代码 / 场景

```sql
ORDER BY created_at DESC,id DESC
```


## 🧪 简单例子与返回结果

### 例子

```sql
SELECT name, score
FROM users
ORDER BY score DESC;
```

### 运行 / 返回结果

```text
Tom  | 95
Leon | 88
Amy  | 80
```

## 🔗 关联知识

- [[17-Offset分页]]
- [[18-游标分页]]
