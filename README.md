# Personal Moat Skills

个人护城河技能库 — 面向个人提效、阅读学习与知识管理的 Claude Skills 集合。

## MECE 工具地图

本仓库按“个人提效链路”重新组织：先用 `personal-effectiveness-system` 判断用户卡在哪个环节，再路由到专门工具。每次只选择一个主工具；如果请求跨多个环节，按链路顺序串行推进。

| 提效环节 | 主工具 | 输入 | 产出 | 排除边界 |
|---|---|---|---|---|
| 1. 收集 Capture：信息、想法、任务散落 | `personal-effectiveness-system` | 原始 inbox、聊天记录、会议记录、临时想法 | 去重后的 inbox 清单 | 不排序、不承诺执行 |
| 2. 澄清 Clarify：不知道条目到底是什么 | `personal-effectiveness-system` | inbox 条目、背景、约束 | 项目 / 动作 / 等待 / 资料 / someday 分类 | 不做长期目标判断 |
| 3. 取舍 Prioritize：事情太多，不知道先做什么 | `personal-effectiveness-system` | 已澄清清单、目标、截止期、能量 | Now / Next / Later / Drop | 不排具体日程 |
| 4. 计划 Plan：目标太大，不知道怎么推进 | `personal-effectiveness-system` | 目标、项目、约束 | 里程碑、下一步、风险、验收标准 | 不替代执行现场反馈 |
| 5. 执行 Execute：拖延、卡住、注意力分散 | `personal-effectiveness-system` | 当前任务、卡点、可用时间 | 25/50/90 分钟执行块、阻塞解除动作 | 不重开战略讨论 |
| 6. 复盘 Review：做完了但没沉淀 | `personal-effectiveness-system` | 周期记录、结果、偏差 | 继续 / 停止 / 开始、系统调整 | 不责备用户 |
| 7. 知识资产 Knowledge：内容很多但不可调用 | `personal-effectiveness-system` | 笔记、经验、模板、输出 | 可检索笔记、checklist、prompt、SOP | 不收藏无触发条件的材料 |
| 8. 阅读学习 Learning：读书、课程、资料内化 | `ai-era-reading` / `reading-notes-organizer` | 书名、章节、批注、读书笔记 | 分流、理解检验、资产化或结构化归档 | 深读与归档不并行混用 |

### 路由决策树

1. 用户提出的是通用个人提效问题（任务、时间、目标、执行、复盘、习惯、知识资产）？→ `personal-effectiveness-system`。
2. 用户是在问“这本书要不要读 / 怎么读 / 我读懂了吗 / 读完能产出什么”？→ `ai-era-reading`。
3. 用户是在说“我已经有读书笔记，请帮我整理成脑图 / 大纲 / 摘要 / 可归档材料”？→ `reading-notes-organizer`。
4. 用户同时需要消化与归档？→ 严格串行：先 `ai-era-reading` 完成理解检验与资产化，再 `reading-notes-organizer` 整理最终材料。
5. 用户请求跨多个提效环节？→ 按 `Capture → Clarify → Prioritize → Plan → Execute → Review → Knowledge → Learning` 顺序推进，不跳步。

### 工具组合顺序

```text
个人提效总控：Capture → Clarify → Prioritize → Plan → Execute → Review → Knowledge
                personal-effectiveness-system 覆盖以上通用提效链路

阅读学习专项：选书/分流 → 读前预测 → 读中对话 → 读后资产化 → 笔记结构化归档
                ai-era-reading 覆盖前四步                         reading-notes-organizer 覆盖最后一步
```

## 技能列表

### 🧭 personal-effectiveness-system — 个人提效总控

覆盖任务、时间、目标、执行、复盘、习惯和知识资产化的 MECE 路由系统：

- **收集** — 把散落的信息、想法和任务放入 inbox
- **澄清** — 区分项目、下一动作、等待、资料和 someday
- **取舍** — 生成 Now / Next / Later / Drop
- **计划** — 拆成里程碑、下一动作、风险和验收标准
- **执行** — 处理拖延、卡点和注意力问题
- **复盘** — 用最小系统调整提高下一周期质量
- **知识资产** — 把经验沉淀成 checklist / prompt / SOP

**触发方式：** 用户提到个人提效、任务管理、时间管理、目标拆解、执行卡住、习惯、复盘、知识管理、工作流整理，或不知道该用哪个工具时使用。

