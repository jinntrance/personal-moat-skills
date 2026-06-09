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

## 安装 Skills

将 `.skill` 文件拖入 Claude 桌面应用的 Settings → Capabilities → Skills 即可安装。

## 贡献

欢迎提 PR，添加新的个人效率技能。
