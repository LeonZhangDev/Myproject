# 张坤

**求职方向：AI 算法工程师 / 大模型应用 / RAG / Agent**

**电话：** 待填写　|　**邮箱：** 待填写　|　**所在地：** 待填写  
**学历：** 硕士　|　**英语：** IELTS Academic 6.5　|　**GitHub / Gitee：** 待填写

---

# 教育经历

**2024.06-2026.02  Taylor's University（泰莱大学） | School of Computer Science | 应用计算硕士（人工智能方向）**

参与人工智能、深度学习与序列建模相关学习与研究，重点围绕自动音乐生成、多模态学习及模型评测开展课程与毕业课题实践。

1. **硕士论文：** Automatic Music Generation and Key Standardization Using LSTM，围绕音乐调性标准化与自动音乐生成展开研究，采用 C 调统一、Octuple 音乐表示、LSTM + Attention 及 Temperature Sampling 完成序列建模与生成。
2. **课程实践：** 完成深度学习、NLP 与多模态相关课程项目，包括基于 BLIP + XLM-RoBERTa 的 CrisisMMD 灾害信息识别，具备 PyTorch 模型训练、实验设计、指标评测及 Bad Case 分析经验。
3. **语言能力：** IELTS Academic 6.5。

**2019.09-2023.06  四川大学网络教育学院 | 计算机科学与技术 | 本科**

系统学习计算机科学基础课程，逐步从通用软件开发转向人工智能、后端工程与模型部署方向。

1. **核心课程：** C 语言程序设计、数据结构、操作系统、数据库原理、计算机网络、面向对象程序设计等。
2. **专业基础：** 建立程序设计、数据结构、数据库、网络及操作系统等计算机基础，为后续 Python 后端、AI 模型训练、RAG 与模型部署提供基础。

**2013.09-2018.06  四川托普信息技术职业学院 | 电子商务 | 大专**

学习电子商务与计算机应用相关课程，接触网站建设、网页设计及互联网应用，为后续转向计算机科学与软件开发方向积累基础。

1. **核心课程：** 电子商务、计算机应用、网站建设、网页设计、网络营销等。
2. **学习方向：** 建立早期 Web 与互联网应用基础，后续通过本科阶段进一步系统学习计算机科学核心课程。

# 项目经历

**MindTrip 智旅 | RAG + Agent 智能旅行规划系统 | 核心开发**

围绕多约束旅行规划场景构建 RAG + Agent 系统，负责知识检索、Agent 工作流、结构化规划、模型服务及评测优化，实现从自然语言需求到可验证旅行方案的生成链路。

1. **RAG 检索：** 基于 LlamaIndex 搭建独立 RAG 服务，使用 BGE-M3 召回与 BGE-Reranker-v2-m3 精排，并支持版本化索引、缓存及 source_id 证据追踪；351 条离线检索测试中 Recall@5 达 **98.01%**、MRR@10 达 **92.04%**、P95 检索延迟 **31 ms**。
2. **Agent 规划：** 基于 LangGraph 搭建 Retrieve → Plan → Validate 工作流，通过 Pydantic TripPlan 定义结构化输出，并加入时间、交通、预算等确定性规则校验，降低大模型约束遗漏与格式漂移。
3. **评测迭代：** 建立真实 HTTP Agent Eval，完成 **200 条独立本机 HTTP 请求评测**，围绕首次业务成功、最终任务成功、Constraint Satisfaction 与 Repair 等指标归纳 Bad Case，持续优化规划和校验链路。

**AtlasSplit | LLM 表格分摊智能体 | 核心开发**

围绕财务及运营报表中的自然语言分摊需求构建表格智能体，将自然语言规则转换为结构化执行计划，并通过受限执行、校验和审计机制提升自动化分摊的可靠性与可追踪性。

1. **规则规划：** 将自然语言分摊规则转换为结构化 AllocationPlan / DSL，明确筛选条件、分摊维度、权重、金额计算及输出要求，并使用 Pydantic Schema 对模型结果进行约束。
2. **安全执行：** 采用确定性 Pandas / openpyxl 执行链路，并结合 AST 静态检查、受限执行模式及 SHA-256 审计信息，对输入、计划、执行结果和产物进行可追踪记录。
3. **评测迭代：** 基于 **200 条真实业务任务**构建端到端评测，通过 Bad Case 复盘定位 Schema、规则理解和复杂分摊语义问题，并持续优化结构化生成、Repair 与执行链路。

# 专业技能

1. **大模型与 RAG：** 熟悉 LlamaIndex、LangGraph、RAG、Dense Retrieval、Reranker、Query Rewrite、Agent Workflow、Tool Calling、结构化输出与 AI Eval。
2. **深度学习：** 熟悉 PyTorch、LSTM、Transformer、Attention、CTC、GAN / CycleGAN、BLIP、XLM-RoBERTa、YOLO 等模型与训练流程。
3. **模型部署：** 熟悉 vLLM、ONNX Runtime、TensorRT、模型量化与本地 GPU 推理优化，具备 FastAPI / SSE / WebSocket 模型服务经验。
4. **后端与数据：** 熟悉 Python、FastAPI、Django、MySQL、PostgreSQL、Redis、FAISS、Neo4j、Docker、Git。
