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
