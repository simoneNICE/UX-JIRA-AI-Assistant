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
        "blurb": "Builds a UX Epic under a Capability in CXUX autonomously — you only choose which tasks to add at the end.",
        "inputs": "Capability key or name (e.g. CXUX-12754)",
        "metrics": "None — autonomous creation, not measurement",
        "tags": ["writes", "autonomous"],
    },
    {
        "file": "ux-my-health-prompt.md",
        "category": "designers",
        "title": "My health check",
        "blurb": "How your own workload looks right now, across all projects. Flags idle, overload, and stalled tasks or epics.",
        "metrics": "In-progress band (0 / 1 / 2–4 / 5+) · stalled task >14d · stalled epic >45d · epic out-of-sync",
        "tags": ["self-service", "read-only"],
    },
    {
        "file": "ux-my-report-prompt.md",
        "category": "designers",
        "title": "My annual report",
        "blurb": "Your closed work for a year, by Task Type and Story Points, with average SP per task.",
        "inputs": "Year (e.g. 2025)",
        "metrics": "Task count · Story Points · avg SP/task (excl. Build Review) · by Task Type",
        "tags": ["self-service", "read-only"],
    },
    # --- Researchers ---
    # (no research-specific prompt ready yet — see prompts-status.md)
    # --- Managers ---
    {
        "file": "ux-overview-prompt.md",
        "category": "managers",
        "title": "Team sprint overview",
        "blurb": "How much work each designer has this sprint — tasks by status and Story Points. CXUX only. Asks first: team, region, or one person.",
        "inputs": "Scope: whole team, a region, or one designer (the prompt asks)",
        "metrics": "Task count by status (New / In Progress / Done) · Story Points",
        "tags": ["team", "read-only"],
    },
    {
        "file": "ux-designer-health-prompt.md",
        "category": "managers",
        "title": "Designer health check",
        "blurb": "Whether anyone's overloaded, idle, or stalled — across all projects, with a sprint-phase lens. Asks first: team, region, or one person.",
        "inputs": "Scope: whole team, a region, or one designer (the prompt asks)",
        "metrics": "In-progress band (0 / 1 / 2–4 / 5+) · stalled task >14d · stalled epic >45d · epic out-of-sync",
        "tags": ["team", "read-only"],
    },
    {
        "file": "ux-research-health-prompt.md",
        "category": "managers",
        "title": "Researcher health check",
        "blurb": "Whether any researcher's overloaded, idle, or stalled — on the UX Research portfolio under CXUX-12163.",
        "metrics": "In-progress band (0 / 1 / 2–4 / 5+) · stalled task >14d · stalled epic >45d · on research tasks",
        "tags": ["team", "research", "read-only"],
    },
    {
        "file": "ux-capability-review-prompt.md",
        "category": "managers",
        "title": "Research capability review (DRAFT)",
        "blurb": "DRAFT, not validated. Reviews every research Epic in the current semester Capability: status counts, how long each is in progress, stalls, out-of-sync tasks, researches per app, thematic categories, and possible duplicate researches.",
        "inputs": "Optional — a Capability key (defaults to the current semester Capability under CXUX-12163)",
        "metrics": "Epic counts New/In Progress/Done · days-in-progress per epic · stalled epic >45d / task >14d · out-of-sync · researches per app (Component) · thematic categories · overlap detection",
        "tags": ["draft", "team", "research", "portfolio", "read-only"],
    },
    {
        "file": "ux-annual-report-prompt.md",
        "category": "managers",
        "title": "Designer annual report",
        "blurb": "Work closed in a year, per designer and Task Type. Includes who closed nothing. Asks first: team, region, or one person.",
        "inputs": "Year · scope: team, region, or one designer (the prompt asks)",
        "metrics": "Task count · Story Points · avg SP/task (excl. Build Review) · by Task Type",
        "tags": ["team", "read-only"],
    },
    {
        "file": "ux-lob-summary-prompt.md",
        "category": "managers",
        "title": "Design readiness",
        "blurb": "A traffic light showing which capabilities are design-ready for this release and next, across all LOB projects. Per capability, not per person.",
        "inputs": "Optional — two release codes like 26.3 and 26.4 (auto-computed if omitted)",
        "metrics": "Design-ready (done/total tasks) · design-deadline flags · 🔴 / 🟠 / 🟢 traffic light",
        "tags": ["portfolio", "read-only"],
    },
    {
        "file": "ux-release-workload-prompt.md",
        "category": "managers",
        "title": "Release workload",
        "blurb": "Sizes one project's release: how many Capabilities, how many carry UX work, the Story Points behind it, who owns it, and the status of both.",
        "inputs": "Project key + fix version (e.g. CXREC, 26.4)",
        "metrics": "Capabilities in release · with a CXUX Epic · total Story Points · epic assignees · capability & epic status",
        "tags": ["portfolio", "read-only"],
    },
    # --- Leadership (VP) ---
    {
        "file": "ux-capacity-demand-prompt.md",
        "category": "leadership",
        "title": "Capacity vs demand (DRAFT)",
        "blurb": "DRAFT, not validated. Forward look: does the team's historical throughput cover the design work in the next releases? Demand and capacity both in Story Points on CXUX Epics.",
        "inputs": "Look-ahead releases (default 3) + baseline releases (default 4)",
        "metrics": "Demand SP per release · baseline capacity (avg SP/release closed) · load % & gap · unestimated epics · Israel/India split",
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


def spec_table(inputs: str, metrics: str) -> str:
    """Render Inputs / Output as a compact two-column spec table (label | values).
    Each value is a '·'-separated item shown as a chip. Rows with no text are skipped;
    an empty table returns ''. Labels are inserted as-is; items are escaped."""
    rows = []
    for label, text in (("Inputs", inputs), ("Output", metrics)):
        if not text:
            continue
        chips = "".join(
            f'<span class="spec-chip">{html.escape(item.strip())}</span>'
            for item in text.split("·")
            if item.strip()
        )
        rows.append(
            f'<div class="spec-row"><div class="spec-label">{label}</div>'
            f'<div class="spec-vals">{chips}</div></div>'
        )
    if not rows:
        return ""
    return f'<div class="spec-table">{"".join(rows)}</div>'


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
        spec_html = spec_table(p.get("inputs", ""), p.get("metrics", ""))
        # DRAFT_ALL: every prompt is flagged Draft until it's re-validated in Rovo after the
        # hardening pass. Set to False to go back to per-prompt "draft" tags only.
        draft_badge = '<span class="badge-draft">Draft</span>' if (DRAFT_ALL or "draft" in p.get("tags", [])) else ""
        updated_iso = p["updated"]
        added_iso = p["added"]
        search_text = " ".join(
            [p["title"], p["blurb"], p.get("inputs", ""), p.get("metrics", ""), updated_iso]
            + p.get("tags", [])
        )
        card = f"""
        <article class="card" data-search="{html.escape(search_text.lower())}" data-title="{html.escape(p['title'].lower())}" data-added="{added_iso}" data-modified="{updated_iso}">
          <div class="card-head">
            <h3>{html.escape(p['title'])}</h3>
            {draft_badge}
          </div>
          <p class="blurb">{html.escape(p['blurb'])}</p>
          {spec_html}
          <div class="card-actions">
            <button class="btn btn-primary" data-copy="{pid}">Copy prompt</button>
            <span class="updated" title="Last updated {updated_iso}">Updated {html.escape(human_date(updated_iso))}</span>
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

  .tabs {{
    display: flex; gap: 8px; margin: 18px 0 20px; flex-wrap: wrap;
    border-bottom: 1px solid var(--border);
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

  .controls {{ display: flex; align-items: center; gap: 8px; margin: 0 0 20px; }}
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

  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; }}
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
  .blurb {{ color: var(--text-dim); font-size: 14px; margin: 10px 0 14px; flex: 1; }}
  .spec-table {{ margin: 0 0 14px; border-top: 1px solid var(--border); }}
  .spec-row {{ display: grid; grid-template-columns: 68px 1fr; gap: 10px; align-items: start;
               padding: 9px 0; border-bottom: 1px solid var(--border); }}
  .spec-label {{ font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em;
                 color: var(--text-dim); padding-top: 3px; }}
  .spec-vals {{ display: flex; flex-wrap: wrap; gap: 5px; }}
  .spec-chip {{ font-size: 11.5px; line-height: 1.45; color: var(--text-subtlest);
                background: var(--surface-2); border: 1px solid var(--border);
                border-radius: 5px; padding: 2px 7px; }}
  .card-actions {{ display: flex; align-items: center; gap: 8px; margin-top: 16px; }}
  .updated {{ margin-left: auto; font-size: 11.5px; color: var(--text-subtlest); white-space: nowrap; }}
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
