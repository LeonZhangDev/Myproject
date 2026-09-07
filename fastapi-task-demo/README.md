# Task API - PostgreSQL + SQLAlchemy + Redis 版

这个版本是在原来的 FastAPI Task 项目上逐步升级得到的完整学习项目：

```text
FastAPI
   │
   ├── SQLAlchemy 2.x AsyncSession
   │        ↓
   │     asyncpg
   │        ↓
   │   PostgreSQL 18（Docker）
   │
   └── redis.asyncio
            ↓
        Redis 8（Docker）
```

PostgreSQL 是持久化数据的**真实来源（source of truth）**；Redis 只负责缓存和限流。Redis 清空或临时故障，不应该造成 Task 数据丢失。

---

## 1. 当前功能

### PostgreSQL / SQLAlchemy

- Task CRUD
- Category 关联
- `AsyncSession`
- 每请求独立 Session
- 数据库事务
- OFFSET / LIMIT 分页
- 数据库索引
- Task `LEFT JOIN` Category
- Alembic 数据库迁移

### Redis

- `GET /tasks/{task_id}` 使用 Cache-Aside
- 正常 Task 缓存 TTL 默认 300 秒
- `__NULL__` 空值缓存 TTL 默认 60 秒，降低缓存穿透
- Task 创建后清理可能存在的空值缓存
- Task 更新后删除缓存
- Task 删除后删除缓存
- `/tasks` 使用 Redis 固定窗口限流
- Lua 脚本原子执行 `INCR + EXPIRE`
- Redis 故障采用 fail-open：核心 PostgreSQL CRUD 继续工作

### 原项目保留功能

- Token 校验
- 全局异常处理
- PDF 上传
- BackgroundTasks
- SSE 流式聊天
- CORS
- 请求日志中间件

---

# 2. 项目目录

```text
task-api-split/
├── app/
│   ├── main.py
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   ├── redis.py              # Redis 客户端 / 连接池
│   │   └── task_cache.py         # Cache-Aside、空值缓存、缓存失效
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── cors.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py            # Engine、Session 工厂、get_db
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── rate_limit.py         # Redis Lua 固定窗口限流
│   │
│   ├── models/
│   │   ├── category.py
│   │   └── task.py
│   │
│   ├── routers/
│   │   ├── tasks.py              # CRUD、事务、分页、JOIN、缓存失效
│   │   ├── categories.py
│   │   ├── files.py
│   │   └── chat.py
│   │
│   ├── schemas/
│   ├── exceptions/
│   ├── middleware/
│   └── services/
│
├── alembic/
│   └── versions/
│       └── 20260903_01_create_task_tables.py
│
├── alembic.ini
├── compose.yaml                  # PostgreSQL + Redis
├── .env.example
├── pyproject.toml
└── README.md
```

---

# 3. 第一次启动

进入项目：

```bash
cd task-api-split
```

复制环境变量：

```bash
cp .env.example .env
```

安装 Python 依赖：

```bash
uv sync
```

启动 PostgreSQL 和 Redis：

```bash
docker compose up -d
```

查看容器：

```bash
docker compose ps
```

正常情况下应看到：

```text
task-postgres
task-redis
```

---

# 4. 创建 PostgreSQL 表

Redis 没有引入新的 PostgreSQL 表，所以仍然使用原来的 Alembic migration。

执行：

```bash
uv run alembic upgrade head
```

创建：

```text
alembic_version
categories
tasks
```

以及索引：

```text
ix_categories_name
ix_tasks_category_id
ix_tasks_completed_priority
```

---

# 5. 启动 FastAPI

```bash
uv run fastapi dev app/main.py
```

Swagger：

```text
http://127.0.0.1:8000/docs
```

Task / Category 请求需要：

```text
X-Token: dev-token
```

---

# 6. 检查 PostgreSQL

进入：

```bash
docker compose exec db \
psql -U task_user -d task_db
```

查看表：

```sql
\dt
```

查看 Task 表：

```sql
\d tasks
```

查看索引：

```sql
\di
```

退出：

```sql
\q
```

---

# 7. 检查 Redis

进入 Redis CLI：

```bash
docker compose exec redis redis-cli
```

测试：

```redis
PING
```

返回：

```text
PONG
```

退出：

```redis
QUIT
```

---

# 8. Cache-Aside：查询单个 Task

接口：

```http
GET /tasks/{task_id}
```

流程：

```text
Request
   ↓
Redis GET task-api:task:{id}
   │
   ├── hit → 直接返回
   │
   └── miss
         ↓
     PostgreSQL
         │
         ├── 找到 → Redis SET + TTL → 返回
         │
         └── 不存在 → Redis SET __NULL__ + 短 TTL → 404
```

缓存代码：

```text
app/cache/task_cache.py
```

Redis Key 示例：

```text
task-api:task:1
task-api:task:25
```

