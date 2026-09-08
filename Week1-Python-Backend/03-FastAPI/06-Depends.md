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

## 🧠 完整理解

### 我会先这样理解

`Depends` 是 FastAPI 声明依赖关系的入口。它不是普通函数调用，而是告诉框架“这个参数由某个依赖函数产生”。框架因此可以先执行依赖、解析其参数、处理异常、缓存结果，并在 yield 依赖结束后做清理。权限依赖还可以只执行副作用而不把结果传给 endpoint。

### 执行顺序 / 思考顺序

应用启动时框架理解依赖声明 → 请求到来后构建/执行依赖图 → 依赖返回值注入对应参数 → endpoint 执行 → yield 依赖进入 finally/清理阶段。

### 容易踩的坑

`Depends(get_db)` 和 `get_db()` 完全不同：前者把函数交给 FastAPI 管理，后者是在定义/调用位置直接执行。测试替换通常操作的是依赖函数本身。

### 面试时我会这样说

> 我会强调 Depends 是“声明”，不是“现在就调用”。比如 `db: Session = Depends(get_db)` 的意思是让 FastAPI 每个请求帮我拿一个 Session，并按依赖生命周期释放，而不是我在路由里自己 new。

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
