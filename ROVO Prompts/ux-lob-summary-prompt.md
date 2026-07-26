# Rovo Chat prompt — Design readiness (manager)

Converted from `/ux-lob-summary` in `JIRA Agent/manager/agent-ux-manager.md`.
Paste into Rovo Chat. This is a product view (design coverage/readiness by capability
for one LOB project + one release), not a per-person view.

---

You are helping me build a design-readiness summary for ONE line-of-business (LOB) project in ONE release: for each Capability in that project+release, is the UX design ready?

INPUT — two values I must give you:
PROJECT: [leave blank or paste the LOB project key, e.g. CXREC]
FIX VERSION: [leave blank or paste the release exactly as in Jira, e.g. 26.4]

Before doing anything: if either PROJECT or FIX VERSION is blank or still shows the placeholder text, STOP and ask me for the missing one(s) — ask for both if both are missing — and wait for my answer. Do not guess, do not proceed with an empty value, do not run any search until you have both.

STEP 1 — Design deadline for the release
Compute the design deadline for FIX VERSION: first day of its work quarter minus 2 months, where work quarter = release quarter − 1. Release format is "YY.Q" (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
Example: release 26.4 → work starts 1 Jul 2026 → design deadline 1 May 2026.

STEP 2 — Fetch Capabilities in scope
Find all issues of type Capability in PROJECT whose fix version STARTS WITH the FIX VERSION code, status not "Removed". Release names are NOT always consistent: some projects (e.g. CSA) use suffixed variants like "27.1-CSA". Match by prefix — for 27.1 also include "27.1-CSA" and any other "27.1…" name — not only the exact string, or you may drop part of the release. For each, keep: key, summary, status, fix version(s).

STEP 3 — Fetch UX Epics
Find Epics in project CXUX whose parent is one of the Capabilities from Step 2 — this is the definition of a "UX Epic" here (don't filter by summary text/prefix, naming isn't consistent across teams). For each UX Epic keep: key, summary, status, parent, assignee. A Capability with no UX Epic still appears in the output (it means UX work was never attached) — flag it, don't discard it.

STEP 4 — Fetch UX Tasks
Find Tasks in project CXUX whose parent is one of the UX Epics from Step 3. Keep: key, summary, status, parent, assignee.

STEP 5 — Apply red-light logic
For each Capability → UX Epic → its Tasks (IMPORTANT: ignore tasks with status "Removed" — they are cancelled; counting them would make design_ready impossible and raise false red flags):
- task_count = number of NON-Removed tasks under the epic
- done_count = NON-Removed tasks with status Done
- design_ready = (task_count > 0 AND done_count == task_count) OR (task_count == 0 AND epic status == Done)
- no_ux_epic = the Capability has no UX Epic at all
- has_no_tasks = (has a UX Epic but task_count == 0 AND epic status != Done)
- epic_unassigned = epic has no assignee
- tasks_unassigned = any task under it has no assignee

Collect ALL applicable flags:
- 🔴 "No UX Epic" — no_ux_epic (UX work never attached to this Capability)
- 🔴 "Design overdue" — today is past the design deadline AND NOT design_ready
- 🔴 "Dev ahead of design" — Capability status is In Progress or Done AND NOT design_ready
- 🟠 "No tasks" — has_no_tasks
- 🟠 "Epic unassigned" — epic_unassigned
- 🟠 "Task(s) unassigned" — tasks_unassigned

Overall traffic light = 🔴 if any 🔴 flag, else 🟠 if any 🟠 flag, else 🟢.
Notes column = comma-separated list of the triggered flag names.

Status emoji: Done → 🟢 · In Progress / In Definition → 🟡 · New / Ready for Dev → 🟦 · Removed → ⚪.

STEP 6 — Output
Header:
```
# Design readiness — <PROJECT> · <FIX VERSION>
*Generated: <date> | Read-only | Design deadline: <date>*
Scope: N capabilities
```

One table, ordered 🔴 first, then 🟠, then 🟢:
```
| 🚦 | Capability | Cap. Status | UX Epic | Tasks | Notes |
```
Example row: `| 🔴 | [CXREC-133289] iHub – hourly deletion | 🟦 New | CXUX-12690 🟦 New | 0/3 | Design overdue, Epic unassigned |`
For a Capability with no UX Epic, show "—" in the UX Epic / Tasks columns and "No UX Epic" in Notes.

One summary line: `**<PROJECT> · <FIX VERSION>:** N capabilities — X 🔴 · Y 🟠 · Z 🟢`

Close with a **⚠️ Needs Attention** section: a flat list of every 🔴 item, sorted by capability key — this is the section I should read first.

Read-only — do not create, edit, or transition any issues.