正常缓存默认：

```text
TTL = 300 秒
```

---

# 9. 怎么观察缓存命中

先创建一个 Task，然后第一次请求：

```http
GET /tasks/1
```

第一次：

```text
Redis miss
    ↓
PostgreSQL SELECT
    ↓
Redis SET
```

进入 Redis：

```bash
docker compose exec redis redis-cli
```

查看：

```redis
GET task-api:task:1
```

查看剩余 TTL：

```redis
TTL task-api:task:1
```

第二次再调用：

```http
GET /tasks/1
```

此时直接 Redis hit，正常情况下不需要再次执行 `SELECT Task WHERE id=1`。

学习阶段 `SQL_ECHO=true`，可以从 FastAPI 终端 SQL 日志观察区别。

---

# 10. 空值缓存：降低缓存穿透

请求一个不存在的 ID：

```http
GET /tasks/999999
```

第一次：

```text
Redis miss
    ↓
PostgreSQL miss
    ↓
Redis:
task-api:task:999999 = __NULL__
TTL = 60 秒
```

查看：

```redis
GET task-api:task:999999
```

得到：

```text
__NULL__
```

再次请求同一个不存在 ID：

```text
Redis hit __NULL__
    ↓
直接 404
```

因此短时间大量重复访问不存在 ID 时，不会每次都打 PostgreSQL。

为什么空值只缓存 60 秒，而正常数据缓存 300 秒？

因为这个 ID 后面有可能真的被创建。空值 TTL 太长会让新数据在一段时间内仍被误判为不存在。

---

# 11. 更新 / 删除后的缓存一致性

本项目使用：

```text
先更新 PostgreSQL
       ↓
COMMIT
       ↓
DEL Redis Key
```

例如：

```http
PUT /tasks/1
```

成功后执行：

```text
DEL task-api:task:1
```

下一次：

```http
GET /tasks/1
```

Redis miss，于是重新读取 PostgreSQL 最新数据并重建缓存。

删除 Task 同样执行：

```text
PostgreSQL DELETE
       ↓
COMMIT
       ↓
Redis DEL
```

这是 Cache-Aside 中很常见的“写数据库后使缓存失效”策略。

注意：当前学习项目 Redis 删除失败时会记录日志并 fail-open，因此极端情况下旧缓存最多持续到 TTL。生产系统可以继续加入重试、消息队列或补偿任务。

---

# 12. 为什么创建 Task 后也 DELETE 缓存？

假设有人提前请求：

```text
/tasks/100
```

数据库还没有 ID=100，于是 Redis 存：

```text
task-api:task:100 = __NULL__
```

之后 PostgreSQL 创建的新 Task 恰好得到：

```text
id = 100
```

所以创建成功后项目会执行：

```text
DEL task-api:task:100
```

防止旧的空值缓存遮住刚创建的数据。

---

# 13. Redis 限流

所有 `/tasks` 接口统一经过：

```text
app/dependencies/rate_limit.py
```

默认规则：

```text
每个客户端
60 秒
最多 60 次 /tasks 请求
```

环境变量：

```env
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW_SECONDS=60
```

Redis Key 示例：

```text
task-api:rate-limit:tasks:127.0.0.1
```

第 61 次请求会返回：

```http
HTTP 429 Too Many Requests
```

类似：

```json
{
  "code": 42901,
  "message": "Too many requests",
  "data": {
    "limit": 60,
    "window_seconds": 60,
    "retry_after_seconds": 23
  }
}
```

---

# 14. 为什么限流用 Lua？

错误思路：

```text
INCR key

程序突然异常

EXPIRE key 没执行
```

这时计数 Key 可能没有 TTL。

本项目把：

```text
INCR
+
第一次请求时 EXPIRE
```

写成 Redis Lua 脚本，由 Redis 一次原子执行。

核心思路：

```lua
local current = redis.call('INCR', KEYS[1])

if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
```

---

# 15. Redis 为什么不使用“每请求一个客户端”？

SQLAlchemy：

```text
每请求一个 AsyncSession
```

是因为 Session 是有状态的事务工作区：

```text
Request A → Session A → Transaction A
Request B → Session B → Transaction B
```

Redis 客户端则不同。

`Redis.from_url()` 内部维护连接池，因此项目采用：

```text
整个 FastAPI 应用
        ↓
一个 redis_client
        ↓
Redis Connection Pool
      ↙   ↓   ↘
  connection ...
```

应用关闭时：

```text
lifespan
   ↓
redis_client.aclose()
```

所以可以记：

```text
SQLAlchemy Engine      应用级共享
AsyncSession           每请求独立

Redis client/pool      应用级共享
Redis Key              按业务设计
```

---

# 16. PostgreSQL 为什么仍然是真实数据源？

本项目不把 Task 只存在 Redis。

因为 Redis 在这里承担的是：

```text
缓存
限流计数
临时状态
```

