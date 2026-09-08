我在 `task-api-split` 接完 PostgreSQL 以后，下一步接 Redis，主要不是为了再增加一个“数据库”，而是想解决后端项目里比较常见的性能问题。

PostgreSQL 还是这个项目真正的数据存储层，Task、Category 这些数据最终还是以 PostgreSQL 为准。Redis 在这里更像是一个高速缓存层，主要负责把一些经常查询、但是不会每次都变化的数据暂时放到内存里面。

所以我这里的思路不是：

Redis 替代 PostgreSQL。

而是：

FastAPI 先查 Redis，Redis 没有的时候再查 PostgreSQL，然后把 PostgreSQL 查到的数据写回 Redis。

这样下一次再查相同数据的时候，就不用每次都访问 PostgreSQL 了。

整个结构大概可以理解成：

```text
Client
   ↓
FastAPI
   ↓
Router
   ↓
Service / Cache Logic
   ↓
先查 Redis
   │
   ├── 命中 → 直接返回
   │
   └── 未命中
          ↓
      PostgreSQL
          ↓
      查询数据
          ↓
      写入 Redis
          ↓
        返回
```

这就是我在这个项目里面使用的核心缓存思路，也就是比较典型的 Cache Aside，也叫旁路缓存模式。

首先 Redis 本身我也是通过 Docker 启动的。

因为项目里面 PostgreSQL 已经用 Docker Compose 管理了，所以我没有单独手动启动 Redis，而是直接把 Redis 服务也加进 `compose.yaml`。

大概结构就是：

```text
Docker Compose
│
├── PostgreSQL
│
└── Redis
```

这样开发的时候执行一次 Docker Compose，就可以同时把 PostgreSQL 和 Redis 都启动起来。

PostgreSQL 负责持久化数据，Redis 负责缓存。

Redis 的连接地址我也没有直接写死在代码里面，而是继续放到 `.env` 里面。

比如：

```env
REDIS_URL=redis://localhost:6379/0
```

然后还是通过 `config.py` 统一读取。

所以配置这一层会变成：

```text
.env
│
├── DATABASE_URL
└── REDIS_URL
```

我这样做主要是希望所有外部依赖的地址都集中管理。

比如以后本地 Redis 是：

```text
localhost:6379
```

但是上线以后可能是：

```text
redis-server:6379
```

甚至可能直接换成云 Redis。

那业务代码完全不用改，只修改环境变量就可以了。

接下来我会单独增加一个 Redis 连接模块，比如：

```text
app/
├── core/
│   └── config.py
│
├── database/
│   └── session.py
│
└── cache/
    └── redis.py
```

这里我会刻意把 Redis 和 PostgreSQL 分开。

因为这两个东西虽然都属于数据层，但是职责完全不一样。

`database/session.py` 管 PostgreSQL。

`cache/redis.py` 管 Redis。

Redis 模块里面主要负责创建 Redis Client。

这个 Client 和 SQLAlchemy 的 Session 思路又不完全一样。

PostgreSQL 的 Session 我是每个请求创建一个独立 Session，因为它里面有事务状态。

但是 Redis Client 一般可以作为一个应用级对象共享，因为它底层维护的是连接池。

所以整体思路是：

```text
PostgreSQL：

Engine
全局共享

AsyncSession
每个请求独立


Redis：

Redis Client
全局共享
```

Redis Client 本身不会像 SQLAlchemy Session 那样保存一个复杂的 ORM 事务上下文，所以没有必要每来一个 HTTP 请求就重新创建 Redis 连接。

项目启动以后，可以创建 Redis 连接池，然后所有请求通过这个连接池获取连接。

这样会比每次请求都重新 TCP 连接 Redis 高效很多。

Redis 真正接进业务以后，我首先会把它放在 Task 查询这一块。

比如现在有一个接口：

```text
GET /tasks/{task_id}
```

原来没有 Redis 的时候，流程就是：

```text
请求进来
↓
FastAPI
↓
Task Router
↓
AsyncSession
↓
PostgreSQL
↓
SELECT
↓
返回 Task
```

也就是说每查一次 Task，都要访问一次 PostgreSQL。

接入 Redis 以后，我会先根据 `task_id` 生成一个缓存 Key。

比如：

```text
task:1
task:2
task:100
```

我一般不会直接把 Key 写成：

```text
1
2
3
```

因为 Redis 后面可能不只是缓存 Task。

以后还可能有：

```text
category:1

user:100

task:list:page:1

task:count
```

所以 Key 最好带上业务前缀。

这样一眼就知道这个缓存属于什么数据。

比如查询：

```text
GET /tasks/10
```

我会生成：

```text
task:10
```

然后先执行：

```text
Redis GET task:10
```

如果 Redis 里面已经有数据，这时候就叫缓存命中。

