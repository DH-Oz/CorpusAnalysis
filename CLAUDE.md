# DH-Oz Corpus Analysis Masterclass

Last verified: 2026-05-19

Local working directory for the `DH-Oz/CorpusAnalysis` evergreen repo — a living document for the Digital Humanities Winter School corpus-analysis stream. The 2026 edition is a presentation pivot of the 2025 course from R/Rmd to Python/Jupyter; content is stable, delivery is new.

## Project context

- **Course shape**: 4 days × 2 sessions × 2 hours = 16 contact hours, 8 sessions total.
- **Instructors**: Mark Alfano (lecture; first author) and Brian Ballsun-Stanton (code-along; second author). Both have local checkouts of this repo. CLAUDE.md addresses "the instructor" — assume either could be driving Claude.
- **Two-instructor pedagogy**: Mark lectures and runs light demos; Brian leads code-alongs and interjects over Mark's beats. Antagonistic banter between the two is a deliberate teaching device. See memory `interjection-pedagogy`.
- **History**: Mark Alfano and Brian Ballsun-Stanton have delivered this for three prior years (most recently as the 2025 R/Rmd masterclass). 2025 source material lives in `2025-WinterSchool/` and in `Corpus Analysis Masterclass 2025.pdf` / `.pptx`.
- **Pivot scope**: translation, not redesign. The 2025 content carries forward; the work is R → Python, Rmd → Jupyter, plus just-in-time Python basics scaffolding.

## Audience

- Mixed: roughly 50% own laptops with userland install rights, 50% restricted institutional machines.
- **Pre-course install** is expected: Miniconda + Jupyter. Day 1 AM is verify-installs, not install-from-scratch.
- **Colab is the documented backstop** for fully-locked-down machines. Every notebook MUST open and run in Colab using only pip-installable deps.
- Assume **no prior Python** unless and until that assumption is explicitly revised.

## Tech stack

- **Python**: 3.14, pinned in `pyproject.toml`. `pyproject.toml` is the canonical dependency list AND is taught to students as lesson content, not just project metadata. Student machines run Miniconda / Anaconda; the conda env is a thin wrapper that pip-installs from `pyproject.toml`. A pip-only `requirements.txt` ships alongside as the Colab / restricted-machine fallback.
- **Notebooks**: Jupyter `.ipynb` files. Each cell carries Slideshow metadata (Slide / Sub-Slide / Fragment / Skip / Notes).
- **Slides**: `jupyter nbconvert --to slides notebook.ipynb` → reveal.js HTML. RISE was attempted and parked — architecture must not preclude switching later, but ship with nbconvert for now.
- **Site**: GitHub Pages hosts a landing page plus the rendered nbconvert slides.
- **Distribution**: students download a **release zip** from GitHub Releases via a link on the Pages site. No git operations for students. See memory `no-git-for-students`.
- **Library stack for corpus analysis**: not yet locked. The Day-1 rendering task is expected to propose a starting set (likely `wordcloud`, `scipy.cluster.hierarchy`, `matplotlib`, plus tokenization choice between stdlib and `nltk`). Lock decisions here as they land.

## Pedagogy rules (hard)

These live in memory under `~/.claude/projects/-home-brian-people-Mark-2026-WinterSchool/memory/`. Read MEMORY.md and every linked file before authoring lesson content.

- **`no-unearned-python-idioms`** — every Python construct shown to learners must already have been explicitly taught. No comprehensions / f-string format specs / `with` blocks / type hints / etc. for elegance. Verbose-and-explicit beats clever.
- **`interjection-pedagogy`** — leave structural room in lessons for a second voice and Brian's live interjections over Mark's conceptual beats. Don't pack every minute; don't write as if one voice owns the lesson.
- **`no-git-for-students`** — no `git clone`, `git pull`, fork or branch references anywhere in student-facing material. Distribution is the release zip.
- **`liwc-dictionary-handling`** — `liwcdict.dic` (and any LIWC dictionary in any language) NEVER enters the public repo or release zip. Custom open dictionaries (`nietzsche.dic`, `macdvirtue.dic`, `nuke.dic`, etc.) DO ship publicly.

Carpentries pedagogy (`carpentriesCollabLessonTraining.html`) is used as **reference only** — apply principles (explicit learner objectives, prerequisites, keypoints, frequent formative checks) without adopting The Workbench or Incubator infrastructure.

## Python basics integration

Just-in-time. No standalone Python primer session. Loops, conditionals, simple functions surface inside Brian's code-along beats at the exact moment a corpus task demands them. Day 1 AM's "R installation" becomes Python install verification with a brief syntactic orientation.

## Repo structure

Local working directory currently:

