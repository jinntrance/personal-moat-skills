#!/usr/bin/env python3
"""Local macOS sleep habit reminders for sleep-quality-coach."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any


CONFIG_DIR = Path.home() / ".config" / "sleep-quality-coach"
CONFIG_PATH = CONFIG_DIR / "config.json"
STATE_DIR = Path.home() / ".local" / "state" / "sleep-quality-coach"
STATE_PATH = STATE_DIR / "state.json"


DEFAULT_CONFIG: dict[str, Any] = {
    "target_bedtime": "23:30",
    "target_wake_time": "07:30",
    "enabled": True,
    "reminders": [
        {
            "id": "morning-sunlight",
            "title": "晨间日光",
            "time": "07:30",
            "body": "出门晒太阳 20-30 分钟，帮今晚的睡眠节律对时。",
            "enabled": True,
        },
        {
            "id": "caffeine-cutoff",
            "title": "咖啡因截止",
            "time": "13:45",
            "body": "现在停止咖啡因：咖啡、茶、可乐、能量饮料明天再喝。",
            "enabled": True,
        },
        {
            "id": "exercise-window",
            "title": "运动窗口",
            "time": "17:30",
            "body": "安排 30-45 分钟有氧运动，别拖到太晚。",
            "enabled": True,
        },
        {
            "id": "dinner-support",
            "title": "晚餐支持",
            "time": "18:30",
            "body": "晚餐加入适量复合碳水，比如燕麦、红薯或米饭。",
            "enabled": True,
        },
        {
            "id": "dim-lights",
            "title": "调暗灯光",
            "offset_minutes_before_bed": 90,
            "body": "调暗灯光并减少蓝光；补剂只在适合自己时使用。",
            "enabled": True,
        },
        {
            "id": "warm-soak",
            "title": "热水澡/泡脚",
            "offset_minutes_before_bed": 60,
            "body": "用 40-42 C 热水淋浴或泡脚 15 分钟，然后让身体自然降温。",
            "enabled": True,
        },
        {
            "id": "cool-room",
            "title": "卧室降温",
            "offset_minutes_before_bed": 30,
            "body": "把卧室调凉，粉红噪音有帮助再打开。",
            "enabled": True,
        },
        {
            "id": "sleep-breathing",
            "title": "入睡呼吸",
            "offset_minutes_before_bed": 0,
            "body": "开始 NSDR 或 4-7-8 呼吸，把手机放远。",
            "enabled": True,
        },
    ],
}


@dataclass(frozen=True)
class DueReminder:
    reminder_id: str
    title: str
    body: str
    scheduled_at: datetime


def parse_hhmm(value: str) -> time:
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise SystemExit(f"Invalid HH:MM time: {value}") from exc


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default.copy()
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def init_config(bedtime: str | None, wake_time: str | None) -> None:
    config = DEFAULT_CONFIG.copy()
    config["reminders"] = [item.copy() for item in DEFAULT_CONFIG["reminders"]]
    if bedtime:
        parse_hhmm(bedtime)
        config["target_bedtime"] = bedtime
    if wake_time:
        parse_hhmm(wake_time)
        config["target_wake_time"] = wake_time
        for reminder in config["reminders"]:
            if reminder["id"] == "morning-sunlight":
                reminder["time"] = wake_time
    save_json(CONFIG_PATH, config)
    print(f"Wrote {CONFIG_PATH}")


def combine(day: date, value: str) -> datetime:
    return datetime.combine(day, parse_hhmm(value))


def scheduled_datetime(reminder: dict[str, Any], config: dict[str, Any], now: datetime) -> datetime:
    if "time" in reminder:
        return combine(now.date(), reminder["time"])
    bedtime = combine(now.date(), config["target_bedtime"])
    wake_time = combine(now.date(), config["target_wake_time"])
    if bedtime < wake_time:
        bedtime += timedelta(days=1)
    return bedtime - timedelta(minutes=int(reminder["offset_minutes_before_bed"]))


def in_window(now: datetime, scheduled: datetime, window_minutes: int) -> bool:
    return scheduled <= now < scheduled + timedelta(minutes=window_minutes)


def sent_key(reminder_id: str, scheduled: datetime) -> str:
    return f"{scheduled.date().isoformat()}::{reminder_id}"


def get_due_reminders(config: dict[str, Any], state: dict[str, Any], now: datetime, window: int) -> list[DueReminder]:
    if not config.get("enabled", True):
        return []

    sent = set(state.get("sent", []))
    due: list[DueReminder] = []
    for reminder in config.get("reminders", []):
        if not reminder.get("enabled", True):
            continue
        scheduled = scheduled_datetime(reminder, config, now)
        key = sent_key(reminder["id"], scheduled)
        if key in sent:
            continue
        if in_window(now, scheduled, window):
            due.append(DueReminder(reminder["id"], reminder["title"], reminder["body"], scheduled))
    return due


def notify(title: str, body: str) -> None:
    script = "\n".join(
        [
            "on run argv",
            '  display notification (item 2 of argv) with title (item 1 of argv) sound name "Submarine"',
            "end run",
        ]
    )
    subprocess.run(["osascript", "-e", script, title, body], check=False)


def mark_sent(state: dict[str, Any], reminders: list[DueReminder]) -> dict[str, Any]:
    sent = list(state.get("sent", []))
    for reminder in reminders:
        sent.append(sent_key(reminder.reminder_id, reminder.scheduled_at))
    cutoff = (datetime.now() - timedelta(days=14)).date().isoformat()
    state["sent"] = [item for item in sent if item[:10] >= cutoff]
    state["last_run_at"] = datetime.now().isoformat(timespec="seconds")
    return state


def print_schedule(config: dict[str, Any]) -> None:
    now = datetime.now()
    rows: list[tuple[datetime, str, str]] = []
    for reminder in config.get("reminders", []):
        if reminder.get("enabled", True):
            rows.append((scheduled_datetime(reminder, config, now), reminder["title"], reminder["body"]))
    for scheduled, title, body in sorted(rows):
        print(f"{scheduled.strftime('%H:%M')}  {title}: {body}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-config", action="store_true", help="Write default config.")
    parser.add_argument("--bedtime", help="Target bedtime as HH:MM.")
    parser.add_argument("--wake-time", help="Target wake time as HH:MM.")
    parser.add_argument("--list", action="store_true", help="Print today's reminder schedule.")
    parser.add_argument("--due", action="store_true", help="Check due reminders and send notifications.")
    parser.add_argument("--notify-test", action="store_true", help="Send a test notification.")
    parser.add_argument("--window-minutes", type=int, default=16)
    args = parser.parse_args()

    if args.init_config:
        init_config(args.bedtime, args.wake_time)
        return 0

    if args.notify_test:
        notify("睡眠提醒测试", "通知可以正常发送。")
        return 0

    config = load_json(CONFIG_PATH, DEFAULT_CONFIG)
    if args.list:
        print_schedule(config)
        return 0

    if args.due:
        state = load_json(STATE_PATH, {"sent": []})
        due = get_due_reminders(config, state, datetime.now(), args.window_minutes)
        for reminder in due:
            notify(reminder.title, reminder.body)
            print(f"sent {reminder.reminder_id} scheduled {reminder.scheduled_at.isoformat(timespec='minutes')}")
        if due:
            save_json(STATE_PATH, mark_sent(state, due))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
