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
