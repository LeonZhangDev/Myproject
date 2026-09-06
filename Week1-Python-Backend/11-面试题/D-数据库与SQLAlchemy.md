---
tags: [week1, interview, d]
difficulty: P0
status: learning
---

# D｜数据库与SQLAlchemy


## W1-Q24｜为什么 AsyncSession 不应该在多个并发任务之间共享？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
AsyncSession 是可变、有状态的单事务上下文，多任务共享会让事务、连接和 ORM 状态互相干扰。通常每请求/每独立并发任务一个 Session。

### 最小代码 / 场景
```python
# avoid
await asyncio.gather(do_a(session),do_b(session))
```

### 关联知识
- [[../05-数据库与SQLAlchemy/13-AsyncSession]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q25｜一个 Web 请求中的 SQLAlchemy Session 通常应如何创建、提交、回滚和关闭？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
通过 yield 依赖每请求创建 Session；业务边界提交；异常 rollback；退出阶段 close。不要跨请求保存全局 Session。

### 最小代码 / 场景
```python
async def get_session():
    async with SessionLocal() as s:
        try: yield s
        except: await s.rollback(); raise
```

### 关联知识
- [[../05-数据库与SQLAlchemy/12-Session生命周期]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q26｜flush、commit 和 rollback 分别做什么？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
flush 把 SQL 发到数据库但不结束事务；commit 提交事务；rollback 撤销当前未提交事务。

### 最小代码 / 场景
```python
await session.flush()
await session.commit()
# 或 await session.rollback()
```

### 关联知识
- [[../05-数据库与SQLAlchemy/14-flush-commit-rollback]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q27｜数据库索引为什么能加速查询？索引是否越多越好？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
索引通过额外数据结构减少扫描，但增加存储和写入维护成本。应依据 WHERE/JOIN/ORDER BY、选择性和执行计划设计。

### 最小代码 / 场景
```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### 关联知识
- [[../05-数据库与SQLAlchemy/06-数据库索引]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q28｜什么是 ORM 的 N+1 查询问题？怎样发现和解决？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
先查一批主记录，再因懒加载为每条记录额外查关联数据。用 SQL 日志/查询计数发现；用 selectinload、joinedload、显式 JOIN 或批量查询解决。

### 最小代码 / 场景
```python
stmt=select(User).options(selectinload(User.tasks))
```

### 关联知识
- [[../05-数据库与SQLAlchemy/15-N加1问题]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q29｜Offset 分页和游标分页各有什么优缺点？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
Offset 简单、支持跳页，但深分页性能差且并发变化会重复/遗漏；游标分页按稳定唯一键继续，性能和一致性更好，但不便任意跳页。

### 最小代码 / 场景
```sql
SELECT * FROM tasks WHERE id<:last_id ORDER BY id DESC LIMIT 20;
```

### 关联知识
- [[../05-数据库与SQLAlchemy/18-游标分页]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q30｜数据库连接池耗尽通常有哪些原因？如何排查？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
常见：Session 泄漏、事务过长、慢 SQL、占着连接调外部 API、流量突增、池太小。看 pool wait、活跃连接、慢查询和 trace。

### 最小代码 / 场景
```text
request -> pool wait -> SQL -> release
```

### 关联知识
- [[../05-数据库与SQLAlchemy/19-连接池]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？
