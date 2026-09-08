---
tags: [week1]
difficulty: P0
status: learning
---

# Python GIL

## 一句话理解

传统 CPython 同一进程通常只有一个线程执行 Python 字节码。

## 核心理解

它限制 CPU 密集型多线程并行，但不等于 Python 不能并发；I/O、asyncio、多进程都可并发/并行。

## 🧠 完整理解

### 我会先这样理解

CPython 的 GIL 保证同一进程里通常只有一个线程在执行 Python 字节码，因此纯 Python CPU 密集代码很难通过多线程获得真正的多核并行。但线程在等待 I/O 时会释放执行机会，一些 C/CUDA 扩展也会在重计算阶段释放 GIL，所以“有 GIL”不等于 Python 不能并发。关键是区分 Python 字节码、I/O 等待和原生扩展计算。

### 执行顺序 / 思考顺序

多个线程存在 → 获取 GIL 的线程执行 Python 字节码 → 运行一段时间/进入阻塞或原生代码后让出 → 另一个线程获取。对于 CPU 密集纯 Python 循环，线程会争同一个 GIL；对于网络 I/O，等待阶段线程不用一直占着。

### 容易踩的坑

不要用“GIL 所以线程没用”这种绝对说法。数据库驱动、HTTP 客户端、文件 I/O 等阻塞场景，线程池依然常用；NumPy/PyTorch 的性能也不能简单按 GIL 推断。

### 面试时我会这样说

> 我会说 GIL 主要限制的是“同一进程里多个线程同时执行 Python 字节码”。所以 CPU 密集纯 Python 多线程通常收益不大，但 I/O 等待时线程仍然能并发。真要吃多核，我会考虑多进程，或者把计算交给会释放 GIL 的原生库。

## 最小代码 / 场景

```python
def cpu_work():
    return sum(i*i for i in range(10_000_000))
```


## 🧪 简单例子与返回结果

### 例子

```python
from threading import Thread

results = []
def work(x):
    results.append(x * x)

threads = [Thread(target=work, args=(i,)) for i in (2, 3)]
for t in threads: t.start()
for t in threads: t.join()
print(sorted(results))
```

### 运行 / 返回结果

```text
[4, 9]
```

**怎么理解：** 线程当然可以并发；GIL 主要限制的是同一 CPython 进程里 CPU 密集 Python 字节码的多核并行。

## 🔗 关联知识

- [[16-CPU密集任务]]
