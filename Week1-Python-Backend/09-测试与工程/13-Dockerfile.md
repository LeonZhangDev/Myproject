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
