# Rovo Chat prompt — My annual report (designer, self-service)

Converted from `/ux-my-report <year>` in `JIRA Agent/public/agent-ux-process.md`.
Paste into Rovo Chat.

---

You are helping me build a breakdown of my own closed Jira work for a given year, in project CXUX only.

YEAR: [e.g. 2025 — ask me if I don't specify]

Window: Tasks resolved between <year>-01-01 and <year>-12-31 inclusive.

IMPORTANT — field names (this Jira has look-alikes, use the exact ones):
- Story Points: use the field named exactly "Story Points". Do NOT use "Story point estimate" or "Estimated Story Points" — those are different fields and are usually empty on these tasks, so using them makes every number come out as 0. (If you need the internal id, Story Points is customfield_10038.)
- Task Type: the field named exactly "Task Type" (customfield_10286).

WHAT COUNTS: only genuinely completed work. Include tasks with status = Done. EXCLUDE tasks whose resolution is "Removed" (cancelled work), even though they share the Done status category.

HOW TO QUERY (do it one Task Type at a time — don't try to load every task at once):
Task Type values to report, one row each:
Discovery · Ideation · Usability test · Validation · Design Spec · Build Review · Marketing activities · Sol migration · Other · (no type, i.e. Task Type empty).

For EACH Task Type value, run a separate search — Tasks in project CXUX, assigned to me (currentUser), status = Done, resolution != Removed, resolved within the window, and Task Type = that value — then:
- read the Count of that search, and
- sum the "Story Points" field across those tasks (treat empty Story Points as 0).
Then move to the next Task Type. This keeps each batch small and reliable.
Fold any unexpected/unrecognized Task Type value into "Other" and note it in a footnote.

AVERAGE: compute average Story Points per task EXCLUDING Build Review tasks:
sum(SP of tasks where type ≠ Build Review) / count(tasks where type ≠ Build Review), rounded to 1 decimal. Show "—" if there are no non-Build-Review tasks.

PRESENT:

   | Task Type | Count | SP |
   |-----------|------:|---:|
   | Ideation  | 5     | 20 |
   | …         |       |    |

Summary line: `Total: N tasks · X SP · Avg SP/task (excl. Build Review): Y.Z`

Footnotes: count of tasks with no Task Type set, and any unexpected types folded into Other.

Read-only — do not create, edit, or transition any issues.
