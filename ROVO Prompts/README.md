# ROVO Designers — prompt library

Rovo Chat prompts converted from the Claude Code JIRA Agent (`../JIRA Agent/`). Each file
is a single self-contained prompt — paste it into a Rovo Chat conversation and fill in the
bracketed parameter at the top.

## Designer prompts (from `JIRA Agent/public/agent-ux-process.md`)

| File | Converted from | What it does |
|------|-----------------|---------------|
| [ux-epic-prompt.md](ux-epic-prompt.md) | `/ux-epic <capability>` | Creates a UX Epic under a Capability, with guided task selection |
| [ux-my-health-prompt.md](ux-my-health-prompt.md) | `/ux-my-health` | Self-service health check on your own active work |
| [ux-my-report-prompt.md](ux-my-report-prompt.md) | `/ux-my-report <year>` | Your own closed-task breakdown for a year |

## Manager prompts (from `JIRA Agent/manager/agent-ux-manager.md`)

| File | Converted from | What it does |
|------|-----------------|---------------|
| [ux-overview-prompt.md](ux-overview-prompt.md) | `/ux-overview <team\|all>` | Active-sprint snapshot per designer |
| [ux-designer-health-prompt.md](ux-designer-health-prompt.md) | `/ux-designer-health <team\|all>` | Health check across designers (Israel/India/USA/all) |
| [ux-research-health-prompt.md](ux-research-health-prompt.md) | `/ux-research-health` | Health check on the UX Researches portfolio |
| [ux-annual-report-prompt.md](ux-annual-report-prompt.md) | `/ux-annual-report <team\|all> <year>` | Per-designer closed-work breakdown for a year |
| [ux-lob-summary-prompt.md](ux-lob-summary-prompt.md) | `/ux-lob-summary [release1 release2]` | Design readiness across all LOB projects/releases |

## Not converted

- `/ux-setup` (both agents) — Claude Code–specific: creates a local `user-profile.md` and
  checks MCP connections. Doesn't apply to Rovo, which already knows the current user's
  identity and Jira access inside the chat.

## Conversion notes (apply to all prompts here)

- Rosters (names + account IDs) from `JIRA Agent/manager/team-config.md` are embedded
  directly in each prompt — Rovo has no file access, so the source of truth for names/IDs
  lives in `team-config.md`; update both if the roster changes.
- No custom field IDs (`customfield_10xxx`) — Rovo resolves fields by their visible name.
- No subagent delegation, file-based JQL pagination, or HTML/Chart.js report generation —
  those are Claude Code environment mechanics. Output is presented directly in the chat as
  text/tables. Every prompt ends with "read-only" to keep these reporting-only, no writes.
- Stalled-epic age checks use the JQL "status changed to X before Nd" pattern instead of a
  changelog fetch, since it works the same way for Epics as it does for Tasks.
