#!/usr/bin/env python3
"""Export Douban book annotations, reviews, and collection comments.

This uses the persistent Playwright profile documented by the local
douban-bookmark skill. Public profile exports can run with --user-id and do not
require login. Run with --login --headed only when private/login-only pages are
needed.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


DEFAULT_PROFILE = Path("~/.openclaw/browser-profiles/douban-playwright").expanduser()


def safe_text(value: Any) -> str:
    return re.sub(r"\s+", " ", value.get_text(" ", strip=True) if hasattr(value, "get_text") else str(value or "")).strip()


def subject_id_from_url(url: str) -> str:
    match = re.search(r"/subject/(\d+)/?", url)
    return match.group(1) if match else ""


def annotation_id_from_url(url: str) -> str:
    match = re.search(r"/annotation/(\d+)/?", url)
    return match.group(1) if match else ""


def review_id_from_url(url: str) -> str:
    match = re.search(r"/review/(\d+)/?", url)
    return match.group(1) if match else ""


def star_from_classes(classes: list[str]) -> int | None:
    joined = " ".join(classes)
    match = re.search(r"rating(\d)-t", joined)
    return int(match.group(1)) if match else None


def find_user_id(page) -> str:
    page.goto("https://www.douban.com/mine/", wait_until="domcontentloaded", timeout=30000)
    if "passport/login" in page.url:
        return ""
    match = re.search(r"/people/([^/]+)/?", page.url)
    if match:
        return match.group(1)
    soup = BeautifulSoup(page.content(), "html.parser")
    link = soup.select_one("a[href*='/people/']")
    if not link:
        return ""
    match = re.search(r"/people/([^/]+)/?", link.get("href", ""))
    return match.group(1) if match else ""


def root_for_link(link):
    for parent in link.parents:
        if parent.name in {"li", "tr"}:
            return parent
        classes = parent.get("class") or []
        if any(cls in classes for cls in ["item", "review-item", "annotation-item", "subject-item"]):
            return parent
    return link.parent or link


def extract_subject_items(html: str, item_type: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    seen: set[tuple[str, str]] = set()
    items: list[dict[str, Any]] = []
    for link in soup.select("a[href*='book.douban.com/subject/'], a[href^='/subject/']"):
        href = urljoin("https://book.douban.com", link.get("href", ""))
        sid = subject_id_from_url(href)
        title = safe_text(link)
        if not sid or not title:
            continue
        root = root_for_link(link)
        raw_text = safe_text(root)
        if len(raw_text) < len(title):
            raw_text = title
        rating_node = root.select_one("[class*='rating'][class*='-t']")
        star = star_from_classes(rating_node.get("class") or []) if rating_node else None
        comment_node = root.select_one(".comment, .short-note, .review-short, blockquote")
        date_node = root.select_one(".date, .pubtime, .pl")
        key = (sid, raw_text[:80])
        if key in seen:
            continue
        seen.add(key)
        items.append(
            {
                "source": "douban",
                "type": item_type,
                "subjectId": sid,
                "subjectUrl": href,
                "title": title,
                "star": star,
                "comment": safe_text(comment_node) if comment_node else "",
                "dateText": safe_text(date_node) if date_node else "",
                "rawText": raw_text,
            }
        )
    return items


def extract_annotation_items(html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    results = extract_subject_items(html, "annotation")
    by_sid = {item["subjectId"]: item for item in results}
    for link in soup.select("a[href*='/annotation/']"):
        root = root_for_link(link)
        subject = root.select_one("a[href*='/subject/']")
        href = urljoin("https://book.douban.com", link.get("href", ""))
        sid = subject_id_from_url(subject.get("href", "")) if subject else ""
        item = by_sid.get(sid) or {"source": "douban", "type": "annotation", "subjectId": sid, "subjectUrl": "", "title": safe_text(subject) if subject else ""}
        item["annotationId"] = annotation_id_from_url(href)
        item["annotationUrl"] = href
        item["rawText"] = safe_text(root)
        if sid:
            by_sid[sid] = item
    return list(by_sid.values())


def extract_review_items(html: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    items: list[dict[str, Any]] = []
    for root in soup.select(".tlst"):
        subject_link = root.select_one(".ilst a[href*='/subject/'], .starb a[href*='/subject/']")
        review_link = root.select_one("h3 a[href*='/review/'], .rr a[href*='/review/']")
        if not subject_link or not review_link:
            continue
        subject_url = urljoin("https://book.douban.com", subject_link.get("href", ""))
        review_url = urljoin("https://book.douban.com", review_link.get("href", ""))
        rating_node = root.select_one("[class*='allstar']")
        star = None
        if rating_node:
            match = re.search(r"allstar(\d+)", " ".join(rating_node.get("class") or []))
            if match:
                star = int(match.group(1)) // 10
        comment_node = root.select_one(".review-short")
        title = review_link.get("title") or safe_text(review_link)
        subject_title = subject_link.get("title") or safe_text(subject_link)
        items.append(
            {
                "source": "douban",
                "type": "review",
                "subjectId": subject_id_from_url(subject_url),
                "subjectUrl": subject_url,
                "title": subject_title,
                "reviewTitle": title,
                "reviewId": review_id_from_url(review_url),
                "reviewUrl": review_url,
                "star": star,
                "comment": safe_text(comment_node) if comment_node else "",
                "rawText": safe_text(root),
            }
        )
    return items


def enrich_detail_pages(page, items: list[dict[str, Any]], url_key: str, sleep: float, limit: int | None) -> None:
    enriched = 0
    for item in items:
        if limit is not None and enriched >= limit:
            return
        url = item.get(url_key)
        if not url:
            continue
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            soup = BeautifulSoup(page.content(), "html.parser")
            content = soup.select_one(".review-content, .article .indent, .annotation, #link-report")
            title = soup.select_one("h1, .article h1")
            item["detailTitle"] = safe_text(title) if title else ""
            item["detailText"] = safe_text(content) if content else safe_text(soup.select_one("body"))
            item["detailUrl"] = page.url
            enriched += 1
            time.sleep(sleep)
        except Exception as exc:  # noqa: BLE001
            item["detailError"] = str(exc)


def paged_export(page, base_url: str, extractor, sleep: float, max_pages: int, page_size: int) -> list[dict[str, Any]]:
    all_items: list[dict[str, Any]] = []
    seen_pages: set[str] = set()
    start = 0
    for _ in range(max_pages):
        url = base_url.format(start=start)
        if url in seen_pages:
            break
        seen_pages.add(url)
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        if "passport/login" in page.url:
            raise RuntimeError("Douban profile is not logged in. Run --login --headed first.")
        items = extractor(page.content())
        if not items:
            break
        all_items.extend(items)
        start += page_size
        time.sleep(sleep)
    return all_items


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Douban book notes and comments")
    parser.add_argument("--out-dir", default="data/douban")
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--user-id", help="Douban user ID, e.g. jinntrance")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--login", action="store_true", help="Open login page and wait")
    parser.add_argument("--sleep", type=float, default=1.2)
    parser.add_argument("--max-pages", type=int, default=200)
    parser.add_argument("--detail-limit", type=int, default=0, help="Fetch up to N review/annotation detail pages; 0 disables detail fetch")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(args.profile, headless=not args.headed)
        page = ctx.new_page()
        if args.login:
            page.goto("https://accounts.douban.com/passport/login", wait_until="domcontentloaded", timeout=30000)
            print("请在打开的豆瓣窗口中登录。登录完成后回到这里按 Ctrl-C 停止，或等待脚本超时。")
            page.wait_for_timeout(180_000)
            ctx.close()
            return

        user_id = args.user_id or find_user_id(page)
        if not user_id:
            ctx.close()
            raise SystemExit("Provide --user-id or log in with: python3 reading-notes-sync/douban_export.py --login --headed")

        annotations = paged_export(page, f"https://book.douban.com/people/{user_id}/annotation?start={{start}}", extract_annotation_items, args.sleep, args.max_pages, 10)
        reviews = paged_export(page, f"https://book.douban.com/people/{user_id}/reviews?start={{start}}", extract_review_items, args.sleep, args.max_pages, 10)
        collections = paged_export(page, f"https://book.douban.com/people/{user_id}/collect?start={{start}}&sort=time&rating=all&filter=all&mode=list", lambda html: extract_subject_items(html, "collection"), args.sleep, args.max_pages, 30)
        detail_limit = args.detail_limit or None
        if detail_limit:
            enrich_detail_pages(page, reviews, "reviewUrl", args.sleep, detail_limit)
            enrich_detail_pages(page, annotations, "annotationUrl", args.sleep, detail_limit)
        ctx.close()

    write_json(out_dir / "annotations.json", annotations)
    write_json(out_dir / "reviews.json", reviews)
    write_json(out_dir / "collections.json", collections)
    merged = annotations + reviews + collections
    write_json(out_dir / "all.json", merged)
    print(json.dumps({"userId": user_id, "annotations": len(annotations), "reviews": len(reviews), "collections": len(collections), "outDir": str(out_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
