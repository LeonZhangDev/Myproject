# RAG 基础知识详解：从数据入库到检索、生成与评测

> 适用：RAG 入门、算法工程师复习、面试准备、项目设计  
> 重点：完整理解 RAG 的逻辑链路，而不是只会调用向量数据库  
> 公式格式：本文统一使用标准 LaTeX 块公式 `$$ ... $$`，尽量仅使用 ASCII 数学命令，避免乱码。

---

## 目录

1. RAG 是什么
2. 为什么需要 RAG
3. RAG 与大模型本身的关系
4. 一套完整 RAG 的总体架构
5. 离线阶段：知识库构建
6. 文档解析与数据清洗
7. Chunking：文档切块
8. Embedding：文本向量化
9. 向量相似度计算
10. Vector Index / Vector Database
11. Sparse Retrieval：BM25
12. Dense Retrieval：向量检索
13. Hybrid Retrieval：混合检索
14. RRF：倒数排名融合
15. TopK、Recall 与噪声之间的关系
16. Reranker：重排序
17. Bi-Encoder 与 Cross-Encoder
18. Metadata Filter
19. Query Understanding 与 Query Rewrite
20. Multi-Query / Query Decomposition
21. Context 构建
22. Prompt 构建与 Grounding
23. LLM 生成阶段
24. Citation / Source Attribution
25. RAG 的三类主要错误
26. RAG 检索指标
27. 生成质量指标
28. End-to-End 指标
29. RAG 与 Long Context 的关系
30. RAG 与 Fine-tuning 的区别
31. RAG 与 Agent 的关系
32. LlamaIndex、FAISS、LangGraph 的区别
33. 一个现代 RAG 的完整执行链路
34. 常见优化方向
35. 常见误区
36. 面试总结
37. 最小知识框架

---

# 1. RAG 是什么

RAG 全称：

**Retrieval-Augmented Generation**

中文通常翻译为：

**检索增强生成**

它的核心思想非常简单：

> 大模型在回答问题之前，先从外部知识库中检索相关资料，再根据这些资料生成答案。

最基础的流程：

```text
用户问题
   ↓
Query
   ↓
检索知识库
   ↓
获得相关文档
   ↓
把文档放进 Prompt
   ↓
LLM
   ↓
最终答案
```

如果没有 RAG：

```text
用户问题
   ↓
LLM
   ↓
直接依赖模型参数中的知识回答
```

如果有 RAG：

```text
用户问题
   ↓
外部知识检索
   ↓
相关证据
   ↓
LLM
   ↓
基于证据回答
```

所以 RAG 的本质不是“让模型背更多知识”，而是：

> **让模型在回答时临时获取它当前需要的知识。**

---

# 2. 为什么需要 RAG

大模型本身有几个天然限制。

## 2.1 模型训练数据存在时间边界

模型训练完成以后，参数中的知识不会自动更新。

例如公司今天刚发布：

```text
2026 年新版差旅报销制度
```

模型训练阶段不可能提前知道。

RAG 可以：

```text
用户问题
   ↓
检索最新公司制度
   ↓
把最新内容交给 LLM
   ↓
回答
```

---

## 2.2 私有知识无法天然存在于模型参数中

例如：

```text
企业内部文档
项目代码
公司数据库
合同
内部 Wiki
个人知识库
旅游业务数据
```

通用大模型通常不知道这些内容。

RAG 可以在推理时访问这些外部知识。

---

## 2.3 降低幻觉

LLM 可能根据语言概率生成“看起来正确”的答案。

RAG 的思路是：

```text
不要完全依赖模型记忆
        ↓
给它提供真实上下文
        ↓
要求它基于上下文回答
```

但要注意：

> RAG 只能降低幻觉，不能彻底消灭幻觉。

如果检索错了，模型仍然可能基于错误内容回答。

---

## 2.4 提供来源和证据

很多业务要求答案可以追溯：

```text
这个结论来自哪份文档？
对应哪一页？
对应哪个 URL？
对应哪个 source_id？
```

RAG 可以把检索结果的 metadata 一起返回，最终形成：

```text
答案
+
来源
+
文档 ID
+
URL
+
页码
```

---

# 3. RAG 与大模型本身的关系

一个非常重要的概念：

> **RAG 的 Embedding 模型不需要和生成大模型相同。**

例如：

```text
Embedding：
BGE-M3

Reranker：
bge-reranker-v2-m3

Generator：
Qwen / DeepSeek / GPT / Claude
```

它们职责完全不同。

## 3.1 Embedding 模型

负责：

```text
文本
 ↓
向量
```

用于检索。

## 3.2 Reranker 模型

负责：

```text
Query + Document
 ↓
相关性分数
```

用于重新排序。

## 3.3 LLM

负责：

