# Personal Moat Skills

个人护城河技能库 — 面向个人提效、阅读学习与知识管理的 Claude Skills 集合。

## MECE 工具地图

本仓库按“个人提效链路”重新组织：先用 `personal-effectiveness-system` 判断用户卡在哪个环节，再路由到专门工具。每次只选择一个主工具；如果请求跨多个环节，按链路顺序串行推进。

| 提效环节 | 主工具 | 输入 | 产出 | 排除边界 |
|---|---|---|---|---|
| 1. 收集 Capture：信息、想法、任务散落 | `personal-effectiveness-system` | 原始 inbox、聊天记录、会议记录、临时想法 | 去重后的 inbox 清单 | 不排序、不承诺执行 |
| 2. 澄清 Clarify：不知道条目到底是什么 | `personal-effectiveness-system` | inbox 条目、背景、约束 | 项目 / 动作 / 等待 / 资料 / someday 分类 | 不做长期目标判断 |
| 3. 取舍 Prioritize：事情太多，不知道先做什么 | `personal-effectiveness-system` | 已澄清清单、目标、截止期、能量 | Now / Next / Later / Drop | 不排具体日程 |
| 3a. 快速决策 Decision：日常选择和购物反复纠结 | `quick-decision-shopping` | 商品/选择、预算、需求、候选项、平台信息 | 买 / 不买 / 延迟 / 奖励品结论，含时间盒和停止比较条件 | 不处理重大人生、医疗、法律或高风险财务决策 |
| 4. 计划 Plan：目标太大，不知道怎么推进 | `personal-effectiveness-system` | 目标、项目、约束 | 里程碑、下一步、风险、验收标准 | 不替代执行现场反馈 |
| 5. 执行 Execute：拖延、卡住、注意力分散 | `personal-effectiveness-system` | 当前任务、卡点、可用时间 | 25/50/90 分钟执行块、阻塞解除动作 | 不重开战略讨论 |
| 6. 复盘 Review：做完了但没沉淀 | `personal-effectiveness-system` | 周期记录、结果、偏差 | 继续 / 停止 / 开始、系统调整 | 不责备用户 |
| 7. 知识资产 Knowledge：内容很多但不可调用 | `personal-effectiveness-system` | 笔记、经验、模板、输出 | 可检索笔记、checklist、prompt、SOP | 不收藏无触发条件的材料 |
| 8. 阅读学习 Learning：读书、课程、资料内化 | `ai-era-reading` / `reading-notes-organizer` | 书名、章节、批注、读书笔记 | 分流、理解检验、资产化或结构化归档 | 深读与归档不并行混用 |

### 路由决策树

1. 用户提出的是通用个人提效问题（任务、时间、目标、执行、复盘、习惯、知识资产）？→ `personal-effectiveness-system`。
2. 用户是在问“这本书要不要读 / 怎么读 / 我读懂了吗 / 读完能产出什么”？→ `ai-era-reading`。
3. 用户是在问“要不要买 / 选哪个 / 别让我纠结 / 帮我快速决定”，尤其涉及新品、二手、预算、销量、优惠、刚需、欲望或奖励品？→ `quick-decision-shopping`。
4. 用户是在说“我已经有读书笔记，请帮我整理成脑图 / 大纲 / 摘要 / 可归档材料”？→ `reading-notes-organizer`。
5. 用户同时需要消化与归档？→ 严格串行：先 `ai-era-reading` 完成理解检验与资产化，再 `reading-notes-organizer` 整理最终材料。
6. 用户请求跨多个提效环节？→ 按 `Capture → Clarify → Prioritize → Plan → Execute → Review → Knowledge → Learning` 顺序推进，不跳步。

### 工具组合顺序

```text
个人提效总控：Capture → Clarify → Prioritize → Plan → Execute → Review → Knowledge
                personal-effectiveness-system 覆盖以上通用提效链路

阅读学习专项：选书/分流 → 读前预测 → 读中对话 → 读后资产化 → 笔记结构化归档
                ai-era-reading 覆盖前四步                         reading-notes-organizer 覆盖最后一步
```


