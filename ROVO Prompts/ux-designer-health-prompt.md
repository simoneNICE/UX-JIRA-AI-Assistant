# Rovo Chat prompt — Designer health check (manager)

Converted from the Claude Code `/ux-designer-health <team|all>` routine
(`JIRA Agent/manager/agent-ux-manager.md`). Paste into a Rovo Chat conversation.
Rosters are embedded below (from `team-config.md`) so Rovo doesn't need file access.

---

You are helping me run a health check across my UX designers' active work in Jira. Scope is **all projects** the designers work in (CXUX, CXQM, CXDV, CXREC, CXWFM, PMN, CXDSCVR, VOC, etc.) — do NOT restrict to project = CXUX. Measure everything **by task assignee** (the task is the unit of work for designers).

SCOPE — ask me first. Before running any query, ask me exactly this and wait for my answer:
"Which scope do you want? (1) the whole team, (2) a specific region — Israel, India, or USA, or (3) a single designer (tell me the name)?"
Do not query Jira until I reply.
- Whole team → all rosters combined; label each person's team in the output.
- A region → only that region's roster (Israel, India, or USA).
- A single designer → just that one person, resolved from the rosters. If the name isn't in the rosters or is ambiguous, tell me and ask again.

ROSTER — Israel designers (account_id in parentheses):
Yaara Bar (557058:f02910b4-7a33-4532-ae52-65b2d02fc245), Chelsea Franz (712020:65c25382-da24-4a4f-9c1a-b9794892207f), Assaf Zinger (712020:0861d082-a1db-4b17-aeba-563afe001639), Eitan Koren (712020:5e21d1f2-366c-4c8e-90fe-3bfb9247687d), Tali Silon-Shacham (70121:f9675544-965d-4261-8c69-dd0b5af1f36b), Erez Bar (63ea3e479e626e54cc5ab8fd), Michael Dalal (712020:e6a03127-1281-4a20-a573-1cc6d59fcf0d), Yoav Chen (61151844627b5600688e908b), Libi Becker Tidhar (61190114650a26006e0f1823), Sveta Fomchenko (712020:d95bc91f-6277-4ae6-988a-bf4a191b66be), Lee Winkler (62cd77d61e326fd9301283b1), Lihi Shrem (712020:b7ff7587-41a6-4539-ba06-e2da1ca0810c), Tal Segev (712020:826cc4e2-1cd8-4e8e-ac09-c37294c8d27e).

ROSTER — India designers (account_id in parentheses):
Advait Patil (712020:7514f68a-9d45-45f5-8c66-991834165754), Ajit Vaidya (63adc588741248746bf6bdcc), Deepa Bhamare (62b16a22cebad33432f6b5c6), Deepak Badgujar (622ba91e8a4bb60068f70032), Dinesh Koli (712020:721636e8-4f81-48c0-aa3e-d38298047b60), Gajanan Rajput (712020:aa37b218-7608-4133-9500-aac224528ebc), Manashree Thokal (712020:ddc645bb-ccd2-41f5-9cc4-c019304c84e0), Mayur Chaudhari (712020:d488a8df-551b-4325-aa41-7d8e1dababca), Parimal Khanolkar (712020:27f92cd9-b054-4cf2-9ef0-56b974e21536), Prafull Mane (62cdb715dcf59ca4ad0145d2), Sheetal Barge-Gole (712020:c7abe286-b08a-4898-a5c1-9276f430c8df), Shikha Shukla (62baf1fbd752af0e54ebfa75), Shilpa Sarkar (712020:89eeca07-0de1-40bc-b3b2-1c87271ff292), Sushanth Civi (712020:df95749d-30dc-4c39-b333-aa73a4742b7a), Tapas Chowdhury (626094579506d6006fd9fec6), Umajit Mongjam (70121:d43b183a-1a5a-41a1-87ec-cc0e549e8adc), Kalpesh Gurav (712020:8dab633f-0bed-41cd-b93a-d7d95746b0b5), Nirmitee Sisodia (712020:2f630343-f304-4df5-bcb2-ea638aaa72b5), Nutan Doiphode (712020:43f68da3-a554-4afc-ae7d-06fd5df96380).

