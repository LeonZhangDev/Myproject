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

## 🔗 关联知识

- [[14-Docker-Compose]]
