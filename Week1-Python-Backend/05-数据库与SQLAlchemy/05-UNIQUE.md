---
tags: [week1]
difficulty: P0
status: learning
---

# UNIQUE

## 一句话理解

数据库唯一约束保证指定列/组合不重复。

## 核心理解

它首先是正确性约束，其次常通过唯一索引实现。

## 🧠 完整理解

### 我会先这样理解

UNIQUE 是数据库层对“某列或某组列不能重复”的强约束。它不只是一个查询优化手段，更重要的是在并发条件下保证业务不变量，比如邮箱唯一、订单业务号唯一。应用层先查重只能提供友好提示，不能取代数据库 UNIQUE，因为两个并发事务可能同时查到“不存在”。

### 执行顺序 / 思考顺序

INSERT/UPDATE 到达数据库 → 数据库检查唯一索引/约束 → 没冲突则继续写入 → 有冲突则语句失败并让事务进入相应错误路径 → 应用捕获 IntegrityError 并转成 409 等业务响应。

### 容易踩的坑

NULL 与 UNIQUE 的语义因数据库而异；复合 UNIQUE 约束的是字段组合，不是每个字段分别唯一。别把所有重复错误都当 500。

### 面试时我会这样说

> 我会把 UNIQUE 当成最终一致性底线。注册邮箱可以先查一下告诉用户“已存在”，但最终数据库必须有 UNIQUE，否则两个并发注册请求还是可能同时通过应用层检查。

## 最小代码 / 场景

```sql
CREATE UNIQUE INDEX uq_users_email ON users(email);
```


## 🧪 简单例子与返回结果

### 例子

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE
);

INSERT INTO users(email) VALUES ('a@test.com');
INSERT INTO users(email) VALUES ('a@test.com');
```

### 运行 / 返回结果

```text
第一次 INSERT：成功
第二次 INSERT：失败，duplicate key / unique constraint violation
```

## 🔗 关联知识

- [[../04-Pydantic/10-Pydantic与数据库约束]]
- [[../06-Redis与缓存/14-幂等键]]