ROSTER — USA designers (account_id in parentheses):
Doug Clement (6077f6ccb5dffc006f4cb020), Janet Gonzales (6307037507b7804d7aa1da43), David Stoker (712020:ba6ab7d2-69f7-44ae-b2dc-e534b51c426e), Sara Evans (712020:8e26db37-d04f-4937-b9fd-0b5779f0485a), Lorina Binning (611cf7d5ee947000719686d9), Serena Yang (6318920b6856bdd60aa03d2b), Andrew Wong (712020:ce3e4425-40fd-4dee-bceb-7a773f98b5b9).

Apply the health model only to the people the scope resolved to: all rosters (whole team), one region's roster, or the single designer. For a single designer, drop the "team" labelling in the output header (use their name).

HEALTH MODEL — apply these exact rules per person:

Per-person In Progress task count (the band):
- 0 tasks → 🔴 idle — nothing active.
- 1 task → 🟠 under-engaged.
- 2–4 tasks → ✅ ok.
- 5+ tasks → 🔴 too many in progress.

Other flags:
- 🟠 stalled task — a task that has been In Progress for more than 14 days. Measure from the status-change date (`status CHANGED TO "In Progress" BEFORE -14d`), NOT the Updated field, which any edit bumps.
- 🟠 epic out of sync — the epic's status doesn't reflect the work inside it. Flag BOTH directions: (a) a task is In Progress or Done while its parent Epic is still "New"; and (b) a task is still In Progress while its parent Epic is already "Done" (the common real case here). If a task has no parent Epic, skip this check for it.
- 🟠 stalled epic — an Epic that has been In Progress for more than 45 days (status-change date, same rule as above).

Sprint-phase lens (not a hard rule — context to apply on top):
- Because scope is all projects, there is usually NO single active sprint — designers' In Progress work mostly sits outside any sprint, and different boards have different sprint dates. Only apply this lens when the scope is a single designer who works mostly in one project (use that board's current sprint). Otherwise state "sprint lens not applicable (work spans multiple boards)" and skip it — do not guess one sprint's date for the whole roster.
- When it does apply: find the end date of that board's active sprint. If 7 days or fewer remain, we're in the "last week" of the sprint:
  - "too many in progress" becomes a won't-finish risk → treat as more severe.
  - "under-engaged" is expected that week (work has converged toward Done) → suppress that flag entirely for the last week.

STEPS:

1. For every person in scope, find their Jira tasks currently In Progress (issue type = Task, status = In Progress, assignee = that person, across ALL projects — no project filter). For each, note the parent Epic and that Epic's current status. Anyone in the roster with zero In Progress tasks is idle (0 tasks), even if you have to check them explicitly.
2. Apply the In Progress band per person from the Health model above.
3. Flag any task that has been In Progress for more than 14 days (stalled task).
4. Flag any task whose parent Epic is still "New" while the task itself is In Progress or Done (epic out of sync).
5. For the distinct parent Epics that are In Progress, check how long each has been In Progress; flag any epic over 45 days (stalled epic).
6. Check the active sprint's end date and apply the sprint-phase lens if we're in the last 7 days.
7. Present the result exactly in this format, most severe first, English only, every issue key labelled with its type (e.g. "task CXUX-12345" / "epic CXUX-6789"):

```
# <Team> — health
*All projects · today <date>*
🗓️ Sprint <name> — last week (<days> days left)   ← only include this line if ≤7 days remain

## 🔴 Overloaded
- <Name> — N tasks in progress; M stalled >14d; epic out of sync: epic KEY

## 🔴 Idle
- <Name> — 0 tasks in progress

## 🟠 Watch
- <Name> — <under-engaged / stalled task KEY / epic KEY out of sync>

*No issues:* <names with no flags, one line>
```

8. If a flag is pervasive across most of the team (e.g. most people have an out-of-sync epic), say so once at the top as a process-level note instead of repeating it for every person.

Do not create, edit, or transition any Jira issues — this is read-only reporting.
