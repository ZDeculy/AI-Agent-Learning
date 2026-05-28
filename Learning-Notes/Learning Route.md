# AI Agent Route

## 总目标

构建一个面向科研场景的 **PV Research Agent**，系统学习并打通：

**LLM API → Tool Calling → Agent Loop → RAG → Memory → Workflow → Skills → Evaluation → Deployment → Git/Open-source Collaboration**

最终目标不是只会调用 API，而是能够：

* 从零实现一个 mini-agent；

* 理解 Agent 的完整回答链路；

* 构建本地 PV Research Agent；

* 给成熟 Code Agent 写 skills；

* 搭建 skill evaluation framework；

* 用 Git 管理项目并参与开源完善。

***

# 0. 前置基础层：开发环境与工程习惯

## 0.1 本地开发环境

### 学习目标

建立稳定的 Mac 本地开发环境，为后续 Agent 项目开发做准备。

### Key Words

* macOS development

* Homebrew

* Terminal

* Warp / iTerm2

* zsh / fish

* tmux

* neovim

* VS Code / Cursor / Codex

* Python environment

* uv / conda / venv

* pip

* pyproject.toml

* requirements.txt

* .env

* API key management

### 应掌握内容

* 如何创建 Python 虚拟环境；

* 如何管理依赖；

* 如何配置 `.env`；

* 如何在终端中运行 Python 项目；

* 如何组织一个基础项目目录；

* 如何阅读报错和日志。

***

## 0.2 Git 与开源协作

### 学习目标

掌握项目管理、版本控制和开源贡献基本流程。

### Key Words

* Git

* GitHub

* repository

* commit

* branch

* merge

* rebase

* pull request

* issue

* fork

* clone

* remote

* origin

* .gitignore

* README.md

* LICENSE

* semantic commit

* code review

### 应掌握内容

* 初始化 Git 仓库；

* 提交代码；

* 创建分支；

* 回滚修改；

* 解决冲突；

* 阅读 GitHub 开源项目；

* 提交 issue；

* 提交 pull request；

* 编写 README。

***

# 1. LLM API 基础层

## 1.1 大模型交互基础

### 学习目标

理解“程序如何和大模型通信”。

### Key Words

* LLM

* API

* SDK

* client

* request

* response

* model

* prompt

* system prompt

* user message

* assistant message

* messages array

* input

* output

* token

* context window

* temperature

* max tokens

* streaming

### 应掌握内容

* API 调用的基本结构；

* system / user / assistant 的区别；

* messages 数组如何组织对话；

* token 是什么；

* 上下文窗口是什么；

* streaming 输出是什么；

* temperature 如何影响回答稳定性；

* 如何保存对话历史。

### 实战产出

* `mini-agent-v0.1`

* 一个命令行聊天助手；

* 支持 system prompt；

* 支持多轮对话；

* 支持保存 conversation history。

***

## 1.2 Responses API / Chat Completions API

### 学习目标

理解传统聊天 API 和新式 Agent API 的差异。

### Key Words

* Chat Completions API

* Responses API

* messages

* items

* role

* content

* function\_call

* function\_call\_output

* tool output

* structured output

* JSON schema

### 应掌握内容

* `messages` 是什么；

* `role/content` 是什么；

* 为什么 Agent 不只是普通聊天；

* 为什么 function call / tool output 也需要进入上下文；

* 结构化输出为什么重要；

* JSON schema 如何约束模型输出。

### 实战产出

* 写一个简单脚本，对比普通文本输出和 JSON 结构化输出。

***

# 2. Prompt Engineering 与 Context Engineering

## 2.1 Prompt Engineering

### 学习目标

从“写提示词”升级到“设计任务协议”。

### Key Words

* prompt engineering

* instruction

* role prompting

* task specification

* output format

* few-shot prompting

* zero-shot prompting

* chain-of-thought

* hidden reasoning

* structured prompt

* prompt template

* constraint

* rubric

* examples

* negative examples

### 应掌握内容

* 如何定义角色；

* 如何定义任务边界；

* 如何规定输入输出格式；

* 如何写 few-shot examples；

* 如何避免 prompt 过长；

* 如何避免模糊指令；

* 如何让输出稳定。

### 实战产出