#### 适用场景
见 `personal-effectiveness-system/SKILL.md`。
## MECE 技能地图

这个库按「用户要完成的工作」而不是按工具名划分，避免多个 Skill 抢同一个入口：

| 用户意图 | 唯一主 Skill | 边界 | 可调用的辅助能力 |
|---|---|---|---|
| 规划今天/复盘今天/周复盘/整理任务、时间、项目和知识库 | `personal-ai-ops-workflow` | 负责个人运营闭环：任务、时间证据、开发进展、知识沉淀、自动化候选 | 可把读书产出的 artifact 收进知识库，但不负责读书教练过程 |
| 判断一本书值不值得读、怎么读、读中对质、读后检验与产出 | `ai-era-reading` | 负责阅读策略和理解质量：分流、读前预测、读中追问、读后费曼、间隔检索 | 需要把已有笔记做成脑图时，转交 `reading-notes-organizer` |
| 已有一段读书笔记/摘录，要快速生成脑图、大纲和关键笔记 | `reading-notes-organizer` | 只做结构化整理和可视化，不替代读前分流、深读教练或检索练习 | 输出可作为 `ai-era-reading` 阶段 4 artifact 或 `personal-ai-ops-workflow` 知识记录输入 |

### 路由规则

1. **先判定用户意图，不按关键词机械触发。** 同样出现“读书笔记”，如果用户要消化一本书，主 Skill 是 `ai-era-reading`；如果用户只要脑图，主 Skill 是 `reading-notes-organizer`。
2. **一个请求只能有一个主 Skill。** 主 Skill 负责最终输出结构；其他 Skill 只能作为明确标注的辅助步骤。
3. **从流程到资产逐级沉淀。** 阅读理解产出先进入 `ai-era-reading`，可视化整理进入 `reading-notes-organizer`，跨项目/跨周期的行动、复盘和自动化候选再进入 `personal-ai-ops-workflow`。
4. **不把摘要当知识资产。** 只有能改变未来行动、判断或检索路径的内容，才进入个人知识库或被提升为 workflow/SKILL。

## 技能列表

### 🧭 personal-ai-ops-workflow — 个人 AI 运营管家

把滴答清单、RescueTime、开发活动和知识库串成一个 human-in-the-loop 的个人运营系统：
- **每日启动 Brief** — 从任务、时间证据、开发进展中提炼今日 3 个重点
- **每日收尾 Review** — 对照计划与现实，沉淀未完成原因、明日候选和知识资产
- **每周复盘** — 聚合任务、时间、项目和知识库，识别注意力模式与下周重点
- **知识沉淀** — 把文章、对话、开发经验和决策转成可检索的笔记、workflow 或 SKILL 候选
- **自动化分级** — 先让 AI 提建议、等用户确认，再逐步升级为半自动或全自动

**触发方式：** 当用户提到滴答清单、RescueTime、每日计划、周复盘、个人管家、AI 帮我整理任务/时间/知识库/开发进展，或想把重复流程沉淀为 workflow/SKILL 时使用。

#### 适用场景
见 `personal-ai-ops-workflow/SKILL.md` 和 `personal-ai-ops-workflow/references/templates.md`

---

### 📖 ai-era-reading — AI 时代读书方法论

把 Claude 从“摘要器”变成“读书过程的对手方与教练”，覆盖一本书从选择到内化的完整生命周期：

- **分流判断** — 决定该跳过、榨取还是深读
- **读前预测** — 暴露先验判断，制造预测误差
- **读中对话** — 用苏格拉底追问、反对意见和跨知识连接促成理解
- **读后产出** — 逼出费曼讲述、决策备忘、可调用资产或对外输出
- **检索入网** — 用间隔检索和知识连接提高留存与迁移

**触发方式：** 当用户提到想读某本书、评估一本书值不值得读、讨论正在读的章节、做读后消化/输出、检验阅读效果，或明确说“用读书 SKILL”时使用。

#### 适用场景
见 `ai-era-reading/SKILL.md`。

---

### 📚 reading-notes-organizer — 读书笔记结构化工具

把用户已经提供的读书笔记、摘录、书评或阅读感悟整理成可归档、可渲染、可复用的结构化材料：

- **Mermaid 脑图** — 可直接在 Obsidian/GitHub 渲染
- **Markdown 层级大纲** — 适合 Notion/Logseq
- **关键笔记摘要** — 提取最有价值的洞见

