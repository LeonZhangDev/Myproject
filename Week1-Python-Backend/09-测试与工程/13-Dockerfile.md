---
tags: [week1]
difficulty: P0
status: learning
---

# Dockerfile

## 一句话理解

描述单个镜像如何构建。

## 核心理解

FROM/WORKDIR/COPY/RUN/CMD 是最常见指令。

## 🧠 完整理解

### 我会先这样理解

Dockerfile 描述如何从基础镜像构建应用镜像。构建优化重点是可复现、镜像小、缓存命中好、安全：固定依赖版本，先复制 requirements 再安装以利用缓存，使用 `.dockerignore`，非 root 运行，多阶段构建去掉编译工具。CMD/ENTRYPOINT 则定义容器启动进程。

### 执行顺序 / 思考顺序

Docker 按指令构建 layer → 某层输入没变可复用缓存 → COPY 代码 → 设置工作目录/用户 → 最终镜像保存启动命令 → run 时执行 ENTRYPOINT/CMD。上层变化只会让其后的层重新构建。

### 容易踩的坑

`COPY . .` 太早会导致每改一行代码都重装依赖；把 `.env`、git、模型大文件无脑 COPY 也会增大镜像并泄密。不要依赖 `latest` 保证可复现。

### 面试时我会这样说

> 我写 Dockerfile 会先考虑缓存层：requirements 先复制安装，代码后复制，这样改业务代码不用每次重装依赖。生产镜像还会尽量非 root、少装工具、固定版本，减少体积和攻击面。

## 最小代码 / 场景

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["uvicorn","app.main:app","--host","0.0.0.0"]
```


## 🧪 简单例子与返回结果

### 例子

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 运行 / 返回结果

```text
docker build 后得到一个可运行 FastAPI 的镜像；
docker run 映射端口后，Uvicorn 在容器内监听 8000。
```

## 🔗 关联知识

- [[14-Docker-Compose]]