* 为 PV Research Agent 写一组 prompt templates：

  * 论文问答 prompt；

  * 实验日志分析 prompt；

  * LaTeX 检查 prompt；

  * reviewer comments 总结 prompt；

  * QR/ablation 分析草稿 prompt。

***

## 2.2 Context Engineering

### 学习目标

理解“给模型什么上下文、不给什么上下文、怎么组织上下文”。

### Key Words

* context engineering

* context window

* context budget

* context compression

* context selection

* context ranking

* prompt assembly

* conversation history

* relevant context

* irrelevant context

* recency

* salience

* truncation

* summarization

* memory injection

### 应掌握内容

* 上下文不是越多越好；

* 如何选择相关上下文；

* 如何压缩长对话；

* 如何把 memory / RAG / tool results 拼进 prompt；

* 如何避免上下文污染；

* 如何处理旧信息和新信息冲突。

### 实战产出

* 给 mini-agent 加入简单上下文管理：

  * 保留最近 N 轮对话；

  * 长对话自动摘要；

  * 项目固定规则注入。

***

# 3. Tool Calling / Function Calling 层

## 3.1 Function Calling 基础

### 学习目标

理解 Agent 如何“请求调用工具”。

### Key Words

* function calling

* tool calling

* tool schema

* function schema

* JSON schema

* arguments

* tool name

* tool description

* parameter validation

* tool result

* tool output

* host program

* external execution

### 应掌握内容

* 模型不会自己执行工具；

* 模型生成结构化 tool call；

* 你的 Python 程序真正执行函数；

* 工具结果再返回模型；

* 模型基于工具结果生成最终回答。

### 实战产出

* `mini-agent-v0.2`

* 支持以下 tools：

  * `get_current_time`

  * `read_file`

  * `list_files`

  * `read_json`

  * `calculate`

  * `run_python`

***

## 3.2 Tool Design

### 学习目标

设计稳定、可控、可评估的工具。

### Key Words

* tool design

* tool description

* input schema

* output schema

* idempotent tool

* side-effect

* permission

* sandbox

* error handling

* retry

* timeout

* logging

* observability

### 应掌握内容

* tool description 会影响模型是否正确选择工具；

* 工具参数必须清晰；

* 工具输出要结构化；

* 危险工具要加权限控制；

* 工具失败要有错误信息；

* 工具调用必须记录日志。

### 实战产出

* 为 PV Research Agent 设计工具集：

  * `read_paper`

  * `search_latex`

  * `read_experiment_log`

  * `read_csv_table`

  * `summarize_reviewer_comments`

  * `check_response_consistency`

  * `generate_plot_with_python`

***

# 4. Agent Loop 核心层

## 4.1 Agent Loop 基础

### 学习目标

理解 Agent 的基本运行循环。

### Key Words

* agent loop

* observe

* think

* act

* reflect

* plan

* execute

* stop condition

* ReAct

* reasoning-action loop

* tool-use loop

* iterative execution

### 应掌握内容

Agent 的基本循环：

1. Observe：读取用户问题和上下文；

2. Decide：判断是否需要工具；

3. Act：调用工具；

4. Integrate：整合工具结果；

5. Reflect：判断是否完成；

6. Repeat：继续循环或最终回答。

### 实战产出

* `mini-agent-v0.3`

* 实现一个简单 Agent Loop：

  * 用户提问；

  * 模型判断是否调用工具；

  * 执行工具；

  * 回填工具结果；

  * 生成最终回答。

***

## 4.2 Planning / Execution

### 学习目标

让 Agent 从单步工具调用升级到多步骤任务执行。

### Key Words

* planning

* planner

* executor

* plan-and-execute

* task decomposition

* subtask

* intermediate result

* self-check

* reflection

* retry

* fallback

* human-in-the-loop

### 应掌握内容

* 如何把复杂任务拆成子任务；

* 什么时候需要 planner；

* 什么时候直接 tool call 就够；

* 如何判断任务完成；

* 如何处理失败；

* 如何让用户确认高风险操作。

### 实战产出

* 实现一个 `ReviewerResponseChecker` workflow：

  1. 读取审稿意见；

  2. 提取 reviewer concerns；

  3. 检索修改稿；

  4. 检查 response letter；

  5. 判断是否闭环；

  6. 输出风险报告。

***

# 5. RAG 知识增强层