## 当前覆盖与补充建议

基于现有代码，仓库已经覆盖“个人提效总控 + 阅读理解 + 读书笔记结构化”三类能力。仍建议按以下优先级继续补充，避免一次性新增过多重叠工具：

| 优先级 | 建议补充 | 归属 | 原因 | 验收标准 |
|---|---|---|---|---|
| P0 | `personal-effectiveness-system` 的真实案例样例 | 通用提效 | 目前有框架，但缺少从混乱输入到输出的端到端示例 | 至少覆盖 inbox 整理、周计划、执行卡住、周复盘 4 个例子 |
| P0 | Skill 打包/校验脚本 | 仓库维护 | README 目前给出手动 `zip` 命令，容易漏包或误提交 `.skill` | 一个脚本完成临时打包、校验压缩包、清理生成物 |
| P1 | `reading-notes-organizer` 输出测试样例 | 读书笔记归档 | 当前脚本有示例输入，但缺少固定输出快照或校验 | 示例命令可稳定生成 Mermaid、Markdown 大纲和关键笔记 |
| P1 | 个人提效模板资产 | 通用提效 | Plan / Review / Knowledge 已有规则，但缺少可复制模板 | 增加周计划、项目计划、周复盘、SOP/checklist 模板 |
| P2 | 非书籍学习材料专项规则 | 阅读学习 | 课程、论文、长文与书籍相似但节奏不同 | 在 `personal-effectiveness-system` 或新 Skill 中明确课程/论文/文章处理边界 |
| P2 | 外部工具集成 | 自动化 | 目前 Skill 只产出文本，不直接对接日历、任务管理器或笔记软件 | 明确支持的导出格式，如 Markdown task list、ICS 草稿、Obsidian frontmatter |

短期最值得补的是 **示例与校验脚本**：它们不会破坏现有 MECE 边界，却能显著提高可用性和维护稳定性。

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

### 🛒 quick-decision-shopping — 快速决策与购物

把日常选择和购物决策限制在明确时间盒内，避免为了小决策持续消耗注意力：

- **日常选择** — 普通选择不超过 1 个番茄钟
- **新品购物** — 按 100 / 500 / 1000 元分档设置决策时限
- **二手购物** — 用卖家信用、历史评价和合理价格过滤风险
- **需求价值点** — 区分刚需、增值需求和欲望强度
- **奖励品** — 可绑定习惯养成触发条件

**触发方式：** 用户提到要不要买、选哪个、购物纠结、新品/二手、预算、优惠、销量、刚需、欲望、奖励品，或要求“快速决定”时使用。重大人生、医疗、法律或高风险财务决策不使用该快速规则。

#### 适用场景
见 `quick-decision-shopping/SKILL.md`。

---

## 安装 Skills

本仓库只保留 Skill 源目录，不提交生成后的 `.skill` 二进制包。需要安装时，可在本地从对应目录重新打包后导入 Claude 桌面应用的 Settings → Capabilities → Skills。

```bash
zip -qr personal-effectiveness-system.skill personal-effectiveness-system
zip -qr ai-era-reading.skill ai-era-reading
zip -qr reading-notes-organizer.skill reading-notes-organizer
zip -qr quick-decision-shopping.skill quick-decision-shopping
```

## 维护约定

1. 新增工具时先在“MECE 工具地图”中确认它的独立任务边界。
2. 每个 Skill 的 `description` 必须写清：触发条件、核心产出、与相邻工具的排除边界。
3. 通用提效能力优先放入 `personal-effectiveness-system`；快速日常决策和购物判断放入 `quick-decision-shopping`；阅读理解放入 `ai-era-reading`；已有读书笔记结构化放入 `reading-notes-organizer`。
4. 不提交生成后的 `.skill` 文件；如需分发或安装，在本地按需重新打包。

## 贡献

欢迎提 PR，添加新的个人效率技能。
