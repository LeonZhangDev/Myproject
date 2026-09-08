我这个 `task-api-split` 项目一开始其实主要是练 FastAPI 的接口拆分，比如把不同功能拆到不同 Router 里面。后面我想让它更接近一个真正的后端项目，所以就把 PostgreSQL 接进来了，而且不是只做到“能连数据库、能存数据”这一层，而是把整个数据库访问链路都拆开了。

首先数据库这一层，我是用 Docker 启动 PostgreSQL。这样本地不需要单独去安装和配置 PostgreSQL 服务，项目启动的时候直接通过 Docker Compose 把数据库拉起来就可以了。数据库的用户名、密码、数据库名和连接地址这些信息，我没有直接写死在代码里面，而是统一放在 `.env` 配置文件里，然后通过 `config.py` 读取。这样后面如果开发环境、测试环境或者部署环境的数据库地址不一样，只需要修改配置，不需要改业务代码。

接下来是 SQLAlchemy 这一层。我用了异步的 SQLAlchemy，也就是 `create_async_engine`、`AsyncSession` 和 `async_sessionmaker`。其中 Engine 我把它理解成整个应用和 PostgreSQL 之间的连接管理入口，它底层会维护连接池，所以这个对象是应用级共享的，不需要每来一个请求就重新创建一次。

但是 Session 就不一样了。Session 是和一次具体数据库操作、事务状态绑定在一起的，所以我专门写了一个 `get_db()` 依赖。每次 FastAPI 收到一个请求的时候，通过 `Depends(get_db)` 创建一个独立的 `AsyncSession`，这个请求处理完以后 Session 自动关闭。

我这里特意没有让所有请求共享同一个 Session，因为如果多个请求同时操作一个 Session，很容易把事务状态混在一起。比如一个请求正在提交数据，另外一个请求发生异常执行了 rollback，如果大家共用一个 Session，就可能互相影响。所以我的设计是 Engine 全局共享，但是 Session 按请求创建，也就是一个 HTTP 请求对应一个独立的数据库会话。

然后我把数据库表定义放到了 `models` 目录里面，比如 `Task` 和 `Category`。这些 Model 都继承 SQLAlchemy 的 `Base`。`Task` 对应 PostgreSQL 里面的 `tasks` 表，`Category` 对应 `categories` 表。

这里我没有只做一个单表 Task，而是又加了 Category，主要也是为了把实际项目里比较常见的表关系练进去。一个 Category 可以对应多个 Task，所以它们之间是一个一对多关系。Task 表里面保存 `category_id` 外键，指向 Category 表。

这样后面查询任务的时候，不只是简单执行 `select(Task)`，还可以通过 Join 把任务信息和分类信息一起查出来，比如查到“学习 SQLAlchemy”这个任务属于“Database”分类。这个部分主要就是在练 SQLAlchemy 的 relationship、ForeignKey 和 Join 查询。

另外我把 ORM Model 和 Pydantic Schema 分开了。这个也是我后来比较重视的一点。Model 主要描述数据库表长什么样，比如字段类型、主键、外键、索引、是否允许为空；Schema 主要控制 API 接收什么数据以及返回什么数据。

比如创建 Task 的时候，客户端可能只需要传 `title`、`description` 和 `category_id`，这时候用 `TaskCreate` Schema 做参数校验。但是数据库里面还可能有 `id`、`created_at`、`updated_at` 这些字段，这些并不应该让客户端自己传。所以我会分别定义 Create、Update、Read 这类 Schema，让 API 层和数据库层职责分开。

真正的数据库操作主要是在 Router 里面完成。比如客户端调用 `POST /tasks`，FastAPI 先通过 Pydantic Schema 校验请求参数，然后通过 `Depends(get_db)` 拿到当前请求自己的 AsyncSession。

接下来我会根据请求数据创建一个 `Task` ORM 对象，然后调用 `db.add()` 把这个对象加入当前 Session。这里 `add()` 本身并不等于已经把数据真正永久写进数据库，它只是告诉 SQLAlchemy 这个对象需要被持久化。真正完成事务提交的是 `await db.commit()`。

提交完成之后，我通常还会通过 `refresh()` 把数据库里面最新的数据重新读取回来，因为像主键 ID、创建时间这一类字段有可能是数据库自动生成的。最后再把这个 ORM 对象通过 Pydantic 的返回 Schema 转换成 JSON 返回给前端。

查询这一块我除了普通查询，还专门加了分页。比如前端传 `page=3`、`page_size=20`，后端就通过 `offset` 和 `limit` 控制 PostgreSQL 只返回这一页需要的数据，而不是先把所有数据查询出来再在 Python 里面切片。

这个区别其实挺重要的。如果数据库里面只有几十条数据感觉不明显，但是如果后面有几十万甚至几百万条记录，就肯定不能每次全部查询出来。所以分页一定要尽量放在数据库层完成。

索引这一块我也考虑了实际查询场景。比如任务经常会按照 `category_id`、状态或者创建时间查询，那这些字段就比较适合建立索引。如果经常出现“查询某个分类下面最近创建的任务”这种条件，还可以考虑建立 `category_id + created_at` 的复合索引。

我理解索引主要就是用额外的存储空间换查询速度。没有索引的时候，PostgreSQL 有些查询可能需要扫描大量记录；有合适索引以后，它可以先通过索引快速定位到目标数据。当然索引也不是越多越好，因为插入和更新的时候还需要维护索引，所以还是要根据真实查询条件去设计。

另外我还用了 Alembic 来管理数据库结构。这个我觉得比直接在 PostgreSQL 里面手工建表更符合工程项目。因为代码中的 Model 后面肯定会变化，比如 Task 一开始可能只有 `id` 和 `title`，后面又增加 `status`、`category_id` 或者索引。

如果每次修改模型都手动执行 SQL，很容易出现开发环境、测试环境和部署环境数据库结构不一致。所以我通过 Alembic 生成 migration，每一次数据库结构变化都有自己的版本。比如第一次 migration 创建 Task 和 Category 表，后面再通过新的 migration 增加字段或者索引，然后使用 `alembic upgrade head` 把数据库升级到最新结构。

所以整个项目跑起来以后，完整的数据链路其实就是：客户端先把请求发给 FastAPI，`main.py` 把请求路由到对应的 Router，Router 使用 Pydantic Schema 校验参数，然后通过 `Depends(get_db)` 创建当前请求独立的 AsyncSession，再通过 SQLAlchemy ORM 生成 SQL，底层使用 asyncpg 和 PostgreSQL 通信，PostgreSQL 完成查询或者写入以后，再把结果通过 Schema 转成 JSON 返回给客户端。

所以如果面试官问我“你是怎么给 FastAPI 项目接 PostgreSQL 的”，我不会只说我用了 SQLAlchemy。我会说我把它拆成了配置层、连接和 Session 层、ORM Model 层、Schema 层以及 Router 业务层。

Engine 负责应用级数据库连接管理，Session 按请求隔离事务；Model 负责数据库结构，Schema 负责接口数据结构；Alembic 负责数据库版本迁移；Router 负责具体的 CRUD、分页和 Join 查询。另外我还根据查询场景加了索引，并且考虑了事务和并发请求之间的隔离问题。

这样做完以后，这个项目就不只是一个简单的 FastAPI CRUD Demo 了，而是把一个比较完整的后端数据库访问流程实际走了一遍。