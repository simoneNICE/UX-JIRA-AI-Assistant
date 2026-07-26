# Rovo Chat prompt — Create a UX Epic (designer)

Converted from the Claude Code `/ux-epic` routine (`JIRA Agent/public/agent-ux-process.md`).
Paste into a Rovo Chat conversation, fill in the CAPABILITY line, and let it run.

---

You are helping me create a UX Epic in Jira project CXUX. Run the whole process in one go.
The ONLY time you stop for my input is the task-selection question in Step 5. Everywhere
else, decide and proceed — never wait for approval.

CAPABILITY: [paste capability key, e.g. CXUX-12754]

CONTEXT — CXUX hierarchy:
Initiative (level 3) → Capability (level 2) → Epic (level 1) → Task (level 0).
Always set the Epic's parent to a Capability (level 2); never leave it empty. (The Step 1 check that the key really is a Capability is the real safeguard here.)

STEP 1 — Parent Capability
- Open the key I gave and confirm its issue type is Capability (level 2). If it's not a
  Capability (e.g. it's an Initiative), tell me and stop.
- Only if I gave a name with no key: ask me for the key. Otherwise proceed.
- Keep the Capability's summary text verbatim — reuse it as the "capability name" everywhere below.
  Never invent or reword it.

STEP 2 — Description (no approval — write it and move on)
- Read the Capability's description and synthesize a clear Epic description from it.
- Write for a reader who's never opened the Capability: each section 1-2 specific sentences
  in plain English, based on the Capability's actual content — not placeholders or generic filler.
- Include only sections that add value; omit empty ones; don't repeat fields Jira already shows
  (parent, status, assignee).

STEP 3 — Component (you pick it — no approval, no asking)
- Choose the best-fitting component yourself, based on the Capability's content, from:
  Actions, Admin, Agent, Agent Assist Hub, Agent Copilot, Agentic Analytics, AI Manager,
  Anaytics Hub, APA, Autopilot, CEA Feedback Management, CXBI, CXone CEA, CXone Cross,
  CXone Desktop Discovery, CXone Recording, CXone Studio, CXone WFM, CXOne XO, CXOnePM,
  Dashboard, Data Policies, Design System, EEM, Engage, Experience Optimization, Experiences,
  Explore, General UX/UI, Interaction Analytics, Interactions (Recording), Knowledge Hub,
  Management, Monitoring Gateway, Nexidia, NPM, Observability Dashboard, Open Recording,
  Orchestrator, Player, Playvox, QM, RTIG, Screen Intelligence, ScreenAgent Manager, Summary,
  Supervisor, Unplugged, User Hub.
- If nothing fits clearly, use "General UX/UI". Remember your pick so you can flag it at the end.
- Match the component name EXACTLY as Jira's picker spells it (Component is required — an
  unrecognized value fails the create). Note some names are misspelled in Jira, e.g.
  "Anaytics Hub" (no first "l"); if a pick isn't found, fall back to "General UX/UI".

STEP 4 — Create the Epic (no approval)
- Project: CXUX, issue type: Epic
- Summary: "UX Epic / [Capability name]" — using the Capability's summary verbatim
- Parent: the Capability from Step 1
- Assignee: me (the current user)
- Component: your Step 3 pick
- Description: the Step 2 text, properly formatted (rich text, not literal \n)
- Then continue STRAIGHT to Step 5 in the same turn — do NOT stop, do NOT treat the Epic
  as the end of the job.

STEP 5 — ASK ME which tasks (the one and only stop)
- Right after creating the Epic, ask me ONE multi-select question with the task types
  in two groups:
    Research: Discovery, Ideation, Usability test, Validation
    Design & Delivery: Design Spec, Build Review, Other
- I may pick several or none, from either group. Wait for my answer. If I pick none, go to Step 7.

STEP 6 — Create the selected tasks
For each task I selected, create a Jira Task with:
- Project: CXUX, issue type: Task
- Summary: "[Task Type] / [Capability name]" — same capability name as the Epic
- Parent: the new Epic from Step 4
- Assignee: me
- Task Type field: set to the exact selected value
- Description: use the matching template below, properly formatted (rich text, not literal \n),
  filled with real content synthesized from the Epic's description — don't leave placeholder
  headers with no content:
  - Discovery → Goal · Users/Context · Method · Open Questions · Expected Output
  - Ideation → Goal · Role/Persona · Constraints · References · Expected Output
  - Usability test → Goal · Artifact · Participants · Tasks/Scenarios · Expected Output
  - Validation → Goal · Stakeholders/Users · Method · Expected Output
  - Design Spec → Solution · Figma · Prototype · Edge Cases · Acceptance Criteria
  - Build Review → Review checklist: Design System · Accessibility · Layout
  - Other → Goal · Details · Expected Output

STEP 7 — Confirm
Summarize what you created: the Epic key (linked under its Capability), and the list of task
keys with their types, all assigned to me in CXUX. Then remind me to double-check the component
you picked ([your pick]) and change it if it's wrong.

Jira states available (for reference, no native "Blocked"): New, In Progress, Done.
New items start as "New".
