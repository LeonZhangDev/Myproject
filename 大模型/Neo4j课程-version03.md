## 1 什么是 Neo4j？

​     Neo4j 是一个原生图数据库管理系统（DBMS）。它被设计用来高效地存储、管理和查询数据之间复杂的关系。与传统的关系型数据库（如 MySQL, PostgreSQL）使用表和行不同，Neo4j 使用图结构，其核心是**节点**、**关系**和**属性**。

- 简单来说，Neo4j 是为了处理“关系”而生的数据库，它认为“关系”和“数据”同等重要。
- 企业使用 Neo4j 构建知识图谱

**核心概念：图数据库的基石**

要理解 Neo4j，首先要理解其构建模块：

1. **节点（Nodes）**：
   - 表示实体或对象，例如一个人、一个地点、一件商品或一篇文章。
   - 相当于关系型数据库中的“记录”或“行”。
   - 节点可以有**标签（Labels）**，用于将其分类（例如 `:Person`, `:Movie`）。
2. **关系（Relationships）**：
   - 表示节点之间的**连接**，这是图数据库的灵魂。
   - 关系总是有**方向**（从一个节点指向另一个节点）、**类型**（例如 `:FOLLOWS`, `:ACTED_IN`, `:PURCHASED`）和**属性**。
   - **关系是图数据库的一等公民**，它们不是通过外键查询出来的，而是直接存储在数据库中的。这使得遍历关系速度极快。
3. **属性（Properties）**：
   - 是键值对，用于为节点和关系添加额外信息。
   - 例如，一个 `:Person` 节点可以有 `name: ‘Tom Hanks’`， `born: 1956` 等属性。一个 `:ACTED_IN` 关系可以有 `roles: [‘Forrest Gump’]` 属性。
4. **标签（Labels）**：
   - 附加在节点上的标签，用于将节点分组或分类。
   - 类似于关系型数据库中的“表”，但一个节点可以拥有多个标签。

**一个简单的例子：**

```
(Tom:Hactor {name: ‘Tom Hanks’}) -[:ACTED_IN {roles: [‘Forrest’]}]-> (Forrest:Movie {title: ‘Forrest Gump’})
```

这表示：一个带有 `Actor` 标签和 `name` 属性的“Tom Hanks”节点，通过一个类型为 `ACTED_IN` 且带有 `roles` 属性的关系，连接到一个带有 `Movie` 标签和 `title` 属性的“Forrest Gump”节点。

**Neo4j 如何工作？Cypher 查询语言**

Neo4j 使用一种名为 **Cypher** 的声明式图查询语言。Cypher 的语法非常直观，类似于用 ASCII 艺术来绘制模式。

## 2 环境安装

安装步骤如下：

1 Neo4j底层是java，需要依赖JDK，输入命令检查是否安装。

命令：java --version

```
C:\Users\15740>java --version
java 21.0.7 2025-04-15 LTS
Java(TM) SE Runtime Environment (build 21.0.7+8-LTS-245)
Java HotSpot(TM) 64-Bit Server VM (build 21.0.7+8-LTS-245, mixed mode, sharing)
```

2  安装neo4j-desktop，以管理员身份运行cmd 窗口， 进入到neo4j-desktop-2.0.3-x64.exe 文件所在目录

输入命令 ：neo4j-desktop-2.0.3-x64.exe /S /D=D:\neo4j-desktop

如下所示

```
E:\工具\Neo4j工具>neo4j-desktop-2.0.3-x64.exe /S /D=D:\neo4j-desktop
```

运行完后，稍等几分钟，在 D:\neo4j-desktop目录下可以看到安装文件

## 3 Cypher 查询语言

Cypher 是 Neo4j 图数据库的**声明式图查询语言**。它的设计非常直观，遵循“**按图索骥**”的原则，让你能使用一种类似 ASCII-art 的语法来描述、查询和操作图数据。

**一、核心概念**

在学习 Cypher 之前，必须理解图数据库的三个基本构建块：

