---
tags: [week1]
difficulty: P0
status: learning
---

# AsyncSession

## 一句话理解

异步 Session 仍是可变、有状态的事务上下文。

## 核心理解

多个并发 Task 共享会让连接、事务、ORM 状态互相干扰。

## 最小代码 / 场景

```python
# avoid: gather(do_a(session), do_b(session))
```


## 🧪 简单例子与返回结果

### 例子

```python
result = await db.execute(
    select(User).where(User.id == 1)
)
user = result.scalar_one()
print(user.id)
```

### 运行 / 返回结果

```text
1
```

## 🔗 关联知识

- [[12-Session生命周期]]
- [[../02-Asyncio与并发/13-竞态条件]]
