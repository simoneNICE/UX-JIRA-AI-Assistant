# Rovo Chat prompt — Portfolio UX demand (VP / head of UX) — DRAFT

**DRAFT — not validated.** Same per-project logic as Release Workload, run across the
whole product portfolio for one release. Paste into Rovo Chat, fill in FIX VERSION.

---

You are helping me (UX leadership) get a portfolio-wide view of UX design demand for ONE release, across all line-of-business projects, so I can see where UX is over-stretched and where it is barely involved. This is read-only — do not create, edit, or transition any issue.

INPUT — one value I must give you:
FIX VERSION: [leave blank or paste the release exactly as in Jira, e.g. 26.4]
If FIX VERSION is blank or still shows the placeholder, STOP and ask me for it, then wait for my answer. Do not run any search until you have it.

PROJECTS IN SCOPE — the list is fixed; run the same check for every one of these:
CXUX, PMN, NXQC, CXDSCVR, CSA, UH, AW, CXDV, CXFI, CXWFM, CXREC, SC, CXIRR, CXQM, CXSUP, VOC, CXCN, WFM, CXCO, CXAPP, CXWS, VAAS, CXCROSS, EEM, EMOB, APA, IDE, PSHM, AN, SF, CXMO, DE, NPM, CXIA, CRM, ENG, CXDVI, CARD, CXIFW, PIN, CXCA, CXINT, PRD, AAI, BB, ESP, CXXO, ATT, DL

FIELD NOTES (important):
- "UX work" for a Capability = an Epic in project CXUX whose PARENT is that Capability. Match on the parent link, never on summary text or prefix.
- Story Points: use the field named exactly "Story Points" (customfield_10038); NOT "Story point estimate" or "Estimated Story Points" (empty decoys). Only ~35% of epics have Story Points set, so treat SP as an INDICATIVE secondary signal — lead with counts, not SP.
- fixVersion names are not consistent across LOBs: match by PREFIX — for 26.4 also include "26.4-CSA" and any other "26.4…" name — not only the exact string.

PER PROJECT — work one project at a time to stay reliable. For each project in the list:
1. Find its Capabilities with a fix version starting with FIX VERSION and status != "Removed". Count them = CAPS. If CAPS = 0, mark the project "not in this release" and move on.
2. Find the CXUX Epics whose parent is one of those Capabilities (collect the capability keys, then query `project = CXUX AND issuetype = Epic AND parent in (<keys>)`). Record: how many Capabilities have ≥1 UX epic (CAPS_UX), the number of UX epics (EPICS), and the summed "Story Points" of those epics (SP), plus how many epics had no SP set.

PORTFOLIO ROLL-UP:
- Totals across all projects: total CAPS, total CAPS_UX, total EPICS, total SP.
- Average UX demand = total EPICS ÷ (number of projects that have ≥1 Capability in the release). Call this AVG.

HIGHLIGHT ONLY THE EXTREMES — this is the whole point; do not editorialize the middle of the pack:
- 🔴 Too much UX demand (over-stretched): projects whose EPICS ≥ 2 × AVG (highest first). These are where UX is most loaded this release.
- 🟠 Too little / no UX (possible gap): projects that HAVE real scope (CAPS ≥ 3) but ZERO or near-zero UX epics (CAPS_UX = 0, or EPICS far below AVG). Flag as "little/no UX attached — either no UX needed, or UX not engaged; worth a check." Do not assert it's a problem — it may be legitimately engineering-only.

OUTPUT:
```
# Portfolio UX demand — <FIX VERSION>
*Generated: <date> | Read-only | <N> of <total> projects have scope this release*

## 🔴 Too much UX demand
- <PROJECT> — <EPICS> UX epics across <CAPS_UX>/<CAPS> capabilities · <SP> SP
  …(only projects above the 2× AVG threshold, highest first; "none" if none)

## 🟠 Too little / no UX
- <PROJECT> — <CAPS> capabilities, <CAPS_UX> with UX (<EPICS> epics) — little/no UX attached
  …("none" if none)

## Portfolio overview
| Project | Capabilities | …with UX | UX epics | Story Points |
|---------|-------------:|---------:|---------:|-------------:|
  …(one row per project that has scope this release, sorted by UX epics desc; add a TOTAL row)

Projects not in this release: <comma-separated keys>
```

Close with one ⚠️ line stating what share of the release's epics had Story Points set, so SP is read as indicative and the counts as the reliable signal.

Read-only — do not create, edit, or transition any issues.
