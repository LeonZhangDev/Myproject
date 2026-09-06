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

## 🔗 关联知识

- [[02-Token]]
- [[04-RBAC]]
