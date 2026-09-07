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
