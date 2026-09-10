# 用户输入侧 RAG 方案与实现技术报告

## 1. 报告目标

这份报告只回答两个问题：

1. 用户输入进入 RAG 前，目前有哪些值得使用的处理方案？
2. 这些方案在 MindTrip 当前架构中具体应该怎样实现？

不再展开 BM25、MRR、nDCG、Recall 等基础理论与评测公式。

---

# 2. MindTrip 当前推荐基础架构

当前建议保持以下职责划分：

```text
用户
 ↓
FastAPI
 ↓
LangGraph
 ├─ Query Understanding
 ├─ Query Routing
 ├─ Retrieval Strategy
 ├─ Plan
 └─ Validate
 ↓
LlamaIndex RAG Service
 ├─ Dense Retrieval
 ├─ Sparse Retrieval
 ├─ Metadata Filter
 ├─ Fusion
 └─ Reranker
 ↓
BGE-M3 / BGE Reranker
 ↓
Evidence
 ↓
LLM
```

其中：

```text
LangGraph
=
决定“该怎么检索”

LlamaIndex
=
真正执行“检索”
```

所有下面介绍的方案，都建立在同一个 Retrieval Backend 上：

```text
Dense Retrieval
+
Sparse Retrieval
+
Metadata Filter
+
Fusion
+
Reranker
```

---

# 3. 方案一：Contextual Query Rewrite

## 3.1 解决什么问题

用户输入经常存在：

- 指代
- 省略
- 口语表达
- 上下文依赖
- 搜索关键词不明确

例如：

```text
第一轮：
我想去四姑娘山。

第二轮：
那里两天够吗？
```

如果直接检索：

```text
那里两天够吗？
```

检索器并不知道“那里”指的是四姑娘山。

所以先转换成：

```text
四姑娘山两日旅行是否可行？
```

---

## 3.2 实现流程

```text
User Query
+
最近若干轮 Conversation History
        ↓
Query Rewrite LLM
        ↓
Standalone Query
        ↓
LlamaIndex Retrieval
```

---

## 3.3 LangGraph 中增加节点

增加：

```text
contextualize_query
```

输入：

```python
state["user_query"]
state["chat_history"]
```

输出：

```python
state["standalone_query"]
```

Graph：

```text
START
 ↓
contextualize_query
 ↓
retrieve
 ↓
plan
 ↓
validate
```

---

## 3.4 推荐输出结构

不要让模型只输出一段自然语言。

使用 Pydantic：

```python
class RewrittenQuery(BaseModel):
    original_query: str
    standalone_query: str
    changed: bool
```

例如：

```json
{
  "original_query": "那里两天够吗？",
  "standalone_query": "四姑娘山两日旅行是否可行？",
  "changed": true
}
```

---

## 3.5 Prompt 核心要求

Prompt 必须明确：

```text
你的任务不是回答问题，而是生成一个适合知识检索的独立查询。

要求：
1. 解析聊天历史中的指代。
2. 保留地点。
3. 保留时间。
4. 保留预算。
5. 保留人数。
6. 保留否定条件。
7. 不添加原问题不存在的事实。
8. 不直接回答问题。
```

---

## 3.6 什么时候使用

适合：

```text
“那个地方怎么样？”
“刚才说的景点几点关门？”
“如果改成两天呢？”
“那里适合老人吗？”
```

不建议简单问题每次都 Rewrite。

例如：

```text
九寨沟在哪里？
```

可以直接 Retrieval。

---

# 4. 方案二：Multi-Query Retrieval

## 4.1 解决什么问题

单个 Query 可能只能覆盖用户需求的一个表达方向。

例如：

```text
成都三天怎么玩？
```

可以扩展成：

```text
成都三日经典旅游路线
成都三日历史文化景点
成都三日休闲低强度路线
成都三日特色美食和景点
```

不同 Query 分别检索，可以扩大召回范围。

---

# 4.2 实现流程

