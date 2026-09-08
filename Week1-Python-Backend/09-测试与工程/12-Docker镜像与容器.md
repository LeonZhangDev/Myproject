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

## 🧠 完整理解

### 我会先这样理解

Docker 镜像是只读的应用运行模板，由多层文件系统组成；容器是镜像启动后的一个运行实例，加上可写层、进程、网络和隔离配置。镜像可以重复启动很多容器。理解二者区别后，构建、部署、数据持久化和调试都会清晰很多。

### 执行顺序 / 思考顺序

Dockerfile build → 生成 image layers → `docker run` 基于镜像创建容器可写层和 namespace/cgroup → 启动 ENTRYPOINT/CMD 进程 → 进程退出通常容器结束 → 删除容器不等于删除镜像或 volume。

### 容易踩的坑

容器不是完整虚拟机，通常共享宿主机内核。重要数据不要只写容器可写层，容器删掉就可能丢，需要 volume/外部存储。

### 面试时我会这样说

> 我会把 image 理解成“打包好的模板”，container 是“这个模板跑起来的一次实例”。同一个 FastAPI image 可以起 5 个容器；容器删了没关系，但数据库数据就不能只放容器临时层。

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
