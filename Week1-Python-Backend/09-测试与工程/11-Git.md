---
tags: [week1]
difficulty: P0
status: learning
---

# Git 工程习惯

## 一句话理解

Git 不只是备份，也是开发过程证据。

## 核心理解

提交信息应表达做了什么，不要全是 update。

## 最小代码 / 场景

```bash
git status
git add .
git commit -m "feat: add pagination"
```

## 🧪 简单例子与返回结果

### 例子

```bash
git switch -c feature/redis-cache
git add .
git commit -m "feat: add redis cache"
git switch main
git merge feature/redis-cache
```

### 运行 / 返回结果

```text
创建并切到 feature/redis-cache
提交功能代码
回到 main
把 feature/redis-cache 合并进 main
```

