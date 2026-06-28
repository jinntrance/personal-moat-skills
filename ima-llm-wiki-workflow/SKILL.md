---
name: ima-llm-wiki-workflow
description: ima copilot + LLM Wiki 个人知识库流水线。当用户想把腾讯 ima copilot 作为苹果备忘录、微信资料、录音、截图、网页、PDF 等材料的收集入口和更新后存储层，并用开源 LLM Wiki、workbuddy 或类似工具在中间完成抽取、双链编译、Lint、回写 SOP 时使用。适合设计个人知识库输入标准、自动化流程、资料回写规则、Source Note/Wiki Note 模板和质量检查。
---

# ima copilot + LLM Wiki 工作流

## 定位

把 ima copilot 当作“前台资料库”和“回写后的可问答知识空间”，把 LLM Wiki/workbuddy 当作中间编译器：它负责把原始输入变成有来源、有双链、有 schema、有质量检查的个人 Wiki。

默认目标不是多做摘要，而是建立一条可重复流水线：

```text
ima 收集/暂存 → 文本化 → LLM Wiki 编译 → 人工确认 → 回写 ima → 周期性 Lint
```

## 何时使用

使用本 Skill 当用户要：

- 把 ima copilot 作为个人知识库的主入口或主存储层。
- 处理苹果备忘录、微信文件、公众号、网页、录音、会议纪要、图片截图、PDF 等混合输入。
- 用 LLM Wiki、workbuddy、nashsu/llm_wiki、Dify、RAGFlow、AnythingLLM、Khoj 等工具串成知识库 SOP。
- 设计从 raw source 到 source note、wiki note、MOC、decision、workflow、skill 的转化规则。
- 解决“信息收集在 ima，结构化更新在外部工具，最终还要存回 ima”的闭环。

如果用户只是在通用层面搭建 Obsidian/Notion/Markdown 知识库，使用 `knowledge-base-builder`。如果用户要把日常任务、时间、项目和知识沉淀合成个人运营系统，使用 `personal-ai-ops-workflow`。

## 架构选择

按用户约束选择最小栈：

| 场景 | 推荐中间层 | 说明 |
|---|---|---|
| 想快速跑通、不想维护服务 | workbuddy | 让 workbuddy 负责抽取、更新、回写提示和周期性任务。 |
| 想本地可控、Markdown 可迁移 | 开源 LLM Wiki | 以 raw sources、wiki pages、schema、lint 为核心，适合长期资产。 |
| 已经有自动化平台 | Dify/RAGFlow/n8n + LLM Wiki | 自动化平台负责编排，LLM Wiki 负责知识结构，不要只做向量问答。 |
| 资料高度敏感 | 本地 LLM Wiki + 本地模型 | ima 只保留可接受上云的副本或索引，敏感原文留本地。 |

优先判断：用户是否坚持“收集和更新后存储都在 ima”。如果是，外部中间层只保存必要的工作副本、ID、schema、日志和可回写结果。

## 标准对象

### Source Record

每个输入都必须有稳定 ID，便于回写和去重。

```markdown
---
id: YYYYMMDD-HHMM-source-short-title
type: source
source_type: apple-note/audio/screenshot/wechat/web/pdf/manual
captured_at: YYYY-MM-DD HH:mm
ima_space: ""
ima_url: ""
status: raw/normalized/compiled/updated/review_needed
privacy: public/private/sensitive
projects: []
topics: []
people: []
---

# 来源标题

## 原始内容

## 转写/OCR/提取文本

## 初步摘要

## 待确认

## 可进入 Wiki 的点
```

### Wiki Page

Wiki 页面是长期知识，不是来源摘要。

```markdown
---
type: concept/project/person/decision/workflow/moc
status: draft/evergreen/review_needed
updated: YYYY-MM-DD
source_ids: []
ima_sync: pending/synced
---

# 页面标题

## 核心结论

## 适用场景

## 证据与来源

## 反例/边界

## 相关页面
```

## SOP

### 1. 收集到 ima

1. 为不同用途建立 ima 空间或知识库：`Inbox`、`Projects`、`Reading`、`Meetings`、`Screenshots`、`Archive`。
2. 原始材料先进入 ima，不在第一步强行清洗。
3. 对录音、图片、截图、网页、苹果备忘录建立统一标题：`YYYYMMDD-HHMM 来源 简短主题`。
4. 如果有 ima skill/connector，优先用它读取、创建、更新资料；没有时让用户导出文本、图片、音频或粘贴内容。

