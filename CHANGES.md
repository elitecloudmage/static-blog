# CHANGES.md — Blowfish Migration Ledger

Logging started 2026-08-06. All changes to this repo are recorded below.

---

## 2026-08-06 14:00 — Relocate Blowfish submodule to standard themes/blowfish path
- Files: `themes/blowfish/` (deleted regular-tracked files), `config/_default/themes/blowfish` (submodule removed), `.gitmodules` (edited), `.git/modules/config/_default/themes/blowfish/` (internals cleared)
- What: Removed Blowfish from two incorrect locations — as regular committed files at `themes/blowfish` and as a misplaced submodule at `config/_default/themes/blowfish`. Re-registered it as a proper git submodule at `themes/blowfish`. Also removed dangling `themes/risotto` entry from `.gitmodules` (directory never existed).
- Why: Hugo looks for a theme named "blowfish" at `themes/blowfish`. The previous state was split across two paths with neither being a clean canonical submodule. Blowfish is now a single, standard submodule at v2.105.0+5.
- Notes: `themes/hello-friend-ng` submodule still present — Phase 1 removal pending user approval in next step.

## 2026-08-06 14:05 — Phase 1: Remove hello-friend-ng submodule
- Files: `themes/hello-friend-ng/` (submodule removed), `.gitmodules` (hello-friend-ng entry removed), `.git/modules/themes/hello-friend-ng/` (internals cleared)
- What: Ran `git submodule deinit -f`, `git rm -f`, and `rm -rf .git/modules/` to fully de-register and clean up the old theme.
- Why: Site is migrating to Blowfish. hello-friend-ng was the old theme and is no longer needed.
- Notes: `themes/` now contains only `blowfish`. `.gitmodules` contains only the blowfish submodule entry.

## 2026-08-06 20:55 — Phase 3: fix misplaced config content, populate config/_default
- Files: `config/_default/hugo.toml`, `config/_default/languages.en.toml`, `config/_default/menus.en.toml`, `config/_default/params.toml`, `assets/css/custom.css` (created), `static/css/custom.css` (emptied)
- What: Found that a prior session's Phase 3 edit had landed in the wrong file — the Hugo TOML config (baseURL, theme, pagination, markup settings) had been written into `static/css/custom.css` instead of `config/_default/hugo.toml`, leaving all four Phase 3 config files empty (this was already committed in `f878400 "new theme"`). Moved that TOML content into `config/_default/hugo.toml`, and wrote `languages.en.toml`, `menus.en.toml`, and `params.toml` per the CLAUDE.md Phase 3 spec. Separately, `static/css/custom.css` had *originally* held real site CSS (Fira Code font-face + `.home-socials` styling used by `layouts/partials/home-socials.html`) before it got overwritten by the misplaced TOML — recovered that original CSS from git history (`799f8c5`) and placed it at `assets/css/custom.css`, since Blowfish's `head.html` loads custom CSS via `resources.Get "css/custom.css"`, which resolves against `assets/`, not `static/`. `static/css/custom.css` is now empty (nothing references it under Blowfish).
- Why: Without valid config, Hugo had no baseURL/theme/menu/author params wired up at all — the earlier build "succeeding" was misleading, since with all config files empty, Hugo wasn't really using Blowfish, just falling back to project-level layouts. This blocked Phase 2 (confirm Blowfish wired as active theme) and Phase 3 outright.
- Notes: Rebuilding now surfaces a *new*, unrelated blocker — see next entry. `static/css/custom.css` is now dead weight (empty, unreferenced) and a candidate for deletion pending your approval.

## 2026-08-06 21:10 — Bump CI Hugo version to match Blowfish's minimum
- Files: `.github/workflows/deploy.yml`
- What: Changed `hugo-version: '0.151.0'` to `'0.164.0'` in the "Setup Hugo" step.
- Why: Blowfish (current pin and even the last stable tag v2.105.0) requires Hugo >= 0.158.0. CI was pinned to 0.151.0, which would have broken the live build with a template error (`can't evaluate field Locale`). You upgraded local Hugo to 0.164.0 and explicitly asked me to bump this file to match.
- Notes: This is a workflow file change, done only because you explicitly asked (per CLAUDE.md Rule 4). Not committed/pushed — staged locally for your review.

## 2026-08-06 21:20 — Remove leftover hello-friend-ng layout overrides (approved deletion)
- Files deleted: `layouts/_default/single.html`, `layouts/index.html`, `layouts/partials/header.html`, `layouts/partials/home-socials.html`, `layouts/partials/svg/linkedin.html`, `layouts/partials/svg/github.html`, `layouts/partials/svg/email.html`
- What: Removed uncleaned hello-friend-ng-style project-level template overrides. `single.html` called `tags.html`/`categories.html` partials that don't exist in Blowfish (the build error you hit running `hugo server -D`). `index.html` was a custom homepage conflicting with the Blowfish `profile` homepage layout already set in `params.toml`. `header.html` was dead code (Blowfish's `baseof.html` looks for `header/basic.html`, a different name). `home-socials.html` and the `svg/*` partials were only used by the removed `index.html`.
- Why: Hugo always prefers project-level layouts over theme layouts, so these were silently blocking Blowfish's own templates from ever rendering. You approved this deletion explicitly.
- Notes: `layouts/partials/stats.html` (and its backing `data/content_stats.json` / `scripts/generate_stats.py`) was intentionally left alone — that's your separate "stats GUI" feature, not a hello-friend-ng leftover — but it's now orphaned since nothing calls it anymore. Flagged for you to decide on later. Build now succeeds and renders 25 pages via Blowfish's native templates (up from 14 with the broken overrides in place).

