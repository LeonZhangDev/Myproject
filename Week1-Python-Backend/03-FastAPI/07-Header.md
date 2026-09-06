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

## 最小代码 / 场景

```python
x_token:str|None=Header(default=None)
```

## 🔗 关联知识

- [[../07-认证与权限/02-Token]]
