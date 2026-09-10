# RAG与向量检索

> 共 15 题

## Q01｜RAG 解决了纯大模型的哪些问题？

- **难度**：⭐
- **题目来源**：[GitHub｜AI Engineer Interview Questions - RAG](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/04-rag-and-retrieval/questions.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

RAG 最大的价值是给模型接了一个‘外部资料库’。纯 LLM 的知识会过时，也看不到企业私有数据；RAG 可以在回答前先把相关资料找出来，再让模型基于这些证据回答，所以知识能更新、答案能带来源，也能减少一部分凭空编造。注意我会说‘减少’，不会说完全消灭幻觉。

> **记忆钩子：** LLM 像闭卷考试；RAG 是先允许它查资料再答。

---

## Q02｜一个生产级 RAG 的完整链路是什么？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜AI Engineer Interview Questions (atryx)](https://github.com/atryx/ai-engineer-interview-questions)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

我会把生产级 RAG 分成离线和在线两条链。离线是文档解析、清洗、切块、Embedding、建索引；在线是 Query 处理、召回、过滤或混合检索、Rerank、拼上下文、交给 LLM 生成，最后再做引用和评测。面试里只说‘向量库+LLM’通常太粗，因为真正影响效果的环节都在中间。

> **记忆钩子：** 记成两段：资料先入库；问题来了再“找→排→拼→答”。

---

## Q03｜为什么不能简单把整篇文档直接做一个 embedding？

- **难度**：⭐
- **题目来源**：[GitHub｜AI Engineer Interview Questions - RAG](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/04-rag-and-retrieval/questions.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

整篇文档只做一个 embedding，最容易出现的问题是语义被‘平均掉’。一篇几十页文档可能同时讲很多主题，最后只剩一个向量，检索时很难精准命中某个细节。而且真召回后整篇都塞给 LLM，也浪费上下文。所以一般要切成合适粒度，让每个 chunk 尽量语义完整又足够具体。

> **记忆钩子：** 一本书不能只贴一个标签就指望找到其中某句话。

---

## Q04｜Chunk Size 和 Overlap 应如何权衡？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜RAG Interview Questions and Answers Hub](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub/blob/main/README.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

Chunk Size 没有一个万能数字，我会看‘信息完整性’和‘检索精度’之间的平衡。太小，句子被切碎，证据不完整；太大，又容易混进很多无关内容。Overlap 是为了防止关键语义正好被切在边界上，但重叠太多会导致索引膨胀、重复召回。所以一般会结合数据集做实验，而不是死背 500 token。

> **记忆钩子：** 块太小会断句，块太大会夹杂；Overlap 是保险，但保险买太多也贵。

---

## Q05｜BM25 和向量检索各自擅长什么？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜AI Engineer Interview Questions - RAG](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/04-rag-and-retrieval/questions.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

BM25 和向量检索其实不是谁替代谁。BM25 对专有名词、编号、产品名、数字这类精确词特别敏感；向量检索擅长‘说法不一样但意思一样’的语义匹配。所以生产里常把两者混起来做 Hybrid Retrieval，再统一排序。

> **记忆钩子：** BM25 找“字面像”，向量找“意思像”。

---

## Q06｜为什么初次召回后还需要 Reranker？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜RAG Interview Questions and Answers Hub](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub/blob/main/README.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

第一阶段召回的目标是别漏，所以通常会多拿一些候选；但‘召回来’不等于‘最相关’。Reranker 会拿 query 和候选文档做更细的交叉匹配，把真正相关的排到前面。可以理解成向量检索是海选，Reranker 是复试。

> **记忆钩子：** Retriever 负责别漏人；Reranker 负责把最合适的人排前面。

---

## Q07｜Top-k 取值太大或太小分别有什么问题？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜AI Engineer Interview Questions - RAG](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/04-rag-and-retrieval/questions.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

Top-k 太小，风险是关键证据根本没进上下文；太大又会把噪声、重复内容一起塞给模型，token 成本和延迟都上升，甚至让模型被错误材料带偏。所以我通常不是单独调 k，而是结合召回率、Reranker、上下文预算和最终答案指标一起看。

> **记忆钩子：** k 小怕漏，k 大怕吵。

---

## Q08｜Cosine Similarity、Dot Product、Euclidean Distance 有什么区别？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜RAG Interview Questions and Answers Hub](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub/blob/main/README.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

我会先看 embedding 模型是怎么训练的。Cosine 更关注方向，常见做法是先归一化后比较语义方向；Dot Product 还会受向量模长影响；Euclidean 是直接看空间距离。很多时候向量归一化以后，Cosine 和 Dot Product 的排序会非常接近，所以关键不是背公式，而是保证检索度量和模型训练方式一致。

> **记忆钩子：** Cosine 看方向，Dot 看方向+大小，Euclidean 看两点离多远。

---

## Q09｜长上下文模型出现后，RAG 还有必要吗？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜RAG Interview Questions and Answers Hub](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub/blob/main/README.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

长上下文能塞更多东西，但它并没有替你解决‘该塞什么’。如果企业知识每天变化、文档有权限、上下文很贵、还要给引用来源，RAG 依然很有价值。甚至上下文越长，噪声越多时，检索和排序反而更重要。所以长上下文更像扩大桌面，不代表你就不用整理资料。

> **记忆钩子：** 上下文窗口变大只是桌子更大，不等于桌上所有文件都该摊开。

---

## Q010｜RAG 怎么降低幻觉？为什么不能完全消除？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜RAG Interview Questions and Answers Hub](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub/blob/main/README.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

RAG 降幻觉的逻辑是先给模型事实证据，再要求它基于证据回答。但如果第一步检索就找错了，或者几段资料互相冲突，甚至模型拿到正确证据却没遵守，还是会胡说。所以生产里还要做引用、grounding 校验、拒答策略和评测。

> **记忆钩子：** RAG 能给模型参考书，但参考书拿错了，照样会答错。

---

## Q011｜RAG 知识库如何做到不停服更新？

- **难度**：⭐⭐⭐
- **题目来源**：[牛客｜阿里/蚂蚁/字节 Agent 开发面经总结](https://www.nowcoder.com/discuss/877151327091027968)
- **来源类型**：真实面经
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

我不会直接在正在服务的索引上做一堆危险修改。更稳的方式是后台构建新版本索引，验证通过后做原子切换，类似蓝绿发布；小规模变化也可以增量更新，但要维护版本和一致性。关键是用户的一次查询最好读到同一版本，不要查一半切到新索引。

> **记忆钩子：** 把知识库更新当成发版：后台建新版本，验证完再切流量。

---

## Q012｜如何定位 RAG 的问题到底出在检索还是生成？

- **难度**：⭐⭐⭐
- **题目来源**：[GitHub｜Awesome AI Engineer Interview 2026](https://github.com/landedjobs/awesome-ai-engineer-interview)
- **来源类型**：真实面经汇总/题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

我会把 RAG 拆开测，不然很容易‘全链路差但不知道谁背锅’。先看检索有没有把正确证据找回来，比如 Recall@k、MRR、Rerank 排名；然后我会人为把正确上下文直接喂给 LLM。如果这时候仍然答错，那问题主要在生成；如果给对上下文就能答对，那就先修检索。

> **记忆钩子：** 先问“资料找对没”，再问“拿到对资料后会不会答”。

---

## Q013｜Query Rewrite 为什么能提升 RAG？

- **难度**：⭐⭐
- **题目来源**：[GitHub｜AI Engineer Interview Questions - RAG](https://github.com/ombharatiya/AI-Engineer-Interview-Questions/blob/main/04-rag-and-retrieval/questions.md)
- **来源类型**：公开题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

用户的问题往往不是天然适合搜索的，比如‘它支持吗？’里面连‘它’是谁都没说清楚。Query Rewrite 会结合上下文补全实体、去掉歧义，或者把口语问题改成更适合检索的表达。它本质上不是让问题变漂亮，而是让后面的 Retriever 更容易找到正确证据。

> **记忆钩子：** 用户说人话，检索器更喜欢搜索话；Rewrite 就是翻译这一层。

---

## Q014｜如何处理多跳问题（Multi-hop QA）？

- **难度**：⭐⭐⭐
- **题目来源**：[GitHub｜Awesome AI Engineer Interview 2026](https://github.com/landedjobs/awesome-ai-engineer-interview)
- **来源类型**：真实面经汇总/题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

多跳问题通常不是一次检索能解决的。比如先要找 A 属于哪个公司，再基于公司去查某项政策。我会把复杂问题拆成几个子问题，每一步检索得到的新证据继续作为下一步输入，最后再汇总。如果路径比较动态，可以用 Agent 或 LangGraph 控制多轮检索。

> **记忆钩子：** 多跳题别想着一步跳到终点，要一站一站拿证据。

---

## Q015｜RAG 的核心评测指标有哪些？

- **难度**：⭐⭐⭐
- **题目来源**：[GitHub｜Awesome AI Engineer Interview 2026](https://github.com/landedjobs/awesome-ai-engineer-interview)
- **来源类型**：真实面经汇总/题单
- **掌握情况**：较模糊

### 自测
- [ ] 我能在 30 秒内先给出结论
- [ ] 我能继续解释原理/权衡
- [ ] 我能结合项目或代码举例

### 参考答案

**面试时可以这样答：**

RAG 评测我一定会分检索侧和生成侧。检索侧关心正确文档有没有被找回来、排得靠不靠前，所以看 Recall@k、MRR、nDCG；生成侧关心答案是不是基于上下文、是否回答了问题，可以看 Faithfulness、Answer Relevance、Context Relevance。最后最好再配人工抽检，因为自动指标不等于业务满意度。

> **记忆钩子：** 检索评测看“找得对不对”，生成评测看“拿到资料后答得好不好”。

---
