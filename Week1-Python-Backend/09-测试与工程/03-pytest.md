---
tags: [week1]
difficulty: P0
status: learning
---

# pytest

## 一句话理解

Python 常用测试框架。

## 核心理解

核心能力：简洁断言、fixture、参数化。

## 🧠 完整理解

### 我会先这样理解

pytest 是 Python 常用测试框架，核心优势是普通 assert、fixture、参数化和丰富插件生态。测试发现通常基于文件/函数命名规则，失败时会重写 assert 展示差异。大型项目的关键不是会执行 `pytest`，而是建立清晰的 fixture 层级、marker 和测试目录结构。

### 执行顺序 / 思考顺序

pytest 收集 test 文件/函数 → 解析所需 fixtures → 按作用域创建 fixture → 执行测试 → assert 失败生成详细 diff → teardown yield fixture → 汇总结果和退出码。

### 容易踩的坑

fixture autouse 和高作用域如果滥用，会让测试隐式依赖太多；测试能单独运行、顺序无关比“看起来少写几行”更重要。

### 面试时我会这样说

> 我喜欢 pytest 是因为测试函数本身很像普通 Python，assert 也直接。真正用起来我会把公共准备放 fixture，重复输入放 parametrize，但尽量保持每个测试的依赖一眼能看出来。

## 最小代码 / 场景

```bash
pytest -q
```


## 🧪 简单例子与返回结果

### 例子

```python
def test_math():
    assert 1 + 1 == 2
```

### 运行 / 返回结果

```text
$ pytest -q
1 passed
```

## 🔗 关联知识

- [[04-fixture]]
- [[05-参数化测试]]
