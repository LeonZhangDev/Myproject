---
tags: [week1, interview, c]
difficulty: P0
status: learning
---

# C｜FastAPI-Pydantic-HTTP


## W1-Q15｜FastAPI 依赖注入解决了什么问题？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
把 Session、认证、配置和公共校验从路由拆出去，便于复用、测试替换和资源清理；FastAPI 还可把依赖纳入校验和 OpenAPI。

### 最小代码 / 场景
```python
@app.get('/tasks')
async def tasks(session=Depends(get_session)):
    ...
```

### 关联知识
- [[../03-FastAPI/05-依赖注入]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q16｜Pydantic 校验和数据库约束有什么区别？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
Pydantic 在应用入口校验类型、格式和业务组合；数据库约束是最终防线，防止绕过应用的非法写入。关键唯一性/非空规则常两层都要有。

### 最小代码 / 场景
```sql
ALTER TABLE users ADD CONSTRAINT uq_email UNIQUE(email);
```

### 关联知识
- [[../04-Pydantic/10-Pydantic与数据库约束]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q17｜ASGI 和 WSGI 有什么区别？为什么 FastAPI 通常运行在 ASGI 服务器上？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
WSGI 主要面向同步 HTTP；ASGI 支持异步 I/O、WebSocket 和长连接。FastAPI 是 ASGI 应用，常由 Uvicorn 等运行。

### 最小代码 / 场景
```bash
uvicorn app.main:app --reload
```

### 关联知识
- [[../03-FastAPI/17-ASGI与WSGI]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q18｜FastAPI 路由应该使用 def 还是 async def？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
调用异步数据库/HTTP 客户端时用 async def；必须调用阻塞库时可用普通 def。最危险是在 async def 中直接长时间阻塞。

### 最小代码 / 场景
```python
@app.get('/bad')
async def bad():
    time.sleep(5)
```

### 关联知识
- [[../03-FastAPI/18-def还是async-def]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q19｜中间件与依赖注入分别适合处理什么逻辑？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
中间件适合 request_id、统一耗时、CORS 等全局横切逻辑；依赖注入适合路由级认证、Session 和可组合校验，更容易测试替换。

### 最小代码 / 场景
```python
@app.middleware('http')
async def mw(request,call_next):
    return await call_next(request)
```

### 关联知识
- [[../03-FastAPI/10-中间件]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q20｜FastAPI lifespan 适合管理哪些资源？为什么不应在每个请求中重复初始化？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
适合连接池、Redis 客户端、模型、共享 HTTP Client 等昂贵应用级资源。复用可减少初始化开销，并集中关闭。

### 最小代码 / 场景
```python
@asynccontextmanager
async def lifespan(app):
    app.state.client=AsyncClient(); yield; await app.state.client.aclose()
```

### 关联知识
- [[../03-FastAPI/14-lifespan]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q21｜BackgroundTasks 适合做什么？为什么不能把它当作可靠任务队列？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
适合响应后轻量、短时、允许偶尔失败的同进程任务；没有持久队列、跨进程协调和可靠重试。

### 最小代码 / 场景
```python
background_tasks.add_task(write_log,'created')
```

### 关联知识
- [[../03-FastAPI/16-BackgroundTasks]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q22｜为什么要区分请求模型、数据库模型和响应模型？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
三者分别表达客户端允许提交、数据库如何持久化、API 对外返回。分离可避免敏感字段泄露和 API 与表结构强耦合。

### 最小代码 / 场景
```text
TaskCreate -> Task ORM -> TaskOut
```

### 关联知识
- [[../04-Pydantic/09-请求模型数据库模型响应模型]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q23｜SSE 和 WebSocket 分别适合什么场景？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
SSE 是 Server→Client 单向 HTTP 事件流，适合 LLM token；WebSocket 是全双工长连接，适合实时协作、游戏、双向高频消息。

### 最小代码 / 场景
```javascript
const source=new EventSource('/stream')
```

### 关联知识
- [[../08-流式通信/07-SSE-vs-WebSocket]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？
