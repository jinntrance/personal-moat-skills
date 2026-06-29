#!/usr/bin/env python3
"""Bulk export personal WeRead notes to local JSON files.

The script uses the official WeRead Agent API through weread-plus helpers.
It is intentionally resumable: existing per-book JSON files are skipped unless
--force is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

def weread_plus_scripts_dir() -> Path:
    candidates = [
        Path(value).expanduser()
        for value in [
            os.environ.get("WEREAD_PLUS_SCRIPTS", ""),
            "~/.claude/skills/weread-plus/scripts",
            "~/.codex/skills/weread-plus/scripts",
        ]
        if value
    ]
    for candidate in candidates:
        if (candidate / "weread_common.py").exists():
            return candidate
    raise SystemExit("Cannot find weread-plus scripts. Set WEREAD_PLUS_SCRIPTS=/path/to/weread-plus/scripts")


sys.path.insert(0, str(weread_plus_scripts_dir()))

from weread_common import api_post, book_author, book_id, book_title, json_dumps  # noqa: E402
from weread_notes_export import export_data  # noqa: E402


def with_retries(label: str, fn, attempts: int = 4, base_sleep: float = 1.0):
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - API/network retries are best effort.
            last_exc = exc
            if attempt == attempts:
                break
            wait = base_sleep * attempt
            print(f"{label}: retry {attempt}/{attempts - 1} after {exc}", file=sys.stderr)
            time.sleep(wait)
    assert last_exc is not None
    raise last_exc


def safe_slug(text: str, fallback: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\s]+", "_", text).strip("._")
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned[:90] or fallback


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_dumps(data) + "\n", encoding="utf-8")


def fetch_notebooks(limit: int | None = None, page_size: int = 100, sleep: float = 0.25) -> list[dict[str, Any]]:
    books: list[dict[str, Any]] = []
    last_sort: int | None = None
    while True:
        params: dict[str, Any] = {"count": page_size}
        if last_sort is not None:
            params["lastSort"] = last_sort
        data = with_retries("fetch notebooks", lambda: api_post("/user/notebooks", params))
        page = data.get("books") or []
        books.extend(page)
        if limit and len(books) >= limit:
            return books[:limit]
        if not data.get("hasMore") or not page:
            return books
        last_sort = page[-1].get("sort")
        if not last_sort:
            return books
        time.sleep(sleep)


def clean_book_from_notebook(item: dict[str, Any]) -> dict[str, Any]:
    book = item.get("book") if isinstance(item.get("book"), dict) else {}
    if "bookId" not in book and item.get("bookId"):
        book = {**book, "bookId": item["bookId"]}
    return book


def notebook_summary(item: dict[str, Any]) -> dict[str, Any]:
    book = clean_book_from_notebook(item)
    return {
        "source": "weread",
        "sourceBookId": book_id(book),
        "title": book_title(book),
        "author": book_author(book),
        "reviewCount": item.get("reviewCount") or 0,
        "highlightCount": item.get("noteCount") or 0,
        "bookmarkCount": item.get("bookmarkCount") or 0,
        "readingProgress": item.get("readingProgress"),
        "markedStatus": item.get("markedStatus"),
        "sort": item.get("sort"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk export personal WeRead notes")
    parser.add_argument("--out-dir", default="data/weread", help="Output directory")
    parser.add_argument("--limit", type=int, help="Only export the first N books")
    parser.add_argument("--sleep", type=float, default=0.35, help="Delay between book exports")
    parser.add_argument("--force", action="store_true", help="Overwrite existing per-book JSON files")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    books_dir = out_dir / "books"
    notebooks = fetch_notebooks(limit=args.limit)
    summaries = [notebook_summary(item) for item in notebooks]
    write_json(out_dir / "notebooks.json", summaries)

    exported = 0
    skipped = 0
    failed: list[dict[str, str]] = []
    for index, item in enumerate(notebooks, 1):
        book = clean_book_from_notebook(item)
        bid = book_id(book)
        title = book_title(book)
        slug = safe_slug(f"{title}_{book_author(book)}_{bid}", bid or f"book_{index}")
        path = books_dir / f"{slug}.json"
        if path.exists() and not args.force:
            skipped += 1
            continue
        try:
            data = with_retries(f"export {title}", lambda: export_data(book))
            data["notebook"] = notebook_summary(item)
            write_json(path, data)
            exported += 1
            print(f"[{index}/{len(notebooks)}] exported {title} -> {path.name}")
        except Exception as exc:  # noqa: BLE001 - keep long export moving.
            failed.append({"bookId": bid, "title": title, "error": str(exc)})
            print(f"[{index}/{len(notebooks)}] failed {title}: {exc}", file=sys.stderr)
        time.sleep(args.sleep)

    write_json(out_dir / "failures.json", failed)
    print(json.dumps({"books": len(notebooks), "exported": exported, "skipped": skipped, "failed": len(failed), "outDir": str(out_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
