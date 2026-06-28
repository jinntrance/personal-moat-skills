# Personal Moat Skills

个人护城河技能库 — 提升个人效率、知识管理的 Claude Skills 集合。

## MECE 技能地图

这个库按「用户要完成的工作」而不是按工具名划分，避免多个 Skill 抢同一个入口：

| 用户意图 | 唯一主 Skill | 边界 | 可调用的辅助能力 |
|---|---|---|---|
| 规划今天/复盘今天/整理任务、时间、项目和知识库 | `personal-ai-ops-workflow` | 负责日常个人运营闭环：任务、时间证据、开发进展、知识沉淀、自动化候选 | 可把读书产出的 artifact 收进知识库，但不负责读书教练过程 |
| 做周度 Review/复盘，按 Get Clear/Get Current/Get Future 清空、回顾、规划下周 | `weekly-review-retrospective` | 负责周复盘仪式：Inbox/Waiting/Someday、时间与注意力、OKR/九宫格、习惯健康、阅读知识、财务风险、下周 P1/P2 | 可调用 `personal-ai-ops-workflow` 的任务/时间/知识层作为输入，但最终输出由周复盘 Skill 负责 |
| 做月度九宫格复盘，校准工作/生活/健康/关系/财务/成长等领域并规划下月 | `monthly-nine-grid-review` | 负责月复盘仪式：借鉴《只管去做》的愿景、年度九宫格、SMART、项目倒推、习惯和 4D，把月度事实转成下月九宫格推进项 | 可调用 `weekly-review-retrospective` 的周复盘结果和 `personal-ai-ops-workflow` 的任务/时间/知识层作为证据 |
| 判断一本书值不值得读、怎么读、读中对质、读后检验与产出 | `ai-era-reading` | 负责阅读策略和理解质量：分流、读前预测、读中追问、读后费曼、间隔检索 | 需要把已有笔记做成脑图时，转交 `reading-notes-organizer` |
| 已有一段读书笔记/摘录，要快速生成脑图、大纲和关键笔记 | `reading-notes-organizer` | 只做结构化整理和可视化，不替代读前分流、深读教练或检索练习 | 输出可作为 `ai-era-reading` 阶段 4 artifact 或 `personal-ai-ops-workflow` 知识记录输入 |
| 用 ima copilot 收集和存储苹果备忘录、录音、截图、网页、微信资料，并用 LLM Wiki/workbuddy 编译成可维护个人 Wiki | `ima-llm-wiki-workflow` | 负责 ima 作为前台收集/回写层、LLM Wiki/workbuddy 作为中间编译层的 SOP、模板、质量检查和回写规则 | 通用知识库结构设计仍由 `knowledge-base-builder` 负责；日常任务/项目运营仍由 `personal-ai-ops-workflow` 负责 |

### 路由规则

1. **先判定用户意图，不按关键词机械触发。** 同样出现“读书笔记”，如果用户要消化一本书，主 Skill 是 `ai-era-reading`；如果用户只要脑图，主 Skill 是 `reading-notes-organizer`。
2. **一个请求只能有一个主 Skill。** 主 Skill 负责最终输出结构；其他 Skill 只能作为明确标注的辅助步骤。
3. **从流程到资产逐级沉淀。** 阅读理解产出先进入 `ai-era-reading`，可视化整理进入 `reading-notes-organizer`，跨项目/跨周期的行动、复盘和自动化候选按粒度进入对应 Skill：周复盘进入 `weekly-review-retrospective`，月度九宫格进入 `monthly-nine-grid-review`，日常运营进入 `personal-ai-ops-workflow`。
4. **不把摘要当知识资产。** 只有能改变未来行动、判断或检索路径的内容，才进入个人知识库或被提升为 workflow/SKILL。

## 技能列表

### 🗓️ weekly-review-retrospective — 周度 Review / 复盘

把一周的任务、时间、OKR、项目、习惯、健康、阅读、财务和风险串成 Get Clear → Get Current → Get Future 的复盘流程：
- **Get Clear** — 清空 Inbox、脑内遗留、Waiting、未来日历准备和归档
- **Get Current** — 用 RescueTime/Screen Time、滴答清单、OKR、九宫格、习惯、健康、阅读和财务证据看清本周
- **Get Future** — 用 SMART、2/8 原则、120% 挑战、周四前安排和提前风险预判设计下周
- **确认后写入** — 创建、删除、改期、禁用、退群、归档等动作先给建议，等待用户确认

**触发方式：** 当用户要做周复盘、GTD Weekly Review、Get Clear/Get Current/Get Future、下周规划、OKR/九宫格周回顾、习惯健康阅读财务周总结时使用。

