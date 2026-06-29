---
name: reading-notes-sync
description: 豆瓣读书与微信读书笔记同步归并工作流。Use when the user wants to export, update, deduplicate, or merge WeRead/微信读书 highlights, thoughts, public reviews, and Douban/豆瓣读书 read-list comments, reviews, annotations, ratings, tags, and book records into local JSON files.
---

# Reading Notes Sync

Export and merge reading data from WeRead and Douban into local JSON files.

## Scope

Use this skill when the user wants to:

- Export WeRead personal highlights, thoughts, and per-book public reviews.
- Export Douban read-list records, ratings, short comments, public reviews, and public annotations.
- Merge and deduplicate the two sources by normalized title/author.
- Refresh an existing local reading-note archive.

Do not use this skill for reading coaching or note interpretation. Route those to `ai-era-reading` or `reading-notes-organizer` after export.

## Files

Scripts are in `scripts/`:

- `weread_bulk_export.py` — exports WeRead personal notes to `data/weread/books/*.json`.
- `weread_public_reviews_export.py` — appends WeRead public reviews into each exported book JSON as `publicReviews`.
- `douban_export.py` — exports Douban public reviews, public annotations, and collection/list pages.
- `merge_reading_notes.py` — merges WeRead and Douban exports into one `merged_books.json`.

## Requirements

WeRead:

- `WEREAD_API_KEY` must be set.
- `weread-plus` scripts must be installed. The scripts search:
  - `$WEREAD_PLUS_SCRIPTS`
  - `~/.claude/skills/weread-plus/scripts`
  - `~/.codex/skills/weread-plus/scripts`

Douban:

- Public profile exports only need a Douban user ID, e.g. from `https://book.douban.com/people/<id>/reviews`.
- Browser/detail export uses Playwright and BeautifulSoup.
- For richer read-list fields, use a separate Douban public-list skill if installed; otherwise `douban_export.py` still captures collection page records.

## Workflow

Use a workspace output directory such as `reading-notes-sync/data`.

1. Export WeRead personal notes:

```bash
python3 scripts/weread_bulk_export.py --out-dir data/weread --sleep 0.35
```

2. Append WeRead public reviews:

```bash
python3 scripts/weread_public_reviews_export.py --weread-dir data/weread --limit 20 --sleep 0.25 --full-content
```

3. Export Douban public reviews, annotations, and collection list:

```bash
python3 scripts/douban_export.py --user-id <douban_user_id> --out-dir data/douban --max-pages 200 --sleep 1.0 --detail-limit 1000
```

4. If the `douban-fbfl` skill is installed, export detailed Douban read-list records:

```bash
python3 ~/.claude/skills/douban-fbfl/fetch_douban.py --user <douban_user_id> --output "$PWD/data/douban/douban_books.json" --format json --type collect
```

5. Merge and deduplicate:

```bash
python3 scripts/merge_reading_notes.py --weread-dir data/weread --douban-dir data/douban --out data/merged_books.json
```

## Data Model

Expected output:

```text
data/
├── weread/
│   ├── notebooks.json
│   ├── failures.json
│   ├── public_review_failures.json
│   └── books/*.json
├── douban/
│   ├── douban_books.json
│   ├── reviews.json
│   ├── collections.json
│   ├── annotations.json
│   └── all.json
└── merged_books.json
```

`merged_books.json` groups source records and reports counts:

- `wereadHighlights`
- `wereadThoughts`
- `wereadPublicReviews`
- `doubanItems`

## Reliability Rules

- All exporters are safe to rerun. WeRead personal-note and public-review scripts skip existing data unless `--force` is used.
- Keep delays enabled for Douban and WeRead. If SSL EOF or temporary network errors appear, rerun the same command; completed files are skipped.
- Treat Douban annotations returning `[]` as valid when the user has no public annotations or the page is private.
- Do not print API keys or private notes into chat. Store exports in local files and summarize counts.
