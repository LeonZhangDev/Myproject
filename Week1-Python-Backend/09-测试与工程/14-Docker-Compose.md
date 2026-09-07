---
tags: [week1]
difficulty: P0
status: learning
---

# Docker Compose

## 一句话理解

描述多个服务如何一起运行。

## 核心理解

配置 API、DB、Redis、网络、卷、环境变量、健康检查。

## 最小代码 / 场景

```yaml
services:
  api:
    build: .
  db:
    image: postgres:18
  redis:
    image: redis:7
```


## 🧪 简单例子与返回结果

### 例子

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
  redis:
    image: redis:7
```

### 运行 / 返回结果

```text
docker compose up -d
-> 启动 api 服务
-> 启动 redis 服务
两个服务进入同一个 Compose 网络，可通过服务名 redis 互相访问。
```

## 🔗 关联知识

- [[12-Docker镜像与容器]]
