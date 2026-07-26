# Deploy to GitHub Pages

The site is a single self-contained static file: [`site/index.html`](site/index.html).
No dependencies, no server-side build step — GitHub Pages serves it as-is.

## When we're ready to publish

We need from you: the **repo name** and **GitHub account/org**. Then one of two paths.

### Option A — dedicated repo, Pages from the `/docs` folder (recommended)
GitHub Pages can serve directly from a `docs/` folder on the main branch.

```bash
# from the "ROVO Agent" folder
cp -r site docs           # Pages wants a "docs" folder
git init
git add docs prompts-status.md build-site.py "ROVO Prompts"
git commit -m "ROVO Prompts: public site + prompt library"
git branch -M main
git remote add origin https://github.com/<ACCOUNT>/<REPO>.git
git push -u origin main
```
Then on GitHub: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / `/docs`**.
Final URL: `https://<ACCOUNT>.github.io/<REPO>/`

### Option B — site only in a repo, Pages from root
If you want a repo containing only the site:

```bash
cd site
git init
git add index.html
git commit -m "ROVO Prompts site"
git branch -M main
git remote add origin https://github.com/<ACCOUNT>/<REPO>.git
git push -u origin main
```
Then **Settings → Pages → Branch: `main` / `/ (root)`**.

## Updating the site after publishing
1. Edit/add prompts in `ROVO Prompts/` and update the `MANIFEST` in `build-site.py`
2. `python3 build-site.py`
3. With Option A: `cp -r site/. docs/` then commit & push. With Option B: commit & push from `site/`.

Each card carries an **Updated** date. It's derived automatically from git — no
manual field to maintain. A committed prompt shows its last commit date; a prompt
with uncommitted edits shows today, so the date is always current at build time.

## Notes
- The "Copy prompt" button uses `navigator.clipboard`, which requires **HTTPS** — GitHub Pages is already HTTPS, so it works. Locally over `file://` copy may fail in some browsers: to test locally run `python3 -m http.server` inside `site/`.
- The site is public: anyone with the URL sees the prompts. The manager prompts contain the **rosters with designer names and account IDs** (needed because Rovo can't read files). If that's a privacy concern, options: a private repo with Pages on a plan that supports it, or removing the account IDs from the manager prompts before publishing.
