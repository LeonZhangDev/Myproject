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