**触发方式：** 用户粘贴读书笔记并要求“整理成脑图 / 做大纲 / 结构化 / 可视化 / 归档”。

#### 快速使用（命令行）
```bash
python reading-notes-organizer/scripts/process_notes.py my_notes.md
# 或
cat my_notes.md | python reading-notes-organizer/scripts/process_notes.py --output result.md
```

#### 示例
见 `reading-notes-organizer/examples/sample_notes.md`。
### 🧱 personal-moat-workflow-designer — 个人壁垒 Workflow 设计器

把重复任务、项目经验和个人 know-how 沉淀为可复用的高杠杆工作流：
- **护城河单元定义** — 明确触发场景、输入材料、产出和回写规则
- **工具栈选择** — 按需求匹配 Obsidian/Notion、Skills、脚本、自动化、数据库与检索工具
- **最小可运行 workflow** — 设计 SOP、checklist、prompt、自动化与质量门槛
- **SKILL 沉淀判断** — 判断哪些 workflow 值得变成新的 AI Skill

**触发方式：** 当用户想构建个人壁垒、设计工作流、沉淀 SOP/prompt/checklist/自动化，或询问“这个项目中可以用哪些工具”时使用。

---

### 🧠 knowledge-base-builder — 个人知识库构建器

搭建能被自己和 AI 长期调用的个人知识库：
- **捕获到输出闭环** — Capture → Distill → Link → Retrieve → Produce → Review
- **知识库结构** — inbox、sources、atomic notes、MOC、workflows、projects、decisions、outputs
- **笔记模板** — source note、atomic note、MOC、decision note
- **AI 协作协议** — 让 AI 做连接、质疑、检索和流程沉淀，而不只是摘要

**触发方式：** 当用户想搭建 Obsidian/Notion/Logseq/Markdown 知识库、整理长期笔记、设计标签/MOC、或用知识库构建个人壁垒时使用。

---

## 安装 Skills
### 📚 reading-notes-organizer — 读书笔记整理工具

将**已经存在**的读书笔记自动转化为：
- **Mermaid 脑图** — 可直接在 Obsidian/GitHub 渲染
- **Markdown 层级大纲** — 适合 Notion/Logseq
- **关键笔记摘要** — 提取最有价值的洞见

**触发方式：** 用户粘贴读书笔记，并明确要求“整理成脑图/大纲/结构化笔记”。如果用户要判断怎么读、讨论理解、检验掌握或做读后产出，应使用 `ai-era-reading` 作为主 Skill。

#### 快速使用（命令行）
```bash
python reading-notes-organizer/scripts/process_notes.py my_notes.md
# 或
cat my_notes.md | python reading-notes-organizer/scripts/process_notes.py --output result.md
```

#### 示例
见 `reading-notes-organizer/examples/sample_notes.md`

---

## 使用原始 Skill 文件

本仓库只保留 Skill 源目录，不提交生成后的 `.skill` 二进制包。需要安装时，可在本地从对应目录重新打包后导入 Claude 桌面应用的 Settings → Capabilities → Skills。

```bash
zip -qr personal-effectiveness-system.skill personal-effectiveness-system
zip -qr ai-era-reading.skill ai-era-reading
zip -qr reading-notes-organizer.skill reading-notes-organizer
```

## 维护约定

1. 新增工具时先在“MECE 工具地图”中确认它的独立任务边界。
2. 每个 Skill 的 `description` 必须写清：触发条件、核心产出、与相邻工具的排除边界。
3. 通用提效能力优先放入 `personal-effectiveness-system`；阅读理解放入 `ai-era-reading`；已有读书笔记结构化放入 `reading-notes-organizer`。
4. 不提交生成后的 `.skill` 文件；如需分发或安装，在本地按需重新打包。
本仓库不保留打包后的 `.skill` 文件，统一以各目录中的原始 `SKILL.md`、`references/`、`scripts/`、`agents/` 等文件作为唯一来源。需要安装或分发时，请从对应目录读取原始文件，避免压缩包与源文件内容漂移。

## 贡献

欢迎提 PR，添加新的个人效率技能。新增 Skill 前请先检查上面的 MECE 技能地图：如果只是既有 Skill 的一个阶段或输出格式，优先整合进现有 Skill；只有当它有独立触发、独立输入输出和独立验收标准时，再新增。