## 5.1 RAG 基础

### 学习目标

让 Agent 能读取你的私有知识，而不是只靠模型记忆。

### Key Words

* RAG

* Retrieval-Augmented Generation

* document loading

* chunking

* embedding

* vector database

* semantic search

* keyword search

* hybrid search

* top-k retrieval

* rerank

* context injection

* citation

* grounded generation

### 应掌握内容

* RAG 解决什么问题；

* 文档如何切 chunk；

* embedding 是什么；

* 向量库如何检索；

* 检索结果如何进入 prompt；

* 回答为什么要带证据；

* 如何减少 hallucination。

### 实战产出

* `PV Research Agent v0.3`

* 支持导入：

  * paper PDF；

  * LaTeX；

  * response letter；

  * reviewer comments；

  * experiment logs；

  * CSV/Excel 表格；

  * Markdown notes。

***

## 5.2 Vector Database / Search

### 学习目标

掌握文档检索系统的核心组件。

### Key Words

* Chroma

* FAISS

* Qdrant

* Milvus

* SQLite

* PostgreSQL

* pgvector

* BM25

* hybrid retrieval

* metadata filtering

* document index

* collection

* namespace

* similarity score

* cosine similarity

### 应掌握内容

* Chroma / FAISS 的基本使用；

* metadata filter 的作用；

* 语义检索和关键词检索的区别；

* hybrid search 的价值；

* 为什么需要 rerank；

* 如何评估 retrieval quality。

### 实战产出

* 为 PV Research Agent 建立本地知识库：

  * `papers`

  * `responses`

  * `logs`

  * `latex`

  * `figures`

  * `tables`

***

## 5.3 RAG Evaluation

### 学习目标

评估 RAG 是否真的检索到了正确证据。

### Key Words

* RAG evaluation

* faithfulness

* answer relevancy

* context precision

* context recall

* citation correctness

* hallucination rate

* retrieval accuracy

* groundedness

* Ragas

* LLM-as-judge

### 应掌握内容

* 怎么判断回答有没有证据；

* 怎么判断检索结果是否相关；

* 怎么判断模型是否编造；

* 怎么设计 RAG 测试集；

* 怎么用自动评分 + 人工复核。

### 实战产出

* 制作一个 PV QA eval set：

  * shared backbone 定义；

  * QR 实验设置；

  * ablation 结论；

  * RevIN 使用范围；

  * classification / forecasting 差异；

  * reviewer response consistency。

***

# 6. Memory 记忆管理层

## 6.1 Memory 类型

### 学习目标

理解 Agent 如何在多轮任务中“记住”重要信息。

### Key Words

* memory

* short-term memory

* long-term memory

* working memory

* episodic memory

* semantic memory

* project memory

* user memory

* conversation summary

* memory retrieval

* memory update

* memory conflict

### 应掌握内容

* 当前对话记忆；

* 长期用户偏好；

* 项目固定背景；

* 某次任务的历史记录；

* 何时保存 memory；

* 何时不保存 memory；

* 旧 memory 和新信息冲突怎么办。

### 实战产出

* 为 PV Research Agent 建立 project memory：

  * TriP-Net 与 KBS 工作分离；

  * shared backbone 不是 shared weights；

  * forecasting/classification 分开训练；

  * classification 不使用 RevIN；

  * QR 设置；

  * 论文写作风格偏好。

***

## 6.2 Memory Engineering

### 学习目标

让 memory 可控、可更新、可检索。

### Key Words

* memory store

* memory schema

* memory summarization

* memory compression

* memory retrieval

* memory ranking

* memory pruning

* stale memory

* conflict resolution

* persistent memory

* SQLite memory

* vector memory

### 应掌握内容

* memory 不能无限塞；

* memory 要有结构；

* memory 要能被检索；

* memory 要能过期或被更新；

* memory 与 RAG 的区别；

* memory 如何注入 prompt。

### 实战产出

* 实现：

  * `project_memory.json`

  * `conversation_summary.md`

  * `memory_retriever.py`

  * `memory_update_rule.md`

***

# 7. Workflow / Orchestration 层

## 7.1 LangChain

### 学习目标

了解主流 Agent/RAG 开发框架。

### Key Words

* LangChain

* chain

* prompt template

* output parser

* retriever

* tool

* agent

