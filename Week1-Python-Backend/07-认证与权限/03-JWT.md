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
