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