* runnable

* LCEL

* document loader

* text splitter

* vector store

* agent executor

### 应掌握内容

* LangChain 是什么；

* 它解决了哪些重复工程；

* 如何用它做 RAG；

* 如何接入 tools；

* 如何构建简单 agent；

* 什么时候不需要 LangChain。

### 实战产出

* 用 LangChain 重写一个简单 RAG demo；

* 对比手写版本和 LangChain 版本。

***

## 7.2 LangGraph

### 学习目标

掌握复杂 Agent 工作流编排。

### Key Words

* LangGraph

* graph

* node

* edge

* state

* state machine

* conditional edge

* checkpoint

* durable execution

* human-in-the-loop

* workflow

* multi-step agent

* orchestration

* persistence

### 应掌握内容

* Agent 可以建模成图；

* state 如何保存；

* node 如何执行；

* edge 如何控制流向；

* 如何中断等待人工确认；

* 如何恢复失败任务；

* 如何避免无限循环。

### 实战产出

* 用 LangGraph 实现 PV Research Agent 工作流：

  * `PaperQAWorkflow`

  * `ExperimentLogAnalyzer`

  * `LatexTableInspector`

  * `ReviewerResponseChecker`

  * `QRAnalysisDraftGenerator`

***

## 7.3 OpenAI Agents SDK

### 学习目标

了解 OpenAI 官方 Agent 开发范式。

### Key Words

* OpenAI Agents SDK

* agent

* runner

* handoff

* tool

* guardrail

* tracing

* structured output

* session

* hosted tools

* function tools

* MCP tools

### 应掌握内容

* Agent 如何定义；

* tools 如何注册；

* handoff 是什么；

* guardrails 是什么；

* tracing 如何记录执行过程；

* 什么时候用 Agents SDK；

* Agents SDK 与 LangGraph 的区别。

### 实战产出

* 用 Agents SDK 写一个简单 Research Agent；

* 支持一个 tool；

* 支持 structured output；

* 支持 trace 记录。

***

# 8. Skills 系统层

## 8.1 Skill 基础

### 学习目标

理解 skill 不是普通 prompt，而是可复用工作流封装。

### Key Words

* skill

* reusable workflow

* skill description

* skill trigger

* skill instruction

* skill resource

* skill script

* SKILL.md

* progressive disclosure

* project instruction

* AGENTS.md

* Codex skills

### 应掌握内容

* skill 的组成；

* skill 与 prompt 的区别；

* skill 与 tool 的区别；

* skill 如何被 Agent 选择；

* description 为什么关键；

* skill 如何组织资源和脚本；

* skill 如何适配特定项目。

### 实战产出

* 编写第一个 Codex skill：

  * `reviewer-response-checker`

  * `latex-table-checker`

  * `experiment-log-analyzer`

  * `qr-analysis-generator`

***

## 8.2 Skill Design

### 学习目标

设计高质量、可复用、可评估的 skill。

### Key Words

* skill design

* trigger condition

* scope

* input contract

* output contract

* workflow steps

* examples

* counterexamples

* failure mode

* fallback

* checklist

* rubric

* task boundary

### 应掌握内容

* 一个 skill 只做一类任务；

* 触发条件要清楚；

* 输入输出要固定；

* 操作步骤要稳定；

* 要包含成功示例和失败示例；

* 要有错误处理；

* 要避免过度泛化。

### 实战产出

* 设计 PV Research Agent skills：

  * 论文返修一致性检查；

  * LaTeX 表格检查；

  * 实验日志解释；

  * 消融分析草稿生成；

  * QR 鲁棒性分析草稿生成；

  * reviewer comments 总结。

***

# 9. Evaluation / A-B Test / Benchmark 层

## 9.1 Agent Evaluation 基础

### 学习目标

从“感觉好用”变成“可量化评估”。

### Key Words

* evaluation

* eval

* benchmark

* dataset

* test case

* golden answer

* expected output

* grader

* scoring rubric

* pass rate

* regression test

* LLM-as-judge

* human evaluation

* automatic evaluation

### 应掌握内容

* 如何构建测试集；

* 如何定义标准答案；

* 如何自动评分；

* 如何人工复核；

* 如何比较两个 prompt；

* 如何判断版本是否退化；

* 如何做回归测试。

