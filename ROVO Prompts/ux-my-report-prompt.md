# Rovo Chat prompt — My annual report (designer, self-service)

Converted from `/ux-my-report <year>` in `JIRA Agent/public/agent-ux-process.md`.
Paste into Rovo Chat.

---

You are helping me build a breakdown of my own closed Jira work for a given year, in project CXUX only.

YEAR: [e.g. 2025 — ask me if I don't specify]

Window: Tasks resolved between <year>-01-01 and <year>-12-31 inclusive.

STEPS:
1. Find all Tasks in project CXUX assigned to me, with status category Done, resolved within that window.
2. For each, read its Task Type field and its Story Points (treat missing/null Story Points as 0).
3. Bucket by Task Type — one column per type:
   Discovery · Ideation · Usability test · Validation · Design Spec · Build Review · Marketing activities · Sol migration · Other · (no type, i.e. field empty/null).
   Fold any unexpected/unrecognized Task Type value into "Other" and note it in a footnote.
4. Compute average Story Points per task, EXCLUDING Build Review tasks:
   sum(SP of tasks where type ≠ Build Review) / count(tasks where type ≠ Build Review), rounded to 1 decimal. Show "—" if there are no non-Build-Review tasks.
5. Present:

   | Task Type | Count | SP |
   |-----------|------:|---:|
   | Ideation  | 5     | 20 |
   | …         |       |    |

   Summary line: `Total: N tasks · X SP · Avg SP/task (excl. Build Review): Y.Z`

   Footnotes: count of tasks with no Task Type set, and any unexpected types folded into Other.

Read-only — do not create, edit, or transition any issues.
