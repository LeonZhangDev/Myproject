---
tags: [week1]
difficulty: P0
status: learning
---

# dependency_overrides

## 一句话理解

测试时替换 FastAPI 依赖。

## 核心理解

特别适合认证、数据库、外部服务依赖。

## 🧠 完整理解

### 我会先这样理解

FastAPI 的 `app.dependency_overrides` 可以把某个 Depends 依赖替换成测试版本，例如把生产数据库 Session 换成测试 Session，把真实认证换成固定测试用户。它比 patch 深层实现更贴合 FastAPI 的依赖边界，也能让接口测试保持真实路由、校验和响应流程。

### 执行顺序 / 思考顺序

测试设置 `app.dependency_overrides[get_db] = override_get_db` → 请求进入 → FastAPI 解析 Depends 时使用替代函数 → endpoint 无需修改 → 测试结束清空 overrides，避免影响其他测试。

### 容易踩的坑

测试后一定要恢复/clear overrides；替换函数的 yield 生命周期也应与原依赖兼容。不要为了过测试把权限逻辑全部绕过，应同时保留真实权限集成测试。

### 面试时我会这样说

> 我测试 FastAPI 时优先用 dependency_overrides，因为它就是框架预留的替换点。比如生产 get_db 不动，测试时注入 test Session；测试完清空 override，路由代码完全不用写 if test。

## 最小代码 / 场景

```python
app.dependency_overrides[get_session]=get_test_session
```


## 🧪 简单例子与返回结果

### 例子

```python
def fake_get_user():
    return {"id": 999}

app.dependency_overrides[get_user] = fake_get_user
r = client.get("/me")
print(r.json())
```

### 运行 / 返回结果

```text
{'id': 999}
```

**怎么理解：** 只在测试里把真实依赖替换成 fake 依赖，不需要改业务路由代码。

## 🔗 关联知识

- [[../03-FastAPI/05-依赖注入]]
