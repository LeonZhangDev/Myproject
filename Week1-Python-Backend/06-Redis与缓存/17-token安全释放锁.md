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
