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
