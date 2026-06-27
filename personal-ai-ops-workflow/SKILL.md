---
name: personal-ai-ops-workflow
description: 个人 AI 运营管家工作流。Use when the user wants to organize personal productivity around TickTick/滴答清单 tasks, RescueTime time logs, software development activity, GitHub/Git commits, knowledge base notes, daily planning, weekly review, personal moat building, workflow automation, or asking AI to act as a secretary/operator who prepares briefs, drafts outputs, tracks follow-ups, and waits for human feedback before committing important changes.
---

# Personal AI Ops Workflow

## Operating Principle

Build a human-in-the-loop personal operating system:

1. The user owns reality capture, judgment, priorities, and final feedback.
2. AI owns ingestion, synthesis, candidate outputs, reminders, and consistency checks.
3. Automation starts as observation and suggestion; only stable, low-risk routines graduate to direct execution.

Default stance: **AI proposes, the user confirms, AI records the feedback, then the system improves.**

## Core Data Layers

Use these layers when designing or running the workflow:

| Layer | Source | Purpose | AI responsibility |
|---|---|---|---|
| Task | TickTick / 滴答清单 | Actions, reminders, waiting-for, project next steps | Read tasks, detect drift, propose changes, create/update only after confirmation |
| Time | RescueTime | Actual behavior and attention allocation | Compare plan vs reality, detect focus patterns, generate review evidence |
| Development | Git, GitHub, local repos, issues, PRs | Real output and project state | Summarize progress, identify blockers, propose next engineering actions |
| Knowledge | Markdown/Obsidian/Notion-style notes | Reusable thinking, decisions, workflows, prompts | Distill raw inputs into notes, decisions, MOCs, and candidate skills |
| Feedback | User accept/edit/reject signals | Personal preference and judgment calibration | Record why suggestions worked or failed; adjust future briefs |

If a connector or API is unavailable, ask the user for exported text/CSV/screenshots or summarize from the provided context instead of blocking.

## Workflow Router

Choose the smallest useful workflow:

- **Daily start brief**: user asks what to focus on today, wants a morning plan, or shares today's tasks.
- **Daily shutdown review**: user asks what happened today, why tasks slipped, or wants tomorrow's candidate plan.
- **Weekly review**: user asks for weekly summary, GTD review, project/accountability review, or time allocation analysis.
- **Knowledge distillation**: user shares articles, conversations, development lessons, decisions, or messy notes to preserve.
- **Development operator**: user wants AI to manage project context, read a repo, track TODOs, prepare issues/PR notes, or extract reusable workflows from engineering work.
- **Automation/SKILL extraction**: the same workflow has appeared at least three times or has a clear trigger, input, output, and validation rule.

For detailed output templates, read `references/templates.md` when producing a recurring brief, review, knowledge entry, or skill-candidate report.

## Daily Start Brief

Goal: turn commitments and recent evidence into a realistic operating plan.

1. Gather inputs:
   - TickTick: today, overdue, high-priority, waiting-for, and project tasks.
   - Calendar if available: hard constraints and meetings.
   - RescueTime from yesterday or the last work session.
   - Recent development activity: Git commits, PRs, issues, local TODOs.
   - Any user-stated energy, constraints, or deadlines.
2. Normalize commitments into:
   - Must do today
   - Should do if capacity allows
   - Waiting / blocked
   - Candidate defer/delete/delegate
3. Produce a brief with:
   - Top 3 focus outcomes
   - A realistic time budget
   - Risks and likely interruptions
   - Proposed task edits, not silent edits
   - One knowledge/workflow item worth capturing
4. Ask for confirmation before creating, deleting, rescheduling, or reprioritizing tasks.

## Daily Shutdown Review

Goal: convert the day into learning and a cleaner tomorrow.

1. Compare planned tasks against completed tasks and RescueTime evidence.
2. Separate unfinished work by cause:
   - Bad estimate
   - External interruption
   - Avoidance / unclear next action
   - Blocked dependency
   - No longer important
3. Summarize real output, not just activity.
4. Propose tomorrow's candidates and any task hygiene changes.
5. Capture one lesson, decision, or reusable workflow if present.

## Weekly Review

Goal: identify patterns that daily review cannot see.

1. Aggregate:
   - TickTick completed/overdue/rescheduled tasks
   - RescueTime category totals and top apps/sites
   - Git/GitHub project movement
   - Notes, decisions, and unfinished loops
2. Produce:
   - Weekly theme
   - Output inventory
   - Attention allocation vs intended priorities
   - Stuck projects and next actions
   - Commitments to renegotiate
   - Workflows repeated enough to automate
3. End with a small next-week plan: no more than 3 priorities and 5 operational next actions.

## Knowledge Distillation

Goal: transform raw information into personal moat assets.

Use this pipeline:

1. Capture raw source without over-cleaning.
2. Distill into atomic notes only when the note has future use.
3. Link the note to a project, decision, person, workflow, or recurring problem.
4. Create a decision record when the user made or revised a judgment.
5. Create a workflow record when the same steps can be repeated.
6. Promote to a SKILL only when it has:
   - A clear trigger
   - Stable inputs
   - Repeatable operations
   - Expected output format
   - Quality checks or failure modes

Avoid turning the knowledge base into a graveyard of summaries. Prefer notes that change future behavior.

## Development Operator

When the workflow involves software development:

1. Read the repo before proposing project actions.
2. Summarize current state from real artifacts: branch, diff, commits, issues, PRs, failing checks, TODOs.
3. Convert ambiguity into explicit next actions:
   - Investigate
   - Implement
   - Verify
   - Document
   - Publish
4. When lessons repeat, capture them as:
   - Debugging playbooks
   - Repo-specific checklists
   - PR templates
   - Architecture decision records
   - Candidate skills

## Automation Graduation Rules

Do not automate a process just because it is annoying. Graduate by stage:

1. **Manual**: user and AI run the workflow conversationally.
2. **Assisted**: AI reads sources and drafts outputs; user confirms all writes.
3. **Semi-automated**: scheduled AI briefs or scripts produce drafts; user approves changes.
4. **Automated**: low-risk, reversible writes run automatically with error notifications.

Automation is ready only if:

- It happens at least weekly or saves meaningful cognitive load.
- The trigger and output are unambiguous.
- Failure is visible.
- The user can override it easily.
- The workflow has been accepted without major edits several times.

## Tooling Recommendations

Prefer the lightest stack that closes the loop:

- TickTick/滴答清单: source of truth for actions and reminders.
- RescueTime: source of truth for time and attention evidence.
- Markdown knowledge base: source of truth for notes, decisions, workflows, and skills.
- Git/GitHub: source of truth for development output.
- n8n/Make/Zapier/cron: only after the conversational workflow is stable.

When using live tools, separate read and write permissions. Reads can be broad; writes should be confirmed unless the user explicitly opted into automation.

## Quality Bar

A good output is:

- Evidence-based: cites which task/time/dev/knowledge inputs shaped the conclusion.
- Small enough to act on today.
- Honest about uncertainty and missing data.
- Explicit about suggested changes that require user confirmation.
- Designed to improve after user feedback.

Red flags:

- Producing a giant plan with no calendar or time evidence.
- Creating tasks without clarifying the next action.
- Treating RescueTime as moral judgment instead of evidence.
- Summarizing everything into knowledge notes without future retrieval value.
- Automating writes before the user has trusted the workflow.
