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


## 🧪 简单例子与返回结果

### 例子

```python
# .env
# APP_NAME=MindTrip

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "demo"

    model_config = {"env_file": ".env"}

settings = Settings()
print(settings.app_name)
```

### 运行 / 返回结果

```text
MindTrip
```

**怎么理解：** 如果当前目录存在示例中的 .env，Settings 会读取 APP_NAME。

## 🔗 关联知识

- [[../09-测试与工程/14-Docker-Compose]]
