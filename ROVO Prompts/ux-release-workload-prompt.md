# Rovo Chat prompt — Release workload (manager)

Read-only sizing of a single project's release: how many Capabilities are in it, how
many have UX design work attached (a CXUX Epic as child), the Story Points that work
carries, and the status of both. Paste into Rovo Chat, fill in PROJECT and FIX VERSION.

---

You are helping me size the UX workload for one project in one release. This is read-only — do not create, edit, or transition any issue.

INPUT — two values I must give you:
PROJECT: [leave blank or paste the project key, e.g. CXREC]
FIX VERSION: [leave blank or paste the release/fix version exactly as in Jira, e.g. 26.4]

Before doing anything: if either PROJECT or FIX VERSION is blank or still shows the placeholder text, STOP and ask me for the missing one(s) — ask for both if both are missing — and wait for my answer. Do not guess, do not proceed with an empty value, do not run any search until you have both.

CONTEXT — CXUX hierarchy:
Capabilities live in the line-of-business (LOB) projects. UX design work lives in project CXUX. A "CXUX Epic" here means an Epic in project CXUX whose PARENT is one of those Capabilities — that is the link between a Capability and its UX work. Naming isn't consistent across teams, so match on the parent relationship, never on summary text or prefix.

STEP 1 — Fetch the Capabilities in scope
Find all issues in PROJECT of type Capability with fixVersion = FIX VERSION and status not "Removed". For each keep: key, summary, status, fix version(s). This is the set for output metric #1.

STEP 2 — Find the CXUX Epics under each Capability
For each Capability from Step 1, find Epics in project CXUX whose parent is that Capability. For each such Epic keep: key, summary, status, parent (the Capability), assignee, Story Points.
A Capability "has UX work" if it has at least one CXUX Epic child. Capabilities with zero CXUX Epics still count in metric #1 but not in metric #2.

STEP 3 — Sum the Story Points
Sum the Story Points field across all CXUX Epics found in Step 2 (all Capabilities combined). Use the field named exactly "Story Points" (customfield_10038) — NOT "Story point estimate" and NOT "Estimated Story Points", which are decoy fields that are empty on these epics and would collapse the total to ~0. Treat an Epic with no Story Points value as 0, and note separately how many Epics had no value set (so the total isn't read as complete when it isn't).

STEP 4 — Output
Header:
```
# Release workload — <PROJECT> · <FIX VERSION>
*Generated: <date> | Read-only*
```

Then the four headline numbers, up top and unmissable:
- **Capabilities in release:** N  (project <PROJECT>, fixVersion <FIX VERSION>)
- **…with a CXUX Epic:** M  (of N — the rest have no UX work attached)
- **Total Story Points (CXUX Epics):** P  (across Q epics; R epics had no SP set)
- **Assignees (CXUX Epics):** the distinct people the CXUX Epics are assigned to, each with their epic count, e.g. "Jane Doe (3), John Smith (1)". Note any unassigned epics as "Unassigned (K)".

Status emoji: Done → 🟢 · In Progress / In Definition → 🟡 · New / Ready for Dev → 🟦 · Removed → ⚪.

Then a table of every Capability in scope, Capabilities WITH a CXUX Epic first:
```
| Capability | Cap. Status | CXUX Epics | Epic Status | Assignee | Story Points |
```
- One row per Capability. If it has several CXUX Epics, list each epic key + status in the "Epic Status" column and its assignee in the "Assignee" column (aligned to the same epic), and put the summed SP for that Capability in "Story Points".
- Capabilities with no CXUX Epic: show "—" in the CXUX Epics / Epic Status / Assignee / Story Points columns so the gap is visible.
Example row: `| [CXREC-133289] iHub – hourly deletion | 🟦 New | CXUX-12690 | 🟡 In Progress | Jane Doe | 8 |`

Close with a one-line recap:
`**<PROJECT> · <FIX VERSION>:** N capabilities · M with UX work · P Story Points across Q epics.`
