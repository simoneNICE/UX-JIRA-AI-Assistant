#!/usr/bin/env python3
"""
Generator for the public ROVO Prompts site (GitHub Pages).

Reads the prompts in `ROVO Prompts/`, extracts the copyable body (everything after
the first `---`) and regenerates `site/index.html`.

Usage:
    python3 build-site.py

To add/edit a prompt: edit the .md in `ROVO Prompts/`, update the MANIFEST below
(category, title, blurb, tags) and re-run this script.

Each card shows an "Updated" date. It is derived automatically from git (see
`last_updated`) — there is nothing to bump by hand. Editing a prompt and
re-running this script is enough: the date tracks the file's last change.
"""

import datetime
import html
import pathlib
import subprocess
import sys

# Flag every card as Draft (until each prompt is re-validated in Rovo). See use below.
DRAFT_ALL = True

ROOT = pathlib.Path(__file__).resolve().parent
PROMPTS_DIR = ROOT / "ROVO Prompts"
SITE_DIR = ROOT / "site"
OUT = SITE_DIR / "index.html"

# --- Manifest: order, category, clean title and short blurb for each prompt ---
# category: "designers" | "researchers" | "managers" | "leadership"
MANIFEST = [
    # --- Designers ---
    {
        "file": "ux-epic-prompt.md",
        "category": "designers",
        "title": "Create a UX Epic",
        "what_for": "Create a well-structured UX Epic under a Capability in CXUX, without building it by hand.",
        "input": "A Capability key (e.g. CXUX-12754).",
        "does": "Reads the capability, writes the epic for you and files it under that capability in your name, then asks which tasks you want and adds them — each already filled in with a starting template.",
        "output": "The new Epic plus the chosen tasks, all linked and assigned to you.",
        "note": "The only prompt that writes to Jira — and only after you confirm the tasks.",
        "tags": ["writes", "autonomous"],
    },
    {
        "file": "ux-my-health-prompt.md",
        "category": "designers",
        "title": "My health check",
        "what_for": "See in seconds whether your current workload is healthy.",
        "input": "None — it looks at your own issues across all projects.",
        "does": "Looks at everything you have on the go and tells you whether it's too much, too little, or just right — and points out anything that's been sitting still too long.",
        "output": "A short verdict, most severe flag first.",
        "note": "Counts only leaf work items (not Epics/Capabilities); ages measured from the status-change date.",
        "tags": ["self-service", "read-only"],
    },
    {
        "file": "ux-my-report-prompt.md",
        "category": "designers",
        "title": "My annual report",
        "what_for": "See your closed work for a year, broken down by task type.",
        "input": "The year (e.g. 2025).",
        "does": "Pulls together everything you finished that year and sorts it by type of work, with totals and an average effort per task.",
        "output": "A Task Type / Count / SP table plus a total line.",
        "note": "Read-only; uses the exact “Story Points” field and excludes cancelled tasks.",
        "tags": ["self-service", "read-only"],
    },
    # --- Researchers ---
    # (no research-specific prompt ready yet — see prompts-status.md)
    # --- Managers ---
    {
        "file": "ux-overview-prompt.md",
        "category": "managers",
        "title": "Team sprint overview",
        "what_for": "A snapshot of the active sprint — how much work each designer has right now.",
        "input": "Asks your scope first: whole team, a region, or a single designer.",
        "does": "For the current sprint, shows how much each designer has on their plate and how far along it is; people with nothing still show up.",
        "output": "A per-designer table sorted by Story Points, with a total row.",
        "note": "Excludes “Removed” tasks; uses the exact Story Points field.",
        "tags": ["team", "read-only"],
    },
    {
        "file": "ux-designer-health-prompt.md",
        "category": "managers",
        "title": "Designer health check",
        "what_for": "The team version of the personal health check — who's overloaded, idle, or stalled.",
        "input": "Scope: whole team, a region, or a single designer (the prompt asks).",
        "does": "Checks each person's live workload and points out who's stretched thin, who has nothing going, and who's stuck.",
        "output": "Overloaded / Idle / Watch lists, plus who's fine.",
        "note": "Sprint-phase lens only applies to a single designer; out-of-sync now checks both directions.",
        "tags": ["team", "read-only"],
    },
    {
        "file": "ux-research-health-prompt.md",
        "category": "managers",
        "title": "Researcher health check",
        "what_for": "The same health check on the Research portfolio (Epics under CXUX-12163), for researchers.",
        "input": "None — the researcher roster is built into the prompt.",
        "does": "Goes through the current researches and checks each researcher's workload the same way — too much, too little, or stuck.",
        "output": "One block per researcher, most severe first.",
        "note": "Read-only; counts a researcher's tasks under their Epics regardless of the task's own assignee.",
        "tags": ["team", "research", "read-only"],
    },
    {
        "file": "ux-capability-review-prompt.md",
        "category": "managers",
        "title": "Research capability review",
        "what_for": "Review all the researches inside the current-semester Capability — a portfolio view, not per person.",
        "input": "Optional — a Capability key (defaults to the current one under CXUX-12163).",
        "does": "Goes through all the researches in the current cycle: how many are new, running, or done, which ones are dragging, how they split across apps and topics, and which look like duplicates.",
        "output": "A report with status counts, health, researches-per-app, categories, and overlap candidates.",
        "note": "DRAFT, not validated. Overlap detection is advisory AI judgment; age is shown in buckets, not exact days.",
        "tags": ["draft", "team", "research", "portfolio", "read-only"],
    },
    {
        "file": "ux-annual-report-prompt.md",
        "category": "managers",
        "title": "Designer annual report",
        "what_for": "The manager version of the annual report — closed work in a year for every designer.",
        "input": "Year + scope: whole team, a region, or a single designer (the prompt asks).",
        "does": "Shows what every designer finished that year, sorted by type of work, including anyone who closed nothing.",
        "output": "A table sorted by total SP, with a TOTAL row and team average.",
        "note": "Uses the exact Story Points field, excludes cancelled tasks, works in small batches to stay reliable.",
        "tags": ["team", "read-only"],
    },
    {
        "file": "ux-lob-summary-prompt.md",
        "category": "managers",
        "title": "Design readiness",
        "what_for": "A traffic light of design readiness per capability, for one LOB project + release.",
        "input": "Project key + fix version (e.g. CXREC, 26.4) — asks if missing.",
        "does": "For each feature going into that release, checks whether the design is ready and flags the ones that are behind, or that design never picked up at all.",
        "output": "One table with a red/amber/green light per capability, plus a “Needs Attention” red list.",
        "note": "Matches fix versions by prefix (catches names like 26.4-CSA); ignores cancelled tasks.",
        "tags": ["portfolio", "read-only"],
    },
    {
        "file": "ux-release-workload-prompt.md",
        "category": "managers",
        "title": "Release workload",
        "what_for": "Size the UX workload of one project in one release.",
        "input": "Project key + fix version (e.g. CXREC, 26.4).",
        "does": "Adds up how much design work a release carries — how many features need it, how much effort it adds up to, and who owns it.",
        "output": "Four headline numbers plus a per-capability table.",
        "note": "The Capability↔UX Epic link is by parent, not by name; uses the exact Story Points field.",
        "tags": ["portfolio", "read-only"],
    },
    # --- Leadership (VP) ---
    {
        "file": "ux-capacity-demand-prompt.md",
        "category": "leadership",
        "title": "Capacity vs demand",
        "what_for": "A forward look — does the team's historical throughput cover the design work in the next releases?",
        "input": "Optional — look-ahead releases (default 3) and baseline releases (default 4).",
        "does": "Compares how much design work is coming up against how much the team has usually delivered, to see whether the next releases are over or under what the team can handle.",
        "output": "A headline with baseline capacity, demand per release, and gap with a traffic light, plus two tables.",
        "note": "DRAFT and data-limited — only ~35% of epics have Story Points set, so the forecast is indicative only.",
        "tags": ["draft", "portfolio", "read-only"],
    },
]