```text
用户问题 + 检索上下文
 ↓
理解 / 推理 / 生成
```

---

## 3.4 需要保持一致的是谁

建库阶段：

```text
Document
 ↓
Embedding Model A
 ↓
Document Vector
```

查询阶段：

```text
Query
 ↓
Embedding Model A
 ↓
Query Vector
```

通常必须使用同一个 Embedding 模型。

原因是：

> 两边必须位于同一个向量空间中。

即使两个模型输出维度相同，也不能直接混用。

---

# 4. 一套完整 RAG 的总体架构

完整 RAG 可以分为两个阶段：

```text
离线阶段：知识库构建
在线阶段：用户查询
```

---

## 4.1 离线阶段

```text
原始文档
   ↓
Parsing
   ↓
Cleaning
   ↓
Chunking
   ↓
Embedding
   ↓
Index
   ↓
Vector Store / Search Engine
```

---

## 4.2 在线阶段

```text
User Query
   ↓
Query Understanding
   ↓
Query Rewrite
   ↓
Retrieval
   ↓
Hybrid Search
   ↓
Metadata Filter
   ↓
Reranker
   ↓
TopN Context
   ↓
Prompt Builder
   ↓
LLM
   ↓
Answer
   ↓
Citation
```

可以记成一句：

> **文档先变成可检索知识，问题再变成检索请求，最后把最相关证据交给 LLM。**

---

# 5. 离线阶段：知识库构建

离线阶段解决：

> 怎么把原始数据变成未来可以搜索的数据。

例如：

```text
PDF
Word
Markdown
HTML
数据库
CSV
JSON
网页
```

先经过：

```text
Loader / Parser
```

得到统一 Document。

然后：

```text
Document
 ↓
Chunk
 ↓
Embedding
 ↓
Index
```

---

# 6. 文档解析与数据清洗

真实数据往往不是干净文本。

例如 PDF 可能包含：

```text
页眉
页脚
页码
重复标题
表格
乱码
OCR 文本
导航栏
广告
```

如果直接 Embedding：

```text
垃圾输入
 ↓
Embedding
 ↓
垃圾向量
 ↓
检索质量下降
```

所以常见清洗包括：

```text
去除重复页眉页脚
去除无意义空格
统一换行
删除导航文本
保留标题层级
修正编码
结构化 metadata
```

注意：

> RAG 的质量从数据质量开始，而不是从 LLM 开始。

---

# 7. Chunking：文档切块

Chunking 是 RAG 中最重要的基础环节之一。

因为通常不能把整本书直接作为一个向量。

例如：

```text
100 页 PDF
```

需要切成：

```text
Chunk 1
Chunk 2
Chunk 3
...
Chunk N
```

---

## 7.1 为什么必须 Chunk

如果整个文档只有一个向量：

```text
文档里有：
旅游
交通
酒店
天气
美食
政策
```

最终只有一个总体向量。

用户问：

```text
成都地铁怎么买票？
```

整篇文档的向量可能无法准确表达这个局部语义。

Chunk 后：

```text
Chunk A：成都景点
Chunk B：成都交通
Chunk C：成都酒店
Chunk D：成都美食
```

检索可以直接命中：

```text
Chunk B
```

---

## 7.2 Chunk 太大的问题

```text
优点：
上下文完整

缺点：
噪声多
Embedding 表达不够集中
Prompt Token 增加
检索精度可能下降
```

---

## 7.3 Chunk 太小的问题

```text
优点：
语义更加局部

缺点：
上下文被切断
信息不完整
实体关系丢失
回答可能缺乏背景
```

---

## 7.4 Chunk Overlap

为了避免边界信息丢失，经常使用 overlap。

例如：

```text
Chunk 1：
Token 1 ~ 500

Chunk 2：
Token 401 ~ 900
```

其中：

```text
401 ~ 500
```

重复出现在两个 Chunk 中。

如果：

```text
chunk_size = 500
chunk_overlap = 100
```

那么下一块不是从 501 开始，而是从 401 左右开始。

---

## 7.5 常见 Chunk 方法

### 固定长度切分

```text
每 500 Token 一块
```

简单但不理解语义。

### 按句子切分

尽量保持句子完整。

### 按段落切分

适合结构化文档。

### 按标题切分

例如：

```text
# 成都
## 交通
## 景点
## 酒店
```

保持语义结构。

### Semantic Chunking

根据语义变化决定切分位置。

---

# 8. Embedding：文本向量化

Embedding 的作用：

```text
文本
 ↓
Embedding Model
 ↓
Vector
```

例如：

```text
"成都有哪些景点？"
```

可能被编码成：

```text
[0.12, -0.31, 0.88, ..., 0.07]
```

这个向量不是随机数字，而是模型学习出的语义表示。

---

## 8.1 为什么向量可以检索语义

如果：

