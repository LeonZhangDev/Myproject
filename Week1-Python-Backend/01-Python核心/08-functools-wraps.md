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

## 🧠 完整理解

### 我会先这样理解

`functools.wraps` 用在装饰器的 wrapper 上，它会把原函数的重要元数据复制/关联回来，例如 `__name__`、`__doc__`、`__annotations__`、`__wrapped__`。这不只是为了“看起来好看”，很多调试、文档生成、依赖注入和反射工具都依赖这些信息。FastAPI 这类框架尤其关心函数签名和注解。

### 执行顺序 / 思考顺序

定义装饰器 → `@wraps(func)` 修饰 wrapper → wraps 内部基于 `update_wrapper` 写回元数据 → 调用行为仍然走 wrapper，但工具检查函数时可以沿着 `__wrapped__` 找回原函数语义。

### 容易踩的坑

wraps 不会自动修复你装饰器里的逻辑错误，也不会让同步 wrapper magically 变成异步 wrapper。它解决的是“包装后函数身份信息丢失”这一类问题。

### 面试时我会这样说

> 我把 wraps 当成写装饰器的默认配置。因为不加的话，日志里函数名可能全是 wrapper，框架做签名检查也容易出问题。它本质上是在告诉外部工具：这个 wrapper 包的是谁，原来的函数信息是什么。

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
