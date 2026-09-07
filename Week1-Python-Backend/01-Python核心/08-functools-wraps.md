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


## 🧪 简单例子与返回结果

### 例子

```python
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@log_call
def pay():
    """支付函数"""
    return "ok"

print(pay.__name__)
print(pay.__doc__)
print(pay())
```

### 运行 / 返回结果

```text
pay
支付函数
ok
```

**怎么理解：** 如果去掉 @wraps(func)，pay.__name__ 通常会变成 wrapper。

## 🔗 关联知识

- [[07-装饰器]]