```text
成都有什么好玩的？
```

和：

```text
成都旅游景点推荐
```

文字并不完全一样。

关键词系统可能认为差异较大。

Embedding 模型会尽量让它们在向量空间里靠近。

因此：

```text
语义相似
 ↓
向量方向相似
 ↓
相似度高
```

---

# 9. 向量相似度计算

## 9.1 Cosine Similarity

最常见的是余弦相似度：

$$
\mathrm{cosine}(q, d)
=
\frac{q \cdot d}
{\lVert q \rVert_2 \lVert d \rVert_2}
$$

其中：

```text
q = Query Vector
d = Document Vector
```

点积：

$$
q \cdot d
=
\sum_{i=1}^{n} q_i d_i
$$

L2 范数：

$$
\lVert q \rVert_2
=
\sqrt{\sum_{i=1}^{n} q_i^2}
$$

如果两个向量已经归一化：

$$
\lVert q \rVert_2 = 1
$$

$$
\lVert d \rVert_2 = 1
$$

那么：

$$
\mathrm{cosine}(q,d) = q \cdot d
$$

所以归一化以后，余弦相似度可以直接转化为内积搜索。

---

## 9.2 Dot Product

内积：

$$
s(q,d)
=
q \cdot d
=
\sum_{i=1}^{n} q_i d_i
$$

值越大，一般认为越相似。

---

## 9.3 Euclidean Distance

欧氏距离：

$$
D(q,d)
=
\sqrt{
\sum_{i=1}^{n}
(q_i-d_i)^2
}
$$

与相似度不同：

```text
距离越小
=
越相似
```

---

# 10. Vector Index / Vector Database

文档向量可能有：

```text
1000 条
10 万条
1000 万条
10 亿条
```

不能每次都用 Python 循环计算所有向量。

所以需要：

```text
Vector Index
```

用于快速找到最近邻。

---

## 10.1 FAISS 是什么

FAISS：

**Facebook AI Similarity Search**

主要解决：

> 大规模向量相似度搜索。

例如：

```text
Query Vector
   ↓
FAISS
   ↓
Nearest Vectors
   ↓
TopK IDs
```

FAISS 不是完整 RAG 框架。

它主要负责：

```text
Vector Search
```

---

## 10.2 Vector Database

常见系统：

```text
Milvus
Qdrant
Weaviate
Pinecone
Chroma
pgvector
Elasticsearch / OpenSearch
```

它们可能同时提供：

```text
向量存储
ANN Search
Metadata Filter
持久化
分布式
权限
Hybrid Search
```

---

# 11. Sparse Retrieval：BM25

Embedding 检索并不是唯一检索方式。

传统搜索领域非常重要的方法：

**BM25**

它属于：

```text
Sparse Retrieval
```

主要依赖关键词统计。

---

## 11.1 TF

Term Frequency：

一个词在文档中出现多少次。

基本思想：

```text
某个词在文档中频繁出现
→ 这个词可能与文档主题相关
```

---

## 11.2 IDF

Inverse Document Frequency：

如果一个词在所有文档里都出现，它的区分能力就低。

常见 IDF 思路：

$$
\mathrm{IDF}(t)
=
\log
\left(
\frac{N+1}{df(t)+1}
\right)
$$

其中：

```text
N     = 文档总数
df(t) = 包含词 t 的文档数量
```

一个词越稀有：

```text
IDF 越大
```

---

## 11.3 BM25 公式

常见 BM25 形式：

$$
\mathrm{BM25}(q,d)
=
\sum_{t \in q}
\mathrm{IDF}(t)
\cdot
\frac{
f(t,d)(k_1+1)
}{
f(t,d)
+
k_1
\left(
1-b+b\frac{|d|}{\mathrm{avgdl}}
\right)
}
$$

其中：

```text
f(t,d)  = 词 t 在文档 d 中的出现次数
|d|     = 当前文档长度
avgdl   = 平均文档长度
k1      = TF 饱和控制参数
b       = 文档长度归一化参数
```

核心思想：

```text
关键词越重要
+
出现越合理
+
文档长度经过归一化
=
BM25 分数越高
```

---

# 12. Dense Retrieval：向量检索

Dense Retrieval 使用神经网络生成稠密向量。

流程：

```text
Document
 ↓
Embedding
 ↓
Document Vector

Query
 ↓
Embedding
 ↓
Query Vector

然后计算相似度
```

Dense Retrieval 的优势：

```text
理解语义
不要求关键词完全一致
跨语言能力较强
能够处理同义表达
```

缺点：

```text
精确 ID
型号
订单号
代码符号
人名
缩写
```

这些场景纯 Dense 可能不如关键词检索。

---

# 13. Hybrid Retrieval：混合检索

现代 RAG 很常见：

```text
BM25
+
Dense Retrieval
```

