---
tags: [week1]
difficulty: P0
status: learning
---

# Future

## 一句话理解

Future 表示一个未来才完成的结果。

## 核心理解

业务代码通常直接用 Task；Task 属于 Future 体系的高级封装。

## 🧠 完整理解

### 我会先这样理解

Future 是“未来某个时间会有结果”的占位对象，内部主要表达 pending、done、cancelled 以及 result/exception 状态。它比 Task 更底层：Task 本身就是一种 Future 风格的对象，只是额外负责推进 coroutine。业务代码通常直接使用 Task/await，Future 更多出现在事件循环、回调式 API 与异步框架内部的桥接层。

### 执行顺序 / 思考顺序

创建 Future（pending）→ 某个生产者稍后 `set_result` 或 `set_exception` → Future 变成 done → 等待它的协程被事件循环唤醒 → `await future` 得到结果或重新抛异常。

### 容易踩的坑

不要为了“异步”手工到处 new Future。除非你在封装回调式 API 或设计底层异步组件，否则 Task 通常更自然。

### 面试时我会这样说

> 我会把 Future 解释成“未来结果的抽象”。它不一定知道结果怎么计算，只负责表示现在没有、以后会有。Task 则更进一步，知道自己要运行哪个 coroutine 来把这个结果算出来。

## 最小代码 / 场景

```text
Coroutine -> Task -> future result
```


## 🧪 简单例子与返回结果

### 例子

```python
import asyncio

async def main():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    future.set_result("done")
    print(await future)

asyncio.run(main())
```

### 运行 / 返回结果

```text
done
```

**怎么理解：** Future 更像一个“未来会有结果的容器”；Task 是 Future 的一种高级封装。

## 🔗 关联知识

- [[06-Task]]
