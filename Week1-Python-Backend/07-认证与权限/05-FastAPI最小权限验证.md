---
tags: [week1]
difficulty: P0
status: learning
---

# FastAPI 最小权限验证

## 一句话理解

把鉴权写成依赖，路由只声明需要什么权限。

## 核心理解

更易复用，也更容易测试替换。

## 最小代码 / 场景

```python
async def delete_task(user=Depends(require_admin)):
    ...
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import Depends, FastAPI, HTTPException
app = FastAPI()

def current_role():
    return "user"

def require_admin(role=Depends(current_role)):
    if role != "admin":
        raise HTTPException(403, "forbidden")

@app.delete("/users/{id}")
def delete_user(id: int, _=Depends(require_admin)):
    return {"deleted": id}
```

### 运行 / 返回结果

```text
当前 role=user：
DELETE /users/1
403 Forbidden
{"detail":"forbidden"}
```

## 🔗 关联知识

- [[../03-FastAPI/05-依赖注入]]