也就是：

**Hybrid Search / Hybrid Retrieval**

流程：

```text
              ┌→ BM25 → Sparse Results
Query ────────┤
              └→ Dense → Vector Results

                     ↓
                   Fusion
                     ↓
                 Final Rank
```

为什么要融合？

因为两者优势互补。

BM25 擅长：

```text
精确关键词
型号
术语
ID
代码
名称
```

Dense 擅长：

```text
语义
同义词
自然语言表达
跨语言
```

---

# 14. RRF：倒数排名融合

Hybrid Search 常见融合算法：

**Reciprocal Rank Fusion**

简称：

**RRF**

公式：

$$
\mathrm{RRFScore}(d)
=
\sum_{r \in R}
\frac{1}{k + \mathrm{rank}_r(d)}
$$

其中：

```text
R               = 多个检索器结果集合
rank_r(d)       = 文档 d 在检索器 r 中的排名
k               = 平滑常数
```

例如：

```text
BM25：
D1 rank 1
D2 rank 2

Dense：
D2 rank 1
D1 rank 3
```

D1 和 D2 都会从两个检索器获得分数。

RRF 的重要特点：

> 不要求 BM25 分数和 Dense Similarity 分数处于同一个尺度。

因为它主要融合：

```text
排名
```

而不是直接把两个原始分数相加。

---

# 15. TopK、Recall 与噪声之间的关系

TopK：

> 取检索排名前 K 条结果。

例如：

```text
TopK = 5
```

表示：

```text
取最相关的 5 个 Chunk
```

TopK 并不是越大越好。

---

## 15.1 K 太小

可能：

```text
正确文档没有被召回
```

也就是：

```text
Recall 下降
```

---

## 15.2 K 太大

可能：

```text
噪声增加
Prompt 变长
成本增加
LLM 注意力被无关信息分散
```

所以 TopK 的本质是：

> **召回率和上下文噪声之间的平衡。**

---

# 16. Reranker：重排序

Retriever 的任务通常是：

```text
从 100 万文档
 ↓
快速筛选
 ↓
Top50
```

Reranker：

```text
Top50
 ↓
更加精确判断 Query 与 Document 的相关性
 ↓
Top5
```

典型结构：

```text
Query
 ↓
Retriever
 ↓
Top50
 ↓
Reranker
 ↓
Top5
 ↓
LLM
```

---

# 17. Bi-Encoder 与 Cross-Encoder

## 17.1 Bi-Encoder

Retriever 常用 Bi-Encoder。

结构：

```text
Query
 ↓
Encoder
 ↓
Query Vector

Document
 ↓
Encoder
 ↓
Document Vector
```

然后：

```text
Similarity(Query Vector, Document Vector)
```

优势：

```text
Document Vector 可以提前计算
查询速度快
适合大规模召回
```

---

## 17.2 Cross-Encoder

Reranker 常用 Cross-Encoder。

输入：

```text
Query + Document
```

一起送入模型：

```text
[Query, Document]
      ↓
Transformer
      ↓
Relevant Score
```

优点：

```text
Query 和 Document 可以充分交互
相关性判断通常更准
```

缺点：

```text
每个 Query-Document Pair 都需要重新推理
速度慢
```

所以工程上经常使用：

```text
Bi-Encoder
负责 Recall

Cross-Encoder
负责 Precision
```

也就是：

```text
先粗召回
再精排序
```

---

# 18. Metadata Filter

向量相似度不一定能够表达所有业务约束。

例如用户问：

```text
成都适合亲子的景点
```

系统已经知道：

```text
city = 成都
type = attraction
audience = family
```

可以先过滤：

```text
Metadata Filter
```

再做向量检索。

例如：

```text
city == "成都"
category == "景点"
```

优点：

```text
减少候选范围
提高精度
降低检索成本
```

典型 metadata：

```text
source_id
city
category
language
publish_date
document_type
user_id
permission
url
page
```

---

# 19. Query Understanding 与 Query Rewrite

用户输入通常并不是理想搜索词。

例如：

```text
我跟爸妈准备十一出去玩三天，不想太累，
成都附近有什么合适的？
```

直接 Embedding 可以做。

但更高级 RAG 会先理解：

```text
destination = 成都附近
duration = 3 天
audience = parents
preference = low intensity
time = National Day
```

然后生成更适合检索的 Query：

```text
成都周边 三日游 老年人 轻松 景点
```

这就是：

**Query Rewrite**

---

## 19.1 Query Rewrite 解决的问题

```text
口语表达
指代
错别字
信息冗余
查询太长
关键词不足
上下文依赖
```

---

# 20. Multi-Query / Query Decomposition

复杂问题往往不应该只检索一次。

例如：

```text
帮我规划成都三日亲子游，
预算 3000，
需要地铁方便，
还要适合下雨天。
```