### 实战产出

* 构建 `pv_agent_eval_set.jsonl`：

  * 论文事实问答；

  * 实验设置问答；

  * LaTeX 检查任务；

  * reviewer response consistency；

  * QR/ablation 分析生成任务。

***

## 9.2 Skill Evaluation Framework

### 学习目标

完善你朋友提到的 skills 评估框架。

### Key Words

* skill evaluation

* skill trigger accuracy

* false trigger rate

* missed trigger rate

* step completion rate

* tool call correctness

* evidence usage rate

* citation correctness

* output format compliance

* actionability score

* stability score

* cross-agent evaluation

* cross-model evaluation

* cross-repo evaluation

### 应掌握内容

评估一个 skill 至少看：

1. 是否被正确触发；

2. 是否按步骤执行；

3. 是否调用正确工具；

4. 是否读取正确上下文；

5. 是否输出正确格式；

6. 是否有证据支撑；

7. 是否稳定；

8. 是否高效；

9. 是否能跨模型迁移；

10. 是否能跨 Agent 迁移。

### 实战产出

* `agent-skill-eval`

* 包含：

  * dataset；

  * runner；

  * trace collector；

  * grader；

  * report generator；

  * A/B comparison；

  * failure analysis。

***

## 9.3 Trace / Observability

### 学习目标

观察 Agent 每一步到底做了什么。

### Key Words

* trace

* tracing

* observability

* logging

* span

* event

* model call

* tool call

* tool output

* latency

* token usage

* cost

* error log

* debug

* LangSmith

* OpenTelemetry

### 应掌握内容

* 记录每次模型调用；

* 记录每次工具调用；

* 记录输入输出；

* 记录 token 和耗时；

* 记录失败原因；

* 根据 trace 定位问题；

* 比较不同版本表现。

### 实战产出

* 给 mini-agent 加入 trace 日志；

* 每次运行保存：

  * prompt；

  * tool calls；

  * retrieved documents；

  * final answer；

  * latency；

  * token cost；

  * score。

***

# 10. MCP 与外部工具生态

## 10.1 MCP 基础

### 学习目标

理解 MCP 是工具接入协议。

### Key Words

* MCP

* Model Context Protocol

* MCP server

* MCP client

* tools

* resources

* prompts

* transport

* stdio

* HTTP

* tool discovery

* schema

* external integration

### 应掌握内容

* MCP 解决什么问题；

* MCP server 提供什么；

* MCP client 调用什么；

* MCP 与 function calling 的关系；

* 如何把本地工具暴露给 Agent；

* 如何接入文件系统、数据库、GitHub、浏览器等工具。

### 实战产出

* 写一个简单 MCP server：

  * 提供 `read_project_file`

  * 提供 `search_experiment_log`

  * 提供 `list_latex_sections`

***

## 10.2 Codex + MCP

### 学习目标

把成熟 Code Agent 纳入自己的 Agent 系统。

### Key Words

* Codex CLI

* coding agent

* AGENTS.md

* Codex skills

* Codex MCP

* code modification

* repository agent

* code review agent

* software engineering agent

### 应掌握内容

* Codex 是成熟 Code Agent；

* Codex 不是空壳；

* 可以通过 AGENTS.md 管理项目行为；

* 可以通过 skills 扩展能力；

* 可以通过 MCP 作为工具被其他 Agent 调用；

* Codex 适合做 code worker。

### 实战产出

* 为 Codex 配置：

  * `AGENTS.md`

  * project rules；

  * PV research skills；

  * skill eval workflow；

  * 本地代码修改规范。

***

# 11. Safety / Guardrails / Permission 层

## 11.1 Agent 安全基础

### 学习目标

防止 Agent 乱执行、乱调用、乱泄露。

### Key Words

* safety

* guardrails

* permission

* sandbox

* prompt injection

* data leakage

* tool abuse

* dangerous command

* confirmation

* access control

* allowlist

* denylist

* human approval

* safe execution

### 应掌握内容

* 为什么工具调用有风险；

* 哪些工具需要确认；

* 如何防止 prompt injection；

* 如何限制文件访问范围；

* 如何限制命令执行；

* 如何避免泄露 API key；

* 如何设置 human-in-the-loop。

### 实战产出