1. **节点 (Nodes)**：表示实体/对象，用圆括号表示 `()`。
   - **标签 (Labels)**：节点的类别或类型，类似于表名。用冒号表示，如 `:Person`、`:Movie`。一个节点可以有多个标签 `:Person:Customer`。
   - **属性 (Properties)**：节点的键值对数据，用大括号表示 `{name: 'Tom Hanks', born: 1956}`。
2. **关系 (Relationships)**：表示节点之间的连接，用箭头表示  `-[ ]->`。
   - **类型 (Type)**：关系的类别，如 `:ACTED_IN`、`:DIRECTED`、`:FRIENDS_WITH`。
   - **方向 (Direction)**：关系是有方向的 (`-->` 或 `<--`)，但查询时可以忽略方向。
   - **属性**：和节点一样，关系也可以有属性 `{roles: ['Forrest'], rating: 5}`。
3. **路径 (Paths)**：由节点和关系连接而成的序列，例如：`(:Person)-[:ACTED_IN]->(:Movie)`。



### 3.0 数据库创建和查看

```
-- 查看服务器上的所有数据库（包括系统数据库）
SHOW DATABASES

-- 查看当前正在使用的数据库
SHOW DEFAULT DATABASE

-- 查看特定数据库的状态和信息
SHOW DATABASE neo4j

-- 切换到另一个数据库
:use system
```

**创建数据库**

**重要提示**：在 Neo4j 中，创建数据库的权限和方式取决于 Neo4j 的版本和配置。

**社区版创建数据库**

Neo4j 社区版**不支持**通过 Cypher 创建多个数据库。你只能使用默认的 `neo4j` 数据库

```
-- 在社区版中，这个命令会失败
-- 如果数据库不存在则创建
CREATE DATABASE mynewdb IF NOT EXISTS
```

**社区版足够的情况：**

- 🎓 学习和个人项目
- 🧪 开发和测试环境
- 💼 中小型项目
- 🔧 单服务器部署



### 3.1 Cypher 增删改查操作

#### 3.1.1 新增

**一 创建节点并使用变量**

```
CREATE (p:Person {name:"马云",age:55})
```

1. **CREATE** - 创建指令

- 表示要创建新的图元素（节点或关系）
- 这是Neo4j的写操作关键字

2. **(p:Person)** - 节点定义

- **( )**：括号表示一个节点
- **p**：变量名，用于后续引用这个节点
- **:Person**：节点标签，表示这个节点的类型或类别

3. **{name:"马云", age:55}** - 属性集合

- **{ }**：花括号包含节点的属性键值对
- **name:"马云"**：字符串属性，值为"马云"
- **age:55**：数字属性，值为55
- 多个属性用逗号分隔

再创建一个节点 ：公司阿里巴巴

```
CREATE (c:Company {name:"阿里巴巴"})
```

**二 创建关系**

```
MATCH (p:Person{name:"马云"}),(c:Company{name:"阿里巴巴"}) create (p)-[r:FOUNDED {role:"创始人",startYear:1999}] -> (c) RETURN p,r,c
```

1. **MATCH (p:Person {name: "马云"}), (c:Company {name: "阿里巴巴"})**

- **MATCH作用**：查找已存在的节点
- **p:Person {name: "马云"}**：查找标签为Person且name属性为"马云"的节点，赋值给变量p
- **c:Company {name: "阿里巴巴"}**：查找标签为Company且name属性为"阿里巴巴"的节点，赋值给变量c
- **注意**：如果节点不存在，MATCH会返回空，CREATE不会执行

2. **CREATE (p)-[r:FOUNDED {role: "创始人", startYear: 1999}]->(c)**

- **作用**：创建新的关系
- **(p)-[r:FOUNDED]->(c)**：在节点p和c之间创建FOUNDED类型的关系
- **{role: "创始人", startYear: 1999}**：为关系添加属性
- **r**：关系变量名，用于后续引用

