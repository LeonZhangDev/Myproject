---
tags: [week1, project]
difficulty: P0
status: learning
---
# Docker 部署
```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
  db:
    image: postgres:18
  redis:
    image: redis:7
```
```bash
docker compose up -d --build
```
