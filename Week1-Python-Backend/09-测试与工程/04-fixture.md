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

## 🧠 完整理解

### 我会先这样理解

fixture 用来提供测试所需的可复用上下文，例如数据库 Session、测试用户、HTTP client。pytest 根据测试函数参数名自动注入 fixture；使用 yield 时，yield 前是 setup，yield 后是 teardown。scope 决定资源多久创建一次，需要在速度和测试隔离之间平衡。

### 执行顺序 / 思考顺序

测试声明参数 `db_session` → pytest 查找同名 fixture → 执行依赖 fixture → yield 返回对象给测试 → 测试结束 → 从内到外执行 teardown → 按 scope 决定何时销毁。

### 容易踩的坑

session/module scope 的可变资源可能让测试互相污染。数据库 fixture 常通过每测试事务回滚或重建 schema 保证隔离。

### 面试时我会这样说

> 我把 fixture 理解成“测试依赖注入”。比如 20 个测试都需要 client，不用每个都手写 setup/teardown。只是 scope 我会很谨慎，速度快不能以测试互相串数据为代价。

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
