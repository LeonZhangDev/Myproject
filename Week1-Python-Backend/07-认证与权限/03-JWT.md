---
tags: [week1]
difficulty: P0
status: learning
---

# JWT

## 一句话理解

带签名的 token 格式，常包含主体、过期、角色等声明。

## 核心理解

至少要验证签名和 exp；按场景验证 iss/aud。

## 🧠 完整理解

### 我会先这样理解

JWT 是一种带签名的自包含 token 格式，常见三段是 header.payload.signature。服务端可以在不查 session 表的情况下验证签名并读取 claims，因此适合分布式身份传递；但 payload 通常只是 Base64URL 编码，不是保密加密。JWT 的难点更多在过期、撤销、密钥轮换和 claim 设计。

### 执行顺序 / 思考顺序

登录 → 服务端生成 header/payload（sub、exp 等）→ 用密钥签名 → 客户端携带 JWT → 服务端校验签名、exp、iss/aud 等 → 验证通过后建立用户身份 → 再做授权。

### 容易踩的坑

不要把密码、敏感隐私写进 payload；只验签名不验 exp/aud/iss 也不够。JWT 一旦签发在过期前通常难以立即撤销，可能需要 denylist、短 access token + refresh token。

### 面试时我会这样说

> 我会特别强调 JWT 是“签名”不是“加密”，payload 解码就能看到。所以敏感信息不放里面。它的优点是服务端不用每次查 session，但代价就是注销和即时撤销会更麻烦。

## 最小代码 / 场景

```text
header.payload.signature
```


## 🧪 简单例子与返回结果

### 例子

```python
import jwt

token = jwt.encode({"sub": "user-1", "role": "admin"}, "secret", algorithm="HS256")
payload = jwt.decode(token, "secret", algorithms=["HS256"])
print(payload)
```

### 运行 / 返回结果

```text
{'sub': 'user-1', 'role': 'admin'}
```

**怎么理解：** JWT 是“签名的声明载体”，不是默认加密；payload 通常可以被读取，所以不要放密码等秘密。

## 🔗 关联知识

- [[02-Token]]
- [[04-RBAC]]