整个流程变成：

```text
GET /tasks/10
↓
Redis GET task:10
↓
发现有数据
↓
JSON 反序列化
↓
直接返回
```

这一次请求就不会访问 PostgreSQL。

Redis 的价值就在这里。

因为 Redis 的数据主要放在内存里面，所以读取速度一般会比每次走关系型数据库查询快很多。

而且数据库连接本身也是有限资源。

如果一个热门 Task 被短时间访问几千次，没有缓存的话：

```text
请求1 → PostgreSQL

请求2 → PostgreSQL

请求3 → PostgreSQL

请求4 → PostgreSQL

……
```

实际上这些请求查的都是同一份数据。

加 Redis 以后就可以变成：

```text
第一次
↓
PostgreSQL


后面的请求
↓
Redis
```

这样 PostgreSQL 压力就会明显降低。

但是 Redis 里面不可能永远都有数据。

比如第一次访问：

```text
task:10
```

Redis 里面还没有这个 Key。

这时候就是缓存未命中。

所以流程会继续向 PostgreSQL 查询。

大概是：

```text
GET /tasks/10
↓
Redis GET task:10
↓
没有
↓
PostgreSQL SELECT
↓
拿到 Task
↓
序列化成 JSON
↓
Redis SET task:10
↓
返回
```

也就是说 PostgreSQL 仍然是最终的数据来源。

Redis 只是把查询结果复制一份到内存里面。

这个地方我觉得有一个比较重要的理解：

Redis 里面的数据可以丢。

PostgreSQL 里面的数据不能随便丢。

因为 Redis 缓存没了，我还可以：

```text
Redis Miss
↓
重新查 PostgreSQL
↓
重新构建缓存
```

但是如果 PostgreSQL 数据没了，那 Redis 里面即使还有缓存，也不能认为它是可靠的持久化数据。

所以在这个项目里面，数据的一致性原则就是：

```text
PostgreSQL
=
Source of Truth
```

也就是 PostgreSQL 才是真实数据源。

Redis 只是缓存副本。

另外我不会让缓存永久保存。

比如写入 Task 缓存的时候，我会设置 TTL。

例如：

```text
task:10

TTL = 300 秒
```

也就是缓存 5 分钟。

5 分钟以后 Redis 自动删除这个 Key。

下一次请求的时候：

```text
Redis Miss
↓
PostgreSQL
↓
重新缓存
```

我设置 TTL 主要考虑两个问题。

第一，防止 Redis 里面的缓存无限增长。

因为如果每访问一个 Task 都永久缓存：

```text
task:1
task:2
task:3
……
task:1000000
```

Redis 内存会一直占下去。

第二，TTL 也可以降低长期数据不一致的问题。

比如某个缓存因为异常没有及时删除，至少它不会永远存在。

到期以后还是会重新从 PostgreSQL 读取最新数据。

但是只靠 TTL 还是不够。

因为假设：

```text
Redis
task:10
title = 学习 Python
```

PostgreSQL 里面我把它改成：

```text
title = 学习 Redis
```

如果我什么都不处理，那么在 TTL 到期之前，用户查询到的还是 Redis 里的旧数据。

所以更新和删除接口，我还需要做缓存失效。

比如：

```text
PUT /tasks/10
```

原来只需要：

```text
UPDATE PostgreSQL
↓
COMMIT
```

现在我会变成：

```text
UPDATE PostgreSQL
↓
COMMIT成功
↓
DELETE Redis task:10
```

为什么我更倾向于删除缓存，而不是直接更新 Redis？

因为这里实际上有两个数据源需要操作：

```text
PostgreSQL
Redis
```

如果我：

```text
更新 PostgreSQL
+
更新 Redis
```

就要考虑两个操作谁先谁后、哪个失败。

例如 PostgreSQL 更新成功，但是 Redis 更新失败。

或者 Redis 更新成功，但是 PostgreSQL commit 失败。

状态就容易乱。

所以在这种简单项目里面，我更喜欢：

```text
先更新数据库
↓
数据库 commit 成功
↓
删除缓存
```

缓存删掉以后也没关系。

下一次用户查询的时候：

```text
Redis Miss
↓
PostgreSQL
↓
拿到最新数据
↓
重新写 Redis
```

这样整体逻辑更简单。

所以我更新接口的思路是：

```text
PUT /tasks/10
↓
更新 Task ORM
↓
await db.commit()
↓
Redis DEL task:10
↓
返回
```

删除 Task 也是一样。

比如：

```text
DELETE /tasks/10
```

流程：

```text
删除 PostgreSQL 数据
↓
commit
↓
Redis DEL task:10
```

这样用户下一次再查询：

```text
Redis 没有
↓
PostgreSQL 也没有
↓
返回 404
```

