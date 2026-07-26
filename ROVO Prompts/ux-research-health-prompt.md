# Rovo Chat prompt — Researcher health check (manager)

Converted from `/ux-research-health` in `JIRA Agent/manager/agent-ux-manager.md`.
Paste into Rovo Chat.

---

You are helping me run a health check on the UX Researches portfolio in Jira project CXUX.

HIERARCHY & SCOPE:
- Root Initiative: CXUX-12163 ("UX Researches Initiative").
- Its child Capabilities (one is the "current" semester capability, e.g. "UX Researches / s2.2026" — it rotates, don't assume a fixed key, discover it as a child of CXUX-12163).
- Each Capability's child Epics = individual "researches". In scope: Epics with status In Progress or New only (exclude Done and Removed).
- Each Epic's child Tasks = research tasks.
- A research's owner = its Epic's assignee. Only report researches owned by someone in the researcher roster below — other owners under the same Capabilities (other names, or unassigned) are out of scope, skip them in the per-researcher breakdown.
- Ignore the test epic CXUX-12409 entirely.
- Flag any in-scope research Epic with no assignee separately (unassigned research), don't attribute it to any researcher.

RESEARCHER ROSTER:
Andrew Wong (andrew.wong@niceincontact.com), Sveta Fomchenko (sveta.fomchenko@nice.com), Lee Winkler (lee.winkler@nice.com), Serena Yang (serena.yang@niceincontact.com).

HEALTH MODEL — same rules as any health check, applied per researcher using their research TASKS (not epics) as the unit of work:

Per-person In Progress task count (the band):
- 0 tasks → 🔴 idle.
- 1 task → 🟠 under-engaged.
- 2–4 tasks → ✅ ok.
- 5+ tasks → 🔴 too many in progress.

Other flags:
- 🟠 stalled task — In Progress for more than 14 days. Measure from the status-change date (`status CHANGED TO "In Progress" BEFORE -14d`), NOT the Updated field.
- 🟠 epic out of sync — a task is In Progress or Done while its parent (research) Epic is still New.
- 🟠 stalled epic — a research Epic In Progress for more than 45 days (status-change date, same rule).

Task-count unit: count the In Progress TASKS that sit under each researcher's Epics, regardless of who the task itself is assigned to (the research owner is the Epic assignee; the tasks under it are that researcher's work).

Sprint-phase lens: use project CXUX's active sprint. If more than one sprint is open, use the one with the soonest end date. If ≤7 days remain: elevate "too many in progress" as a won't-finish risk, suppress "under-engaged" that week.

STEPS:
1. Resolve the tree: Capabilities under CXUX-12163 → their child Epics (keep only those owned by the roster, status In Progress or New, excluding CXUX-12409) → those Epics' child Tasks.
2. Check the active sprint's end date.
3. Among the in-scope tasks, find any In Progress for more than 14 days (stalled task).
4. Find any in-scope research Epic that has been In Progress for more than 45 days (stalled epic).
5. Per researcher: apply the In Progress task band, stalled tasks, out-of-sync epics, stalled epics, and the sprint-phase lens.
6. Present, one block per researcher, most severe first:

```
# Researchers — health
*Researches under CXUX-12163 · today <date>*
🗓️ Sprint <name> — last week (<days> days left)   ← only if ≤7 days remain

🔴 <Name> — <verdict>
<one sentence, every key labelled: task CXUX-NNNNN / epic CXUX-NNNNN>
```

Healthy researchers: one 🟢 line, or omit entirely. Mention any unassigned researches once, separately, at the end.

Read-only — do not create, edit, or transition any issues.
