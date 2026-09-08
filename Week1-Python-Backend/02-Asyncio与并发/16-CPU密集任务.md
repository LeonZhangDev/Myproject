---
tags: [week1]
difficulty: P0
status: learning
---

# CPU 密集任务

## 一句话理解

长时间 CPU 计算不 await，会阻塞事件循环。

## 核心理解

可用多进程/ProcessPool/原生扩展/任务队列/独立计算服务。

## 🧠 完整理解

### 我会先这样理解

CPU 密集任务的瓶颈是持续计算，而不是等待 I/O。把这类工作直接放进 asyncio 事件循环会长时间不让出，导致所有请求响应都被拖慢。纯 Python 计算还受 GIL 影响，所以通常考虑进程池、独立计算服务、任务队列，或者 NumPy/PyTorch 等原生计算库。

### 执行顺序 / 思考顺序

请求进入 → 如果直接在 event loop 做大循环/模型前处理 → loop 长时间无法调度其他 Task。更合理的是把计算 offload 到进程/专用 worker，API 层只负责提交任务、查询状态或等待受控结果。

### 容易踩的坑

线程池并不一定能加速纯 Python CPU 计算；而多进程也不是免费午餐，有序列化、进程通信、内存复制和启动成本。模型推理还要结合 GPU batch 与显存设计。

### 面试时我会这样说

> 我会先把 CPU 密集和 I/O 密集分开。大量 HTTP、数据库等待适合 async；纯 Python 重计算放 async 里反而会卡整个 loop。计算重的话我会考虑多进程、Celery/任务服务，或者让 NumPy、PyTorch 这种原生库去做。

## 最小代码 / 场景

```python
from concurrent.futures import ProcessPoolExecutor
```


## 🧪 简单例子与返回结果

### 例子

```python
from concurrent.futures import ProcessPoolExecutor

def calc(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor() as pool:
    print(pool.submit(calc, 1_000_000).result())
```

### 运行 / 返回结果

```text
333332833333500000
```

**怎么理解：** CPU 密集型工作通常更适合多进程，因为可以利用多个 CPU 核心。

## 🔗 关联知识

- [[03-Python-GIL]]
- [[09-阻塞调用]]