而不是从 Redis 里面拿出一个已经被删除的 Task。

这就是我在项目里面处理数据库和缓存一致性的基本原则。

还有一个我会特别处理的问题，就是缓存穿透。

比如用户不断访问一个根本不存在的任务：

```text
GET /tasks/999999999
```

Redis 肯定没有。

于是：

```text
Redis Miss
↓
PostgreSQL查询
↓
不存在
```

如果我什么都不缓存，那么下一次还是：

```text
Redis Miss
↓
PostgreSQL查询
```

假如有人不停请求：

```text
999999999
888888888
777777777
```

大量不存在的数据，就会绕过 Redis，一直打到 PostgreSQL。

所以对于明确不存在的数据，我会考虑设置一个短时间的空值缓存。

比如：

```text
task:999999999
=
__NULL__
```

然后 TTL 设置得比较短，比如 30 秒或者 60 秒。

这时候下一次请求同样的 ID：

```text
Redis GET
↓
发现 __NULL__
↓
直接返回 404
```

就不用再查 PostgreSQL。

这个地方 `__NULL__` 并不是 Redis 自带的特殊值。

只是我自己约定的一个标记。

它的意思是：

```text
这个 Key 我查过数据库了
数据库里确实没有
```

所以：

```text
Redis 没 Key
```

和：

```text
Redis 有 Key
值是 __NULL__
```

其实代表两个完全不同的状态。

没有 Key 表示：

```text
我还不知道数据库有没有
```

`__NULL__` 表示：

```text
我已经确认数据库没有
```

不过这种空值缓存我一般不会设置太久。

因为假设刚开始：

```text
task:100
```

不存在，所以 Redis 缓存了：

```text
__NULL__
```

结果下一秒又创建了 Task 100。

如果 NULL 缓存设置了几个小时，新数据就可能暂时查不到。

所以空值缓存一般 TTL 会明显短于正常缓存。

另外，如果这个项目以后访问量继续变大，我还会考虑缓存击穿。

缓存击穿和缓存穿透不是一个问题。

缓存穿透是：

```text
查询的数据本来就不存在
```

缓存击穿是：

```text
这个数据存在
而且还是热点数据
但是缓存刚好过期了
```

比如：

```text
task:1
```

是一个特别热门的 Task。

刚好 Redis TTL 到期。

这个时候同时来了 1000 个请求。

它们都会看到：

```text
Redis Miss
```

于是：

```text
1000个请求
↓
同时访问 PostgreSQL
```

Redis 本来是为了保护数据库，结果缓存过期那一瞬间还是把数据库打满了。

这种情况下，如果项目访问量真的比较大，就可以考虑 Redis 锁、single flight 或者逻辑过期这类方案，让只有一个请求负责回源 PostgreSQL，其他请求等待或者继续使用旧缓存。

不过对于 `task-api-split` 这个学习项目，我不会一上来把所有复杂方案都堆进去。

我会先把：

```text
缓存命中

缓存未命中

TTL

缓存失效

空值缓存
```

这些最核心的东西做好。

这样比较符合项目当前体量。

Redis 接进来以后，我还会考虑分页列表缓存。

比如现在有：

```text
GET /tasks?page=1&page_size=20
```

可以生成：

```text
tasks:list:page:1:size:20
```

作为 Key。

这样热门的第一页 Task 就不需要每次查询 PostgreSQL。

但是列表缓存会比单对象缓存麻烦一些。

因为假设我新增了一个 Task：

```text
POST /tasks
```

原来的第一页列表可能已经发生变化。

所以新增 Task 后，不只是：

```text
task:{id}
```

的问题。

还可能需要把：

```text
tasks:list:*
```

相关缓存清掉。

所以我一般会优先缓存：

```text
GET /tasks/{id}
```

这种单对象查询。

因为这种缓存和数据库记录之间基本是一一对应的：

```text
Task ID 10
↔
Redis task:10
```

失效逻辑比较清楚。

列表缓存可以等确实发现列表接口访问频率比较高以后再做。

这个我觉得也是项目里面比较重要的一点：

不是看到 Redis 就什么东西都缓存。

而是先判断：

```text
这个数据查得多不多？

数据改得频不频繁？

缓存失效成本高不高？

缓存以后真的能减少数据库压力吗？
```

像 Task 详情这种：

```text
读多
写少
Key明确
```

就比较适合缓存。

Redis 在这个项目里面除了缓存，其实以后还可以扩展其他功能。

比如接口限流。

Redis 很适合做类似：

```text
rate_limit:user:100
```

记录某个用户一分钟调用接口多少次。

因为 Redis 有：

```text
INCR
EXPIRE
```

这种原子操作，所以可以用来实现一个简单的限流器。

例如：

```text
一分钟最多调用 100 次
```