```text
User Query
 ↓
Query Generator
 ↓
Q1
Q2
Q3
 ↓
并行 Retrieval
 ↓
Result Fusion
 ↓
Deduplicate
 ↓
Reranker
 ↓
Top-K Evidence
```

---

## 4.3 LangGraph 实现

增加：

```text
generate_queries
```

输出：

```python
state["retrieval_queries"]
```

例如：

```python
[
    "成都三日经典旅游路线",
    "成都三日历史文化景点推荐",
    "成都三日低强度休闲旅游路线",
]
```

然后：

```text
multi_retrieve
```

对这些 Query 并行调用 LlamaIndex RAG Service。

---

## 4.4 LlamaIndex 服务接口

可以让 RAG 服务支持：

```json
POST /retrieve
{
  "queries": [
    "成都三日经典旅游路线",
    "成都三日历史文化景点推荐"
  ],
  "filters": {
    "city": "成都"
  },
  "top_k": 15
}
```

服务内部：

```text
for query in queries:
    dense_search(query)
    sparse_search(query)

所有结果
 ↓
Fusion
 ↓
Deduplicate
 ↓
Rerank
```

---

## 4.5 Query 数量

第一版建议：

```text
2~3 个 Query
```

不要默认生成：

```text
5~10 个 Query
```

因为会线性增加：

- Embedding
- Search
- Fusion
- Reranking
- Latency

---

## 4.6 什么时候使用

适合：

```text
推荐类问题
开放式问题
需求比较模糊的问题
需要扩大召回范围的问题
```

例如：

```text
成都有什么适合年轻人的地方？
川西秋天有什么值得去的？
上海周末怎么玩？
```

---

# 5. 方案三：HyDE

HyDE：

```text
Hypothetical Document Embeddings
```

---

## 5.1 解决什么问题

有时候用户问题和知识库文档的语言差异很大。

例如：

```text
哪里适合秋天看蓝色的高原湖？
```

知识库中可能不会出现这句话。

HyDE 先让 LLM 生成一段“可能长得像知识库文档”的文本：

```text
川西地区秋季具有多个高原湖泊景观，
部分湖泊在九月至十月具有较高观赏价值……
```

然后拿这段文本做 Embedding。

---

## 5.2 实现流程

```text
User Query
 ↓
LLM
 ↓
Hypothetical Document
 ↓
BGE-M3 Embedding
 ↓
Dense Retrieval
 ↓
Reranker
```

---

## 5.3 LangGraph 节点

增加：

```text
hyde_transform
```

输入：

```python
state["standalone_query"]
```

输出：

```python
state["hyde_document"]
```

然后传给：

```text
retrieve
```

---

## 5.4 推荐使用方式

不要默认：

```text
所有 Query
→ HyDE
```

推荐把它作为：

```text
Retrieval Fallback
```

即：

```text
正常 Retrieval
 ↓
检索质量低
 ↓
HyDE
 ↓
再次 Retrieval
```

Graph：

```text
retrieve
 ↓
retrieval_gate
 ├─ pass → plan
 └─ fail → hyde_transform
             ↓
          retrieve_retry
```

---

## 5.5 为什么只做 Fallback

因为 HyDE 的 hypothetical document 是 LLM 生成的。

如果模型一开始理解错用户意图：

```text
Wrong Hypothesis
 ↓
Wrong Embedding
 ↓
Wrong Retrieval
```

所以不应该把 HyDE 放在默认主链路。

---

# 6. 方案四：Query Decomposition

## 6.1 解决什么问题

复杂问题通常包含多个独立问题。

例如：

```text
成都出发去四姑娘山三天，
预算2500，
不自驾，
比较高铁加大巴和纯大巴，
同时帮我安排三天路线。
```

一次 Retrieval 很难同时得到：

- 交通
- 价格
- 时间
- 景点
- 行程
- 预算

所以应该拆成多个 Sub-Query。

---

# 6.2 拆解结果

例如：