* 给 PV Research Agent 加安全规则：

  * 禁止删除文件；

  * 禁止自动提交 Git；

  * 运行 shell 命令前确认；

  * 只读取项目目录；

  * 不输出 `.env` 内容；

  * 高风险操作需要人工确认。

***

# 12. Deployment / 产品化层

## 12.1 本地部署

### 学习目标

让 Agent 从脚本变成可使用的本地项目。

### Key Words

* local deployment

* FastAPI

* Streamlit

* Gradio

* CLI

* REST API

* Web UI

* SQLite

* Docker

* docker-compose

* environment variable

* config file

* logging

### 应掌握内容

* CLI 版本；

* Web UI 版本；

* FastAPI 后端；

* 本地数据库；

* Docker 化；

* 配置管理；

* 日志管理。

### 实战产出

* PV Research Agent 本地版本：

  * CLI；

  * Streamlit UI；

  * FastAPI backend；

  * SQLite 保存历史；

  * Chroma 保存知识库；

  * Docker 一键启动。

***

## 12.2 云端 / 混合部署

### 学习目标

理解本地模型和云端模型如何结合。

### Key Words

* cloud API

* local model

* Ollama

* LM Studio

* vLLM

* hybrid deployment

* model routing

* cost control

* latency

* privacy

* inference server

* GPU

* quantization

### 应掌握内容

* 本地模型适合什么；

* 云模型适合什么；

* 如何根据任务选择模型；

* 如何控制成本；

* 如何保护隐私数据；

* 如何做模型 fallback。

### 实战产出

* 模型路由策略：

  * 简单任务走本地模型；

  * 复杂论文分析走云端模型；

  * 敏感文件只走本地模型；

  * 失败时 fallback 到更强模型。

***

# 13. PV Research Agent 主项目路线

## 13.1 项目定位

### 项目名称

**PV Research Agent**

### 项目目标

构建一个面向光伏时序科研工作的本地 AI Agent，用于：

* 读取论文；

* 读取实验日志；

* 读取代码；

* 读取数据表；

* 回答实验问题；

* 生成 QR/ablation 分析草稿；

* 检查 LaTeX 表格；

* 总结 reviewer comments；

* 检查 response letter 与正文是否闭环；

* 调用 Python 画图；

* 管理项目记忆；

* 评估 skills 效果。

***

## 13.2 功能模块

### Key Words

* research agent

* paper QA

* experiment traceability

* manuscript revision

* reviewer-response consistency

* LaTeX checker

* QR analysis

* ablation analysis

* Python plotting

* research workflow

* PV time-series

* photovoltaic forecasting

* fault classification

### 模块设计

1. **PaperQA**

   * 论文问答；

   * 方法章节解释；

   * claim 检查；

   * contribution 检查。

2. **ExperimentLogAnalyzer**

   * 读取 JSON / CSV；

   * 总结实验设置；

   * 对比 clean vs QR；

   * 生成实验解释。

3. **LatexTableInspector**

   * 检查 LaTeX 表格；

   * 检查 caption；

   * 检查 label；

   * 检查数值一致性；

   * 检查表述是否过强。

4. **ReviewerResponseChecker**

   * 提取审稿意见；

   * 匹配正文修改；

   * 检查 response letter；

   * 输出风险等级。

5. **QRAnalysisDraftGenerator**

   * 根据 QR 实验结果生成分析草稿；

   * 控制语气；

   * 避免过强 claim；

   * 强调 controlled observation-quality degradation。

6. **AblationAnalysisGenerator**

   * 总结 ablation 结果；

   * 指出不是所有子项最优；

   * 强调 balanced performance；

   * 生成审稿友好表述。

7. **SkillEval**

   * 评估每个 skill；

   * 记录 trace；

   * 输出评分报告；

   * 做 A/B prompt 对比。

***

# 14. 推荐最终项目目录

## Key Words

* project structure

* modular design

* src layout

* config

* tests

* evals

* data

* logs

* docs

* README

## 项目结构

ai-agent-learning/

* README.md

* AGENTS.md

* .env

* .gitignore

* pyproject.toml

mini\_agent/

* main.py

* llm.py

* tools.py

* memory.py

* agent\_loop.py

* tracing.py

pv\_research\_agent/

* app.py

* config.py

* prompts/

* tools/

* rag/

* memory/

