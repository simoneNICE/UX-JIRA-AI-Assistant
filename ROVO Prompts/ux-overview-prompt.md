# Rovo Chat prompt — Team sprint overview (manager)

Converted from `/ux-overview <team|all>` in `JIRA Agent/manager/agent-ux-manager.md`.
Paste into Rovo Chat. Rosters embedded below.

---

You are helping me get an active-sprint snapshot of my UX designers' work in Jira, grouped by designer. Scope is project CXUX only, current active sprint only. Measure by task assignee.

SCOPE — ask me first. Before running any query, ask me exactly this and wait for my answer:
"Which scope do you want? (1) the whole team, (2) a specific region — Israel, India, or USA, or (3) a single designer (tell me the name)?"
Do not query Jira until I reply.
- Whole team → all rosters combined (no overlap between regions); include a Team column labelling each person.
- A region → only that region's roster (Israel, India, or USA); no Team column.
- A single designer → just that one person, resolved from the rosters; no Team column. If the name isn't in the rosters or is ambiguous, tell me and ask again.

ROSTER — Israel designers:
Yaara Bar, Chelsea Franz, Assaf Zinger, Eitan Koren, Tali Silon-Shacham, Erez Bar, Michael Dalal, Yoav Chen, Libi Becker Tidhar, Sveta Fomchenko, Lee Winkler, Lihi Shrem, Tal Segev.

ROSTER — India designers:
Advait Patil, Ajit Vaidya, Deepa Bhamare, Deepak Badgujar, Dinesh Koli, Gajanan Rajput, Manashree Thokal, Mayur Chaudhari, Parimal Khanolkar, Prafull Mane, Sheetal Barge-Gole, Shikha Shukla, Shilpa Sarkar, Sushanth Civi, Tapas Chowdhury, Umajit Mongjam, Kalpesh Gurav, Nirmitee Sisodia, Nutan Doiphode.

ROSTER — USA designers:
Doug Clement, Janet Gonzales, David Stoker, Sara Evans, Lorina Binning, Serena Yang, Andrew Wong.

The "roster" below refers to whichever set the scope resolved to: all rosters (whole team), one region's roster, or the single designer.

FIELD NOTE (this Jira has look-alikes): for Story Points use the field named exactly "Story Points" (customfield_10038). Do NOT use "Story point estimate" or "Estimated Story Points" — those are different fields, empty on these tasks, and would make every SP total come out as 0.

STEPS:
1. Find all Tasks in project CXUX assigned to anyone in the roster, in the currently active sprint. EXCLUDE tasks with status "Removed" (cancelled) — otherwise the New/In Progress/Done columns won't sum to Total.
2. Group by assignee: count tasks by status (New / In Progress / Done) and sum Story Points (treat missing as 0). Roster members with zero tasks still appear, with all-zero counts.
3. Note separately any tasks in the active sprint assigned to someone NOT in the roster (don't fold them into the table).
4. Present a table sorted by Total Story Points descending:

   | Designer | Team | New | In Progress | Done | Total | SP |
   |----------|------|----:|------------:|-----:|------:|---:|

   Show the Team column only when the scope is the whole team; omit it for a single region or a single designer. Add a final TOTAL row.

Read-only — do not create, edit, or transition any issues.