可以拆成：

```text
Query 1：成都亲子景点
Query 2：成都地铁交通
Query 3：成都雨天室内景点
Query 4：成都三日游预算
```

分别搜索以后再融合。

这叫：

```text
Query Decomposition
Multi-Query Retrieval
```

这是传统单次 RAG 向 Agentic Retrieval 演进的重要方向。

---

# 21. Context 构建

检索结果不能直接无脑全部拼接。

典型过程：

```text
Retrieved Chunks
 ↓
Deduplication
 ↓
Reranking
 ↓
Filter
 ↓
Compression
 ↓
排序
 ↓
Context
```

需要考虑：

```text
相关性
来源
时间
Token 数量
重复内容
冲突内容
```

---

# 22. Prompt 构建与 Grounding

最终一般会构造：

```text
System Prompt
+
Retrieved Context
+
User Question
```

例如：

```text
你是旅游规划助手。
只能根据提供的 Sources 回答。
如果资料不足，请明确说明。
回答中的事实应尽量附上来源编号。

Sources:
[1] ...
[2] ...
[3] ...

User Question:
...
```

这里最重要的概念：

**Grounding**

也就是：

> 让模型的回答建立在外部证据上，而不是完全依赖参数记忆。

---

# 23. LLM 生成阶段

LLM 输入：

```text
用户问题
+
检索 Context
+
System Prompt
```

输出：

```text
Answer
```

生成阶段主要负责：

```text
理解
综合
推理
总结
格式化
自然语言表达
```

Retriever 负责：

```text
找到证据
```

Generator 负责：

```text
利用证据回答
```

两个模块不要混为一谈。

---

# 24. Citation / Source Attribution

现代 RAG 经常要求：

```text
答案
+
来源
```

来源可能包括：

```text
URL
source_id
document_id
page
chunk_id
title
```

推荐做法不是让 LLM 自己“编 URL”。

而是：

```text
Retriever 返回真实 metadata
        ↓
Context 中携带 source_id / URL
        ↓
LLM 只引用已提供的 source_id
        ↓
系统再映射到真实 URL
```

这样可以减少：

```text
伪造引用
错误链接
来源不存在
```

---

# 25. RAG 的三类主要错误

一个 RAG 答错，不一定是 LLM 的问题。

---

## 25.1 Retrieval Failure

正确资料没有被检索出来。

```text
Query
 ↓
Retriever
 ↓
错误文档
```

此时再强的 LLM 也无法知道正确事实。

---

## 25.2 Context Failure

正确资料被召回了，但：

```text
排序不好
噪声太多
Chunk 不完整
上下文冲突
```

导致 LLM 无法正确使用。

---

## 25.3 Generation Failure

Retriever 已经找对资料。

但是 LLM：

```text
理解错误
推理错误
忽略证据
编造额外信息
```

因此：

> RAG 评测必须把 Retrieval 和 Generation 分开。

---

# 26. RAG 检索指标

## 26.1 Precision@K

前 K 个结果中，有多少是相关结果。

$$
\mathrm{Precision@K}
=
\frac{
\text{TopK 中相关文档数量}
}{
K
}
$$

例如 Top5 中 4 条相关：

$$
\mathrm{Precision@5}
=
\frac{4}{5}
=
0.8
$$

---

## 26.2 Recall@K

所有正确文档中，有多少进入 TopK。

$$
\mathrm{Recall@K}
=
\frac{
\text{TopK 中相关文档数量}
}{
\text{全部相关文档数量}
}
$$

对于很多 QA 数据集，如果每个 Query 只有一个标准相关文档，那么：

```text
正确文档是否进入 TopK
```

就非常直观。

---

## 26.3 Hit Rate@K

至少有一个正确文档进入 TopK：

$$
\mathrm{HitRate@K}
=
\frac{
\text{命中至少一个相关文档的 Query 数量}
}{
\text{Query 总数}
}
$$

---

## 26.4 MRR

MRR：

**Mean Reciprocal Rank**

对每个 Query，看第一个正确文档排名。第一个相关结果，排得有多靠前。

$$
\mathrm{RR}
=
\frac{1}{\mathrm{rank}}
$$

例如：

```text
第一个正确结果排名 1
RR = 1

排名 2
RR = 1/2

排名 5
RR = 1/5
```

整体：

$$
\mathrm{MRR}
=
\frac{1}{N}
\sum_{i=1}^{N}
\frac{1}{\mathrm{rank}_i}
$$

MRR 更关心：

> 正确结果是不是排得足够靠前。

---

## 26.5 DCG

DCG：

**Discounted Cumulative Gain** 排名前面的相关结果价值更高，排得越后，贡献越小。


$$
\mathrm{DCG@K}
=
\sum_{i=1}^{K}
\frac{
2^{rel_i}-1
}{
\log_2(i+1)
}
$$

