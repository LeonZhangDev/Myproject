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


## 🧪 简单例子与返回结果

### 例子

```python
import pytest

@pytest.fixture
def user():
    return {"name": "Leon"}

def test_user(user):
    assert user["name"] == "Leon"
```

### 运行 / 返回结果

```text
$ pytest -q
1 passed
```

**怎么理解：** pytest 会自动把同名 fixture 的返回值注入 test_user(user)。

## 🔗 关联知识

- [[08-数据库测试隔离]]
