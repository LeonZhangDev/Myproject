---
tags: [week1]
difficulty: P0
status: learning
---

# Field 字段约束

## 一句话理解

`Field()` 添加长度、范围、描述等约束。

## 核心理解

让接口在进入业务逻辑前就拒绝非法输入。

## 最小代码 / 场景

```python
title:str=Field(min_length=1,max_length=100)
priority:int=Field(ge=1,le=5)
```

## 🔗 关联知识

- [[05-field-validator]]
