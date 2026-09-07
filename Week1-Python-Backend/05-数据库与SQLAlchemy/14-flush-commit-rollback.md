---
tags: [week1]
difficulty: P0
status: learning
---

# flush、commit、rollback

## 一句话理解

flush 发 SQL 但不结束事务；commit 提交；rollback 撤销未提交事务。

## 核心理解

flush 后常能拿到数据库生成主键，但其他事务未必可见。

## 最小代码 / 场景

```python
await session.flush(); await session.commit()
```


## 🧪 简单例子与返回结果

### 例子

```python
user = User(name="Leon")
db.add(user)
await db.flush()
print(user.id)       # 已拿到数据库生成的 id
await db.rollback()  # 事务撤销
```

### 运行 / 返回结果

```text
例如：
1

随后 rollback，数据库中不会保留这条未提交记录。
```

**怎么理解：** flush 把 SQL 发给数据库但不等于最终提交；commit 才提交事务；rollback 撤销当前事务。

## 🔗 关联知识

- [[10-事务]]
