#!/usr/bin/env python3
"""Add public WeRead book reviews to existing per-book exports.

This is separate from weread_bulk_export.py so previously exported personal
notes do not need to be fetched again.
"""

from __future__ import annotations

import argparse
import json
import os
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

from weread_common import api_post, book_id, book_title, json_dumps, timestamp_to_date  # noqa: E402
from weread_reviews import REVIEW_TYPES, clean_review_item  # noqa: E402


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json_dumps(data) + "\n", encoding="utf-8")


def with_retries(label: str, fn, attempts: int = 4, base_sleep: float = 1.0):
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - keep long export moving.
            last_exc = exc
            if attempt == attempts:
                break
            wait = base_sleep * attempt
            print(f"{label}: retry {attempt}/{attempts - 1} after {exc}", file=sys.stderr)
            time.sleep(wait)
    assert last_exc is not None
    raise last_exc


def public_reviews_paginated(book: dict[str, Any], review_type: str, limit: int, page_size: int, *, full_content: bool) -> dict[str, Any]:
    bid = book_id(book)
    if not bid.isdigit():
        return {
            "summary": {
                "reviewType": review_type,
                "exportLimit": limit,
                "exportedAt": timestamp_to_date(int(time.time())),
                "skipped": True,
                "skipReason": "public review endpoint only accepts regular numeric WeRead book IDs",
            },
            "reviews": [],
        }
    reviews: list[dict[str, Any]] = []
    max_idx = 0
    synckey = 0
    summary: dict[str, Any] = {}

    while len(reviews) < limit:
        count = min(page_size, limit - len(reviews))
        params: dict[str, Any] = {
            "bookId": bid,
            "reviewListType": REVIEW_TYPES[review_type],
            "count": count,
        }
        if max_idx:
            params["maxIdx"] = max_idx
        if synckey:
            params["synckey"] = synckey
        data = api_post("/review/list", params)
        page = data.get("reviews") or []
        if not summary:
            summary = {
                "reviewType": review_type,
                "reviewsCnt": data.get("reviewsCnt"),
                "recentTotalCnt": data.get("recentTotalCnt"),
                "reviewsHasMore": data.get("reviewsHasMore"),
                "reviewsHas5Star": data.get("reviewsHas5Star"),
                "reviewsHas1Star": data.get("reviewsHas1Star"),
                "friendCommentCount": data.get("friendCommentCount"),
                "friendUniqueCount": data.get("friendUniqueCount"),
                "deepVRecommendInfo": data.get("deepVRecommendInfo"),
                "deepVRecommendValue": data.get("deepVRecommendValue"),
                "deepVUniqueCount": data.get("deepVUniqueCount"),
                "exportedAt": timestamp_to_date(int(time.time())),
                "exportLimit": limit,
            }
        reviews.extend([clean_review_item(item, full_content=full_content) for item in page])
        if not data.get("reviewsHasMore") or not page:
            break
        last_idx = page[-1].get("idx")
        if last_idx in (None, ""):
            break
        max_idx = last_idx
        synckey = data.get("synckey") or synckey
        time.sleep(0.15)

    return {
        "summary": summary or {"reviewType": review_type, "exportLimit": limit, "exportedAt": timestamp_to_date(int(time.time()))},
        "reviews": reviews,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export public WeRead reviews into existing book JSON files")
    parser.add_argument("--weread-dir", default="data/weread")
    parser.add_argument("--limit", type=int, default=20, help="Max public reviews per book")
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--type", choices=tuple(REVIEW_TYPES), default="all")
    parser.add_argument("--sleep", type=float, default=0.35)
    parser.add_argument("--full-content", action="store_true", help="Store full returned public review content")
    parser.add_argument("--force", action="store_true", help="Refresh reviews even when already present")
    parser.add_argument("--max-books", type=int, help="Only process the first N book files")
    args = parser.parse_args()

    weread_dir = Path(args.weread_dir).expanduser().resolve()
    book_files = sorted((weread_dir / "books").glob("*.json"))
    if args.max_books:
        book_files = book_files[: args.max_books]

    exported = 0
    skipped = 0
    failed: list[dict[str, str]] = []
    for index, path in enumerate(book_files, 1):
        data = read_json(path)
        if data.get("publicReviews") and not args.force:
            skipped += 1
            continue
        book = data.get("book") or {}
        title = book_title(book) or path.stem
        try:
            reviews = with_retries(
                f"public reviews {title}",
                lambda: public_reviews_paginated(book, args.type, args.limit, args.page_size, full_content=args.full_content),
            )
            data["publicReviews"] = reviews
            write_json(path, data)
            exported += 1
            print(f"[{index}/{len(book_files)}] reviews {len(reviews.get('reviews') or [])}: {title}")
        except Exception as exc:  # noqa: BLE001
            failed.append({"path": str(path), "title": title, "error": str(exc)})
            print(f"[{index}/{len(book_files)}] failed {title}: {exc}", file=sys.stderr)
        time.sleep(args.sleep)

    write_json(weread_dir / "public_review_failures.json", failed)
    print(json.dumps({"books": len(book_files), "exported": exported, "skipped": skipped, "failed": len(failed), "wereadDir": str(weread_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
