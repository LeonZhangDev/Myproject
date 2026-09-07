---
tags: [week1]
difficulty: P0
status: learning
---

# TaskGroup

## 一句话理解

TaskGroup 用作用域管理一组并发任务。

## 核心理解

组内失败会协调取消其他任务，并统一等待/汇总异常，结构化并发更清晰。

## 最小代码 / 场景

```python
async with asyncio.TaskGroup() as tg:
    t1=tg.create_task(a())
    t2=tg.create_task(b())
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def double(x):
    await asyncio.sleep(0.1)
    return x * 2

async def main():
    async with asyncio.TaskGroup() as tg:
        a = tg.create_task(double(2))
        b = tg.create_task(double(3))
    print(a.result(), b.result())

asyncio.run(main())
```

### 运行 / 返回结果

```text
4 6
```

**怎么理解：** TaskGroup 是 Python 3.11+ 的结构化并发方式；离开上下文前会等待组内任务结束。

## 🔗 关联知识

- [[10-asyncio-gather]]
- [[12-超时与取消]]
