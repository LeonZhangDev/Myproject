---
tags: [week1]
difficulty: P0
status: learning
---

# pytest

## 一句话理解

Python 常用测试框架。

## 核心理解

核心能力：简洁断言、fixture、参数化。

## 最小代码 / 场景

```bash
pytest -q
```


## 🧪 简单例子与返回结果

### 例子

```python
def test_math():
    assert 1 + 1 == 2
```

### 运行 / 返回结果

```text
$ pytest -q
1 passed
```

## 🔗 关联知识

- [[04-fixture]]
- [[05-参数化测试]]
