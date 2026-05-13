# Tasks

State of work for the 2026 DH Winter School pivot (R/Rmd → Python/Jupyter). Living document — edit freely. See `CLAUDE.md` for project context, conventions, and decisions.

Last updated: 2026-05-13

**Status convention**: `[ ]` to do · `[~]` in progress · `[x]` done · `[!]` blocked · `[?]` deferred / pending decision.

---

## 1. Repo and infrastructure

- [ ] **Create `DH-Oz/CorpusAnalysis` repo** on GitHub. Push initial scaffold: CLAUDE.md, TASKS.md, README.md, .gitignore, LICENSE-CONTENT (CC-BY-NC 4.0), LICENSE-CODE (MIT). Configure GitHub Pages to publish from `main` (path TBD).
- [x] **Create `DH-Oz/2025-corpus-analysis` repo** on GitHub for the historical R/Rmd archive — live at https://github.com/DH-Oz/2025-corpus-analysis. Initial scaffold + 2025 R/Rmd content + custom dictionaries committed across three commits on `main`. LIWC stripped from both the repo and the bundled release zip. Release `v2025` published with `corpusmasterclass2025-archive.zip` (17.6MB) as an asset.
- [ ] **Write `.gitignore`** for `CorpusAnalysis`. Must exclude: `2025-WinterSchool/`, `Corpus Analysis Masterclass 2025.pdf`, `Corpus Analysis Masterclass 2025.pptx`, `carpentriesCollabLessonTraining.html`, `liwcdict.dic` (and `LIWC*.dic`, `liwc*.dic`), `.venv/`, `__pycache__/`, `*.ipynb_checkpoints/`, build artefacts.
- [ ] **Write `README.md`** for the public-facing repo. Audience = students and curious browsers. Should link to the GitHub Pages site, the latest release zip, and a short "what is this course" blurb. No git instructions for students (see memory `no-git-for-students`).
- [ ] **Decide environment.yml vs requirements.txt** for the conda/pip story. Most likely both: `environment.yml` for conda users, `requirements.txt` for Colab/pip fallback. Lock once Day-1 library set is proposed.

## 2. Slides — split 2025 source

- [ ] **Split `Corpus Analysis Masterclass 2025.pdf` (or .pptx) into 8 session sections** matching the 2025 agenda. Output a folder with one slide subset per session so each future render task has its canonical hand-off map to work against.

## 3. Content — per-session translation (R/Rmd → Python/Jupyter)

Each Day-N task produces Jupyter notebooks under `2026/day-N/`, slideshow metadata on every cell, runnable in both local conda and Colab, obeying memory rules.

- [ ] **Day 1 AM (Mark)** — introductions, examples of what's to come, **Python install verification** (was R install). Prompt for this task drafted in the setup chat; paste into a fresh chat.
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
- [ ] **GitHub Actions: release-zip generation** triggered on git tag. Bundle `2026/**/*.ipynb`, corpora, dictionaries (open only — never LIWC), and a short student-facing README. Attach as a Release asset.

## 5. Deferred decisions (mirror of `CLAUDE.md` § Open / deferred decisions)

- [?] **Python library stack** — locked once the Day-1 render task proposes a starting set.
- [?] **Release versioning scheme** — `v2026.0.1` semver-ish, or `v2026-w1` date-based, or other.
- [?] **Mark ↔ Brian review cadence** — does each translated session need explicit sign-off before slides deploy?
- [?] **Live-slide future**: RISE was tried and parked; revisit if/when Brian gets it working. Architecture should not preclude switching.
- [?] **Audience prior Python knowledge** — current assumption is "none". Revise if cohort intake changes.

## 6. Notes for future chats

- Read `CLAUDE.md` and the project memory (`~/.claude/projects/-home-brian-people-Mark-2026-WinterSchool/memory/`) before doing any content work.
- The 2025 slides PDF/PPTX is the canonical hand-off map between Mark's and Brian's portions of each session — consult it when translating.
- The Day-1 render prompt is a model for subsequent days; reuse its shape (read memory → read 2025 source → halt for user approval on libraries and layout → implement → verify nbconvert → commit).
- Halt on uncertainty rather than guess. Especially on LIWC handling, licence questions, anything touching the release zip.
