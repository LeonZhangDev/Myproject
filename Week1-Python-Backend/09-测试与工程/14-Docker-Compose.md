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

## 🧠 完整理解

### 我会先这样理解

Docker Compose 用一个 YAML 描述本地/单机多容器应用，例如 FastAPI、PostgreSQL、Redis 的镜像、环境变量、端口、volume 和网络关系。它特别适合开发与集成测试，把“怎么把依赖一起跑起来”写进代码库。容器间通信应使用 service name，而不是 localhost。

### 执行顺序 / 思考顺序

`docker compose up` → 读取 compose.yml → 创建网络/volume → 按依赖启动 services → DNS 用 service 名解析容器 → 应用连接 `postgres:5432`、`redis:6379` → down 时停止/删除容器，volume 是否删除取决于参数。

### 容易踩的坑

`depends_on` 只代表启动顺序/条件配置，不天然等于数据库已经可接受请求；通常还需要 healthcheck 和应用重试。容器里的 localhost 指当前容器自己。

### 面试时我会这样说

> Compose 我主要用来把开发环境一键拉起来。最常见的新手坑就是 API 容器里写 `localhost:5432`，其实那指 API 自己；连 PostgreSQL 应该用 compose 的 service name，比如 `db:5432`。

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