---

### 🧭 monthly-nine-grid-review — 月度九宫格复盘

借鉴邹小强《只管去做》的愿景 → 年度九宫格 → 月计划 → 周计划 → 日行动落地思路，把一个月的工作、生活、健康、关系、财务、成长和心智状态做成证据化复盘：
- **年度方向校准** — 检查年度九宫格/OKR 是否真正落到本月行动
- **九宫格总览** — 每格记录事实、评分、根因、停止动作和下月推进项
- **项目与习惯拆解** — 区分结果目标、项目里程碑和习惯连续性
- **4D 任务清理** — 立刻做、计划做、委托/等待、删除
- **下月落地链** — 把下月重点拆到第一周行动和每日最小动作

**触发方式：** 当用户要做月度复盘、月总结、月底回顾、工作生活九宫格、《只管去做》月度复盘、OKR 月度检查、下月 KR 规划或极简清单时使用。

---

### 🧭 personal-ai-ops-workflow — 个人 AI 运营管家

把滴答清单、RescueTime、开发活动和知识库串成一个 human-in-the-loop 的个人运营系统：
- **每日启动 Brief** — 从任务、时间证据、开发进展中提炼今日 3 个重点
- **每日收尾 Review** — 对照计划与现实，沉淀未完成原因、明日候选和知识资产
- **知识沉淀** — 把文章、对话、开发经验和决策转成可检索的笔记、workflow 或 SKILL 候选
- **自动化分级** — 先让 AI 提建议、等用户确认，再逐步升级为半自动或全自动

**触发方式：** 当用户提到滴答清单、RescueTime、每日计划、每日收尾、个人管家、AI 帮我整理任务/时间/知识库/开发进展，或想把重复流程沉淀为 workflow/SKILL 时使用。完整周复盘请使用 `weekly-review-retrospective`；完整月度九宫格请使用 `monthly-nine-grid-review`。

#### 适用场景
见 `personal-ai-ops-workflow/SKILL.md` 和 `personal-ai-ops-workflow/references/templates.md`

---

### 📖 ai-era-reading — AI 时代读书方法论

把 Claude 从“摘要器”变成“读书过程的对手方与教练”，帮助用户围绕一本书完成：
- **分流判断** — 决定该跳过、榨取还是深读
- **读前预测** — 暴露先验判断，制造预测误差
- **读中对话** — 用苏格拉底追问、反对意见和跨知识连接促成理解
- **读后产出** — 逼出费曼讲述、决策备忘、可调用资产或对外输出
- **检索入网** — 用间隔检索和知识连接提高留存与迁移

**触发方式：** 当用户提到想读某本书、评估一本书值不值得读、讨论正在读的章节、做读后笔记/输出，或明确说“用读书 SKILL”时使用。

#### 适用场景
见 `ai-era-reading/SKILL.md`

---

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

### 🧩 ima-llm-wiki-workflow — ima + LLM Wiki 知识库流水线

把腾讯 ima copilot 作为收集入口和更新后存储层，把 LLM Wiki、workbuddy 或开源 RAG/Wiki 框架作为中间编译器：
- **混合输入收集** — 苹果备忘录、录音、截图、网页、微信资料、PDF 先进 ima
- **Source Record 标准化** — 为每条输入生成稳定 ID、来源类型、转写/OCR、隐私级别和处理状态
- **LLM Wiki 编译** — 去重、抽取实体、生成/更新 Wiki 页面、添加双链、标注冲突
- **人工确认后回写** — 把 Source、Wiki Page、Review Log 写回 ima 对应空间
- **周期性 Lint** — 检查未处理来源、孤立页面、重复页面、过期决策和隐私风险

**触发方式：** 当用户明确希望“收集、更新后的存储都用 ima copilot”，中间用 LLM Wiki、workbuddy、Dify、RAGFlow、AnythingLLM、Khoj 等工具完成结构化知识编译时使用。

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

本仓库不保留打包后的 `.skill` 文件，统一以各目录中的原始 `SKILL.md`、`references/`、`scripts/`、`agents/` 等文件作为唯一来源。需要安装或分发时，请从对应目录读取原始文件，避免压缩包与源文件内容漂移。

## 贡献

欢迎提 PR，添加新的个人效率技能。新增 Skill 前请先检查上面的 MECE 技能地图：如果只是既有 Skill 的一个阶段或输出格式，优先整合进现有 Skill；只有当它有独立触发、独立输入输出和独立验收标准时，再新增。
