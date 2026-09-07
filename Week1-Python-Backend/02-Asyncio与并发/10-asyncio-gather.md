---
tags: [week1]
difficulty: P0
status: learning
---

# asyncio.gather

## 一句话理解

`gather` 并发等待一组 awaitable，并按输入顺序返回结果。

## 核心理解

适合“全部完成后一起拿结果”；异常传播策略要明确。

## 最小代码 / 场景

```python
r=await asyncio.gather(a(),b(),c())
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def double(x):
    await asyncio.sleep(0.1)
    return x * 2

async def main():
    result = await asyncio.gather(double(1), double(2), double(3))
    print(result)

asyncio.run(main())
```

### 运行 / 返回结果

```text
[2, 4, 6]
```

**怎么理解：** gather 会并发等待多个 awaitable，并按传入顺序返回结果。

## 🔗 关联知识

- [[11-TaskGroup]]
