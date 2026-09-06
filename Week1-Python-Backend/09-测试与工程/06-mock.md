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

## 🔗 关联知识

- [[07-dependency-overrides]]
