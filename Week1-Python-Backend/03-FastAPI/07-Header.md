---
tags: [week1]
difficulty: P0
status: learning
---

# Header

## 一句话理解

`Header()` 声明参数来自 HTTP 请求头。

## 核心理解

常用于 token、request id、自定义协议头。

## 🧠 完整理解

### 我会先这样理解

Header 用来读取 HTTP 请求头，常见于 Authorization、X-Request-ID、幂等键、客户端版本等元数据。FastAPI 可以通过 `Header()` 做类型转换和校验，并默认把 Python 参数名中的下划线映射为 HTTP 头里的连字符。认证头应遵循标准方案，不要把敏感信息随意定义在自制 header 中。

### 执行顺序 / 思考顺序

请求到达 → ASGI headers 是字节键值 → FastAPI 根据 Header 声明查找对应字段 → 转换/校验 → 注入 endpoint 或依赖 → 业务逻辑使用。

### 容易踩的坑

HTTP Header 名通常大小写不敏感，但代理和基础设施可能会过滤某些自定义头。不要在日志中无掩码打印 Authorization/token。

### 面试时我会这样说

> 我一般把 Header 当成“请求的元信息”，像 token、request-id、幂等键都很合适。真正业务数据我还是放 path/query/body，不会什么都往 header 里塞。

## 最小代码 / 场景

```python
x_token:str|None=Header(default=None)
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI, Header
app = FastAPI()

@app.get("/who")
def who(x_token: str | None = Header(default=None)):
    return {"token": x_token}
```

### 运行 / 返回结果

```text
请求头：X-Token: abc123
GET /who
200 OK
{"token":"abc123"}
```

## 🔗 关联知识

- [[../07-认证与权限/02-Token]]
