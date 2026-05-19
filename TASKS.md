# Tasks

State of work for the 2026 DH Winter School pivot (R/Rmd → Python/Jupyter). Living document — edit freely. See `CLAUDE.md` for project context, conventions, and decisions.

Last updated: 2026-05-19

**Status convention**: `[ ]` to do · `[~]` in progress · `[x]` done · `[!]` blocked · `[?]` deferred / pending decision.

---

## 1. Repo and infrastructure

- [x] **Create `DH-Oz/CorpusAnalysis` repo** on GitHub — live at https://github.com/DH-Oz/CorpusAnalysis. Repo scaffolded (licences, README, CLAUDE.md, TASKS.md, pyproject, .gitignore) on `main`. GitHub Pages not yet configured. No release tags yet.
- [x] **Create `DH-Oz/2025-corpus-analysis` repo** on GitHub for the historical R/Rmd archive — live at https://github.com/DH-Oz/2025-corpus-analysis. Initial scaffold + 2025 R/Rmd content + custom dictionaries committed across three commits on `main`. LIWC stripped from both the repo and the bundled release zip. Release `v2025` published with `corpusmasterclass2025-archive.zip` (17.6MB) as an asset.
- [x] **Write `.gitignore`** for `CorpusAnalysis` — committed and verified via `git check-ignore`. Catches `2025-WinterSchool/`, both 2025 slide files, `carpentriesCollabLessonTraining.html`, the LIWC dictionary patterns, `.venv/`, `__pycache__/`, `*.ipynb_checkpoints/`, and build outputs (`_site/`, `_build/`, `slides/*.slides.html`, `slides/reveal.js/`). Also gitignores the leftover uv-era `uv.lock` and `main.py` since the project pivoted to conda.
- [x] **Write `README.md`** for the public-facing repo — committed at `README.md`. Covers course blurb, eight-session outline, "no prior Python" assumption, release-zip download flow (links the Pages site even though it isn't deployed yet), Miniconda local-install path, Colab backstop, licence split, both instructor contacts, and a pointer to the 2025 archive repo. References `environment.yml` / `requirements.txt` inside the release zip — those files don't exist yet (depend on the env decision below).
- [~] **Environment files** — shape locked, contents waiting on Day-1 library set. Decision: `pyproject.toml` at repo root is the **canonical** dependency list (Python 3.14 pinned, and taught to students as lesson material); `environment.yml` is a thin conda wrapper that creates the env and `pip install -e .`s from `pyproject.toml`; `requirements.txt` is the pip fallback for Colab / restricted machines. All three live at repo root. Files themselves still need to be written once Day-1 names its libraries.

## 2. Slides — split 2025 source

- [ ] **Split `Corpus Analysis Masterclass 2025.pdf` (or .pptx) into 8 session sections** matching the 2025 agenda. Output a folder with one slide subset per session so each future render task has its canonical hand-off map to work against.

## 3. Content — per-session translation (R/Rmd → Python/Jupyter)

Each Day-N task produces Jupyter notebooks under `day-N/` (at repo root — no `2026/` prefix; year identity comes from the release tag), slideshow metadata on every cell, runnable in both local conda and Colab, obeying memory rules.

- [ ] **Day 1 AM (Mark)** — introductions, examples of what's to come, **Python install verification** (was R install). Prior quick-and-dirty markdown-only draft was removed; restart from scratch. Beats to cover: title + epigraphs, agenda, instructor intros, sticky-note protocol, files-link cell, "examples of what's to come" demo, Python install verification.
- [ ] **Day 1 PM (Brian, code-along)** — first word cloud + hierarchical clustering on Nietzsche corpus. Same prompt as D1 AM.
- [ ] **Day 2 AM (Brian)** — demos of various corpus analyses we've done. Translation from existing material.
- [ ] **Day 2 PM (Mark)** — (re)intro to a Python quanteda-equivalent stack; matrices and their multiplication; collocation networks. Library stack TBD; expect non-trivial design work — sklearn vectorizers + scipy.sparse + nltk collocations is a likely path.
- [ ] **Day 3 AM (Mark)** — more quanteda-equivalent + LIWC-style content analysis in German. LIWC handling per memory `liwc-dictionary-handling` — public path uses open dictionaries only; LIWC integration is optional and gated on a locally-present file.
- [ ] **Day 3 PM (Brian, code-along)** — building your own custom dictionary.
- [ ] **Day 4 AM (Brian/Mark, split class)** — finding and constructing corpora with AI · downloading existing corpora.
- [ ] **Day 4 PM (Brian/Mark)** — brainstorming, planning collaborations, goodbyes.

## 4. Slide rendering and site

- [ ] **Verify nbconvert workflow** end-to-end on the first Day-1 notebook. Render slides, open in browser, confirm cell layout reads sensibly.
- [ ] **Build the GitHub Pages landing page**. Static HTML/markdown. Links: latest release zip, rendered slides for each session (once built), brief course blurb.
- [ ] **GitHub Actions: build slides on push to `main`** with `jupyter nbconvert --to slides`, deploy to `gh-pages` (or Pages-from-main path).
- [ ] **GitHub Actions: release-zip generation** triggered on git tag (`v2026.*`, `v2027.*`, …). Bundle `day-*/**/*.ipynb`, corpora, dictionaries (open only — never LIWC), `pyproject.toml`, `environment.yml`, `requirements.txt`, and a short student-facing README. Attach as a Release asset.

## 5. Deferred decisions (mirror of `CLAUDE.md` § Open / deferred decisions)

- [?] **Python library stack** — locked once the Day-1 render task proposes a starting set.
- [?] **Within-year release versioning scheme** — major version is the calendar year (`v2026.x`, `v2027.x`); minor/patch format is open (e.g. `v2026.0.1` semver-ish, or `v2026-w1` week-of-instruction).
- [?] **Mark ↔ Brian review cadence** — does each translated session need explicit sign-off before slides deploy?
- [?] **Live-slide future**: RISE was tried and parked; revisit if/when Brian gets it working. Architecture should not preclude switching.
- [?] **Audience prior Python knowledge** — current assumption is "none". Revise if cohort intake changes.

## 6. Notes for future chats

- Read `CLAUDE.md` and the project memory (`~/.claude/projects/-home-brian-people-Mark-2026-WinterSchool/memory/`) before doing any content work.
- The 2025 slides PDF/PPTX is the canonical hand-off map between Mark's and Brian's portions of each session — consult it when translating.
- For each per-session translation, the working shape is: read memory → read the relevant section of the 2025 source → halt for user approval on libraries and layout → implement → verify nbconvert → commit. (The first Day-1 AM attempt was scrapped and is being restarted; treat the shape above as the workflow, not any specific prior notebook as the template.)
- Halt on uncertainty rather than guess. Especially on LIWC handling, licence questions, anything touching the release zip.
