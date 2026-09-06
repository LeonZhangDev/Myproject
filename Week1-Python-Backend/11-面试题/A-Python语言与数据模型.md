---
tags: [week1, interview, a]
difficulty: P0
status: learning
---

# A｜Python语言与数据模型


## W1-Q1｜同步函数、线程和 async 协程有什么区别？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
同步函数按当前线程顺序执行；线程由操作系统调度，适合阻塞 I/O；async 协程由事件循环协作调度，在 await 处让出控制权，适合大量 I/O 并发。CPU 密集通常用多进程或独立计算服务。

### 最小代码 / 场景
```python
import asyncio
async def io_task(n):
    await asyncio.sleep(1)
    return n
async def main():
    print(await asyncio.gather(io_task('A'),io_task('B')))
asyncio.run(main())
```

### 关联知识
- [[../02-Asyncio与并发/02-进程线程协程]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q2｜Python GIL 是什么？它是否意味着 Python 不能并发？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
传统 CPython 中 GIL 让同一进程通常只有一个线程执行 Python 字节码，限制 CPU 密集型多线程并行；I/O 等待时线程仍可切换，asyncio 可做 I/O 并发，多进程可利用多核。

### 最小代码 / 场景
```python
# CPU密集多线程不会因为线程数增加就自然获得 Python 字节码多核并行
def cpu_work():
    return sum(i*i for i in range(10_000_000))
```

### 关联知识
- [[../02-Asyncio与并发/03-Python-GIL]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q3｜为什么不建议把可变对象作为函数默认参数？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
默认参数在函数定义时求值一次。list/dict 作为默认值会在多次调用间共享状态；通常用 None 并在函数内部创建新对象。

### 最小代码 / 场景
```python
def add(x, items=None):
    if items is None: items=[]
    items.append(x)
    return items
```

### 关联知识
- [[../01-Python核心/03-可变默认参数]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q4｜浅拷贝与深拷贝有什么区别？什么情况下容易踩坑？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
浅拷贝只复制最外层容器，嵌套对象仍共享；深拷贝递归复制。嵌套列表、配置和缓存对象最容易踩坑。

### 最小代码 / 场景
```python
import copy
a=[[1]]; b=copy.copy(a); c=copy.deepcopy(a)
a[0].append(2)
print(b,c)
```

### 关联知识
- [[../01-Python核心/04-浅拷贝与深拷贝]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q5｜迭代器和生成器是什么关系？生成器有什么优势？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
迭代器按迭代协议逐个返回元素；生成器通过 yield 简洁创建迭代器，惰性计算、节省内存、适合流式数据。

### 最小代码 / 场景
```python
def numbers():
    yield 1
    yield 2
for x in numbers(): print(x)
```

### 关联知识
- [[../01-Python核心/06-生成器与yield]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q6｜Python 装饰器的本质是什么？为什么常使用 functools.wraps？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
装饰器是接收函数并返回新可调用对象的高阶函数；wraps 保留原函数名称、文档和签名等元数据。

### 最小代码 / 场景
```python
from functools import wraps
def deco(fn):
    @wraps(fn)
    def wrapper(*a,**kw): return fn(*a,**kw)
    return wrapper
```

### 关联知识
- [[../01-Python核心/07-装饰器]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？


## W1-Q7｜上下文管理器解决什么问题？with 语句如何保证资源释放？

### 先自己回答
> 先口述 30~60 秒，再看下面。

### 合格回答骨架
上下文管理器把资源获取/释放绑定到作用域；即使中间抛异常，退出逻辑仍执行，适合文件、锁、连接和事务。

### 最小代码 / 场景
```python
with open('a.txt','w') as f:
    f.write('ok')
```

### 关联知识
- [[../01-Python核心/09-上下文管理器]]

### 面试官继续追问
- 为什么？
- 哪些情况下不成立？
- 真实 FastAPI 项目怎么落地？
- 出问题怎么验证和排查？
