# Task API - PostgreSQL / SQLAlchemy 版

这个版本已经把原来的 `app/data/task_store.py` 内存列表替换为真正的 PostgreSQL。

## 当前技术栈

```text
FastAPI
    ↓
SQLAlchemy 2.x AsyncSession
    ↓
asyncpg
    ↓
PostgreSQL 18（Docker）
```

数据库表结构由 Alembic 管理。

---

## 项目结构

```text
task-api-split/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── cors.py
│   ├── database/
│   │   ├── base.py                 # SQLAlchemy Declarative Base
│   │   └── session.py              # Engine、Session 工厂、get_db
│   ├── models/
│   │   ├── category.py             # categories 表
│   │   └── task.py                 # tasks 表、外键与索引
│   ├── routers/
│   │   ├── tasks.py                # CRUD、事务、分页、JOIN
│   │   ├── categories.py           # Category 接口
│   │   ├── files.py
│   │   └── chat.py
│   ├── schemas/
│   │   ├── task.py
│   │   ├── category.py
│   │   ├── common.py
│   │   └── chat.py
│   ├── dependencies/
│   ├── exceptions/
│   ├── middleware/
│   └── services/
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 20260903_01_create_task_tables.py
├── alembic.ini
├── compose.yaml
├── .env.example
├── pyproject.toml
└── README.md
```

---

# 1. 准备环境变量

进入项目目录：

```bash
cd task-api-split
```

复制配置：

```bash
cp .env.example .env
```

`.env` 默认内容对应：

```text
数据库：task_db
用户：task_user
密码：task_password
端口：5432
```

---

# 2. 安装 Python 依赖

```bash
uv sync
```

关键依赖：

```text
sqlalchemy        ORM / SQL 构造
asyncpg           PostgreSQL 异步驱动
pydantic-settings 读取 .env
alembic           数据库迁移
```

---

# 3. Docker 启动 PostgreSQL

```bash
docker compose up -d
```

检查：

```bash
docker compose ps
```

查看数据库日志：

```bash
docker compose logs db
```

---

# 4. 用 Alembic 创建表

```bash
uv run alembic upgrade head
```

这个命令会创建：

```text
categories
tasks
alembic_version
```

同时创建索引：

```text
ix_categories_name
ix_tasks_category_id
ix_tasks_completed_priority
```

注意：不要手工运行 `Base.metadata.create_all()`，本项目统一通过 Alembic 管理表结构。

---

# 5. 进入 PostgreSQL

```bash
docker compose exec db \
psql -U task_user -d task_db
```

查看表：

```sql
\dt
```

查看 tasks 表：

```sql
\d tasks
```

查看索引：

```sql
\di
```

退出 PostgreSQL：

```sql
\q
```

---

# 6. 启动 FastAPI

```bash
uv run fastapi dev app/main.py
```

Swagger：

```text
http://127.0.0.1:8000/docs
```

Task / Category 请求仍需要：

```text
X-Token: dev-token
```

---

# 7. 分页

接口：

```http
GET /tasks?page=1&page_size=10
```

核心 SQLAlchemy：

```python
offset = (page - 1) * page_size

select(Task) \
    .order_by(Task.id) \
    .offset(offset) \
    .limit(page_size)
```

它对应数据库的：

```sql
OFFSET ...
LIMIT ...
```

响应：

```json
{
  "page": 1,
  "page_size": 10,
  "total": 20,
  "items": []
}
```

---

# 8. 事务

创建任务接口：

```http
POST /tasks
```

示例请求：

```json
{
  "title": "学习 SQLAlchemy",
  "description": "完成数据库部分",
  "completed": false,
  "priority": 2,
  "category_name": "学习"
}
```

`app/routers/tasks.py` 中：

```python
async with db.begin():
    # 1. 查询分类
    # 2. 分类不存在则 INSERT Category
    # 3. INSERT Task
```

正常退出：

```text
COMMIT
```

任何一步抛异常：

```text
ROLLBACK
```

所以不会出现“分类创建成功，但任务创建失败后留下半条业务数据”的状态。

`await db.flush()` 与 `commit` 不同：

```text
flush  = 把当前 SQL 发给数据库，可以拿到生成的主键，但事务仍可回滚
commit = 正式提交事务
```

---

# 9. 索引

`app/models/task.py`：

```python
category_id = mapped_column(
    ForeignKey("categories.id"),
    index=True,
)

__table_args__ = (
    Index(
        "ix_tasks_completed_priority",
        "completed",
        "priority",
    ),
)
```

当前项目有：

```text
categories.name
    唯一索引

tasks.category_id
    单列索引

tasks(completed, priority)
    复合索引
```

索引可以减少适合查询条件下需要扫描的数据，但会增加 INSERT / UPDATE / DELETE 的维护成本，所以不是越多越好。

---

# 10. JOIN 查询

接口：

```http
GET /tasks/with-category?page=1&page_size=10
```

SQLAlchemy：

```python
select(
    Task.id,
    Task.title,
    Category.name.label("category_name"),
).outerjoin(
    Category,
    Task.category_id == Category.id,
)
```

对应 SQL 思路：

```sql
SELECT
    tasks.id,
    tasks.title,
    categories.name AS category_name
FROM tasks
LEFT JOIN categories
    ON tasks.category_id = categories.id;
```

这里使用 `LEFT JOIN`，所以即使 Task 没有分类，它仍然会出现在结果中，此时 `category_name = null`。

---

# 11. 为什么每个请求必须使用独立 Session？

`app/database/session.py`：

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

FastAPI：

```python
db: AsyncSession = Depends(get_db)
```

关系是：

```text
Request A → AsyncSession A → Transaction A
Request B → AsyncSession B → Transaction B
Request C → AsyncSession C → Transaction C
```

而不是：

```text
Request A ─┐
Request B ─┼→ 一个全局 AsyncSession   ×
Request C ─┘
```

原因有三点：

1. `AsyncSession` 是有状态对象，它会维护当前事务状态与 ORM 对象状态。
2. 多个并发请求共享同一个 Session 时，一个请求的 `commit()` / `rollback()` 可能干扰另一个请求正在进行的工作。
3. SQLAlchemy 的并发模型要求一个并发 task 使用自己的 `AsyncSession`。

但“每请求一个 Session”不代表每次都重新创建一个 PostgreSQL 物理连接。

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

Engine 和连接池是应用级共享的；请求结束时 Session 关闭，连接通常归还连接池供后续请求复用。

因此可以记成：

```text
Engine        整个应用共享
Session       每个请求独立
Transaction   按一次业务操作划分
```

---

# 12. 当前主要接口

```text
GET     /tasks
GET     /tasks/with-category
GET     /tasks/{task_id}
POST    /tasks
PUT     /tasks/{task_id}
DELETE  /tasks/{task_id}

GET     /categories
POST    /categories

POST    /upload/pdf
POST    /chat/stream
```