3. **RETURN p, r, c**

- **作用**：返回结果
- 返回创建的节点p、关系r和节点c
- 方便查看操作结果

**三 一次性创建节点和关系（如果节点不存在）**

```
create (p:Person {name:"马化腾",age:48}) - [r:FOUNDED {role:"创办人"}] -> (c:Company {name:"腾讯"})
```

**四 添加标签**

```
MATCH (c:Company {name: '阿里巴巴'})
SET c:chinaCompany
RETURN c
```



#### 3.1.2. 查询 

`MATCH` 用于描述图模式来查找数据，`RETURN` 用于指定返回什么

**一  查询所有节点**

```
MATCH (n) RETURN n
```

`-- 警告：在大型数据库上谨慎使用，可能返回海量数据。`

**二 根据标签和属性查询节点**

```
-- 查询所有Person
MATCH (p:Person) RETURN p

-- 查询特定名字的Person
MATCH (p:Person {name:"马云"}) RETURN p

-- 使用WHERE子句进行更复杂的过滤
MATCH (p:Person) WHERE p.name="马云" and p.age > 50 return p
```

**三 遍历路径查询**

```
--查询马云创办了哪些公司
MATCH (p:Person {name:"马云"}) - [r:FOUNDED] -> (c:Company) RETURN p.name,c.name

--查询谁创办了腾讯公司
MATCH (p:Person)-[r:FOUNDED] -> (c:Company {name:"腾讯"}) RETURN p.name


MATCH (p:person) -[:FOUNDED] -> (c:company) where c.name='阿里巴巴' ORDER BY p.age RETURN p.name LIMIT 2 

-- LIMIT 查询 几条，order by 排序 默认升序：ASC, 降序是 DESC。
MATCH (p:person) ORDER BY p.age DESC RETURN p LIMIT 2
```

#### 3.1.3 修改

**修改或添加属性** - 使用 `SET`

```
-- 为马云添加一个属性：国籍
MATCH (p:Person {name:"马云"}) set p.guoji ="中国" RETURN p

-- 修改马云的年龄
MATCH (p:Person {name:"马云"}) set p.age ="54" RETURN p
```

#### 3.1.4 删除

**一 删除属性** - 使用 `REMOVE`

```
-- 删除马云的 国籍属性
MATCH (p:Person {name:"马云"}) REMOVE p.guoji  RETURN p
```

**二 删除关系和节点 - 使用 delete**

**1 删除关系**

```
-- 先找到关系，然后删除它（节点保留）
MATCH (p:Person {name:"马化腾",age:48}) - [r:FOUNDED {role:"创办人"}] -> (c:Company {name:"腾讯"}) DELETE r
```

**2 删除节点**

```
MATCH (p:Person {name:"马化腾"}) DELETE p
```

```
注意 ：如果节点还有关系，无法直接删除
-- 会报错：Cannot delete node<...>, because it still has relationships. To delete this node, you must first delete its relationships
```

**3 删除标签**

```
MATCH (p:Person:id {name: '马云'})
REMOVE p:id
RETURN p
```

**4 清空整个数据库**

```
-- 匹配所有节点和关系，然后分离删除所有节点
MATCH (n)
DETACH DELETE n
-- 极端危险！仅在需要彻底清理时使用。
```









### 3.2 约束

约束用于保证数据的唯一性和完整性，Neo4j 会自动维护约束相关的索引。

#### **3.3.1 节点属性唯一性约束**

**作用**：确保某个标签的节点的某个属性值是唯一的。



1 创建唯一性约束

```
-- 创建唯一性约束（如果不存在）
CREATE CONSTRAINT unique_person_id IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE

```

2  验证约束

```
-- 尝试插入重复ID会报错
CREATE (:Person {id: 'fe317d8d-ae56-4dbf-963e-099d6fb38f8d', name: '马云'})
```

#### 3.3.2 节点属性存在性约束

**作用**：确保某个标签的所有节点都拥有某个属性。

