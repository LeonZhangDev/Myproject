---
tags: [week1]
difficulty: P0
status: learning
---

# RBAC

## 一句话理解

User -> Role -> Permission 的角色权限模型。

## 核心理解

把权限规则从大量 if/else 中抽离出来。

## 最小代码 / 场景

```text
Leon -> admin -> task:delete
Bob -> viewer -> task:read
```


## 🧪 简单例子与返回结果

### 例子

```python
permissions = {
    "admin": {"read", "write", "delete"},
    "user": {"read"},
}

role = "user"
print("delete" in permissions[role])
```

### 运行 / 返回结果

```text
False
```

## 🔗 关联知识

- [[05-FastAPI最小权限验证]]
