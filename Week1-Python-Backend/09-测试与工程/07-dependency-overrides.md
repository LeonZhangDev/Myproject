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

## 🔗 关联知识

- [[../03-FastAPI/05-依赖注入]]