```
-- 创建存在性约束
CREATE CONSTRAINT person_name_exists IF NOT EXISTS
FOR (p:Person)
REQUIRE p.name IS NOT NULL
```

**验证约束**：

```
-- 尝试创建没有name属性的Person会报错
CREATE (:Person {age: 55}) -- 这会失败
CREATE (:Person {name: '马云', age: 55}) -- 这会成功
```

#### **3.3.3 查看和删除约束**

```
-- 查看约束
SHOW CONSTRAINTS

-- 删除约束
DROP CONSTRAINT unique_person_id IF EXISTS
```

### 3.3 索引

索引用于加速查询性能，特别是基于属性的查找。

#### 3.3.1 单属性索引

**作用**：加速基于单个属性的查询。

```cypher
-- 创建单属性索引
CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person)
ON (p.name)
```

**使用场景**：

```cypher
-- 这个查询会使用索引
MATCH (p:Person {name: '马云'}) RETURN p
MATCH (p:Person) WHERE p.name = '马云' RETURN p
```

#### 3.3.2  复合索引

**作用**：加速基于多个属性组合的查询。

```
-- 创建复合索引
CREATE INDEX person_name_age_index IF NOT EXISTS
FOR (p:Person)
ON (p.name, p.age)
```

**使用场景**：

```
-- 这些查询会使用复合索引
MATCH (p:Person) WHERE p.name = '马云' AND p.age = 55 RETURN p
MATCH (p:Person) WHERE p.name = '马云' RETURN p -- 也会使用索引
```

#### 3.3.3  全文索引

一 定义全文索引

```cypher
CREATE FULLTEXT INDEX personFulltextIndex 
FOR (n:Person|Company) 
ON EACH [n.name, n.age, n.id]
```

二 查询全文索引

```cypher
CALL db.index.fulltext.queryNodes("personFulltextIndex", "阿里巴巴") 
YIELD node, score
RETURN node.name, node.description, score
ORDER BY score DESC
```

全文搜索引擎会为每个匹配的结果计算一个**相关性分数（Score）**，你可以根据这个分数对结果进行排序，让最相关的结果排在最前面。

**3.4.4 查看和删除索引**

```
--查看索引
SHOW INDEXES

-- 删除索引
DROP INDEX person_name_index IF EXISTS

-- 删除全文索引
CALL db.index.fulltext.drop("personFulltextIndex")
```





## 4  LangChain操作Neo4j

`Neo4jGraph` 是 LangChain 中用于连接和操作 Neo4j 图数据库的工具类，它提供了将自然语言处理与图数据库相结合的能力

**环境准备**

```
pip install neo4j -i https://mirrors.aliyun.com/pypi/simple/

pip install -U langchain-neo4j -i https://mirrors.aliyun.com/pypi/simple/
```



### 4.1 链接数据库

```python
# 导入操作使用到的包
from langchain_neo4j import Neo4jGraph
url ="bolt://localhost:7687"
username="neo4j"
password="cat2002415"
data_base = "neo4j"
graph = Neo4jGraph(url=url, username=username, password=password, database=data_base)
print("连接成功")
```

### 4.2 数据库操作

**1 新增节点**

```cypher
def create_node():
    graph.query("CREATE (p:Student {name:$name,age:$age})",params={"name":"张三","age":18})
    print("创建成功！")
```

**2 查询节点**

```cypher
def query_node():
    students = graph.query("MATCH (s:Student) RETURN s")
    print( students)

```

**3 修改节点**

```cypher
def update_node():
    student = graph.query("MATCH (s:Student {name:$name}) set s.age=$age return s", params={"name":"张三","age":19})
    if student:
        print("修改成功！")
    else:
        print("未找到该节点！")
```

**4 删除节点**

```cypher
#删除节点
def delete_node():
    # 查询节点
    graph.query("MATCH (s:Student{name:$name}) DELETE s",params={"name":"张三"})
    print("删除成功！")
```





