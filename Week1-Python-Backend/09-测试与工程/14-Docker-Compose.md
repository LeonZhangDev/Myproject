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

## 🔗 关联知识

- [[12-Docker镜像与容器]]
