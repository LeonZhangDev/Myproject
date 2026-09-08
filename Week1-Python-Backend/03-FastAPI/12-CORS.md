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

## 🧠 完整理解

### 我会先这样理解

CORS 是浏览器的同源安全机制相关协议，不是后端“接口能不能被 curl 调用”的权限系统。当网页前端从不同 origin 请求 API 时，浏览器会根据响应里的 CORS 头决定是否允许前端 JavaScript 读取结果；某些请求还会先发送 OPTIONS 预检。后端需要明确允许的 origin、method、header 和 credentials。

### 执行顺序 / 思考顺序

浏览器判断跨域 → 简单请求可能直接发并检查响应头；非简单请求先发 OPTIONS preflight → 服务端返回允许策略 → 浏览器确认后再发实际请求 → 最终仍由浏览器执行 CORS 限制。

### 容易踩的坑

`allow_origins=['*']` 配合 credentials 有限制，也不适合生产环境无脑开放。CORS 不能替代认证授权，因为非浏览器客户端不受同样限制。

### 面试时我会这样说

> 我会特别说明 CORS 是浏览器侧的跨域规则，不是 API 鉴权。开发环境可以放宽，生产环境我会明确列前端域名，尤其开启 cookie/credentials 时不能随便星号全放。

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
