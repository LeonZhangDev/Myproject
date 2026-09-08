---
tags: [week1]
difficulty: P0
status: learning
---

# BackgroundTasks

## 一句话理解

响应返回后执行轻量、短时、允许偶尔失败的同进程任务。

## 核心理解

没有持久队列、跨进程协调、可靠重试，不应当可靠任务队列。

## 🧠 完整理解

### 我会先这样理解

BackgroundTasks 适合“响应可以先返回，但随后做一点轻量工作”的场景，例如发送非关键通知、写辅助日志。它仍然运行在当前应用进程生命周期内，不是可靠任务队列；进程重启、worker 被杀都可能让任务丢失。耗时长、需要重试、必须保证执行的任务更适合 Celery/RQ/消息队列。

### 执行顺序 / 思考顺序

请求进入 → endpoint `background_tasks.add_task(...)` → 构造并发送响应 → 响应发送后 Starlette 在当前进程执行后台任务。它不会把任务持久化到外部 broker。

### 容易踩的坑

不要把模型训练、视频转码、关键支付回调等重任务放 BackgroundTasks。它也可能占用进程线程/事件循环资源，任务抛错时客户端已经拿到成功响应。

### 面试时我会这样说

> 我会把 BackgroundTasks 定位成“轻量的响应后处理”，不是 Celery。比如发一个非关键邮件可以，但只要任务需要可靠重试、执行几分钟或者不能丢，我就会上真正的任务队列。

## 最小代码 / 场景

```python
background_tasks.add_task(write_log, 'created')
```


## 🧪 简单例子与返回结果

### 例子

```python
from fastapi import BackgroundTasks, FastAPI
app = FastAPI()

def write_log(msg: str):
    print(msg)

@app.post("/order")
def order(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "send email")
    return {"status": "accepted"}
```

### 运行 / 返回结果

```text
客户端先得到：
200 {"status":"accepted"}

随后后台任务执行，控制台打印：
send email
```

## 🔗 关联知识

- [[../02-Asyncio与并发/16-CPU密集任务]]
