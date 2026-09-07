---
tags: [week1]
difficulty: P0
status: learning
---

# CORS

## 一句话理解

浏览器跨源访问控制机制。

## 核心理解

前端和 API 不同 origin 时需要正确配置；浏览器可能发 OPTIONS 预检。

## 最小代码 / 场景

```python
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_methods=['*'], allow_headers=['*'])
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 运行 / 返回结果

```text
来自 http://localhost:5173 的浏览器跨域请求：允许
来自未配置来源的浏览器跨域请求：不会获得对应的 CORS 许可头
```

## 🔗 关联知识

- [[10-中间件]]
