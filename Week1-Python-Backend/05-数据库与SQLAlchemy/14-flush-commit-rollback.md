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

## 🧠 完整理解

### 我会先这样理解

`flush` 把当前 Session 中待写的 ORM 变化转成 SQL 发到数据库，但通常还在当前事务里，没有最终提交；`commit` 会先确保 flush，再提交事务使修改持久化；`rollback` 撤销当前未提交事务。flush 很适合在事务中提前拿数据库生成的 id、提前触发约束检查，同时仍保留后续回滚能力。

### 执行顺序 / 思考顺序

修改 ORM 对象 → Session 标记 dirty/new → flush 发 INSERT/UPDATE/DELETE → 数据库在事务内执行 → 可继续更多操作 → commit 最终提交；任何阶段失败 → rollback 清理事务状态。

### 容易踩的坑

flush 之后别人不一定能看到数据，因为事务还没 commit。commit 失败后 Session 通常需要 rollback 才能恢复可用状态。不要每改一行就随意 commit，事务会被切碎。

### 面试时我会这样说

> 我区分这三个词很简单：flush 是“SQL 已经发给数据库，但事务还没结束”，commit 是“正式提交”，rollback 是“这次事务不要了”。所以需要 id 时我可以先 flush，不必为了拿 id 提前 commit。

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
