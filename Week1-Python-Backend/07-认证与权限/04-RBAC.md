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

## 🧠 完整理解

### 我会先这样理解

RBAC（Role-Based Access Control）通过角色聚合权限，再把角色授予用户，避免给每个用户逐条配置权限。比如 admin 拥有 user:delete、task:write，viewer 只有 read。它适合权限结构相对稳定的系统；如果规则高度依赖资源属性、部门、时间等，可能要结合 ABAC/策略引擎。

### 执行顺序 / 思考顺序

用户认证得到 user → 查询/解析用户角色 → 角色映射到权限集合 → 请求某资源动作时检查所需 permission 是否包含 → 允许或拒绝。资源归属检查可能在 RBAC 之外再做一层。

### 容易踩的坑

只判断 `role == admin` 会让代码到处硬编码角色名，扩展困难。更好的方式是 endpoint 声明所需权限，角色到权限的映射集中管理。

### 面试时我会这样说

> 我更喜欢“权限驱动”而不是接口里到处写 `if user.role == admin`。角色只是权限集合的载体，接口声明需要 `task:delete`，以后角色怎么调整不需要改所有业务代码。

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
