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

## 🔗 关联知识

- [[10-中间件]]
