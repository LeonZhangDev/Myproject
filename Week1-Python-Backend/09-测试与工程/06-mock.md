---
tags: [week1]
difficulty: P0
status: learning
---

# mock

## 一句话理解

替换外部边界并验证交互。

## 核心理解

适合第三方 HTTP、邮件、支付；不要把所有内部实现都 mock。

## 🧠 完整理解

### 我会先这样理解

Mock 用来替代难以控制、昂贵或不应该在单测中真实调用的依赖，例如第三方支付 API、邮件服务、系统时间。它可以预设返回值、抛异常并验证调用。使用原则是 mock 系统边界，而不是把被测模块内部每一步都 mock 掉。

### 执行顺序 / 思考顺序

测试把真实依赖替换为 mock → 调用被测函数 → 业务代码以为自己在调用真实接口 → mock 返回预设结果/异常 → 测试验证最终行为，必要时再验证调用参数。

### 容易踩的坑

最常见错误是 patch 错位置：应该 patch “被测模块实际引用的名字”，不是原始定义所在模块。过度验证 `assert_called_once` 也会让重构脆弱。

### 面试时我会这样说

> 我用 mock 主要隔离外部边界，比如真的不想单测时发短信。对自己内部的 service/repository 我不会层层都 mock，不然最后测试的只是 mock 配置，不是真正业务行为。

## 最小代码 / 场景

```python
mock_client.get.return_value={'ok':True}
```


## 🧪 简单例子与返回结果

### 例子

```python
from unittest.mock import Mock

send_email = Mock(return_value=True)
result = send_email("a@test.com")

print(result)
print(send_email.call_count)
```

### 运行 / 返回结果

```text
True
1
```

**怎么理解：** 测试时可以用 Mock 替代真正的邮件、支付、外部 API 等依赖。

## 🔗 关联知识

- [[07-dependency-overrides]]
