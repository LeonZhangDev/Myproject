---
tags: [week1]
difficulty: P0
status: learning
---

# Pydantic Settings

## 一句话理解

用类型化方式管理环境变量和配置。

## 核心理解

避免把数据库密码、Redis URL 写死在代码。

## 最小代码 / 场景

```python
class Settings(BaseSettings):
    database_url:str
    redis_url:str
```

## 🔗 关联知识

- [[../09-测试与工程/14-Docker-Compose]]
