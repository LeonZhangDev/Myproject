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

## 🧠 完整理解

### 我会先这样理解

Git 是分布式版本控制系统，核心对象是 commit 快照和分支引用。日常流程里 branch 用来隔离工作，commit 表达一个可解释的小变更，merge/rebase 用来整合历史。对工程质量来说，清晰提交历史、可 review 的 PR 和避免把 secret/大二进制文件提交仓库比会背命令更重要。

### 执行顺序 / 思考顺序

修改工作区 → `git add` 放入暂存区 → `git commit` 创建新快照 → branch 指针前移 → push 同步到远端 → PR review → merge/rebase 集成主分支。冲突本质是 Git 无法自动决定同一片内容该保留哪一版。

### 容易踩的坑

`git push --force`、`reset --hard` 都可能破坏别人工作；共享分支要谨慎。Git 也不是备份 secret 的地方，密钥一旦提交即使后来删除，历史里仍可能存在。

### 面试时我会这样说

> 我使用 Git 不只是“能 push”。我会尽量一个 commit 做一件事，分支名能说明任务，PR 方便 review。遇到冲突我会先理解两边改动，而不是直接选 ours/theirs 把代码覆盖掉。

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

