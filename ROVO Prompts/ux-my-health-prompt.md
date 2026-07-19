# Rovo Chat prompt — My health check (designer, self-service)

Converted from `/ux-my-health` in `JIRA Agent/public/agent-ux-process.md`. Paste into
Rovo Chat — no roster needed, this checks your own work only.

---

You are helping me check the health of my own active work in Jira. Scope is ALL projects I work in (not just CXUX) — do not restrict by project. Measure everything against my own assignee identity in this workspace.

HEALTH MODEL — apply these exact rules:

My In Progress task count (the band):
- 0 tasks → 🔴 idle — nothing active.
- 1 task → 🟠 under-engaged.
- 2–4 tasks → ✅ ok.
- 5+ tasks → 🔴 too many in progress.

Other flags:
- 🟠 stalled task — a task that has been In Progress for more than 14 days.
- 🟠 epic out of sync — one of my tasks is In Progress or Done while its parent Epic is still "New".
- 🟠 stalled epic — a parent Epic of mine that has been In Progress for more than 45 days.

Sprint-phase lens:
- Find the active sprint's end date (project CXUX). If 7 days or fewer remain, we're in the last week:
  - "too many in progress" becomes a won't-finish risk → elevate it.
  - "under-engaged" is expected that week → suppress that flag.

STEPS:
1. Find all of my tasks currently In Progress, across all projects. For each, note the parent Epic and its status.
2. Apply the In Progress band.
3. Flag any task In Progress for more than 14 days.
4. Flag any task whose parent Epic is still "New" while my task is In Progress or Done.
5. For my distinct parent Epics that are In Progress, check how long each has been In Progress; flag any over 45 days.
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
