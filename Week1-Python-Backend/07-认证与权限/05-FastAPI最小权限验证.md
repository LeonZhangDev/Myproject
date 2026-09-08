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

## 🧠 完整理解

### 我会先这样理解

FastAPI 很适合把认证和权限检查写成依赖：先有 `get_current_user` 验证 token，再在上层依赖检查角色/permission，路由只声明 `Depends(require_permission(...))`。这样权限逻辑集中、可复用、可测试，还能让不满足条件的请求在进入业务函数前就被拒绝。

### 执行顺序 / 思考顺序

请求 → Authorization Header → get_current_user 验证 token → 得到 User → permission dependency 检查所需权限/资源 → 失败抛 401/403 → 成功后 endpoint 才执行。测试时可以 dependency_overrides 替换当前用户。

### 容易踩的坑

通用权限依赖不能替代所有资源级判断，例如“只能修改自己的订单”还需要结合 path 中订单 id 查询归属。避免只在路由层粗粒度角色判断。

### 面试时我会这样说

> 我在 FastAPI 里一般把 current_user 做成第一层 Depends，再叠 require_permission。这样路由函数一开始拿到的就是“身份已经验证、权限也通过”的上下文，业务代码会干净很多。

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