```text
Q1：
成都到四姑娘山有哪些公共交通方式？

Q2：
成都到四姑娘山的大巴时间和费用是多少？

Q3：
四姑娘山三日游适合安排哪些景点？

Q4：
2500 元预算是否能够覆盖三日行程？
```

---

# 6.3 实现流程

```text
Complex Query
 ↓
Query Decomposer
 ↓
Q1 Q2 Q3 Q4
 ↓
Parallel Retrieval
 ↓
Evidence Pool
 ↓
Fusion
 ↓
Reranker
 ↓
Final Evidence
 ↓
Planner
```

---

## 6.4 LangGraph 节点

增加：

```text
decompose_query
```

输出：

```python
state["subqueries"]
```

结构：

```python
class SubQuery(BaseModel):
    id: str
    query: str
    purpose: str
```

例如：

```json
[
  {
    "id": "transport",
    "query": "成都到四姑娘山公共交通方式",
    "purpose": "交通方案"
  },
  {
    "id": "attractions",
    "query": "四姑娘山三日游景点安排",
    "purpose": "景点安排"
  }
]
```

---

## 6.5 检索

每个 Sub-Query：

```text
SubQuery
 ↓
Dense + Sparse Retrieval
 ↓
Top Candidates
```

所有 Sub-Query Result：

```text
Results(Q1)
+
Results(Q2)
+
Results(Q3)
 ↓
Fusion
 ↓
Deduplicate
 ↓
Reranker
```

---

## 6.6 限制数量

建议：

```text
subqueries <= 4
```

第一版甚至可以：

```text
subqueries <= 3
```

防止：

```text
复杂问题
→ 10 个子问题
→ 20 次 Retrieval
```

造成延迟爆炸。

---

# 7. 方案五：Adaptive Query Routing

这是最推荐最终实现的方案。

它不是一个新的 Retrieval 算法。

它解决的问题是：

> 到底什么时候使用上面的 Rewrite、Multi-Query、Decomposition？

---

## 7.1 核心结构

用户输入首先经过：

```text
Query Analyzer
```

输出：

```text
simple
normal
complex
```

然后：

```text
simple
→ Direct Retrieval

normal
→ Rewrite / Multi-Query

complex
→ Decomposition
```

---

# 7.2 推荐 QueryPlan

```python
class QueryPlan(BaseModel):
    original_query: str
    standalone_query: str

    intent: str

    complexity: str

    need_retrieval: bool
    strategy: str

    semantic_query: str

    filters: dict

    expanded_queries: list[str]
    subqueries: list[str]
```

---

## 7.3 示例

用户：

```text
成都三天两个人，
预算3000，
不想太累，
喜欢古建筑。
```

输出：

```json
{
  "original_query": "成都三天两个人，预算3000，不想太累，喜欢古建筑",
  "standalone_query": "成都两人三日低强度历史文化旅行规划",
  "intent": "trip_planning",
  "complexity": "complex",
  "need_retrieval": true,
  "strategy": "decompose",
  "semantic_query": "成都低强度历史文化古建筑旅游景点",
  "filters": {
    "city": "成都",
    "days": 3,
    "travelers": 2,
    "budget": 3000
  },
  "expanded_queries": [],
  "subqueries": []
}
```

---

# 7.4 Router

LangGraph：

```python
def route_query(state):
    strategy = state["query_plan"].strategy

    if strategy == "direct":
        return "simple_retrieve"

    if strategy == "rewrite":
        return "rewrite_query"

    if strategy == "multi_query":
        return "generate_queries"

    if strategy == "decompose":
        return "decompose_query"
```

---

# 7.5 推荐第一版规则

不需要一开始训练 classifier。

直接让 LLM 做 Structured Output。

规则：

```text
simple：
单实体
单事实
单目标

normal：
存在指代
表达模糊
推荐类问题
需要多个搜索表达

complex：
多个约束
多个目标
比较
规划
多跳推理
```

例如：

```text
九寨沟在哪里？
→ simple

那里适合老人吗？
→ normal

成都去四姑娘山三天，
比较两种交通方案并规划路线
→ complex
```

