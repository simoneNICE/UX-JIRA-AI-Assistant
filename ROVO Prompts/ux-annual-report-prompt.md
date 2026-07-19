# Rovo Chat prompt — Annual closed-work report (manager)

Converted from `/ux-annual-report <team|all> <year>` in
`JIRA Agent/manager/agent-ux-manager.md`. Paste into Rovo Chat. Rosters embedded below.

---

You are helping me build a per-designer breakdown of Jira Tasks closed in a given year, in project CXUX only.

SCOPE — ask me first. Before running any query, ask me these two things and wait for my answer:
1. "Which year?" (e.g. 2025)
2. "Which scope? (1) the whole team, (2) a specific region — Israel or India, or (3) a single designer (tell me the name)?"
Do not query Jira until I reply to both.
- Whole team → the union of all rosters below, counting each person ONCE (dedup by identity, not name string).
- A region → only that region's roster (Israel or India).
- A single designer → just that one person, resolved from the rosters. If the name isn't in the rosters or is ambiguous, tell me and ask again.

Window: Tasks resolved between <year>-01-01 and <year>-12-31 inclusive. Scope of "closed" = issue type Task, status category Done, resolved in that window.

ROSTER — Researchers:
Andrew Wong, Sveta Fomchenko, Lee Winkler, Serena Yang.

ROSTER — Israel designers:
Yaara Bar, Chelsea Franz, Assaf Zinger, Eitan Koren, Tali Silon-Shacham, Erez Bar, Michael Dalal, Yoav Chen, Libi Becker Tidhar, Sveta Fomchenko, Lee Winkler, Lihi Shrem, Tal Segev.

ROSTER — India designers:
Advait Patil, Ajit Vaidya, Deepa Bhamare, Deepak Badgujar, Dinesh Koli, Gajanan Rajput, Manashree Thokal, Mayur Chaudhari, Parimal Khanolkar, Prafull Mane, Sheetal Barge-Gole, Shikha Shukla, Shilpa Sarkar, Sushanth Civi, Tapas Chowdhury, Umajit Mongjam, Kalpesh Gurav, Nirmitee Sisodia, Nutan Doiphode.

Note: Sveta Fomchenko and Lee Winkler appear in BOTH Researchers and Israel — they do research and design work. For the whole team, use the union of all three rosters, counting each person ONCE (dedup by identity, not by name string), and attribute Sveta and Lee to their designer team (Israel) rather than double-counting them under Researchers too.

STEPS:
1. Find all Tasks in project CXUX assigned to anyone in the roster(s) in scope, with status category Done and resolved within the year window.
2. For each, read Task Type and Story Points (missing SP = 0).
3. Bucket per designer, one column per Task Type:
   Discovery · Ideation · Usability test · Validation · Design Spec · Build Review · Marketing activities · Sol migration · Other · (no type).
   Fold unexpected values into Other, note in a footnote. Keep the Sol migration column even if empty for everyone.
4. Per designer, compute average SP/task EXCLUDING Build Review tasks (same formula as above), 1 decimal, "—" if no eligible tasks.
5. Include every roster member even if they closed zero tasks that year (all-zero row).
6. Present a table sorted by Total SP descending, one column per task type, plus a TOTAL row (team-wide average = total SP excl. Build Review / total tasks excl. Build Review):

   | Designer | Team | Disc | Ideation | Usab.test | Valid | Design Spec | Build Rev | Mktg | Sol mig | Other | (no type) | Tasks | SP | Avg SP/task¹ |
   |----------|------|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|

   Show the Team column only when the scope is the whole team; omit it for a single region or a single designer. `¹` = excluding Build Review.

   Footnotes: total tasks, count of (no type), unexpected types folded into Other, roster members with zero closed tasks.

Read-only — do not create, edit, or transition any issues.
