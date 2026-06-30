---
name: sleep-quality-coach
description: Personal sleep improvement workflow and reminder automation. Use when the user wants to improve sleep quality, increase deep sleep, build an evening routine, reduce caffeine/light disruption, create sleep hygiene checklists, review sleep logs, or set up timed macOS reminders for sleep-related habits.
---

# Sleep Quality Coach

## Core Workflow

Use this skill to turn sleep goals into a daily behavior plan and, when useful, timed local reminders.

1. Identify the user's target wake time, target bedtime, current sleep symptoms, caffeine intake, exercise timing, evening screen/light exposure, and any tracked metrics such as deep sleep, sleep latency, awakenings, or resting HR.
2. Build a small daily plan around the default intervention sequence in `references/intervention-plan.md`.
3. Prefer behavior changes before supplements. If supplements are discussed, frame them as optional and tell the user to consider medical context, medications, pregnancy, kidney disease, or clinician guidance.
4. Keep reminders concrete, time-bound, and actionable. Avoid vague reminders such as "sleep better."
5. If the user asks for automation, use `scripts/sleep_reminder.py` and `scripts/install_launch_agent.sh`.

## Reminder Automation

Use the bundled scripts for local macOS notifications:

```bash
python3 scripts/sleep_reminder.py --init-config
python3 scripts/sleep_reminder.py --list
bash scripts/install_launch_agent.sh
```

The reminder script:

- Reads `~/.config/sleep-quality-coach/config.json`.
- Sends macOS notifications through `osascript`.
- Runs safely every 15 minutes and records sent reminders in `~/.local/state/sleep-quality-coach/state.json`.
- Calculates bedtime-relative reminders from `target_bedtime`.

Before installing automation, set or confirm `target_bedtime` and `target_wake_time` in the config when the user has a known schedule. If no schedule is provided, default to `23:30` bedtime and `07:30` wake time.

Useful commands:

```bash
python3 scripts/sleep_reminder.py --init-config --bedtime 23:30 --wake-time 07:30
python3 scripts/sleep_reminder.py --due
python3 scripts/sleep_reminder.py --notify-test
launchctl print gui/$(id -u)/com.codex.sleep-quality-coach
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.codex.sleep-quality-coach.plist
```

## Review Pattern

When reviewing progress, use a 7-day view:

- Target metric: deep sleep minutes, sleep latency, awakenings, total sleep time, subjective morning energy.
- Check adherence to morning sunlight, caffeine cutoff, exercise timing, dinner timing, light control, warm bath/foot soak, bedroom cooling, and breathing/NSDR.
- Change only one or two variables per week unless the user asks for a full reset.
- Treat persistent insomnia, breathing interruptions, heavy snoring, severe daytime sleepiness, or mood deterioration as reasons to seek professional medical evaluation.