CATEGORIES = [
    {
        "id": "designers",  # designers + researchers (individual contributors)
        "label": "Designers & Researchers",
        "icon": "",
        "desc": "Self-service prompts for your day-to-day work: create epics, check your health, review your year.",
    },
    {
        "id": "managers",
        "label": "Managers",
        "icon": "&#128202;",  # 📊
        "desc": "Team and portfolio views: overview, health checks, annual reports, design readiness.",
    },
    {
        "id": "leadership",
        "label": "Leadership (VP)",
        "icon": "&#127919;",  # 🎯
        "desc": "Org-wide forward views for UX leadership: capacity vs demand, strategic risk, trends.",
    },
]


EXPLAIN_ROWS = [
    ("what_for", "What it's for"),
    ("input", "Input"),
    ("does", "What it does"),
    ("output", "Output"),
    ("note", "Note"),
]


def explain_block(entry: dict) -> str:
    """Render the structured card body: a labelled two-column table
    (What it's for / Input / What it does / Output / Note). Rows with no text
    are skipped; the Note row gets a subtler style. Text is escaped."""
    rows = []
    for key, label in EXPLAIN_ROWS:
        text = entry.get(key, "")
        if not text:
            continue
        cls = "ex-row ex-note" if key == "note" else "ex-row"
        rows.append(
            f'<div class="{cls}"><div class="ex-label">{label}</div>'
            f'<div class="ex-val">{html.escape(text)}</div></div>'
        )
    if not rows:
        return ""
    return f'<div class="explain">{"".join(rows)}</div>'


