---
tags: [week1]
difficulty: P0
status: learning
---

# Depends

## 一句话理解

`Depends` 声明当前参数由某个依赖函数提供。

## 核心理解

它是 FastAPI 的依赖声明，不是 Python 关键字。

## 最小代码 / 场景

```python
token:str=Depends(verify_token)
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import Depends, FastAPI
app = FastAPI()

def verify_token():
    return "user-123"

@app.get("/profile")
def profile(user_id: str = Depends(verify_token)):
    return {"user_id": user_id}
```

### 运行 / 返回结果

```text
GET /profile
200 OK
{"user_id":"user-123"}
```

**怎么理解：** Depends(verify_token) 的意思是：先执行 verify_token，再把它的返回值注入 user_id。

## 🔗 关联知识

- [[05-依赖注入]]
