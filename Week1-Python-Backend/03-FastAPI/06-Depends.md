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

## 🔗 关联知识

- [[05-依赖注入]]