### 2. 文本化与规范化

对不同输入做最小必要处理：

- 苹果备忘录：保留原标题、创建时间、列表和附件引用。
- 录音：转写为带时间戳文本，保留音频链接。
- 截图/图片：OCR 出文字，补充图片所处场景。
- 网页/公众号：保留 URL、作者、发布时间、抓取时间。
- PDF/文档：提取标题、目录、正文、表格摘要和页码引用。

产出 Source Record。无法确认的日期、人物、项目一律放入“待确认”，不要猜。

### 3. 交给 LLM Wiki/workbuddy 编译

把本轮 Source Records 交给中间层，执行：

1. 去重：识别已有来源、重复截图、重复网页。
2. 抽取：人物、项目、概念、决策、行动项、工具、日期。
3. 拆分：把可长期复用的内容转成 Wiki Page 候选。
4. 链接：添加 `[[wikilink]]`、上位 MOC、相关项目和来源 ID。
5. 合并：更新已有页面，避免为同义词创建新页面。
6. 标注冲突：新来源与旧页面不一致时，不直接覆盖，写入待确认。

### 4. 人工确认

回写前必须给用户看变更摘要：

- 新增了哪些 Wiki 页面。
- 更新了哪些已有页面。
- 哪些结论有来源支持。
- 哪些内容需要人工确认。
- 哪些行动项应该进任务系统，而不是知识库。

只有在用户明确授权后，才批量写回 ima 或外部任务系统。

### 5. 回写到 ima

回写分三类：

| 回写类型 | 放到 ima 哪里 | 内容 |
|---|---|---|
| Source Record | 原始资料所在空间 | 原文、转写/OCR、来源元数据、处理状态。 |
| Wiki Page | 项目/主题知识库 | 经确认的概念页、项目页、决策页、流程页。 |
| Review Log | 维护日志空间 | 本次新增/更新/冲突/未处理清单。 |

回写后把 `ima_sync` 标为 `synced`，记录更新时间和目标空间。

### 6. 周期性 Lint

每周或每 50 条新来源运行一次：

- 未处理 source：`status=raw/normalized` 超过 7 天。
- 孤立 Wiki 页面：没有来源或没有相关链接。
- 重复页面：标题不同但主题相近。
- 过期页面：项目、决策、工具类页面超过 30 天未更新。
- 断裂行动项：知识库里出现行动项，但没有进入任务系统。
- 隐私风险：敏感内容被同步到不该出现的空间。

## 提示词协议

### Source 规范化

```text
只基于输入内容生成 Source Record，不要补全未知事实。
请输出：
1. 稳定 ID
2. source_type
3. 标题
4. 转写/OCR/正文
5. 5 行以内摘要
6. 人物、项目、主题、日期
7. 待确认问题
8. privacy: public/private/sensitive
```

### Wiki 编译

```text
把这些 Source Records 编译成 Wiki 更新计划。
要求：
- 每个新增或更新结论必须列出 source_id。
- 优先更新已有页面，只有概念独立且可复用时才创建新页面。
- 输出新增页面、更新页面、冲突、待确认、建议回写到 ima 的位置。
- 不要把普通摘要当成 Wiki 页面。
```

### 回写摘要

```text
生成给用户确认的回写摘要：
- 本次处理的来源数量
- 建议新增页面
- 建议更新页面
- 需要人工确认的问题
- 不建议进入知识库的内容
- 回写到 ima 的空间和标题
等待用户确认后再执行写入。
```

## 输出要求

当用户要设计或运行此流程时，输出：

1. **工具栈**：ima + workbuddy/开源 LLM Wiki + 必要转写/OCR/自动化工具。
2. **数据流**：从输入到回写的具体路径。
3. **对象模板**：Source Record、Wiki Page、Review Log。
4. **执行 SOP**：每日收集、单次编译、人工确认、回写、周度 Lint。
5. **质量门槛**：来源引用、去重、冲突处理、隐私边界、人工确认点。

## 反模式

- 只把 ima 当聊天问答工具，知识更新没有结构。
- 外部 LLM Wiki 编译后不回写，导致 ima 和真实知识库分裂。
- 把所有截图和录音都转成长期知识，制造摘要垃圾。
- 没有 source_id，导致未来无法追溯结论。
- 用向量库替代 Wiki 页面和人工确认。
- 未区分原始资料、Wiki 结论、行动项和复盘日志。
