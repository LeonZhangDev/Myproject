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

## 🧠 完整理解

### 我会先这样理解

Token 是客户端证明身份/会话的一种凭证载体，可以是服务端存储的随机 session token，也可以是 JWT 这样的自包含 token。客户端每次请求携带 token，服务端验证后恢复身份上下文。设计时要考虑生成随机性、传输安全、过期、撤销、存储位置和泄露后的影响。

### 执行顺序 / 思考顺序

登录凭证验证成功 → 服务端签发 token → 客户端安全保存 → 后续请求通过 Authorization/Cookie 携带 → 服务端验证 token → 得到用户信息 → token 过期/撤销则要求重新认证或刷新。

### 容易踩的坑

Token 不是加密了就绝对安全；Bearer token 谁拿到谁就能用。必须 HTTPS，日志不能打印完整 token，浏览器存储还要权衡 XSS/CSRF。

### 面试时我会这样说

> 我把 token 理解成“后续请求用的身份凭证”，但它本身也是敏感数据。无论 JWT 还是随机 token，泄露以后都可能被冒用，所以 HTTPS、过期和撤销策略同样重要。

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
