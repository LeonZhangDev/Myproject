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
