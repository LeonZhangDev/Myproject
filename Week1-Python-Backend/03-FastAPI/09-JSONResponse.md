---
tags: [week1]
difficulty: P0
status: learning
---

# JSONResponse

## 一句话理解

显式构造 JSON HTTP 响应。

## 核心理解

HTTP status_code 与业务错误码可以分开。

## 🧠 完整理解

### 我会先这样理解

JSONResponse 是 Starlette/FastAPI 提供的显式 JSON 响应对象，适合你需要自己控制 status_code、headers、content 时使用。普通 endpoint 直接 return dict/Pydantic 模型已经足够，框架会自动序列化；只有在异常处理、统一错误结构、自定义 header 等场景才常需要手工构造 JSONResponse。

### 执行顺序 / 思考顺序

构造 JSONResponse(content, status_code, headers) → 响应对象把内容编码成 JSON bytes → 设置 `content-type: application/json` → ASGI send 发回客户端。此时通常绕过部分自动 response_model 处理。

### 容易踩的坑

content 必须是可 JSON 序列化的数据；datetime、ORM 对象等可能需要 `jsonable_encoder` 或 Pydantic 先转换。不要为了统一格式而在所有接口里机械地手写 JSONResponse。

### 面试时我会这样说

> 我一般正常接口直接 return 模型，让 FastAPI 做响应校验；需要明确控制状态码、header 或在全局异常 handler 里返回统一错误时，我才会用 JSONResponse。

## 最小代码 / 场景

```python
return JSONResponse(status_code=404, content={'code':40401,'message':'not found'})
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()

@app.get("/created")
def created():
    return JSONResponse(status_code=201, content={"id": 1})
```

### 运行 / 返回结果

```text
GET /created
201 Created
{"id":1}
```

## 🔗 关联知识

- [[08-异常处理]]
