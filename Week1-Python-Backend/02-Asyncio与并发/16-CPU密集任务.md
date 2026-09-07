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

## 🔗 关联知识

- [[03-Python-GIL]]
- [[09-阻塞调用]]
