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

## 🧠 完整理解

### 我会先这样理解

Pydantic Settings 用来把环境变量、`.env` 等外部配置解析成有类型的配置对象。它解决的是配置和代码分离：数据库 URL、Redis 地址、密钥不应该硬编码。通过类型校验，缺失配置可以在应用启动时立刻失败，而不是跑到某个请求才发现。

### 执行顺序 / 思考顺序

进程启动 → Settings 读取环境/配置源 → 按字段类型解析和验证 → 得到 settings 对象 → 应用各组件读取 → 敏感值由部署环境注入。不同环境只换配置，不改业务代码。

### 容易踩的坑

不要把真实生产 secret 提交进 `.env` 到 Git；Settings 也不是秘密管理系统，生产环境更适合由 Kubernetes Secret、Vault、云密钥服务等注入。

### 面试时我会这样说

> 我用 Settings 的核心目的就是把配置从代码里拿出去，而且启动时就做类型检查。像 DATABASE_URL、REDIS_URL、JWT_SECRET 都从环境注入；`.env` 我只当本地开发便利，不会把生产密钥提交仓库。

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