其中：

```text
rel_i = 第 i 个结果的相关性等级
```

排名越靠前，权重越大。

---

## 26.6 NDCG

NDCG：

**Normalized Discounted Cumulative Gain**
Top-K 检索结果整体排序得好不好，而且越相关的结果越应该排前面。

$$
\mathrm{NDCG@K}
=
\frac{
\mathrm{DCG@K}
}{
\mathrm{IDCG@K}
}
$$

IDCG：

```text
理想排序情况下的 DCG
```

因此：

```text
NDCG 越接近 1
→ 排序越接近理想顺序
```

---

# 27. 生成质量指标

RAG 最终不是只看检索。

还要看答案。

---

## 27.1 Faithfulness

问题：

> 答案中的陈述是否能够被检索 Context 支持？

核心关注：

```text
有没有基于证据
有没有幻觉
```

---

## 27.2 Answer Relevancy

问题：

> 答案是否真正回答用户的问题？

即使答案内容都是真实的，如果偏题：

```text
Answer Relevancy 仍然低
```

---

## 27.3 Context Precision

问题：

> 被检索回来的 Context 中，真正有用的内容比例是多少？

检索大量垃圾：

```text
Context Precision 低
```

---

## 27.4 Context Recall

问题：

> 回答问题需要的关键证据是否都被检索出来？

缺失关键资料：

```text
Context Recall 低
```

---

# 28. End-to-End 指标

生产系统最终还要看：

```text
Task Success
Constraint Satisfaction
Latency
Cost
HTTP Success
Citation Accuracy
User Satisfaction
```

所以一个 RAG 系统可能出现：

```text
Recall@10 很高
```

但是：

```text
最终业务成功率仍然低
```

因为后面可能还有：

```text
规划错误
约束错误
生成错误
接口错误
结构化输出错误
```

---

# 29. RAG 与 Long Context 的关系

Long Context 并没有让 RAG 消失。

如果知识很少：

```text
几十页资料
```

可以直接：

```text
Entire Document
 ↓
LLM Context
```

这时候 RAG 未必必要。

如果知识非常多：

```text
10 万份文档
数百万记录
整个企业知识库
```

不可能全部塞入 Context。

所以：

```text
大量知识
 ↓
Retrieval
 ↓
只选相关内容
 ↓
LLM
```

Long Context 和 RAG 更像互补关系：

```text
Retrieval
负责缩小搜索空间

Long Context
负责一次读取更多相关证据
```

---

# 30. RAG 与 Fine-tuning 的区别

Fine-tuning：

```text
训练阶段
 ↓
修改模型参数
```

RAG：

```text
推理阶段
 ↓
动态获取知识
```

---

## 30.1 Fine-tuning 更适合

```text
改变回答风格
学习格式
学习任务行为
学习结构化输出
领域语言习惯
```

---

## 30.2 RAG 更适合

```text
事实知识
企业私有数据
经常更新的内容
需要引用来源的数据
大量外部知识
```

一句话：

> **Fine-tuning 更偏“教模型怎么做”，RAG 更偏“告诉模型现在需要知道什么”。**

---

# 31. RAG 与 Agent 的关系

传统 RAG：

```text
Query
 ↓
Retrieve
 ↓
LLM
 ↓
Answer
```

Agent：

```text
User
 ↓
Agent
 ↓
决定下一步动作
```

Agent 可以调用：

```text
RAG
Web Search
SQL
Weather API
Map API
Calculator
Code
```

因此：

```text
Agent
=
决策层 / 编排层

RAG
=
知识检索工具
```

---

## 31.1 Agentic RAG

更加现代的方式：

```text
User Question
 ↓
Agent
 ↓
判断是否需要检索
 ↓
Query Rewrite
 ↓
Multi-Query
 ↓
Retrieve
 ↓
检查证据是否足够
 ↓
必要时再次检索
 ↓
Generate
```

这就是：

**Agentic RAG / Agentic Retrieval**

---

# 32. LlamaIndex、FAISS、LangGraph 的区别

这三个特别容易混淆。

---

## 32.1 FAISS

主要解决：

```text
Vector
 ↓
Nearest Neighbor Search
```

属于：

```text
向量索引 / 向量检索组件
```

不是完整 RAG 框架。

---

## 32.2 LlamaIndex

主要负责：

```text
Document
Node / Chunk
Index
Retriever
Metadata
Postprocessor
Reranker
Query Engine
```

属于：

```text
RAG / Data Retrieval Framework
```

你可以理解为：

> **LlamaIndex 管“知识怎么组织、怎么索引、怎么找”。**

---

## 32.3 LangGraph

主要负责：

```text
State
Node
Edge
Condition
Workflow
Retry
Loop
Agent
```

