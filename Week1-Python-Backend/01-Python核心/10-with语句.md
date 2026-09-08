---
tags: [week1]
difficulty: P0
status: learning
---

# with 语句

## 一句话理解

`with` 是使用上下文管理器的语法。

## 核心理解

异步资源对应 `async with`，如 asyncio Lock、异步事务。

## 🧠 完整理解

### 我会先这样理解

`with` 是使用上下文管理协议的语法糖，它让“申请资源—使用资源—释放资源”写成一个明确的块。它不是只用于文件；任何实现上下文管理器协议的对象都可以放进 with，包括线程锁、数据库会话、事务、`contextlib` 创建的资源管理器。异步资源还有对应的 `async with`。

### 执行顺序 / 思考顺序

计算 with 后面的表达式 → 调 `__enter__`/`__aenter__` → 把返回值绑定给 `as` 后的变量 → 执行块 → 无论成功失败都走 `__exit__`/`__aexit__`。所以它本质上帮我们正确地组织了 try/finally。

### 容易踩的坑

`with` 能保证退出逻辑被调用，但不能保证你的退出逻辑本身一定成功。数据库 commit、网络 close 仍然可能报错，因此关键资源场景还需要异常处理和日志。

### 面试时我会这样说

> 我一般不把 with 只记成“打开文件的写法”，而是把它看成资源生命周期语法。凡是必须成对执行的东西，比如 begin/commit、lock/unlock，都很适合用 with 把边界写清楚。

## 最小代码 / 场景

```python
async with lock:
    ...
```


## 🧪 简单例子与返回结果

### 例子

```python
from pathlib import Path

p = Path("demo.txt")
with p.open("w", encoding="utf-8") as f:
    f.write("hello")

print(f.closed)
```

### 运行 / 返回结果

```text
True
```

**怎么理解：** 离开 with 后文件会自动关闭，即使中间发生异常也会执行清理逻辑。

## 🔗 关联知识

- [[09-上下文管理器]]
- [[../02-Asyncio与并发/14-Lock]]
