---
tags: [week1]
difficulty: P0
status: learning
---

# Token

## 一句话理解

客户端携带的身份/会话凭证。

## 核心理解

最小教学可用 Header token；真实系统需要安全签发、过期和校验。

## 最小代码 / 场景

```python
x_token:str|None=Header(default=None)
```

## 🔗 关联知识

- [[03-JWT]]
- [[../03-FastAPI/07-Header]]
