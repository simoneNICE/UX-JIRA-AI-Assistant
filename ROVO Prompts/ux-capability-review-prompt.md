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
2. Count the Epics by status: New / In Progress / Done.
3. For each In Progress Epic, compute how long it has been In Progress (days since
   it entered In Progress), and flag it 🟠 stalled if > 45 days.
4. Scan the tasks: flag 🟠 stalled tasks (In Progress > 14 days) and 🟠 out-of-sync
   epics (a task In Progress/Done under a New epic).
5. Per app (Component): group the research Epics by their Component field — each
   Component represents an app. Report how many researches fall under each app.
   Note any Epic with no Component separately.
6. Categorize the researches thematically: cluster them into the main research
   categories from the Epic summaries (titles). Report how many researches fall in
   each category.
7. Detect similar / overlapping In Progress researches: compare the In Progress
   Epics' titles and summaries and flag any pairs (or clusters) that look like they
   cover the same topic or user problem — candidates for consolidation. Be
   conservative: only flag genuine overlaps, and name both keys.

Present in this order:

```
# Research capability review
*Capability <name> · under CXUX-12163 · today <date>*

## Status
New <n> · In Progress <n> · Done <n>   (total <n>)

## In Progress — age & health
🟠/🟢 <Epic CXUX-NNNNN> — <title> — In Progress <N>d <stalled? note>
...(most days-in-progress first)

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
