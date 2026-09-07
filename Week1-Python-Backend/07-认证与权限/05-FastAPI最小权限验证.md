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

## 🔗 关联知识

- [[../03-FastAPI/05-依赖注入]]
