---
tags: [week1]
difficulty: P0
status: learning
---

# OpenAPI

## 一句话理解

FastAPI 根据路由、类型注解、Pydantic 模型生成接口契约。

## 核心理解

可用于 /docs、客户端生成、联调与规范化接口。

## 🧠 完整理解

### 我会先这样理解

OpenAPI 是描述 HTTP API 契约的标准格式，FastAPI 会根据路由、类型注解、Pydantic 模型、响应模型等自动生成 schema，再由 Swagger UI/ReDoc 展示。它的价值不只是“有个文档页”，还可以用于生成客户端 SDK、契约测试和前后端协作。

### 执行顺序 / 思考顺序

定义路由与模型 → FastAPI 收集 operation、参数和 schema → 生成 `/openapi.json` → Swagger UI/ReDoc 消费这个 JSON → 展示可交互文档。修改模型后文档能同步变化。

### 容易踩的坑

自动文档质量取决于你定义的接口质量。字段描述、example、status code、response model 都不写，最后得到的文档也会很贫乏。生产环境还要考虑是否公开 docs。

### 面试时我会这样说

> 我喜欢 FastAPI 的一点就是类型和模型不仅服务运行时，还能直接生成 OpenAPI。这样接口契约基本和代码同源，不容易出现“文档写一套、接口实际又是一套”。

## 最小代码 / 场景

```text
FastAPI -> /openapi.json -> Swagger UI
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI
app = FastAPI(title="Demo API")

@app.get("/ping")
def ping():
    return {"pong": True}
```

### 运行 / 返回结果

```text
打开 /docs：可以看到 Swagger UI
打开 /openapi.json：paths 中包含 /ping
```

## 🔗 关联知识

- [[../01-Python核心/12-类型注解]]
- [[../04-Pydantic/01-BaseModel]]
