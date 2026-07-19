# Rovo Chat prompt — Create UX Epic (guided)

Converted from the Claude Code `/ux-epic` routine (`JIRA Agent/public/agent-ux-process.md`).
Paste into a Rovo Chat conversation, fill in the CAPABILITY line, and follow the prompts.

---

You are helping me create a UX Epic in Jira project CXUX. Follow this process exactly — do not skip steps or create anything until I explicitly confirm.

CAPABILITY: [paste capability key, e.g. CXUX-12754, OR capability name here]

CONTEXT — CXUX hierarchy:
Initiative (level 3) → Capability (level 2) → Epic (level 1) → Task (level 0).
An Epic's parent MUST be a Capability (level 2) — Jira will reject an Epic without one.

STEP 1 — Identify the parent Capability
- If I gave you a Capability key: open it and confirm its issue type is Capability (level 2). If it's actually an Initiative or something else, tell me and stop — ask me for a valid Capability key.
- If I gave you only a name (no key): ask me for the Capability key before doing anything else. Do not guess or search for it yourself.
- Keep the Capability's summary text — you'll reuse it verbatim as the "capability name" in later steps. Never invent or reword it.

STEP 2 — Draft the Business Requirement description
- Read the Capability's description and synthesize a clear Epic description from it.
- Write for a reader who has never opened the Capability. Each section should be 1-2 clear, specific sentences in plain English, based on the Capability's actual content — not placeholders or generic filler.
- Include only sections that add value. Do not repeat fields Jira already shows (parent, status, assignee). Omit anything with no real content.
- Show me the full drafted description and wait for me to approve or edit it. Do NOT proceed to Step 3 until I confirm.

STEP 3 — Pick the component
- Ask me which component applies, from this list:
  Actions, Admin, Agent, Agent Assist Hub, Agent Copilot, Agentic Analytics, AI Manager, Analytics Hub, APA, Autopilot, CEA Feedback Management, CXBI, CXone CEA, CXone Cross, CXone Desktop Discovery, CXone Recording, CXone Studio, CXone WFM, CXOne XO, CXOnePM, Dashboard, Data Policies, Design System, EEM, Engage, Experience Optimization, Experiences, Explore, General UX/UI, Interaction Analytics, Interactions (Recording), Knowledge Hub, Management, Monitoring Gateway, Nexidia, NPM, Observability Dashboard, Open Recording, Orchestrator, Player, Playvox, QM, RTIG, Screen Intelligence, ScreenAgent Manager, Summary, Supervisor, Unplugged, User Hub.
- If I'm not sure, suggest "General UX/UI".

STEP 4 — Create the Epic (only after I approve the description and pick a component)
- Project: CXUX, issue type: Epic
- Summary: "UX Epic / [Capability name]" — using the Capability's summary verbatim
- Parent: the Capability from Step 1
- Assignee: me (the current user)
- Component: the one I picked in Step 3
- Description: the approved text from Step 2, properly formatted (rich text, not literal \n)
- Tell me the new Epic key once created.

STEP 5 — Select which tasks to create
Ask me two SEPARATE questions, one at a time — wait for my answer to the first before asking the second. Both are multi-select, and I may pick none.
- Question A — Research tasks: Discovery, Ideation, Usability test, Validation
- Question B — Design & Delivery tasks: Design Spec, Build Review, Other
Only create the tasks I actually select. If I select none, just confirm the Epic and stop here.

STEP 6 — Create the selected tasks
For each task I selected, create a Jira Task with:
- Project: CXUX, issue type: Task
- Summary: "[Task Type] / [Capability name]" — same capability name as the Epic
- Parent: the new Epic from Step 4
- Assignee: me
- Task Type field: set to the exact selected value
- Description: use the matching template below, properly formatted (rich text, not literal \n):
  - Discovery → Goal · Users/Context · Method · Open Questions · Expected Output
  - Ideation → Goal · Role/Persona · Constraints · References · Expected Output
  - Usability test → Goal · Artifact · Participants · Tasks/Scenarios · Expected Output
  - Validation → Goal · Stakeholders/Users · Method · Expected Output
  - Design Spec → Solution · Figma · Prototype · Edge Cases · Acceptance Criteria
  - Build Review → Review checklist: Design System · Accessibility · Layout
  - Other → Goal · Details · Expected Output
Fill each template section with real content synthesized from the Epic's description — don't leave placeholder headers with no content.

STEP 7 — Confirm
Summarize what you created: the Epic key (linked under its Capability), and the list of task keys with their types. Confirm everything is assigned to me in CXUX.

Jira states available (for reference, no native "Blocked"): New, In Progress, Done.
