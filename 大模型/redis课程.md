

## 一、Redis 是什么

**Redis（Remote Dictionary Server）** 是一个 **开源的、基于内存的键值（Key-Value）数据库**，由 Salvatore Sanfilippo 在 2009 年创建。

它最大的特点是：

> 所有数据都存储在内存中，读写速度极快（可达每秒上百万次操作）。

Redis 常被称为：

- **缓存数据库**
- **NoSQL 数据库**
- **内存数据结构存储系统**

**⚡ 二、Redis 的核心特点**

| 特点            | 说明                                       |
| ------------- | ---------------------------------------- |
| 🧩 **多种数据类型** | 支持 String、Hash、List、Set、Sorted Set、Bitmap、HyperLogLog、Stream 等 |
| ⚡ **高性能**     | 所有操作在内存中完成，速度非常快（微秒级）                    |
| 🔁 **持久化**    | 数据可以保存到磁盘（RDB 或 AOF），重启后仍能恢复             |
| 🔗 **丰富功能**   | 发布订阅（Pub/Sub）、事务、Lua 脚本、地理位置、延迟队列等       |
| **多种部署模式**    | 单机、主从复制、哨兵（Sentinel）、集群（Cluster）         |
| 🧰 **轻量易用**   | 单个可执行文件即可运行，配置简单                         |

## 二、安装 Redis 

1 安装 Python 客户端

```
pip install redis
```

## 三、连接 Redis

```
import redis

# 连接本地 Redis（默认端口 6379）
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# 测试连接
print(r.ping())  # 返回 True 表示连接成功

```

## 四、常用操作示例

### 1️⃣ 字符串（String）

```python
r.set('name', 'Tom')          # 设置
print(r.get('name'))          # 获取（返回 bytes 类型）
print(r.get('name').decode()) # 转为字符串

r.incr('count')               # 自增
r.decr('count')               # 自减
r.set("name", "x", ex=60)  # 设置 1 分钟过期时间  

```



### 2️⃣ 哈希（Hash）

```python
r.hset('user:1', 'name', 'Alice')
r.hset('user:1', 'age', 25)
print(r.hget('user:1', 'name'))          # b'Alice'
print(r.hgetall('user:1'))               # {b'name': b'Alice', b'age': b'25'}

```



### 3️⃣ 列表（List）

```python
r.lpush('queue', 'a', 'b', 'c')   # 从左侧插入
r.rpush('queue', 'x', 'y')        # 从右侧插入
print(r.lrange('queue', 0, -1))   # 获取所有元素
print(r.lpop('queue'))            # 从左侧弹出

```



### 4️⃣ 集合（Set）

```python
r.sadd('tags', 'python', 'ai', 'redis')
print(r.smembers('tags'))      # 获取所有成员
print(r.sismember('tags', 'ai'))  # 判断是否存在
r.srem('tags', 'ai')           # 删除元素

```



### 5️⃣ 有序集合（Sorted Set）

```python
r.zadd('rank', {'Tom': 100, 'Jerry': 80})
print(r.zrange('rank', 0, -1, withscores=True))
r.zincrby('rank', 5, 'Jerry')  # Jerry +5分

```



### 6️⃣ 键的管理

```python
print(r.keys('*'))      # 查看所有键
r.delete('name')        # 删除键
r.exists('user:1')      # 判断是否存在
r.expire('user:1', 30)  # 设置过期时间（秒）

```

非常好的问题 👍，这个概念在 **Python 操作 Redis 时非常关键**。
我们来一步步讲清楚 Redis 的 **序列化（serialization）与反序列化（deserialization）**，再配上代码示例。



## 五 redis 序列化和反序列化

**🧠 一、为什么要序列化？**

Redis 是一个 **键值数据库**，底层只认识 **字节数据（bytes）**。
当我们往 Redis 存入复杂的 Python 对象（如字典、列表、自定义类）时，
就必须把它 **序列化为字符串或二进制** 才能存进去。

> 简单说：
>
> - **序列化（serialize）**：把 Python 对象 → 转成可存入 Redis 的字节或字符串
> - **反序列化（deserialize）**：从 Redis 拿出来的字节 → 转回 Python 对象



**二、Redis 默认存储的类型**

当你执行：

```
r.set("user", {"name": "Tom", "age": 20})
```

你以为它存了一个字典，其实会报错，因为 Redis 不知道这个对象是什么。
它只支持像这样：

```
r.set("user", "Tom")  # 字符串
```

所以我们需要把字典“转成字符串”或“转成字节流”。

**三、JSON 序列化示例**

```python
import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Python 字典
user = {"name": "Tom", "age": 25, "tags": ["python", "ai"]}

# 序列化：dict → JSON 字符串
r.set("user:1", json.dumps(user))

# 从 Redis 取出（二进制 bytes）
data = r.get("user:1")

# 反序列化：JSON 字符串 → dict
user_obj = json.loads(data.decode())

print(user_obj)
# 输出: {'name': 'Tom', 'age': 25, 'tags': ['python', 'ai']}

```

✅ **优点**：兼容多语言，常用于 Web 项目（例如缓存 API 响应数据）。
⚠️ **注意**：只能序列化基本类型（str、int、list、dict 等）。



## 六 连接池（推荐用法）

如果频繁连接 Redis，推荐使用连接池，性能更好：

```python
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
```

## **七 redis持久化配置**

AOF 是另一种更安全的持久化方式，它会**记录每一个写入操作命令**，重启后可以更完整地恢复数据。

1 开启 AOF

默认是关闭的：

```
appendonly no
```

把它改成：

```
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
```

这表示：

- ✅ 开启 AOF；
- 每 1 秒执行一次 `fsync` 写入磁盘；
- AOF 文件名为 `appendonly.aof`；

2 启动服务器并读取配置文件

```
redis-server.exe redis.windows.conf
```

3 验证配置是否成功

```
redis-cli
127.0.0.1:6379> CONFIG GET appendonly
1) "appendonly"
2) "yes"
```

如果能看到这两个值正确，说明 AOF 持久化已启用。