每请求一次：

```text
INCR
```

超过 100 次：

```text
429 Too Many Requests
```

另外还可以做计数器。

例如：

```text
task:view:10
```

每访问一次：

```text
INCR task:view:10
```

这种高频计数如果每一次都直接 UPDATE PostgreSQL，其实会给数据库造成比较大的写压力。

Redis 做这种高频计数比较合适，然后再定时或者批量同步到 PostgreSQL。

不过如果面试官问我：

“你这个项目 Redis 主要做了什么？”

我还是会先讲缓存，不会一下子把所有 Redis 功能全说出来。

我会说：

我这里接 Redis 主要是给 Task 查询做 Cache Aside 缓存。查询的时候先根据 `task_id` 生成 Redis Key，比如 `task:10`，先查 Redis。命中就直接反序列化返回；没有命中才去 PostgreSQL 查询，然后把查询结果设置 TTL 后写回 Redis。

对于更新和删除，我不会只更新数据库不管缓存，而是先完成 PostgreSQL 的事务提交，确认数据库修改成功以后，再删除对应 Redis Key。这样下一次查询会重新从 PostgreSQL 加载最新数据并重建缓存。

另外对于数据库里面本来就不存在的 Task，我会设置一个比较短的空值缓存，比如 `__NULL__`，避免同一个不存在的 ID 被频繁请求时，每次都绕过 Redis 查询 PostgreSQL，这主要是防缓存穿透。

Redis Client 本身我会作为应用级对象共享，底层使用连接池，而不会像 SQLAlchemy AsyncSession 一样每个请求重新创建。因为 AsyncSession 本身携带数据库事务状态，所以需要请求级隔离；Redis Client 更像一个无状态的连接入口，可以安全地通过连接池复用。

所以 PostgreSQL 和 Redis 在这个项目里面的定位其实非常清楚。

PostgreSQL 负责：

```text
真正存数据

事务

关系

Join

数据一致性
```

Redis 负责：

```text
缓存

降低数据库查询压力

减少重复查询

提高热点数据访问速度
```

如果把整个 `task-api-split` 现在的数据访问链路画出来，大概就是：

```text
                 Client
                    ↓
                 FastAPI
                    ↓
                  Router
                    ↓
              Pydantic Schema
                    ↓
              Redis Cache
              /           \
          Hit               Miss
           ↓                  ↓
        直接返回          AsyncSession
                              ↓
                         SQLAlchemy
                              ↓
                         PostgreSQL
                              ↓
                           查询结果
                              ↓
                         Redis SET
                              ↓
                            返回
```

如果是写请求：

```text
POST / PUT / DELETE
        ↓
     FastAPI
        ↓
  AsyncSession
        ↓
  PostgreSQL
        ↓
     commit
        ↓
   commit成功
        ↓
删除相关 Redis 缓存
        ↓
      返回
```

所以如果让我在面试里面完整介绍这一段，我大概会这么说：

我给这个项目接完 PostgreSQL 之后，又在数据库前面加了一层 Redis，主要目的是减少一些高频读取接口对 PostgreSQL 的重复访问。

我这里没有把 Redis 当主数据库，真实数据还是以 PostgreSQL 为准，Redis 只是一个缓存副本。查询 Task 的时候，我先根据 Task ID 生成类似 `task:{id}` 的 Key，然后查 Redis。如果缓存命中，就直接返回；如果没有命中，我才通过 SQLAlchemy 的 AsyncSession 去 PostgreSQL 查询，然后把结果序列化以后写进 Redis，并设置 TTL。

写操作这边我主要考虑的是缓存一致性。比如 Task 更新的时候，我先更新 PostgreSQL 并 commit，只有数据库事务真正成功以后，才删除对应 Redis 缓存，而不是直接同时更新两边。这样下一次读取发现缓存不存在，就会重新从 PostgreSQL 获取最新数据并重建缓存，整体逻辑会简单和可靠一些。

对于不存在的 Task，我还加了短 TTL 的空值缓存，避免有人反复请求不存在的 ID，导致每次都直接打到 PostgreSQL，这主要是处理缓存穿透。

另外 Redis 和 PostgreSQL 的连接管理方式我也做了区分。SQLAlchemy 的 AsyncSession 是请求级的，一个 HTTP 请求对应一个独立 Session，主要是为了隔离事务；Redis Client 则是应用级共享，通过连接池复用连接，不需要每个请求重新建立 Redis 连接。

所以接完 Redis 以后，这个项目的数据层就不是简单的“FastAPI 直接查 PostgreSQL”了，而变成了“FastAPI → Redis → PostgreSQL”这一套比较完整的缓存访问链路，同时也把 TTL、缓存失效、空值缓存和数据库一致性这些实际后端项目里比较常见的问题一起考虑进去了。