属于：

```text
Agent Workflow Orchestration
```

你可以理解为：

> **LangGraph 管“下一步做什么”。**

---

## 32.4 三者关系

```text
              LangGraph
        Agent Workflow Layer
                 ↓
              retrieve
                 ↓
             LlamaIndex
          Retrieval Layer
                 ↓
      Vector Store / Search
```

例如：

```text
LangGraph：
retrieve → plan → validate

LlamaIndex：
负责 retrieve 内部知识检索

BGE-M3：
负责 Embedding

底层存储：
由具体实现决定
```

---

# 33. 一个现代 RAG 的完整执行链路

下面这条最好记住。

---

## 33.1 数据入库

```text
Documents
 ↓
Parser
 ↓
Cleaning
 ↓
Chunking
 ↓
Metadata
 ↓
Embedding
 ↓
Index
 ↓
Persistent Store
```

---

## 33.2 用户查询

```text
User Query
 ↓
Intent Detection
 ↓
Query Rewrite
 ↓
Metadata Extraction
```

---

## 33.3 检索

```text
              ┌→ BM25
Query ────────┤
              └→ Dense Retrieval

          ↓
      Hybrid Fusion
          ↓
        TopK
```

---

## 33.4 精排

```text
TopK Candidates
 ↓
Reranker
 ↓
TopN
```

---

## 33.5 Context 构建

```text
TopN
 ↓
Deduplicate
 ↓
Filter
 ↓
Context Compression
 ↓
Source Binding
```

---

## 33.6 生成

```text
System Prompt
+
Context
+
Question
 ↓
LLM
 ↓
Answer
```

---

## 33.7 引用

```text
Answer
 ↓
source_id
 ↓
真实 URL / 文档 / 页码
```

---

## 33.8 评测

```text
Retrieval：
Recall@K
MRR
NDCG

Generation：
Faithfulness
Answer Relevancy

System：
Latency
Cost
E2E Success
Constraint Satisfaction
```

---

# 34. 常见优化方向

## 34.1 数据层

```text
清洗数据
去重
改善 OCR
补 metadata
版本控制
```

---

## 34.2 Chunk 层

```text
chunk_size
overlap
semantic chunking
parent-child chunk
标题感知切分
```

---

## 34.3 Embedding 层

```text
更强 Embedding Model
领域微调
归一化
批处理
量化
```

---

## 34.4 Retrieval 层

```text
Dense
BM25
Hybrid
Metadata Filter
Query Rewrite
Multi-Query
```

---

## 34.5 Ranking 层

```text
Cross-Encoder Reranker
LLM Reranker
Rule-based Filter
Time-aware Ranking
```

---

## 34.6 Context 层

```text
去重
压缩
排序
Token Budget
冲突检测
```

---

## 34.7 Generation 层

```text
Grounding Prompt
Structured Output
Citation
Refusal when evidence is insufficient
```

---

## 34.8 Agent 层

```text
Query Planning
Tool Routing
Retry
Reflection
Multi-hop Retrieval
```

---

# 35. 常见误区

## 误区 1：RAG 就是向量数据库

错误。

完整 RAG 包含：

```text
数据处理
Chunk
Embedding
Retrieval
Ranking
Context
Generation
Citation
Evaluation
```

向量数据库只是其中一个组件。

---

## 误区 2：用了 FAISS 就等于用了 RAG 框架

错误。

FAISS 主要负责：

```text
Vector Search
```

---

## 误区 3：RAG 一定需要向量检索

错误。

RAG 可以使用：

```text
BM25
SQL
Knowledge Graph
Web Search
API
Hybrid Retrieval
```

只要是：

```text
先获取外部知识
再辅助生成
```

广义上都属于 Retrieval-Augmented Generation 思路。

---

## 误区 4：TopK 越大越好

错误。

TopK 越大：

```text
Recall 可能增加
```

但：

```text
Noise
Latency
Token Cost
Context Confusion
```

也可能增加。

---

## 误区 5：Embedding 模型必须和 LLM 一样

错误。

真正需要保持一致的是：

```text
Document Embedding
和
Query Embedding
```

---

## 误区 6：RAG 可以彻底消除幻觉

错误。

RAG 可能发生：

```text
检索错
Context 错
LLM 生成错
```

---

## 误区 7：有 Long Context 就不需要 RAG

错误。

少量文档可以不用 RAG。

大规模知识库仍然需要 Retrieval。

---

# 36. 面试总结

如果面试官问：

## 什么是 RAG？

可以回答：

> RAG 是 Retrieval-Augmented Generation，也就是检索增强生成。它把大模型和外部知识库连接起来，用户问题进入系统以后，先通过 BM25、Dense Retrieval 或 Hybrid Search 找到相关文档，再经过 Reranker 精排，把最相关的 Context 放进 Prompt，最后让 LLM 基于这些外部证据生成答案。它主要解决知识更新、私有知识访问、引用溯源和降低幻觉的问题。

