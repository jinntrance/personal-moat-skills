#!/usr/bin/env python3
"""Merge and deduplicate WeRead and Douban reading-note exports."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(text: Any) -> str:
    value = str(text or "").lower()
    value = re.sub(r"[（(].*?[）)]", "", value)
    value = re.sub(r"[\s:：,，.。;；!！?？·《》<>〈〉\"'“”‘’\-_—]+", "", value)
    return value.strip()


def normalize_author(text: Any) -> str:
    value = str(text or "")
    value = re.sub(r"\[[^\]]+\]|\([^)]+\)|（[^）]+）", "", value)
    value = re.sub(r"等|著|编|作者", "", value)
    return normalize_text(value)


def merge_key(title: str, author: str = "", subject_id: str = "") -> str:
    title_key = normalize_text(title)
    author_key = normalize_author(author)
    if title_key and author_key:
        return f"title_author:{title_key}:{author_key[:16]}"
    if title_key:
        return f"title:{title_key}"
    return f"source_id:{subject_id}"


def weread_records(weread_dir: Path) -> list[dict[str, Any]]:
    records = []
    for path in sorted((weread_dir / "books").glob("*.json")):
        data = load_json(path, {})
        book = data.get("book") or {}
        notebook = data.get("notebook") or {}
        records.append(
            {
                "source": "weread",
                "sourceBookId": str(book.get("bookId") or notebook.get("sourceBookId") or ""),
                "title": book.get("title") or notebook.get("title") or "",
                "author": book.get("author") or notebook.get("author") or "",
                "path": str(path),
                "highlightCount": len(data.get("highlights") or []),
                "thoughtCount": len(data.get("thoughts") or []),
                "publicReviewCount": len((data.get("publicReviews") or {}).get("reviews") or []),
                "notebook": notebook,
            }
        )
    return records


def douban_records(douban_dir: Path) -> list[dict[str, Any]]:
    items = load_json(douban_dir / "all.json", [])
    public_books = load_json(douban_dir / "douban_books.json", [])
    if isinstance(public_books, list):
        for item in public_books:
            if not isinstance(item, dict):
                continue
            items.append(
                {
                    "source": "douban",
                    "type": "collection",
                    "subjectId": item.get("豆瓣ID") or "",
                    "subjectUrl": item.get("豆瓣链接") or "",
                    "title": item.get("书名") or "",
                    "author": item.get("作者") or "",
                    "star": item.get("我的评分") or "",
                    "comment": item.get("我的评论") or "",
                    "dateText": item.get("阅读日期") or "",
                    "status": item.get("状态") or "",
                    "tags": item.get("标签") or "",
                    "raw": item,
                }
            )
    records = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        sid = str(item.get("subjectId") or "")
        key = sid or merge_key(item.get("title") or "", "", sid)
        grouped[key].append(item)
    for key, group in grouped.items():
        first = group[0]
        records.append(
            {
                "source": "douban",
                "sourceBookId": first.get("subjectId") or key,
                "title": first.get("title") or "",
                "author": first.get("author") or "",
                "subjectUrl": first.get("subjectUrl") or "",
                "itemCount": len(group),
                "items": group,
            }
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge WeRead and Douban note exports")
    parser.add_argument("--weread-dir", default="data/weread")
    parser.add_argument("--douban-dir", default="data/douban")
    parser.add_argument("--out", default="data/merged_books.json")
    args = parser.parse_args()

    weread_dir = Path(args.weread_dir).expanduser().resolve()
    douban_dir = Path(args.douban_dir).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    groups: dict[str, dict[str, Any]] = {}
    for record in weread_records(weread_dir) + douban_records(douban_dir):
        key = merge_key(record.get("title") or "", record.get("author") or "", record.get("sourceBookId") or "")
        group = groups.setdefault(
            key,
            {
                "key": key,
                "canonicalTitle": record.get("title") or "",
                "canonicalAuthor": record.get("author") or "",
                "sources": [],
                "sourceIds": {},
                "counts": {"wereadHighlights": 0, "wereadThoughts": 0, "wereadPublicReviews": 0, "doubanItems": 0},
            },
        )
        group["sources"].append(record)
        group["sourceIds"][record["source"]] = record.get("sourceBookId")
        if record["source"] == "weread":
            group["counts"]["wereadHighlights"] += int(record.get("highlightCount") or 0)
            group["counts"]["wereadThoughts"] += int(record.get("thoughtCount") or 0)
            group["counts"]["wereadPublicReviews"] += int(record.get("publicReviewCount") or 0)
        if record["source"] == "douban":
            group["counts"]["doubanItems"] += int(record.get("itemCount") or 0)

    merged = sorted(groups.values(), key=lambda item: (len(item["sources"]) < 2, normalize_text(item["canonicalTitle"])))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    duplicates = sum(1 for item in merged if len({src["source"] for src in item["sources"]}) > 1)
    print(json.dumps({"mergedBooks": len(merged), "crossSourceMatches": duplicates, "out": str(out_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
