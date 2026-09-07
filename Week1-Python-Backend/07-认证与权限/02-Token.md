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


## 🧪 简单例子与返回结果

### 例子

```text
登录成功后服务端返回：
access_token = "abc123"

后续请求：
Authorization: Bearer abc123
```

### 运行 / 返回结果

```text
Token 有效：200 OK
Token 无效/过期：401 Unauthorized
```

## 🔗 关联知识

- [[03-JWT]]
- [[../03-FastAPI/07-Header]]
