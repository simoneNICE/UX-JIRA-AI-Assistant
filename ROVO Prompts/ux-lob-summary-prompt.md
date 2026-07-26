# Rovo Chat prompt — Design readiness (manager)

Converted from `/ux-lob-summary [release1 release2]` in
`JIRA Agent/manager/agent-ux-manager.md`. Paste into Rovo Chat. This is a product view
(design coverage/readiness by capability), not a per-person view.

---

You are helping me build an executive summary of UX design coverage and readiness across all LOB (line-of-business) projects, for the current and next release.

STEP 1 — Determine target releases
RELEASES: [optional — give me two release codes like "26.3 26.4" if you want to override; otherwise compute them]
If not given: compute today's current release (Q+1) and next release (Q+2) in "YY.Q" format, where Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec (after X.4 comes (X+1).1).
Design deadline per release = first day of its work quarter minus 2 months, where work quarter = release quarter − 1.
Example: release 26.3 → work starts 1 Apr 2026 → design deadline 1 Feb 2026.
Example: release 26.4 → work starts 1 Jul 2026 → design deadline 1 May 2026.

STEP 2 — Fetch Capabilities in scope
Find all issues of type Capability, across all projects, with fixVersion matching either of the two target releases, status not "Removed". Skip Capabilities that belong to project CXUX itself (that's the UX-internal project, not a LOB project). For each, keep: key, summary, status, fix version(s), project.

STEP 3 — Fetch UX Epics
Find Epics in project CXUX whose parent is one of the Capabilities from Step 2 — this is the definition of a "UX Epic" here (don't filter by summary text/prefix, naming isn't consistent across teams). Keep only Capabilities that have at least one UX Epic; silently discard Capabilities with none. For each UX Epic keep: key, summary, status, parent, assignee.

STEP 4 — Fetch UX Tasks
Find Tasks in project CXUX whose parent is one of the UX Epics from Step 3. Keep: key, summary, status, parent, assignee.

STEP 5 — Apply red-light logic
For each Capability → UX Epic → its Tasks:
- task_count = number of tasks under the epic
- done_count = tasks with status Done
- design_ready = (task_count > 0 AND done_count == task_count) OR (task_count == 0 AND epic status == Done)
- has_no_tasks = (task_count == 0 AND epic status != Done)
- epic_unassigned = epic has no assignee
- tasks_unassigned = any task under it has no assignee

Collect ALL applicable red flags:
- 🔴 "Design overdue" — today is past the design deadline AND NOT design_ready
- 🔴 "Dev ahead of design" — Capability status is In Progress or Done AND NOT design_ready
- 🟠 "No tasks" — has_no_tasks
- 🟠 "Epic unassigned" — epic_unassigned
- 🟠 "Task(s) unassigned" — tasks_unassigned

Overall traffic light = 🔴 if any 🔴 flag, else 🟠 if any 🟠 flag, else 🟢.
Notes column = comma-separated list of the triggered flag names.

Status emoji: Done → 🟢 · In Progress / In Definition → 🟡 · New / Ready for Dev → 🟦 · Removed → ⚪.

STEP 6 — Output
Group results by: product category → project name → fix version (current release first). Within each group, order 🔴 first, then 🟠, then 🟢.

Header:
```
# Design readiness — Releases <R1> & <R2>
*Generated: <date> | Scope: N capabilities across M projects*
Design deadlines: <R1> → <date> · <R2> → <date>
```

Table per project + release:
```
| 🚦 | Capability | Fix | Cap. Status | UX Epic | Tasks | Notes |
```
Example row: `| 🔴 | [CXREC-133289] iHub – hourly deletion | 26.4 | 🟦 New | CXUX-12690 🟦 New | 0/3 | Design overdue, Epic unassigned |`

After each project's table, one summary line: `**<Project name> (<release>):** N capabilities — X 🔴 · Y 🟠 · Z 🟢`

Close with a **⚠️ Needs Attention** section: a flat list of every 🔴 item across all projects, sorted by project then capability key — this is the section I should read first.

Final summary table across everything:
```
| Product Area | Project | <R1> 🔴 | <R1> 🟢 | <R2> 🔴 | <R2> 🟢 |
```

Read-only — do not create, edit, or transition any issues.
