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

## 🧠 完整理解

### 我会先这样理解

TaskGroup 是 Python 3.11 引入的结构化并发工具。核心思想是：一组子任务有明确的作用域，离开 `async with TaskGroup()` 之前要么全部完成，要么出现异常时按规则取消其余任务并把异常统一交给上层。这样比“到处 create_task 然后自己记得回收”更容易保证生命周期完整。

### 执行顺序 / 思考顺序

进入 TaskGroup → `create_task` 创建多个子任务 → 作用域等待所有任务 → 某个任务失败时取消其他未完成任务 → 等待清理 → 用 ExceptionGroup 汇总传播异常 → 离开作用域。

### 容易踩的坑

TaskGroup 的异常可能以 ExceptionGroup 形式出现，处理方式和单一异常不同。结构化并发也不是说所有任务都必须塞进一个组，要按业务生命周期划边界。

### 面试时我会这样说

> 我现在更喜欢把一批“同生共死”的并发任务放进 TaskGroup。因为这组任务谁失败、其他任务要不要取消、什么时候算真正结束，框架帮我把边界管得更清楚，不容易留下失控的后台 Task。

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
