---
tags: [week1]
difficulty: P0
status: learning
---

# Docker 镜像与容器

## 一句话理解

镜像是只读模板；容器是镜像运行实例。

## 核心理解

Dockerfile 产镜像，docker run/compose 启容器。

## 最小代码 / 场景

```text
Dockerfile -> Image -> Container
```


## 🧪 简单例子与返回结果

### 例子

```bash
docker build -t task-api .
docker run --name task-api -p 8000:8000 task-api
```

### 运行 / 返回结果

```text
镜像：task-api
容器：task-api
本机访问 http://localhost:8000 -> 转发到容器 8000 端口
```

## 🔗 关联知识

- [[13-Dockerfile]]
- [[14-Docker-Compose]]
