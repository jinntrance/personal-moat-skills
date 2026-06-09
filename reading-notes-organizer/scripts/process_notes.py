#!/usr/bin/env python3
"""
Reading Notes Processor
将读书笔记文件解析并输出结构化 Markdown（含 Mermaid 脑图占位）。
用法：python process_notes.py <notes_file> [--output <output_file>]
"""

import argparse
import re
import sys
from pathlib import Path


def parse_notes(text: str) -> dict:
    """从笔记文本中提取书名、要点等基础结构。"""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]

    # 尝试识别书名（第一行，或《》包裹）
    title = None
    for line in lines[:5]:
        m = re.search(r'[《「『](.+?)[》」』]', line)
        if m:
            title = m.group(1)
            break
    if not title and lines:
        title = lines[0]

    # 提取要点：以 - / * / • 开头，或纯句子
    bullets = []
    for line in lines[1:]:
        clean = re.sub(r'^[-*•·>]\s*', '', line)
        clean = re.sub(r'^P\.\d+[：:]\s*', '', clean)  # 去掉页码
        if clean and len(clean) > 3:
            bullets.append(clean)

    # 识别章节标题（## 或全大写短行）
    sections = {}
    current_section = "主要内容"
    for line in lines[1:]:
        if re.match(r'^#{1,3}\s+', line) or (len(line) < 20 and not line.startswith('-')):
            current_section = re.sub(r'^#+\s*', '', line)
            sections.setdefault(current_section, [])
        else:
            clean = re.sub(r'^[-*•·>]\s*', '', line)
            if clean:
                sections.setdefault(current_section, []).append(clean)

    return {
        "title": title or "未知书目",
        "bullets": bullets,
        "sections": sections,
    }


def truncate(text: str, max_len: int = 12) -> str:
    """截断文字用于脑图节点（去除标点，保持简洁）。"""
    text = re.sub(r'[：:，,。.!！?？""\'"\'【】\[\]（）()]', '', text)
    return text[:max_len]


def generate_mermaid(parsed: dict) -> str:
    """生成 Mermaid mindmap 代码块。"""
    title = truncate(parsed["title"], 8)
    sections = parsed["sections"]

    lines = ["mindmap", f"  root(({title}))"]

    if sections:
        for section, points in list(sections.items())[:8]:  # 最多8个主题
            sec_label = truncate(section, 10)
            lines.append(f"    {sec_label}")
            for point in points[:5]:  # 每主题最多5个子点
                point_label = truncate(point, 12)
                lines.append(f"      {point_label}")
    else:
        # 无章节：直接列要点
        for bullet in parsed["bullets"][:10]:
            lines.append(f"    {truncate(bullet, 12)}")

    return "```mermaid\n" + "\n".join(lines) + "\n```"


def generate_markdown_outline(parsed: dict) -> str:
    """生成 Markdown 层级大纲。"""
    title = parsed["title"]
    sections = parsed["sections"]

    out = [f"# 《{title}》\n"]

    if sections:
        for section, points in sections.items():
            out.append(f"## {section}")
            for point in points:
                out.append(f"- {point}")
            out.append("")
    else:
        out.append("## 核心要点")
        for bullet in parsed["bullets"]:
            out.append(f"- {bullet}")

    return "\n".join(out)


def generate_key_notes(parsed: dict, max_notes: int = 7) -> str:
    """提取关键笔记（取最有信息量的条目）。"""
    all_points = parsed["bullets"][:]
    for pts in parsed["sections"].values():
        all_points.extend(pts)

    # 按长度降序（更长的通常信息更丰富）
    ranked = sorted(set(all_points), key=len, reverse=True)[:max_notes]

    notes = []
    for i, point in enumerate(ranked, 1):
        notes.append(f"> **洞见 {i}**\n> {point}")

    return "\n\n".join(notes)


def process(text: str) -> str:
    parsed = parse_notes(text)
    title = parsed["title"]

    sections_out = [
        f"## 📚 《{title}》读书笔记整理\n",
        "### 🗺️ Mermaid 脑图\n",
        generate_mermaid(parsed),
        "\n---\n",
        "### 📋 Markdown 大纲脑图\n",
        "```markdown",
        generate_markdown_outline(parsed),
        "```",
        "\n---\n",
        "### 💡 关键笔记\n",
        generate_key_notes(parsed),
    ]
    return "\n".join(sections_out)


def main():
    parser = argparse.ArgumentParser(description="读书笔记整理工具")
    parser.add_argument("input", nargs="?", help="笔记文件路径（不填则读 stdin）")
    parser.add_argument("--output", "-o", help="输出文件路径（不填则输出到 stdout）")
    args = parser.parse_args()

    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    result = process(text)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"✅ 已保存到 {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