---

# 9. MindTrip 最终推荐实现

建议最终 Graph：

```text
START
  │
  ▼
understand_query
  │
  ▼
route_query
  │
  ├──────── simple ────────┐
  │                        │
  │                simple_retrieve
  │                        │
  ├──────── normal ────────┤
  │                        │
  │                rewrite_query
  │                        │
  │                multi_query
  │                        │
  └──────── complex ───────┤
                           │
                    decompose_query
                           │
                           ▼
                       retrieve
                           │
                           ▼
                        rerank
                           │
                           ▼
                    retrieval_gate
                      │         │
                    pass       fail
                      │         │
                      │   corrective_rewrite
                      │         │
                      │       retrieve
                      │         │
                      │       HyDE
                      │
                      ▼
                     plan
                      │
                      ▼
                   validate
                      │
                      ▼
                     END
```

---

# 11. 推荐实际开发顺序

不要一次全部开发。

## 第一阶段

先实现：

```text
Contextual Query Rewrite
```

增加：

```text
contextualize_query.py
```

完成：

```text
History
+
User Query
→
Standalone Query
```

---

## 第二阶段

实现：

```text
Structured Query Understanding
```

增加：

```text
query_analyzer.py
```

输出：

```text
intent
complexity
semantic_query
filters
strategy
```

---

## 第三阶段

实现：

```text
Adaptive Router
```

增加 LangGraph conditional edge：

```text
direct
rewrite
multi_query
decompose
```

---

## 第四阶段

实现：

```text
Query Decomposition
```

优先支持 MindTrip 最重要的复杂旅行规划 Query。

例如：

```text
交通
景点
住宿
预算
```

---

## 第五阶段

加入：

```text
Multi-Query
```

只给 recommendation / broad search 类问题使用。

---

## 第六阶段

增加：

```text
Retrieval Quality Gate
+
Corrective Rewrite
```

让系统第一次检索失败后可以自己恢复。

---

## 第七阶段

最后增加：

```text
HyDE
```

作为低召回情况下的最后一级知识库检索 fallback。

---

# 12. 推荐代码目录

建议在现有项目增加：

```text
app/
├── agent/
│   ├── graph.py
│   ├── state.py
│   │
│   └── nodes/
│       ├── understand_query.py
│       ├── rewrite_query.py
│       ├── generate_queries.py
│       ├── decompose_query.py
│       ├── route_query.py
│       ├── retrieve.py
│       ├── retrieval_gate.py
│       ├── corrective_rewrite.py
│       ├── plan.py
│       └── validate.py
│
├── schemas/
│   ├── query_plan.py
│   └── retrieval.py
│
└── clients/
    └── rag_client.py
```

独立 LlamaIndex 服务：

```text
rag-service/
├── api/
│   └── retrieve.py
│
├── retrievers/
│   ├── dense.py
│   ├── sparse.py
│   ├── hybrid.py
│   └── fusion.py
│
├── rerankers/
│   └── bge_reranker.py
│
└── schemas/
    └── retrieval.py
```

---

# 13. 最终推荐

MindTrip 不建议选择单独某一种 Query 方法。

推荐组合是：

```text
Adaptive Routing
+
Contextual Query Rewrite
+
Query Decomposition
+
按需 Multi-Query
+
Corrective Retrieval
+
HyDE Fallback
```

底层统一使用：

```text
LlamaIndex
+
BGE-M3 Hybrid Retrieval
+
BGE Reranker
```

最核心的运行逻辑：

```text
用户输入
 ↓
理解问题
 ↓
判断问题复杂度
 ↓
选择检索策略
 ↓
执行检索
 ↓
检查检索质量
 ↓
必要时自动重试
 ↓
将可靠 Evidence 交给 Planner / LLM
```

这比固定：

```text
User Query
→ Rewrite
→ RAG
```

更适合实际工程系统。

最终的目标不是“实现更多 RAG 技术”，而是让系统能够：

> 根据不同用户输入，自动决定最合适的检索方式。
