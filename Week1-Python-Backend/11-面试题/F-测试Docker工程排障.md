---
tags: [week1, interview, f]
difficulty: P0
status: learning
---

# F｜测试Docker工程排障


## W1-Q36｜单元测试和集成测试有什么区别？本项目各测什么？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
单元测试隔离函数/服务，快；集成测试验证 API、DB、Redis 的真实协作。项目中单测校验/纯业务，集成测试关键接口、事务与缓存。

### 最小代码 / 场景
```python
def test_priority_validation():
    with pytest.raises(ValidationError):
        TaskCreate(title='A',priority=99)
```

### 关联知识
- [[../09-测试与工程/01-单元测试]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q37｜pytest fixture、mock 和 FastAPI dependency_overrides 分别适合解决什么问题？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
fixture 准备/清理复用资源；mock 替换外部边界并验证交互；dependency_overrides 替换 FastAPI 依赖，如认证和数据库。

### 最小代码 / 场景
```python
app.dependency_overrides[get_session]=get_test_session
```

### 关联知识
- [[../09-测试与工程/07-dependency-overrides]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q38｜涉及数据库的自动化测试怎样保证用例相互隔离？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
每用例事务后 rollback，或临时数据库/schema；测试数据唯一并统一清理；避免并行用例共享全局 Session/固定主键。

### 最小代码 / 场景
```python
@pytest.fixture
async def db_session():
    async with TestSession() as s:
        yield s
        await s.rollback()
```

### 关联知识
- [[../09-测试与工程/08-数据库测试隔离]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q39｜Docker 镜像和容器有什么区别？Dockerfile 与 Compose 分别负责什么？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
镜像是只读模板，容器是镜像运行实例；Dockerfile 描述单个镜像如何构建，Compose 描述 API/DB/Redis 等多服务如何共同运行。

### 最小代码 / 场景
```bash
docker build -t task-api .
docker compose up -d
```

### 关联知识
- [[../09-测试与工程/12-Docker镜像与容器]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q40｜一个 FastAPI 接口突然变慢，你会按什么顺序排查？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
先确认首字节还是总耗时，再根据 request_id/trace 拆路由、外部 API、DB、Redis；检查慢查询、连接池等待、Event Loop 阻塞、CPU/内存和近期发布；修复后回归压测。

### 最小代码 / 场景
```text
request -> timing -> DB/Redis/API spans -> system metrics -> regression test
```

### 关联知识
- [[../09-测试与工程/15-FastAPI性能排障]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？
