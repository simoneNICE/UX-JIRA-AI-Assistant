# Rovo Chat prompt — Capacity vs Demand forecast (VP / head of UX)

> ⚠️ **DRAFT — not validated.** This prompt has not been confirmed against real Jira
> data yet. The demand/capacity logic and thresholds are a first proposal and may be
> wrong; do not rely on its numbers for decisions until it has been reviewed and tested.

Read-only forward look: does the UX team's historical throughput cover the design
work coming in the next releases? Demand and capacity are BOTH measured as Story
Points on CXUX Epics, so the two sides are comparable. Paste into Rovo Chat.

---

You are helping me forecast whether the UX team is sized for the incoming roadmap.
This is read-only — do not create, edit, or transition any issue.

CONTEXT — CXUX hierarchy:
Capabilities live in the line-of-business (LOB) projects. UX design work lives in
project CXUX. A "CXUX Epic" is an Epic in project CXUX whose PARENT is a Capability —
that parent link is how a Capability connects to its UX work. Naming isn't consistent
across teams, so match on the parent relationship, never on summary text or prefix.

UNIT — everything is measured in Story Points on CXUX Epics, on both sides of the
comparison. Do NOT mix in Task-level Story Points; that would make demand and capacity
non-comparable. Treat an Epic with no Story Points as 0, and always report how many
Epics had no value set so the totals aren't read as complete.

INPUT — you may override, otherwise use the defaults:
LOOK-AHEAD: [how many upcoming releases to size, default 3]
BASELINE: [how many completed releases to average for capacity, default 4]

STEP 1 — Determine releases
Compute release codes in "YY.Q" format, where Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep,
Q4=Oct–Dec (after X.4 comes (X+1).1).
- Demand window = the next LOOK-AHEAD releases starting from the current one (Q+1).
- Baseline window = the BASELINE releases immediately before the current one.
List both sets explicitly before querying so I can confirm they're right.

STEP 2 — Demand (forward)
For each release in the demand window:
a. Find all issues of type Capability, across ALL projects, with fixVersion = that
   release and status not "Removed". Exclude Capabilities that belong to project CXUX
   itself. Keep: key, status, project.
b. For each Capability, find Epics in project CXUX whose parent is that Capability.
c. Per release, report: capability count, how many have ≥1 CXUX Epic, total CXUX Epic
   count, summed Epic Story Points, and count of Epics with no SP set.

STEP 3 — Capacity baseline (historical)
For each release in the baseline window:
a. Find Epics in project CXUX that were completed for that release — status category
   Done AND fixVersion = that release. (If an Epic carries no fixVersion, fall back to
   resolution date falling inside that release's work quarter.)
b. Per release, sum the Epic Story Points closed. Also split the sum by region using
   the Epic assignee against the rosters below (Epics assigned outside all rosters, or
   unassigned, go in an "Other" bucket noted separately — do not silently drop them).
c. Compute the average SP closed per release across the baseline window = capacity baseline.

STEP 4 — Gap
For each demand-window release: load % = demand SP / baseline avg SP, and gap =
baseline avg − demand SP. Traffic light: 🔴 if load > 110%, 🟠 if 90–110%, 🟢 if < 90%.

STEP 5 — Output
Header:
`# UX Capacity vs Demand — Forecast`
`*Generated: <date> | Read-only | Unit: Story Points on CXUX Epics*`

Then a "## Headline" block: baseline capacity (avg SP/release), demand per upcoming
release, gap per release with traffic light, and one ⚠️ confidence line stating how many
upcoming Epics have no SP set (real demand is higher than shown).

Then "## Demand — upcoming releases": a table with columns
| Release | Capabilities | …with CXUX Epic | CXUX Epics | SP (set) | Epics w/o SP | Load vs baseline |

Then "## Capacity baseline — last <BASELINE> completed releases": a table with columns
| Release | Epics closed | SP closed | Israel | India | USA | (Other) |
plus an **Avg** row.

Close with a one-line **Bottom line** naming which releases are over capacity and
whether unestimated Epics would push it further.

ROSTER — Israel designers:
Yaara Bar, Chelsea Franz, Assaf Zinger, Eitan Koren, Tali Silon-Shacham, Erez Bar,
Michael Dalal, Yoav Chen, Libi Becker Tidhar, Sveta Fomchenko, Lee Winkler, Lihi Shrem,
Tal Segev.

ROSTER — India designers:
Advait Patil, Ajit Vaidya, Deepa Bhamare, Deepak Badgujar, Dinesh Koli, Gajanan Rajput,
Manashree Thokal, Mayur Chaudhari, Parimal Khanolkar, Prafull Mane, Sheetal Barge-Gole,
Shikha Shukla, Shilpa Sarkar, Sushanth Civi, Tapas Chowdhury, Umajit Mongjam,
Kalpesh Gurav, Nirmitee Sisodia, Nutan Doiphode.

ROSTER — USA designers:
Doug Clement, Janet Gonzales, David Stoker, Sara Evans, Lorina Binning, Serena Yang,
Andrew Wong.