* workflows/

* skills/

* evals/

* data/

* logs/

skill\_eval/

* datasets/

* runners/

* graders/

* reports/

* traces/

* examples/

docs/

* learning\_notes.md

* function\_calling.md

* rag\_notes.md

* memory\_notes.md

* skill\_design.md

* eval\_design.md

***

# 15. 总学习顺序

## 第一阶段：从零理解 Agent

### Key Words

* LLM API

* messages

* system prompt

* streaming

* structured output

* function calling

* tool output

* agent loop

### 产出

* mini-agent CLI；

* 支持简单工具调用。

***

## 第二阶段：构建工具系统

### Key Words

* tools

* function schema

* parameter validation

* error handling

* logging

* sandbox

### 产出

* 支持文件读取、JSON 读取、Python 执行、LaTeX 检查。

***

## 第三阶段：构建 RAG 知识库

### Key Words

* RAG

* embedding

* chunking

* vector database

* retrieval

* rerank

* citation

* grounded answer

### 产出

* 能读论文、返修信、实验日志并带证据回答。

***

## 第四阶段：构建 Memory 系统

### Key Words

* short-term memory

* long-term memory

* project memory

* summary memory

* memory retrieval

* context injection

### 产出

* 能记住 TriP-Net 项目规则和写作偏好。

***

## 第五阶段：构建 Workflow

### Key Words

* LangChain

* LangGraph

* state graph

* node

* edge

* workflow

* human-in-the-loop

* checkpoint

### 产出

* ReviewerResponseChecker；

* ExperimentLogAnalyzer；

* QRAnalysisGenerator；

* LatexTableInspector。

***

## 第六阶段：构建 Skills

### Key Words

* Codex skills

* SKILL.md

* skill trigger

* reusable workflow

* AGENTS.md

* progressive disclosure

* skill resources

* skill scripts

### 产出

* 为 Codex 写 PV research skills；

* 在成熟 Code Agent 上优化科研工作流。

***

## 第七阶段：构建 Evaluation

### Key Words

* eval

* benchmark

* golden answer

* grader

* LLM-as-judge

* trace

* A/B test

* regression test

* skill evaluation

### 产出

* Agent skill evaluation framework；

* 测试集；

* 自动评分；

* 失败案例分析报告。

***

## 第八阶段：接入 MCP 与开源项目

### Key Words

* MCP

* MCP server

* MCP client

* tool discovery

* external tools

* open-source contribution

* pull request

* issue

* code review

### 产出

* 写一个简单 MCP server；

* 给开源 skill-eval 项目贡献功能；

* 形成 GitHub 项目展示。

***

## 第九阶段：部署与展示

### Key Words

* FastAPI

* Streamlit

* CLI

* Docker

* SQLite

* Chroma

* local deployment

* README

* demo

* documentation

### 产出

* 本地可运行 PV Research Agent；

* GitHub README；

* demo screenshots；

* 项目报告；

* 简历描述。

***

# 16. 最终能力闭环

学完以后，你应该具备以下能力：

1. **能从零写一个 mini-agent**

   * 理解 API、messages、tool calling、agent loop。

2. **能构建科研 RAG 系统**

   * 读取论文、日志、表格、LaTeX，并带证据回答。

3. **能设计 Agent tools**

   * 工具有 schema、有权限、有日志、有错误处理。

4. **能做 memory/context 管理**

   * 知道什么该记、什么该忘、什么该检索。

5. **能设计 workflow**

   * 用 LangGraph / Agents SDK 做多步骤科研任务。

6. **能写 Codex skills**

   * 把科研任务封装成可复用工作流。

7. **能评估 skills 和 agents**

   * 用 benchmark、trace、grader、A/B test 做系统评估。

8. **能参与开源项目**

   * 会读代码、提 issue、改功能、提 PR。

9. **能做完整项目展示**

   * GitHub 仓库、README、demo、报告、简历亮点。

***

# 17. 一句话总路线

**从零实现 mini-agent 理解底层机制 → 构建 PV Research Agent 服务科研场景 → 学习 LangChain/LangGraph/Agents SDK 做复杂工作流 → 编写 Codex skills 优化成熟 Code Agent → 搭建 skill evaluation framework 形成工程亮点 → 用 GitHub 和开源贡献沉淀成果。**
