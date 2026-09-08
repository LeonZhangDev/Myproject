---
tags: [week1]
difficulty: P0
status: learning
---

# token 安全释放锁

## 一句话理解

释放前必须确认锁仍属于自己。

## 核心理解

否则旧持有者可能误删已经被新持有者获得的锁；实际用 Lua 保证比较+删除原子。

## 🧠 完整理解

### 我会先这样理解

释放 Redis 锁时不能简单 `DEL lock_key`，因为你的锁可能已经超时，随后被另一个实例重新获得；此时旧实例再 DEL 会把别人的新锁删掉。正确做法是在抢锁时写唯一 token，释放时原子地“比较 token，只有相等才删除”，通常用 Lua 脚本实现。

### 执行顺序 / 思考顺序

A 获锁 token=A → A 执行过久锁 TTL 到期 → B 获得同名锁 token=B → A 终于结束 → 若直接 DEL 就误删 B；正确脚本先 GET 比较是否仍为 A → 不相等则不删。

### 容易踩的坑

“先 GET token，Python 判断，再 DEL”仍然不是原子操作，GET 和 DEL 之间锁可能变化。比较和删除必须在 Redis 侧一次完成。

### 面试时我会这样说

> 安全释放锁最容易被忽略。我不会直接 DEL，因为锁可能早就过期并被别人拿走了。我的 value 一定是随机 token，释放用 Lua 做 compare-and-delete，保证删的是自己的锁。

## 最小代码 / 场景

```text
if redis_token == my_token: delete lock
```


## 🧪 简单例子与返回结果

### 例子

```lua
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
```

### 运行 / 返回结果

```text
当前锁值 == 自己的 token：返回 1，删除成功
token 不匹配：返回 0，不删除别人的锁
```

## 🔗 关联知识

- [[15-分布式锁]]
