# Rovo Chat prompt — My health check (designer, self-service)

Converted from `/ux-my-health` in `JIRA Agent/public/agent-ux-process.md`. Paste into
Rovo Chat — no roster needed, this checks your own work only.

---

You are helping me check the health of my own active work in Jira. Scope is ALL projects I work in (not just CXUX) — do not restrict by project. Measure everything against my own assignee identity in this workspace.

HEALTH MODEL — apply these exact rules:

IMPORTANT — count only real hands-on work items. CXUX uses a portfolio hierarchy (Initiative > Capability > Epic > Task) and a designer is often assigned at every level. The band must count ONLY leaf work items — issue type Task, Story, Sub-task, or Bug. EXCLUDE Epic, Capability, and Initiative from the "In Progress count", or the band will read 5+ when you actually have one task in hand.

To measure how long something has been In Progress (the 14d / 45d flags), use the status-change date, e.g. `status CHANGED TO "In Progress" BEFORE -14d` (tasks) / `BEFORE -45d` (epics). Do NOT use the Updated date — any edit bumps it.

My In Progress task count (the band):
- 0 tasks → 🔴 idle — nothing active.
- 1 task → 🟠 under-engaged.
- 2–4 tasks → ✅ ok.
- 5+ tasks → 🔴 too many in progress.

Other flags:
- 🟠 stalled task — a task that has been In Progress for more than 14 days.
- 🟠 parent out of sync — one of my tasks is In Progress or Done while its immediate parent is still "New". The parent may be an Epic OR a Capability (my tasks sometimes hang directly off a Capability) — check the immediate parent regardless of its type, and label it by its actual type in the output. If a task has no parent, skip this check for it.
- 🟠 stalled parent — a parent (Epic or Capability) of mine that has been In Progress for more than 45 days.

Sprint-phase lens:
- Find the active sprint's end date (project CXUX). If 7 days or fewer remain, we're in the last week:
  - "too many in progress" becomes a won't-finish risk → elevate it.
  - "under-engaged" is expected that week → suppress that flag.

STEPS:
1. Find my leaf work items (issue type Task, Story, Sub-task, or Bug — NOT Epic/Capability/Initiative) currently In Progress, across all projects. For each, note its immediate parent and that parent's status/type.
2. Apply the In Progress band (leaf items only).
3. Flag any task In Progress for more than 14 days (use the status-change date, not Updated).
4. Flag any task whose immediate parent (Epic or Capability) is still "New" while my task is In Progress or Done.
5. For my distinct parents that are In Progress, check how long each has been In Progress; flag any over 45 days.
6. Check the active sprint's end date (project CXUX) and apply the sprint-phase lens if within 7 days of the end.
7. Present:

```
# My health check
*All projects · today <date>*
🗓️ Sprint <name> — last week (<days> days left)   ← only if ≤7 days remain

🔴 / 🟠 / ✅ <overall verdict>
<one sentence per flag, each issue key labelled: task CXUX-NNNNN / epic CXUX-NNNNN>
```

Lead with the most severe flag. Read-only — do not create, edit, or transition any issues.
