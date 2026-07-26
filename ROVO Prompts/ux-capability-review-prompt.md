# Rovo Chat prompt — Research capability review (manager) — DRAFT

**DRAFT — not validated yet.** Logic and output not yet confirmed against real data.

A portfolio review of every research Epic inside the current semester Capability.
Paste into Rovo Chat.

---

You are helping me review all the research Epics inside the current UX Researches
Capability in Jira project CXUX.

HIERARCHY & SCOPE:
- Root Initiative: CXUX-12163 ("UX Researches Initiative").
- Its child Capabilities: one is the "current" semester capability (e.g.
  "UX Researches / s2.2026" — it rotates, don't assume a fixed key, discover it as
  the current child of CXUX-12163). Default to that one. If I give you a specific
  Capability key, use that instead.
- That Capability's child Epics = the individual "researches". Include ALL statuses
  (New, In Progress, Done) — I want the counts. Exclude only status Removed.
- Each Epic's child Tasks = research tasks.
- Ignore the test epic CXUX-12409 entirely.

HEALTH THRESHOLDS (same model as the other health checks):
- 🟠 stalled epic — an Epic In Progress for more than 45 days.
- 🟠 stalled task — a Task In Progress for more than 14 days.
- 🟠 epic out of sync — a Task is In Progress or Done while its parent Epic is
  still New.

STEPS:
1. Resolve the tree: current Capability under CXUX-12163 → its child Epics
   (all statuses except Removed, excluding CXUX-12409) → those Epics' child Tasks.
   For the task-level scan, reach tasks via all descendants of the Capability
   (e.g. `issue in portfolioChildIssuesOf("<capability key>")`), but drop tasks whose
   parent Epic is Removed or is CXUX-12409.
2. Count the Epics by status: New / In Progress / Done.
3. For each In Progress Epic, bucket how long it has been In Progress using
   status-change-date queries (NOT the Updated field, which any edit bumps): run
   `status = "In Progress" AND status CHANGED TO "In Progress" BEFORE -45d` (stalled,
   🟠) and `... BEFORE -30d` (ageing). Do NOT try to print an exact day count per
   epic or sort by exact days — Rovo can't read per-issue status history reliably at
   this scale; report the bucket instead.
4. Scan the tasks: flag 🟠 stalled tasks (In Progress > 14 days, status-change date)
   and 🟠 out-of-sync epics (a task In Progress/Done under a New epic).
5. Per app (Component): group the research Epics by their Component field — each
   Component represents an app. Report how many researches fall under each app.
   An Epic with several Components is counted under EACH — so per-app counts may sum
   to more than the total; say so. Note any Epic with no Component separately.
6. Categorize the researches thematically: research Epic titles follow the pattern
   "UX Research / <Category> / <name>". Take the category from the 2nd path segment of
   the title (e.g. Competitive Research, Concept Testing, Product Discovery, Journey
   Mapping) rather than free-form clustering, so the grouping is reproducible. Report
   how many researches fall in each category.
7. Detect similar / overlapping researches: compare titles/summaries and flag any
   pairs (or clusters) that look like the same topic — candidates for consolidation.
   Compare across ALL non-Removed statuses, not only In Progress (genuine duplicates
   are often a CLONE pair where one side is already Done). Be conservative: only flag
   genuine overlaps, name both keys. This step is advisory LLM judgment — results are
   not reproducible run-to-run; treat them as suggestions, not facts.

Present in this order:

```
# Research capability review
*Capability <name> · under CXUX-12163 · today <date>*

## Status
New <n> · In Progress <n> · Done <n>   (total <n>)

## In Progress — age & health
🟠 stalled (>45d): <Epic CXUX-NNNNN> — <title>
🟡 ageing (>30d): <Epic CXUX-NNNNN> — <title>
🟢 recent (<30d): <Epic CXUX-NNNNN> — <title>
(group by bucket; no exact day counts)

## Flags
🟠 stalled epics: <keys or "none">
🟠 stalled tasks: <task key (epic key) or "none">
🟠 out-of-sync epics: <epic key — the offending task or "none">

## Researches per app (Component)
<App / Component> — <n> research(es): <keys>
...
No component — <n>: <keys>   ← only if any

## Categories
<Category> — <n> research(es): <keys>
...

## Similar in-progress researches
🔁 <CXUX-NNNNN> ↔ <CXUX-NNNNN> — <one line on the overlap>
...(or "none spotted")
```

Read-only — do not create, edit, or transition any issues.