真实 Task：

```text
PostgreSQL
```

因此即使执行：

```bash
docker compose restart redis
```

Redis 缓存被清空，也只是：

```text
下一次 GET 回源 PostgreSQL
       ↓
重新建立缓存
```

不会丢 Task。

这也是 `compose.yaml` 中 Redis 不需要持久化 volume 的原因。

---

# 17. 为什么暂时不缓存分页列表？

例如：

```text
/tasks?page=1&page_size=10
/tasks?page=2&page_size=10
/tasks?completed=false
/tasks?priority=3
```

如果全部缓存，创建或更新一个 Task 后就要判断应该删除哪些列表 Key。

这会产生复杂的缓存失效问题。

当前项目只缓存：

```text
GET /tasks/{id}
```

因为它具有非常明确的一一对应关系：

```text
Task 17
   ↕
task-api:task:17
```

更新 Task 17：

```text
DEL task-api:task:17
```

简单、稳定，而且适合学习 Cache-Aside。

---

# 18. 数据库事务

创建 Task 时：

```python
async with db.begin():
    # 查找 / 创建 Category
    # 创建 Task
```

正常退出：

```text
COMMIT
```

任何一步异常：

```text
ROLLBACK
```

`flush()`：

```text
把 SQL 发给 PostgreSQL，可以获得主键，但事务尚未提交
```

`commit()`：

```text
正式提交事务
```

Redis 缓存失效放在 PostgreSQL 事务成功之后执行。

---

# 19. PostgreSQL 分页

接口：

```http
GET /tasks?page=1&page_size=10
```

SQLAlchemy：

```python
offset = (page - 1) * page_size

select(Task) \
    .order_by(Task.id) \
    .offset(offset) \
    .limit(page_size)
```

对应：

```sql
OFFSET ...
LIMIT ...
```

---

# 20. PostgreSQL JOIN

接口：

```http
GET /tasks/with-category?page=1&page_size=10
```

核心：

```python
.outerjoin(
    Category,
    Task.category_id == Category.id,
)
```

对应：

```sql
SELECT ...
FROM tasks
LEFT JOIN categories
    ON tasks.category_id = categories.id;
```

使用 LEFT JOIN，所以没有 Category 的 Task 也能返回。

---

# 21. PostgreSQL 索引

当前模型包含：

```text
categories.name
    unique + index

tasks.category_id
    index

tasks(completed, priority)
    composite index
```

查看：

```sql
\di
```

索引的本质是用额外数据结构降低合适查询场景下的数据扫描成本，但会增加存储和写操作维护成本，所以不是所有字段都应该加索引。

---

# 22. 为什么每个 HTTP 请求使用独立 AsyncSession？

```text
Request A → AsyncSession A → Transaction A
Request B → AsyncSession B → Transaction B
Request C → AsyncSession C → Transaction C
```

`AsyncSession` 会维护：

```text
事务状态
ORM 对象状态
当前数据库工作上下文
```

多个并发请求共享同一个 Session 时，一个请求的 `commit()` / `rollback()` 可能干扰其他请求。

但独立 Session 不等于每次重新建立物理 TCP 连接：

```text
                 Engine
                    ↓
              Connection Pool
               ↙    ↓    ↘
            Conn1 Conn2 Conn3
              ↑      ↑
          Session A Session B
              ↑      ↑
          Request A Request B
```

记忆：

```text
Engine        整个应用共享
Session       每个请求独立
Transaction   按业务操作划分
```

---

# 23. 主要接口

```text
GET     /tasks
GET     /tasks/with-category
GET     /tasks/{task_id}          Redis Cache-Aside
POST    /tasks                    PostgreSQL Transaction
PUT     /tasks/{task_id}          DB COMMIT → Redis DEL
DELETE  /tasks/{task_id}          DB COMMIT → Redis DEL

GET     /categories
POST    /categories

POST    /upload/pdf
POST    /chat/stream
```

所有 `/tasks` 接口同时经过 Redis rate limit。

---

# 24. 推荐学习顺序

```text
1. docker compose up -d

2. docker compose ps

3. uv run alembic upgrade head

4. uv run fastapi dev app/main.py

5. POST /tasks 创建 Task

6. GET /tasks/{id} 第一次观察 PostgreSQL SELECT

7. redis-cli GET task-api:task:{id}

8. GET /tasks/{id} 第二次观察 Redis 命中

9. PUT /tasks/{id}

10. redis-cli GET task-api:task:{id}
    应该为空，因为缓存已失效

11. GET 不存在 ID

12. redis-cli GET task-api:task:{不存在ID}
    应得到 __NULL__

13. 连续请求 /tasks，观察 429 限流
```

这套流程能把 PostgreSQL、SQLAlchemy、事务、Session、Redis Cache-Aside、缓存一致性、缓存穿透和限流串成一条完整的后端学习链路。
