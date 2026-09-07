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

## 最小代码 / 场景

```python
return JSONResponse(status_code=404, content={'code':40401,'message':'not found'})
```

## 🔗 关联知识

- [[08-异常处理]]
