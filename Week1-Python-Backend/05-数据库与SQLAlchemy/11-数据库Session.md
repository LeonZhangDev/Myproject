---
tags: [week1]
difficulty: P0
status: learning
---

# 数据库 Session

## 一句话理解

SQLAlchemy Session 是 ORM 工作单元/事务上下文。

## 核心理解

它跟踪 ORM 对象状态、事务和连接使用，不等于数据库本身。

## 🧠 完整理解

### 我会先这样理解

SQLAlchemy Session 不是数据库本身，也不等于一条固定连接。它更像 ORM 的工作单元：跟踪对象状态、组织查询与写入，并管理事务边界；需要访问数据库时再从 engine/连接池获取连接。Session 是有状态对象，因此生命周期必须清晰。

### 执行顺序 / 思考顺序

创建 Session → ORM 查询/对象进入 identity map → 修改对象状态 → flush 把 SQL 发给数据库 → commit 提交事务 → Session 继续或关闭 → connection 归还连接池。

### 容易踩的坑

不要把 Session 做成全局单例给所有请求共用。它持有事务和对象状态，多请求共享会互相污染，线程/协程安全也有问题。

### 面试时我会这样说

> 我把 Session 理解成“一次业务工作单元的上下文”，不是简单的连接。它会跟踪 ORM 对象和事务，所以通常一个请求一个 Session，用完关闭，让连接归还池里。

## 最小代码 / 场景

```python
session.add(task); await session.flush(); await session.commit()
```


## 🧪 简单例子与返回结果

### 例子

```python
# SQLAlchemy 同步示意
user = session.get(User, 1)
user.name = "Leon"
session.commit()
print(user.name)
```

### 运行 / 返回结果

```text
Leon
```

**怎么理解：** Session 负责跟踪 ORM 对象、组织 SQL、管理事务边界；它不是“数据库本身”。

## 🔗 关联知识

- [[12-Session生命周期]]
- [[13-AsyncSession]]
