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