def extract_body(md_text: str) -> str:
    """The copyable body is everything after the first standalone `---` line."""
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---":
            body = "\n".join(lines[i + 1 :]).strip()
            return body
    # No separator: use the whole file
    return md_text.strip()


def last_updated(path: pathlib.Path) -> str:
    """ISO date (YYYY-MM-DD) of the prompt's last real change — the card's
    "Updated" date.

    STANDARD: the date auto-tracks git, so there is nothing to bump by hand.
    A committed prompt shows its last commit date; a prompt with uncommitted
    edits shows today. So every time we edit a prompt and re-run this script,
    the card date is current — no manual step. Falls back to the file's
    modification time when git isn't available (e.g. outside a repo)."""
    rel = str(path)
    try:
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        if dirty.returncode == 0 and dirty.stdout.strip():
            return datetime.date.today().isoformat()
        log = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        date = log.stdout.strip()
        if log.returncode == 0 and date:
            return date
    except Exception:
        pass
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def added_date(path: pathlib.Path) -> str:
    """ISO date (YYYY-MM-DD) the prompt was first added to the repo — the date
    of its earliest commit. Falls back to the file's modification time when git
    isn't available or the file isn't committed yet."""
    rel = str(path)
    try:
        log = subprocess.run(
            ["git", "log", "--reverse", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        if log.returncode == 0 and log.stdout.strip():
            return log.stdout.strip().splitlines()[0]
    except Exception:
        pass
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def human_date(iso: str) -> str:
    """'2026-07-19' -> 'Jul 19, 2026' for display; passthrough on parse error."""
    try:
        return datetime.date.fromisoformat(iso).strftime("%b %-d, %Y")
    except ValueError:
        return iso


def build():
    if not PROMPTS_DIR.is_dir():
        sys.exit(f"Prompts folder not found: {PROMPTS_DIR}")

    # Load bodies
    prompts = []
    for entry in MANIFEST:
        path = PROMPTS_DIR / entry["file"]
        if not path.is_file():
            sys.exit(f"Prompt missing from manifest: {path}")
        body = extract_body(path.read_text(encoding="utf-8"))
        prompts.append({
            **entry, "body": body,
            "updated": last_updated(path),
            "added": added_date(path),
        })

    # Default order: alphabetical by title (the JS "Sort by" control can re-order live)
    prompts.sort(key=lambda p: p["title"].lower())

    # Counts per category
    counts = {c["id"]: 0 for c in CATEGORIES}
    for p in prompts:
        counts[p["category"]] += 1

    total = len(prompts)

    # --- Build HTML ---
    cards_by_cat = {c["id"]: [] for c in CATEGORIES}
    for idx, p in enumerate(prompts):
        pid = f"p-{idx}"
        explain_html = explain_block(p)
        # DRAFT_ALL: every prompt is flagged Draft until it's re-validated in Rovo after the
        # hardening pass. Set to False to go back to per-prompt "draft" tags only.
        draft_badge = '<span class="badge-draft">Draft</span>' if (DRAFT_ALL or "draft" in p.get("tags", [])) else ""
        updated_iso = p["updated"]
        added_iso = p["added"]
        search_text = " ".join(
            [p["title"]]
            + [p.get(k, "") for k, _ in EXPLAIN_ROWS]
            + [updated_iso]
            + p.get("tags", [])
        )
        card = f"""
        <article class="card" data-search="{html.escape(search_text.lower())}" data-title="{html.escape(p['title'].lower())}" data-added="{added_iso}" data-modified="{updated_iso}">
          <div class="card-head">
            <h3>{html.escape(p['title'])}</h3>
            {draft_badge}
          </div>
          {explain_html}
          <div class="card-actions">
            <span class="updated" title="Last updated {updated_iso}">Updated {html.escape(human_date(updated_iso))}</span>
            <button class="btn btn-primary" data-copy="{pid}">Copy prompt</button>
          </div>
          <pre class="prompt-body" id="{pid}" hidden>{html.escape(p['body'])}</pre>
        </article>"""
        cards_by_cat[p["category"]].append(card)

    panels = []
    tabs = []
    for i, c in enumerate(CATEGORIES):
        active = " active" if i == 0 else ""
        cid = c["id"]
        n = counts[cid]
        tabs.append(
            f'<button class="tab{active}" data-tab="{cid}" role="tab" aria-selected="{"true" if i==0 else "false"}">'
            f'{c["label"]} <span class="tab-count">{n}</span></button>'
        )
        cards = "\n".join(cards_by_cat[cid])
        if not cards.strip():
            cards = (
                '<div class="empty">'
                '<div class="empty-icon">&#128220;</div>'
                "<p>No prompts ready in this category yet.</p>"
                '<p class="empty-sub">We\'re writing them &mdash; see the status in <code>prompts-status.md</code>.</p>'
                "</div>"
            )
        panels.append(
            f'<section class="panel{active}" id="panel-{cid}" role="tabpanel">'
            f'<p class="cat-desc">{c["desc"]}</p>'
            f'<div class="grid">{cards}</div>'
            f"</section>"
        )

    tabs_html = "\n".join(tabs)
    panels_html = "\n".join(panels)

    doc = TEMPLATE.format(
        tabs=tabs_html,
        panels=panels_html,
        total=total,
    )

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"OK  {OUT}")
    print(f"    {total} prompts  |  " + "  ".join(f"{c['label']}: {counts[c['id']]}" for c in CATEGORIES))


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ROVO Prompts by Simone</title>
<meta name="description" content="Rovo Chat prompt library for the UX team: monitor and manage work on Jira. Designers, Researchers, Managers.">
<style>
  /* Atlassian Design System tokens */
  :root {{
    --bg: #f7f8f9;               /* elevation.surface.sunken */
    --surface: #ffffff;          /* elevation.surface */
    --surface-2: #f1f2f4;        /* background.neutral */
    --border: #dcdfe4;           /* color.border */
    --text: #172b4d;             /* color.text */
    --text-dim: #44546f;         /* color.text.subtle */
    --text-subtlest: #626f86;    /* color.text.subtlest */
    --accent: #0c66e4;           /* background.brand.bold */
    --accent-hover: #0055cc;     /* background.brand.bold.hovered */
    --accent-soft: #e9f2ff;      /* background.selected / blue subtlest */
    --nav: #0c66e4;              /* Jira global-nav bar (blue, same in light/dark) */
    --neutral-btn: #ebecf0;      /* background.neutral (button subtle) */
    --neutral-btn-hover: #dcdfe4;
    --ok: #22a06b;               /* color.text.success */
    --radius: 8px;               /* radius.medium (cards) */
    --radius-sm: 3px;            /* radius.small (controls, lozenges) */
    --shadow: 0 1px 1px rgba(9,30,66,.25), 0 0 1px rgba(9,30,66,.31); /* elevation.shadow.raised */
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #101214;             /* elevation.surface.sunken (dark) */
      --surface: #1d2125;        /* elevation.surface (dark) */
      --surface-2: #282e33;      /* background.neutral (dark) */
      --border: #2c333a;         /* color.border (dark) */
      --text: #c7d1db;           /* color.text (dark) */
      --text-dim: #9fadbc;       /* color.text.subtle (dark) */
      --text-subtlest: #8c9bab;  /* color.text.subtlest (dark) */
      --accent: #579dff;         /* background.brand.bold (dark) */
      --accent-hover: #85b8ff;   /* hovered (dark) */
      --accent-soft: #1c2b41;    /* background.selected (dark) */
      --neutral-btn: #a1bdd914;
      --neutral-btn-hover: #a6c5e229;
      --ok: #4bce97;
      --shadow: 0 1px 1px rgba(3,4,4,.5), 0 0 1px rgba(3,4,4,.6);
    }}
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font: 14px/1.428 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
    -webkit-font-smoothing: antialiased;
  }}
  .wrap {{ max-width: 1080px; margin: 0 auto; padding: 0 20px 80px; }}

  /* Jira-style global navigation (blue bar, white content) */
  .topbar {{ position: sticky; top: 0; z-index: 50; background: var(--nav); color: #fff; }}
  .topbar-inner {{ padding: 0 16px; height: 48px; display: flex; align-items: center; gap: 4px; }}
  .tb-brand {{ flex: 1; min-width: 0; display: inline-flex; align-items: center; gap: 8px; padding: 6px 8px; font-weight: 600; font-size: 16px; color: #fff; }}
  .tb-brand svg {{ flex: none; fill: #fff; }}
  .tb-brand .brand-text {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .tb-spacer {{ flex: 1; }}
  .tb-search {{ flex: 0 1 480px; margin: 0 8px; position: relative; }}
  .tb-search input {{ width: 100%; height: 32px; padding: 0 12px 0 34px; border-radius: var(--radius-sm); border: 1px solid rgba(255,255,255,.45); background: #fff; color: var(--text); font-size: 14px; outline: none; }}
  .tb-search input:focus {{ box-shadow: 0 0 0 2px rgba(255,255,255,.55); }}
  .tb-search svg {{ position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: var(--text-subtlest); }}
  @media (max-width: 560px) {{ .tb-brand .brand-text {{ display: none; }} }}

  header.hero {{
    padding: 24px 0 12px;
    display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px 14px;
  }}
  .eyebrow {{
    font-size: 11px; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; color: var(--accent);
    padding: 2px 8px; background: var(--accent-soft); border-radius: var(--radius-sm);
  }}
  h1 {{ font-size: 22px; line-height: 1.15; margin: 0; letter-spacing: -.01em; }}
  .lede {{ font-size: 14px; color: var(--text-dim); margin: 0; flex-basis: 100%; }}
  .integrations {{ flex-basis: 100%; display: flex; align-items: center; gap: 9px; margin-top: 4px; font-size: 12px; color: var(--text-dim); }}
  .integrations .il {{ display: inline-flex; align-items: center; gap: 5px; font-weight: 600; color: var(--text); }}
  .integrations .sep {{ opacity: .45; }}
  .ilogo {{ display: block; flex: none; }}

  .search {{ margin: 16px 0 4px; position: relative; max-width: 340px; }}
  .search input {{
    width: 100%; padding: 8px 12px 8px 34px; font-size: 14px;
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm);
    color: var(--text); outline: none; transition: border-color .15s, box-shadow .15s;
  }}
  .search input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }}
  .search svg {{ position: absolute; left: 11px; top: 50%; transform: translateY(-50%); color: var(--text-dim); }}

  .tabbar {{
    display: flex; align-items: flex-end; justify-content: space-between; gap: 12px;
    flex-wrap: nowrap; margin: 18px 0 20px; border-bottom: 1px solid var(--border);
  }}
  .tabs {{
    display: flex; gap: 8px; flex-wrap: wrap; flex: 1 1 auto; min-width: 0;
  }}
  .tab {{
    appearance: none; background: none; border: none; cursor: pointer;
    font: inherit; font-weight: 600; color: var(--text-dim);
    padding: 10px 12px; border-radius: var(--radius-sm) var(--radius-sm) 0 0; position: relative;
    display: inline-flex; align-items: center; gap: 8px; transition: color .15s, background .15s;
  }}
  .tab:hover {{ color: var(--text); background: var(--surface-2); }}
  .tab.active {{ color: var(--accent); }}
  .tab.active::after {{
    content: ""; position: absolute; left: 12px; right: 12px; bottom: -1px; height: 2px;
    background: var(--accent); border-radius: 2px;
  }}
  .tab-icon {{ font-size: 17px; }}
  .tab-count {{
    font-size: 12px; font-weight: 700; background: var(--surface-2); color: var(--text-dim);
    padding: 1px 8px; border-radius: 999px; min-width: 22px; text-align: center;
  }}
  .tab.active .tab-count {{ background: var(--accent-soft); color: var(--accent); }}

  .panel {{ display: none; }}
  .panel.active {{ display: block; animation: fade .2s ease; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
  .cat-desc {{ color: var(--text-dim); margin: 0 0 20px; font-size: 14px; }}

  .controls {{ display: flex; align-items: center; gap: 8px; padding-bottom: 6px; flex: none; }}
  .sort-ctl {{ font-size: 12px; font-weight: 600; color: var(--text-subtlest);
               text-transform: uppercase; letter-spacing: .04em; }}
  #sort {{
    appearance: none; font: inherit; font-size: 13px; color: var(--text); cursor: pointer;
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm);
    padding: 6px 30px 6px 10px; outline: none; transition: border-color .15s, box-shadow .15s;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23626f86' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 8px center;
  }}
  #sort:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }}

  .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
  @media (max-width: 640px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  .card {{
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 20px; box-shadow: var(--shadow); display: flex; flex-direction: column;
    transition: transform .15s, border-color .15s;
  }}
  .card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}
  .card-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 10px; }}
  .card h3 {{ font-size: 17px; margin: 0; letter-spacing: -.01em; }}
  .badge-draft {{ flex: none; align-self: flex-start; font-size: 10px; font-weight: 800;
                  text-transform: uppercase; letter-spacing: .07em; color: #fff;
                  background: #d92d20; border-radius: 5px; padding: 2px 7px; line-height: 1.4;
                  white-space: nowrap; }}
  .explain {{ margin: 12px 0 14px; border-top: 1px solid var(--border); flex: 1; }}
  .ex-row {{ display: grid; grid-template-columns: 92px 1fr; gap: 12px; align-items: start;
             padding: 9px 0; border-bottom: 1px solid var(--border); }}
  .ex-label {{ font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
               color: var(--text-subtlest); padding-top: 2px; }}
  .ex-val {{ font-size: 13px; line-height: 1.5; color: var(--text-dim); }}
  .ex-note .ex-val {{ font-style: italic; color: var(--text-subtlest); }}
  .card-actions {{ display: flex; align-items: center; gap: 8px; margin-top: 16px; }}
  .updated {{ font-size: 11.5px; color: var(--text-subtlest); white-space: nowrap; }}
  .card-actions .btn-primary {{ margin-left: auto; }}
  .btn {{
    appearance: none; font: inherit; font-weight: 500; font-size: 14px; cursor: pointer;
    border-radius: var(--radius-sm); padding: 7px 12px; border: none; transition: background .1s;
  }}
  .btn-primary {{ background: var(--accent); color: #fff; }}
  .btn-primary:hover {{ background: var(--accent-hover); }}
  .btn-primary.copied {{ background: var(--ok); }}
  .btn-ghost {{ background: var(--neutral-btn); color: var(--text-dim); }}
  .btn-ghost:hover {{ background: var(--neutral-btn-hover); color: var(--text); }}
  .prompt-body {{
    margin: 14px 0 0; padding: 14px; background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--radius-sm); font: 12.5px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    white-space: pre-wrap; word-break: break-word; max-height: 380px; overflow-y: auto; color: var(--text);
  }}
  .empty {{
    grid-column: 1 / -1; text-align: center; padding: 56px 20px; color: var(--text-dim);
    background: var(--surface); border: 1px dashed var(--border); border-radius: var(--radius);
  }}
  .empty-icon {{ font-size: 40px; margin-bottom: 8px; }}
  .empty-sub {{ font-size: 14px; margin-top: 4px; }}
  .empty code {{ background: var(--surface-2); padding: 1px 6px; border-radius: 5px; }}

  footer {{ margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 13px; }}
  footer a {{ color: var(--accent); text-decoration: none; }}
  footer a:hover {{ text-decoration: underline; }}
  .no-results {{ display: none; text-align: center; color: var(--text-dim); padding: 40px; }}
</style>
</head>
<body>
<nav class="topbar">
  <div class="topbar-inner">
    <span class="tb-brand">
      <svg viewBox="0 0 24 24" width="22" height="22" role="img" aria-label="Jira"><path d="M11.571 11.513H0a5.218 5.218 0 0 0 5.232 5.215h2.13v2.057A5.215 5.215 0 0 0 12.575 24V12.518a1.005 1.005 0 0 0-1.005-1.005zm5.723-5.756H5.736a5.215 5.215 0 0 0 5.215 5.214h2.129v2.058a5.218 5.218 0 0 0 5.215 5.214V6.758a1.001 1.001 0 0 0-1.001-1.001zM23.013 0H11.455a5.215 5.215 0 0 0 5.215 5.215h2.129v2.057A5.215 5.215 0 0 0 24 12.483V1.005A1.001 1.001 0 0 0 23.013 0Z"/></svg>
      <span class="brand-text">ROVO Prompts by Simone</span>
    </span>
    <div class="tb-search">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <input type="search" id="search" placeholder="Search prompts&hellip;" autocomplete="off">
    </div>
    <div class="tb-spacer"></div>
  </div>
</nav>
<div class="wrap">
  <header class="hero">
    <p class="lede">Ready-to-use Rovo Chat prompts to monitor and manage UX work on Jira. Pick a category, copy the prompt, paste it into Rovo. <b>{total}</b> available.</p>
  </header>

  <div class="tabbar">
    <nav class="tabs" role="tablist">
      {tabs}
    </nav>
    <div class="controls">
      <label class="sort-ctl" for="sort">Sort by</label>
      <select id="sort">
        <option value="title" selected>Title (A&ndash;Z)</option>
        <option value="added">Date added</option>
        <option value="modified">Date modified</option>
      </select>
    </div>
  </div>

  {panels}

  <p class="no-results" id="noResults">No prompts match your search.</p>

  <footer>
    <p>Every prompt ends with &ldquo;read-only&rdquo; where applicable: they're built for reporting and don't modify Jira (except <em>Create a UX Epic</em>, which only writes after your confirmation).</p>
    <p>Site generated by <code>build-site.py</code> &middot; prompt source in <code>ROVO Prompts/</code> &middot; status in <code>prompts-status.md</code>.</p>
  </footer>
</div>

<script>
  // Tabs
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.panel');
  tabs.forEach(tab => tab.addEventListener('click', () => {{
    tabs.forEach(t => {{ t.classList.remove('active'); t.setAttribute('aria-selected','false'); }});
    panels.forEach(p => p.classList.remove('active'));
    tab.classList.add('active'); tab.setAttribute('aria-selected','true');
    document.getElementById('panel-' + tab.dataset.tab).classList.add('active');
    runSearch();
  }}));

  // Copy
  document.addEventListener('click', e => {{
    const copyBtn = e.target.closest('[data-copy]');
    if (copyBtn) {{
      const text = document.getElementById(copyBtn.dataset.copy).textContent;
      navigator.clipboard.writeText(text).then(() => {{
        const orig = copyBtn.textContent;
        copyBtn.textContent = 'Copied \\u2713';
        copyBtn.classList.add('copied');
        setTimeout(() => {{ copyBtn.textContent = orig; copyBtn.classList.remove('copied'); }}, 1600);
      }});
    }}
  }});

  // Search (filters within the active panel)
  const search = document.getElementById('search');
  const noResults = document.getElementById('noResults');
  function runSearch() {{
    const q = search.value.trim().toLowerCase();
    const activePanel = document.querySelector('.panel.active');
    let visible = 0;
    activePanel.querySelectorAll('.card').forEach(card => {{
      const match = !q || card.dataset.search.includes(q);
      card.style.display = match ? '' : 'none';
      if (match) visible++;
    }});
    const hasCards = activePanel.querySelectorAll('.card').length > 0;
    noResults.style.display = (q && hasCards && visible === 0) ? 'block' : 'none';
  }}
  search.addEventListener('input', runSearch);

  // Sort by (reorders cards within every category grid)
  const sortSel = document.getElementById('sort');
  function applySort() {{
    const mode = sortSel.value;
    document.querySelectorAll('.grid').forEach(grid => {{
      const cards = Array.from(grid.querySelectorAll('.card'));
      cards.sort((a, b) => {{
        if (mode === 'title') return a.dataset.title.localeCompare(b.dataset.title);
        // dates: newest first, ties broken alphabetically by title
        const da = a.dataset[mode === 'added' ? 'added' : 'modified'];
        const db = b.dataset[mode === 'added' ? 'added' : 'modified'];
        if (da !== db) return db.localeCompare(da);
        return a.dataset.title.localeCompare(b.dataset.title);
      }});
      cards.forEach(c => grid.appendChild(c));
    }});
  }}
  sortSel.addEventListener('change', applySort);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
