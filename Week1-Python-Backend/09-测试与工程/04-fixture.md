---
tags: [week1]
difficulty: P0
status: learning
---

# fixture

## 一句话理解

准备并清理可复用测试资源。

## 核心理解

常用来构造测试数据、客户端、数据库会话。

## 最小代码 / 场景

```python
@pytest.fixture
def task(): return {'id':1}
```

## 🔗 关联知识

- [[08-数据库测试隔离]]
