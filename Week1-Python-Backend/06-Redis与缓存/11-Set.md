---
tags: [week1]
difficulty: P0
status: learning
---

# Redis Set

## 一句话理解

元素天然去重，适合去重和集合关系。

## 核心理解

重复 SADD 同一元素不会生成多个副本。

## 🧠 完整理解

### 我会先这样理解

Set 保存无序且不重复的成员，适合标签集合、去重、关注关系以及集合运算。`SADD` 天然去重，`SINTER/SUNION/SDIFF` 可以做交集、并集、差集。它解决的是“成员是否属于集合”和集合关系，不适合需要排序或重复计数的场景。

### 执行顺序 / 思考顺序

SADD 把成员加入集合 → 重复成员不会新增 → SISMEMBER 判断成员存在 → SINTER 等命令在集合间计算关系 → 返回无序成员结果。

### 容易踩的坑

大集合做交并集可能消耗 CPU，尤其在 Redis 主线程上执行时要评估延迟。需要排名时应该考虑 Sorted Set，而不是 Set。

### 面试时我会这样说

> 我把 Set 理解成“自动去重的成员集合”。比如文章标签、用户关注集合都很自然。如果还要按分数排序，那就不是 Set 的强项，我会换 ZSet。

## 最小代码 / 场景

```redis
SADD tags python fastapi python
```


## 🧪 简单例子与返回结果

### 例子

```bash
redis-cli SADD tags python fastapi python
redis-cli SMEMBERS tags
```

### 运行 / 返回结果

```text
(integer) 2
1) "python"
2) "fastapi"
```

**怎么理解：** Set 自动去重；SMEMBERS 的显示顺序不保证固定。

## 🔗 关联知识

- [[12-Sorted-Set]]
