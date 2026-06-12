# Personal Moat Skills

个人护城河技能库 — 提升个人效率、知识管理的 Claude Skills 集合。

## 技能列表

### 📚 reading-notes-organizer — 读书笔记整理工具

将杂乱的读书笔记自动转化为：
- **Mermaid 脑图** — 可直接在 Obsidian/GitHub 渲染
- **Markdown 层级大纲** — 适合 Notion/Logseq
- **关键笔记摘要** — 提取最有价值的洞见

**触发方式：** 粘贴读书笔记，说"帮我整理成脑图"

#### 快速使用（命令行）
```bash
python reading-notes-organizer/scripts/process_notes.py my_notes.md
# 或
cat my_notes.md | python reading-notes-organizer/scripts/process_notes.py --output result.md
```

#### 示例
见 `reading-notes-organizer/examples/sample_notes.md`

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

## 安装 Skills

将 `.skill` 文件拖入 Claude 桌面应用的 Settings → Capabilities → Skills 即可安装。

## 贡献

欢迎提 PR，添加新的个人效率技能。