```
/home/brian/people/Mark/2026-WinterSchool/   # local checkout of DH-Oz/CorpusAnalysis
├── day-1/                                   # session notebooks (one folder per teaching day)
├── day-2/                                   # (to be created)
├── day-3/                                   # (to be created)
├── day-4/                                   # (to be created)
├── 2025-slides/                             # COMMITTED — per-session PDF splits of the 2025 deck; canonical hand-off map for translation. Not shipped in the student release zip.
├── 2025-WinterSchool/                       # LOCAL ONLY — gitignored; source material for translation
├── Corpus Analysis Masterclass 2025.pdf     # LOCAL ONLY — gitignored; whole-deck source for 2025-slides/
├── Corpus Analysis Masterclass 2025.pptx    # LOCAL ONLY — gitignored
├── carpentriesCollabLessonTraining.html     # LOCAL ONLY — pedagogy reference
├── CLAUDE.md                                # this file
├── README.md                                # public-facing course intro
├── pyproject.toml                           # canonical dep list, Python 3.14, taught to students
├── environment.yml                          # (to be created) thin conda wrapper; pip-installs from pyproject.toml
└── requirements.txt                         # (to be created) pip fallback for Colab / restricted machines
```

There is intentionally **no `2026/` directory**. The repo is evergreen: `main` always carries the current edition's content, and each year is preserved as a **release tag** (`v2026.x`, `v2027.x`, …) with a release-zip asset. Future years evolve `main`; previous years live on as their release tags. The `2025-WinterSchool/` folder and the `.pdf`/`.pptx`/Carpentries HTML stay on local disk as source material. They DO NOT ship in the public `CorpusAnalysis` repo. A separate repo `DH-Oz/2025-corpus-analysis` archives the 2025 R/Rmd materials publicly (with `liwcdict.dic` stripped before push).

The `2025-slides/` folder is the one exception: it carries per-session PDF subsets of the 2025 deck (split by section-divider slides), is committed to this repo as a translation hand-off map for both instructors, and has a `MANIFEST.md` mapping each PDF to its 2026 notebook target. It is **not** student-facing — exclude it from the release zip alongside the other source materials.

## Distribution model

- **Public site**: GitHub Pages at `DH-Oz.github.io/CorpusAnalysis` (or similar — confirm with the instructor when the repo is created). Hosts landing page + rendered nbconvert slides.
- **Student download**: release zip on GitHub Releases, linked from the landing page. Self-contained: notebooks, corpus, dictionaries, and a short README.
- **Year tracking**: years are carried by **release tags** (`v2026.x`, `v2027.x`, …), not by year-prefixed directories. `main` always holds the current edition's content; previous editions live on as their release tags and zip assets. Within-year versioning scheme is still open (see Open / deferred decisions).
- **Slides build path**: `jupyter nbconvert --to slides day-N/<notebook>.ipynb`. Long-term this should be a CI workflow (GitHub Actions) that builds slides on push and deploys to Pages.

## Licences

- **Lesson content** (notebooks, slides, prose, dictionaries we own): **CC-BY-NC 4.0**.
- **Code** (any utility scripts, build tooling): **MIT**.
- The same split applies to the `DH-Oz/2025-corpus-analysis` archive repo.
- LIWC dictionaries are commercial and outside both licences — never redistribute.

## Commands

```bash
# Render a notebook to reveal.js slides
jupyter nbconvert --to slides day-1/D1-PM-wordcloud-hclust.ipynb

# Run a notebook headless to verify it executes cleanly
jupyter nbconvert --to notebook --execute day-1/D1-PM-wordcloud-hclust.ipynb --output /tmp/check.ipynb

# Build a release zip (sketch — to be implemented as a CI workflow)
# Excludes 2025-WinterSchool/, 2025-slides/, slides PDFs, carpentriesCollabLessonTraining.html, LIWC dicts
```

## Boundaries

- **Safe to author/edit**: `day-N/` lesson folders, `CLAUDE.md`, `README.md`, `.gitignore`, `pyproject.toml`, `environment.yml`, `requirements.txt`, licence files, CI workflows.
- **Read-only / source material**: `2025-WinterSchool/`, `Corpus Analysis Masterclass 2025.{pdf,pptx}`, `2025-slides/` (the committed split — regenerate via `MANIFEST.md`, don't hand-edit), `carpentriesCollabLessonTraining.html`. These inform the translation but do not ship.
- **Never commit**: any LIWC dictionary, in any language.
- **Never propose to students**: `git clone`, branches, forks, or any other git operation.

## Related repos

- `DH-Oz/CorpusAnalysis` (this repo) — evergreen 2026+ Python/Jupyter masterclass.
- `DH-Oz/2025-corpus-analysis` — historical archive of the 2025 R/Rmd masterclass. Live at https://github.com/DH-Oz/2025-corpus-analysis. Release `v2025` carries a bundled `corpusmasterclass2025-archive.zip` (LIWC stripped).

## Open / deferred decisions

These are not blockers but should be locked as work progresses; update this CLAUDE.md when each is settled.

1. **Python library stack** for corpus analysis (word cloud, hierarchical clustering, DFM, collocations, dictionary lookups, German tokenization). The Day-1 rendering task will propose a starting set; lock and document here.
2. **Within-year release versioning scheme** — major version is the calendar year (`v2026.x`, `v2027.x`); minor/patch format is open (e.g. `v2026.0.1` semver-ish, or `v2026-w1` week-of-instruction).
3. **Mark ↔ Brian review cadence** for translated notebooks before slides deploy.
4. **CI workflow** for slide builds and release-zip generation.
