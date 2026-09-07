---
tags: [week1]
difficulty: P0
status: learning
---

# 生成器与 yield

## 一句话理解

生成器用 `yield` 简洁地创建惰性迭代器。

## 核心理解

适合大文件、流式数据、SSE token；数据按需生成，不必一次性占满内存。

## 最小代码 / 场景

```python
def nums():
    yield 1
    yield 2
for x in nums(): print(x)
```


## 🧪 简单例子与返回结果

### 例子

```python
def numbers():
    yield 1
    yield 2
    yield 3

for x in numbers():
    print(x)
```

### 运行 / 返回结果

```text
1
2
3
```

**怎么理解：** yield 每次只产出一个值，并保留函数当前执行位置。

## 🔗 关联知识

- [[05-迭代器]]
- [[../08-流式通信/02-SSE]]
