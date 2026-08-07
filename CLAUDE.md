
# CLAUDE.md — Build guide for the Blowfish migration

You are working in **/Users/burnt_jello/Workspace/Blog/static-blog**, the source for
a Hugo static blog (jadonsblog.com) deployed via GitHub Pages, with Cloudflare handling
DNS/HTTPS and a separate Terraform repo (`ghostoptimizer/iac-infra`) managing infra.
**Do not touch infra, DNS, or the deploy pipeline.** Your job is the site + theme only.

---

## PRIME DIRECTIVE

The repo currently has **two themes installed at once**: the new **Blowfish** theme and
the **old hello-friend-ng** theme. The old one was never removed cleanly. Your #1 job is
to **remove hello-friend-ng properly** (it is a git submodule, so it must be de-registered
correctly, not just `rm`'d) and finish migrating the site onto Blowfish so it builds and
looks right.

Truth over tidiness: if something is ambiguous or you're unsure whether a file is safe to
remove, **stop and ask** rather than guessing. Do not optimize for "looking done."

---

## RULES OF ENGAGEMENT (read before touching anything)

### 1. Deleting files — ALWAYS ASK FIRST
You may **not** delete any file or directory, run `git rm`, `rm`, `git submodule deinit`,
or any destructive command **until you have listed exactly what will be deleted and I have
explicitly approved it in this session.** Present deletions like this and wait for a "yes":

> **Proposed deletion — needs your approval:**
> - `themes/hello-friend-ng/` (git submodule, ~N files)
> - `.gitmodules` entry for hello-friend-ng
> Reason: old theme being replaced by Blowfish.
> Approve? (yes/no)

One approval covers only the items listed in that request. New deletions = new approval.

### 2. Editing / creating files — allowed, but MUST be logged
You may create and edit files **without asking**, on one condition: **every change is
recorded in `CHANGES.md`** (create it at repo root if it doesn't exist). Git diff alone is
NOT sufficient — I want a human-readable explanation of *what* and *why*, not just a diff.

Log format — append a new entry per change or logical group of changes:

```
## <YYYY-MM-DD HH:MM> — <short title>
- Files: <paths touched>
- What: <what you changed, plainly>
- Why: <the reason / what problem it solves>
- Notes: <anything I should double-check, or follow-ups>
```

Never rewrite or delete past `CHANGES.md` entries — it's an append-only ledger.
(Editing `CHANGES.md` itself does not need its own log entry.)

### 3. Never push or commit without me
Stage and describe changes, but **do not `git commit` or `git push`** unless I say so.
I want to review and push myself.

### 4. Don't touch secrets / infra
No changes to `.github/workflows/` deploy logic, `CNAME`, DNS, Cloudflare, Terraform, or
anything auth-related, unless I explicitly ask. If the build needs a workflow tweak
(e.g. submodule checkout), propose it and wait for approval.

---

## STARTING PROCEDURE (do this first, every session)

1. Read `CHANGES.md` (if it exists) to see prior work. If it doesn't exist, create it with
   a header and note that logging has started.
2. Get the lay of the land — run read-only commands and report back before editing:
   ```bash
   git status
   git submodule status
   cat .gitmodules
   ls themes/
   ls -R config 2>/dev/null || echo "no config/ folder yet"
   ls hugo.toml 2>/dev/null || echo "no top-level hugo.toml"
   hugo version
   ```
3. Summarize the current state to me: which themes are present, whether config has been
   moved to `config/_default/`, and what's left to do. Then proceed with the plan below.

---

## THE MIGRATION PLAN

### Phase 1 — Remove hello-friend-ng properly (needs delete approval)
It's a git submodule. The correct, clean removal is:
```bash
git submodule deinit -f themes/hello-friend-ng
git rm -f themes/hello-friend-ng
rm -rf .git/modules/themes/hello-friend-ng
```
Also remove the hello-friend-ng block from `.gitmodules` (edit, not delete the whole file —
Blowfish's submodule entry must stay). Verify afterward:
```bash
git submodule status      # should show ONLY blowfish
cat .gitmodules           # should reference ONLY blowfish
ls themes/                # should show ONLY blowfish
```
**Ask for deletion approval before running any of the above.**

### Phase 2 — Confirm Blowfish is wired as the active theme
- Ensure Blowfish is a proper submodule at `themes/blowfish` (`git submodule update --init --recursive` if needed).
- Config lives in `config/_default/` for Blowfish. If the site still uses a top-level
  `hugo.toml`, migrate it (see Phase 3). A top-level `hugo.toml` AND a `config/_default/`
  both existing causes ambiguous behavior — there should be one source of truth.

### Phase 3 — Port config to `config/_default/`
Create/verify these four files (settings ported from the old hello-friend-ng config):

- `config/_default/hugo.toml` — `baseURL = "https://jadonsblog.com/"`, `theme = "blowfish"`,
  `defaultContentLanguage = "en"`, `enableRobotsTXT = true`, pagination pagerSize 10,
  goldmark `unsafe = true`, highlight `noClasses = false`.
- `config/_default/languages.en.toml` — title "Jadon Lawson", `[params.author]` name
  "Jadon Lawson" with links: github `https://github.com/ghostoptimizer`,
  linkedin `https://linkedin.com/in/jadonlawson`, email `mailto:jslawson2025@gmail.com`.
- `config/_default/menus.en.toml` — main menu: About (pageRef "about", weight 1),
  Projects (pageRef "projects", weight 2).
- `config/_default/params.toml` — `colorScheme` (start "blowfish"),
  `defaultAppearance = "dark"`, `autoSwitchAppearance = false`, `enableThemeToggle = true`,
  `enableSearch = true`, `enableCodeCopy = true`, homepage `layout = "profile"` with recent
  posts shown, article show date/author/readingTime/TOC.

After creating `config/_default/`, the old top-level `hugo.toml` should be removed — but that
is a **deletion, so ask first**. (Rename to `hugo.toml.bak` as a safe intermediate step; a
rename is fine to do without delete-approval, just log it.)

### Phase 4 — Content & front matter polish
- `content/posts/*.md`, `content/projects/<name>/index.md` (leaf bundles with images), and
  `content/about/index.md` should carry over. Verify each builds.
- Check front matter uses standard keys (`title`, `date`, `draft`, `description`, `tags`,
  `categories`). Leave hello-friend-ng-specific keys in place if unsure — they're ignored,
  not errors. Only remove them if you're confident and log each removal.
- Confirm the projects section still renders images correctly under Blowfish.

### Phase 5 — CSS / look re-tune
- hello-friend-ng custom CSS lived in `static/css/custom.css`; its selectors won't match
  Blowfish (Tailwind-based). Start from Blowfish defaults. Put any custom overrides in
  `assets/css/custom.css`. Only re-add overrides that are actually needed — don't port the
  old file wholesale.
- Goal aesthetic: clean, typographic, dark default (like the old site but nicer). If you
  want to chase the vsyrakis.dev feel, the `profile` homepage layout with a centered avatar
  + social icons is the closest — but keep it tasteful and ask before big visual bets.

### Phase 6 — Verify (do this before telling me you're done)
```bash
hugo --gc --minify        # must build with no errors
hugo server -D            # spot-check locally at http://localhost:1313
```
Confirm: only Blowfish in `themes/` and `.gitmodules`; site builds; About + Projects menu
work; social links resolve; posts and project bundles render; dark default with working
toggle. Report a short checklist of what passed. Do **not** commit or push — hand it back
to me with a summary and the `CHANGES.md` entries for review.

---

## IF YOU GET STUCK
Stop and ask. A wrong deletion or a botched submodule removal is worse than a pause.
Surface the exact command you want to run and why, and wait for me.
