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