---

## 为什么需要 Hybrid Search？

> Dense Retrieval 擅长语义匹配，但对产品型号、ID、专有名词等精确关键词不一定稳定；BM25 擅长词面匹配，但不擅长同义表达，所以工程上常把 BM25 和 Dense Retrieval 结合，再通过 RRF 或其他融合策略合并排名。

---

## Retriever 和 Reranker 有什么区别？

> Retriever 面向大规模语料，目标是快速提高 Recall，一般使用 Bi-Encoder；Reranker 只处理 Retriever 已经筛出的少量候选，用 Query 和 Document 的深层交互重新计算相关性，通常使用 Cross-Encoder，所以精度更高但速度更慢。

---

## LlamaIndex 和 FAISS 有什么区别？

> FAISS 是向量索引和最近邻搜索组件，主要解决向量怎么高效搜索；LlamaIndex 是更高层的 RAG 框架，负责 Document、Node、Index、Retriever、Metadata、Postprocessor 等完整检索流程。FAISS 可以作为某种底层组件，但它本身不等于完整 RAG。

---

## LangGraph 和 LlamaIndex 有什么区别？

> LangGraph 负责 Agent 工作流和状态编排，例如 retrieve、plan、validate；LlamaIndex 负责数据索引和知识检索。所以 LangGraph 管流程，LlamaIndex 管知识。

---

# 37. 最小知识框架

如果要快速复习，只记这一条：

```text
                 RAG

Documents
   ↓
Cleaning
   ↓
Chunking
   ↓
Embedding
   ↓
Index
   ↓
──────────────────────────────
             Query
               ↓
        Query Rewrite
               ↓
       Metadata Filter
               ↓
     BM25 + Dense Search
               ↓
          Hybrid / RRF
               ↓
             TopK
               ↓
           Reranker
               ↓
             TopN
               ↓
        Context Builder
               ↓
            Prompt
               ↓
              LLM
               ↓
            Answer
               ↓
           Citation
               ↓
          Evaluation
```

最终把 RAG 理解成三个问题：

```text
1. 知识怎么存？
2. 问题来了以后怎么找？
3. 找到以后怎么让 LLM 正确使用？
```

再往下拆：

```text
怎么存：
Chunk + Embedding + Index

怎么找：
BM25 + Dense + Hybrid + Reranker

怎么用：
Context + Prompt + Grounding + Citation
```

如果这三层真正理解了，RAG 的基础逻辑就完整了。

---

# 附：RAG 核心公式速查

## Cosine Similarity

$$
\mathrm{cosine}(q, d)
=
\frac{q \cdot d}
{\lVert q \rVert_2 \lVert d \rVert_2}
$$

## Dot Product

$$
q \cdot d
=
\sum_{i=1}^{n} q_i d_i
$$

## Euclidean Distance

$$
D(q,d)
=
\sqrt{
\sum_{i=1}^{n}
(q_i-d_i)^2
}
$$

## IDF

$$
\mathrm{IDF}(t)
=
\log
\left(
\frac{N+1}{df(t)+1}
\right)
$$

## BM25

$$
\mathrm{BM25}(q,d)
=
\sum_{t \in q}
\mathrm{IDF}(t)
\cdot
\frac{
f(t,d)(k_1+1)
}{
f(t,d)
+
k_1
\left(
1-b+b\frac{|d|}{\mathrm{avgdl}}
\right)
}
$$

## RRF

$$
\mathrm{RRFScore}(d)
=
\sum_{r \in R}
\frac{1}{k + \mathrm{rank}_r(d)}
$$

## Precision@K

$$
\mathrm{Precision@K}
=
\frac{
\text{TopK 中相关文档数量}
}{
K
}
$$

## Recall@K

$$
\mathrm{Recall@K}
=
\frac{
\text{TopK 中相关文档数量}
}{
\text{全部相关文档数量}
}
$$

## MRR

$$
\mathrm{MRR}
=
\frac{1}{N}
\sum_{i=1}^{N}
\frac{1}{\mathrm{rank}_i}
$$

## DCG

$$
\mathrm{DCG@K}
=
\sum_{i=1}^{K}
\frac{
2^{rel_i}-1
}{
\log_2(i+1)
}
$$

## NDCG

$$
\mathrm{NDCG@K}
=
\frac{
\mathrm{DCG@K}
}{
\mathrm{IDCG@K}
}
$$

---

**一句话总复习：**

> RAG 的本质是 Retrieval + Context + Generation：先从外部知识中找对证据，再把最相关证据交给 LLM，让模型基于证据回答，并通过检索指标、生成指标和端到端业务指标分别评估整条链路。
