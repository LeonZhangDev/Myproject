---
tags: [week1]
difficulty: P0
status: learning
---

# functools.wraps

## 一句话理解

`@wraps` 保留被装饰函数的名称、文档和签名等元数据。

## 核心理解

框架和调试工具经常依赖这些元数据。

## 最小代码 / 场景

```python
from functools import wraps
@wraps(fn)
def wrapper(*a,**kw): return fn(*a,**kw)
```

## 🔗 关联知识

- [[07-装饰器]]
