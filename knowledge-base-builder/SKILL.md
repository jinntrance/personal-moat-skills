---
name: knowledge-base-builder
description: 个人知识库构建与维护工作流。当用户想搭建 Obsidian/Notion/Logseq/Markdown 知识库、整理长期笔记、设计标签/目录/MOC、把读书/项目/对话/灵感沉淀为可检索资产、建立知识库与 AI 的协作方式、或询问如何用知识库构建个人壁垒时使用。强调捕获、原子化、连接、检索、输出、复盘闭环。
---

# 个人知识库构建器

## 原则

知识库不是仓库，而是“未来的自己和 AI 能调用的外部大脑”。优先沉淀会改变判断和行动的内容：案例、框架、反例、决策记录、触发条件、模板、问题清单。

核心闭环：

```text
Capture 捕获 → Distill 蒸馏 → Link 连接 → Retrieve 检索 → Produce 输出 → Review 复盘
```

## 工具选择

根据用户偏好和约束推荐最小工具栈：

| 场景 | 推荐 |
|---|---|
| 喜欢本地、可迁移、长期保存 | Markdown + Obsidian + Git |
| 喜欢数据库、多人协作、低门槛 | Notion |
| 喜欢双链、大纲、日记流 | Logseq |
| 需要代码/脚本/版本控制 | Markdown + GitHub |
| 需要快速检索 | ripgrep、Obsidian Search、全文索引 |
| 需要 AI 问答 | Claude/ChatGPT 项目知识、NotebookLM、RAG |
| 需要自动化 | Python、Shell、n8n、Zapier |

不要为了“更智能”过早引入向量库。先保证命名、结构、链接、引用和回写稳定。

## 推荐目录结构

适合 Markdown/Obsidian/Git，也可映射到 Notion 数据库：

```text
knowledge-base/
  00-inbox/            # 临时捕获，定期清空
  10-sources/          # 原始材料：书、文章、播客、课程、访谈
  20-notes/            # 原子笔记：一个观点/规则/案例一篇
  30-mocs/             # Map of Content：主题索引页
  40-workflows/        # SOP、checklist、prompt、SKILL 草稿
  50-projects/         # 正在推进的项目资料
  60-decisions/        # 决策备忘与复盘
  70-outputs/          # 文章、演讲、方案、课程
  90-archive/          # 归档
```

## 笔记类型

### Source Note

用于保留来源，不追求完整复述。

```markdown
---
type: source
source_type: book/article/podcast/course/conversation
status: raw/processed
created: YYYY-MM-DD
---

# [来源标题]

## 核心信息
- 作者/出处：
- 主题：
- 为什么值得保存：

## 摘要

## 值得转成原子笔记的点
- [[...]]
```

### Atomic Note

一个笔记只承载一个可调用观点。

```markdown
---
type: atomic
status: evergreen
tags: []
created: YYYY-MM-DD
---

# [一句话标题]

## 观点

## 触发条件
当遇到 ____ 时，调用这个观点。

## 证据 / 案例

## 反例 / 边界

## 相关链接
- [[...]]
```

### MOC

主题地图，不是文件夹索引，而是“思考路径”。

```markdown
# MOC - [主题]

## 核心问题
- ...

## 关键框架
- [[...]]

## 典型案例
- [[...]]

## 反例与争议
- [[...]]

## 可复用产物
- [[...]]
```

### Decision Note

用于构建判断力壁垒。

```markdown
---
type: decision
status: open/closed/reviewed
created: YYYY-MM-DD
review_on: YYYY-MM-DD
---

# 决策：[问题]

## 背景
## 选项
## 判断依据
## 最强反对意见
## 决策
## 预期结果
## 复盘
```

## 每周维护流程

1. 清空 `00-inbox/`：删除、归档或转化。
2. 从 source note 中提炼 3–10 条 atomic note。
3. 给每条 atomic note 添加触发条件、反例、至少 1 个链接。
4. 更新相关 MOC，把新笔记放到思考路径里。
5. 从本周项目/决策中提炼一个 workflow、checklist 或 prompt。
6. 选择 1 个旧决策或旧输出复盘，更新规则。

## AI 协作协议

让 AI 帮忙时，明确要求它不要只摘要，而要产出可回写资产：

- 把这段材料拆成 atomic notes，并给每条写触发条件。
- 找出这批笔记之间的 5 个连接、3 个矛盾、2 个可行动 checklist。
- 基于这些项目复盘，更新我的“失败模式清单”。
- 把这个重复流程改写成 SKILL 草案。
- 从知识库中找支持/反对某个决策的证据，并标出引用路径。

## 质量门槛

一条知识只有满足以下至少 2 条才值得长期保存：

- 未来会改变一个决策。
- 能支持一篇文章、方案、课程或产品。
- 能补强一个已有 MOC。
- 有明确触发条件。
- 包含个人经历、案例、反例或判断。

## 输出要求

当用户要求搭建或整理知识库时，输出：

1. **最小工具栈**：根据场景选择 1–3 个工具。
2. **目录/数据库结构**：给出可直接创建的结构。
3. **笔记模板**：只给当前最需要的模板。
4. **处理流程**：每日捕获、每周蒸馏、项目结束复盘。
5. **迁移计划**：从现有笔记开始的 3 个小步骤。

## 反模式

- 收藏即学习。
- 标签过多但没有 MOC 和输出路径。
- 每条笔记都很长，无法被未来调用。
- 知识库只进不出，没有文章、决策、workflow、SKILL。
- 把 AI 当摘要器，而不是连接器、质疑者和流程沉淀器。