## 2026-08-06 21:25 — Fix deprecated languageCode config key
- Files: `config/_default/languages.en.toml`
- What: Changed `languageCode = "en-us"` to `locale = "en-us"`.
- Why: Hugo 0.164.0 build warned that `languageCode` was deprecated in v0.158.0 in favor of `locale`. Clears the warning.

## 2026-08-06 21:35 — Delete hugo.toml.bak, dead static/css/custom.css, empty config/_default/themes/ (approved deletion)
- Files deleted: `hugo.toml.bak`, `static/css/custom.css`, empty directory `config/_default/themes/`
- What: Removed the old pre-migration hugo.toml backup (superseded now that `config/_default/` is fully populated), the emptied/dead `static/css/custom.css` (nothing references it under Blowfish — see the 21:10 entry), and an empty leftover directory from the earlier submodule relocation.
- Why: You approved this deletion explicitly. Pure cleanup, no functional change.

## 2026-08-06 21:40 — Re-wire stats.html into Blowfish's article template
- Files: `layouts/_default/single.html` (new, project-level copy of Blowfish's own template), `layouts/partials/stats.html`
- What: Copied Blowfish's `themes/blowfish/layouts/_default/single.html` into the project at `layouts/_default/single.html` (the sanctioned Hugo pattern for deep-customizing one theme template without discarding the rest of it), then added a single `{{ partial "stats.html" . }}` call right after `{{ .Content }}` in the article body. Also fixed `stats.html` itself: `.Site.Data.content_stats` was deprecated in Hugo v0.156.0, changed to `hugo.Data.content_stats`.
- Why: You asked to keep the stats-GUI feature (site-wide post count / word count / posts-per-year, backed by `data/content_stats.json` via `scripts/generate_stats.py`) and re-wire it into Blowfish rather than deleting it, since it had gone orphaned after the hello-friend-ng `single.html` override was removed. Verified in build output that "Site Stats" now renders on article pages (e.g. `public/projects/self-healing-ec2/index.html`) styled correctly inside Blowfish's Tailwind layout.
- Notes: Because `layouts/_default/single.html` is now a full project-level copy of Blowfish's template (not a theme file), it will **not** automatically pick up future Blowfish theme updates to that template — if you update the Blowfish submodule later, this file may need to be manually re-diffed/re-synced. Currently the stats block shows on every single page (posts and projects alike) unconditionally; say the word if you'd rather scope it to posts only or gate it behind a param.

## 2026-08-06 21:50 — Phase 6 checklist: restore 4 broken project images
- Files: `static/images/status-nginx.png`, `static/images/cloud-init-status.png`, `static/images/sudo-tail.png`, `static/images/bash.png` (all restored)
- What: Found that `content/projects/auto-provisionEC2/index.md` (references `status-nginx.png`, `cloud-init-status.png`, `sudo-tail.png`) and `content/projects/automating-a-linux-setup-with-bash.md` (references `bash.png`) still pointed at `/images/...`, but those four PNGs had been deleted from `static/images/` in the `f878400 "new theme"` commit while the markdown references were left in place. Restored all four from the pre-deletion commit (`f878400^`) — byte sizes match the originals exactly.
- Why: Phase 4/6 requires project images to render correctly; these were silently 404ing. Recovered from git history rather than treated as a deletion (nothing was removed, this restores lost content).
- Notes: Verified in build output — all four now copy into `public/images/` and the pages reference them correctly.

## 2026-08-06 21:55 — Phase 6 verification checklist: PASSED
- `themes/` and `.gitmodules` reference only Blowfish (confirmed via `git submodule status` / `cat .gitmodules`)
- `hugo --gc --minify` builds clean: 0 errors, 0 warnings, 25 pages
- About (`/about/`) and Projects (`/projects/`) menu links present with correct hrefs
- Social links resolve: GitHub and LinkedIn hrefs present; email is JS-obfuscated via Blowfish's own mechanism (expected behavior, not a bug)
- Posts and project bundles render, including the 4 previously-broken images (fixed above)
- Dark default confirmed (`data-default-appearance=dark data-auto-appearance=false` on `<html>`); theme toggle present (`appearance-switcher` / `appearance-switcher-mobile` in output)
- You separately confirmed visually via `hugo server -D` that it "looks nice"
- Nothing committed or pushed — all changes staged locally for review.
