# DH-Oz Corpus Analysis Masterclass

Last verified: 2026-05-21

Local working directory for the `DH-Oz/CorpusAnalysis` evergreen repo — a living document for the Digital Humanities Winter School corpus-analysis stream. The 2026 edition is a presentation pivot of the 2025 course from R/Rmd to Python/Jupyter; content is stable, delivery is new.

## Project context

- **Course shape**: 4 days × 2 sessions × 2 hours = 16 contact hours, 8 sessions total.
- **Instructors**: Mark Alfano (lecture; first author) and Brian Ballsun-Stanton (code-along; second author). Both have local checkouts of this repo. CLAUDE.md addresses "the instructor" — assume either could be driving Claude.
- **Two-instructor pedagogy**: Mark lectures and runs light demos; Brian leads code-alongs and interjects over Mark's beats. Antagonistic banter between the two is a deliberate teaching device. See note `.notes/feedback_interjection-pedagogy.md`.
- **History**: Mark Alfano and Brian Ballsun-Stanton have delivered this for three prior years (most recently as the 2025 R/Rmd masterclass). 2025 source material lives in `2025-WinterSchool/` and in `Corpus Analysis Masterclass 2025.pdf` / `.pptx`.
- **Pivot scope**: translation, not redesign. The 2025 content carries forward; the work is R → Python, Rmd → Jupyter, plus just-in-time Python basics scaffolding.

## Audience

- Mixed: roughly 50% own laptops with userland install rights, 50% restricted institutional machines.
- **Pre-course install** is expected: Miniconda + Jupyter. Day 1 AM is verify-installs, not install-from-scratch.
- **Colab is the documented backstop** for fully-locked-down machines. Every notebook MUST open and run in Colab using only pip-installable deps.
- Assume **no prior Python** unless and until that assumption is explicitly revised.

## Tech stack

- **Python**: 3.14, pinned in `pyproject.toml`. The `dependencies` list in `pyproject.toml` is the **single source** for runtime deps, and it is taught to students as lesson content rather than being only project metadata. Everything downstream is generated from it, and a pre-commit hook keeps it that way:
  - `requirements.txt` is **generated** by `tools/sync_requirements.py`, never hand-edited. It carries the direct dependencies only, because students read it; `uv export` was rejected here since it emits every transitive package with hashes, which is right for reproducing an environment and wrong for teaching material.
  - `environment.yml` installs via `pip: -r requirements.txt`, so the conda path inherits the same list without a second copy to maintain.
  - The dev/instructor side uses **uv**, which reads `pyproject.toml` directly, so `uv run` works with no extra step. Neither instructor runs conda locally; the conda path is what we build *for*, and testing it means a container.
  - Students start **one launcher**, but not the same way on every platform. Windows double-clicks `start-jupyter.bat`. macOS and Linux `cd` to the folder and run `sh start-jupyter.sh`. It finds conda, offers to install Miniforge into `~/miniforge3` if there is none (opt-in, no admin, no shell-profile changes), builds the environment on first run, then starts JupyterLab. There is deliberately **no `conda activate` step**: `conda run --no-capture-output -n corpusanalysis jupyter lab` does the same job and works even where `conda init` has never run, which was the failure that bit an instructor during preparation. Activation was the hard part, not installation.
  - **macOS does not double-click, and the file is `.sh` for that reason** (changed 2026-08-07). Gatekeeper refuses a downloaded unsigned launcher with a dialog offering only Delete and Close, and Sequoia removed the Control-click bypass; what replaced it wants an administrator password and lapses after an hour, which is the wrong shape for the half of the cohort on managed machines. Running the script through `sh` never consults Gatekeeper, because the file is read rather than launched. The old `.command` extension existed only to make Finder double-click work, so it was renamed once that route was abandoned: keeping it would have invited the double-click that fails, and a student who clicks Delete loses the launcher.
  - **`student-path` cannot see Gatekeeper**, so do not read a green run as proof the student path works. It runs the launcher from a git checkout through a shell, and quarantine is set by a browser download and checked on a Finder double-click. The workflow verifies the launcher's logic on Apple Silicon, Intel macOS, Windows and a bare Debian container. It has never verified that a downloaded copy opens, which is how the `.command` path reached a test student broken.
  - To add a dependency: edit `pyproject.toml` and nothing else, then `uv run python tools/sync_requirements.py`. The pre-commit hook does it for you if you forget.
- **Notebooks**: Jupyter `.ipynb` files. The `day-N/` ones still carry Slideshow metadata from when they were rendered as decks; it is inert now and can be ignored.
- **Slides**: built by hand in **Google Slides** (decided 2026-07-29). Notebooks are not rendered to slides. See *Slides are not built from notebooks* below for what was removed and what the deck is built from.
- **Site**: GitHub Pages hosts a landing page and the student download link.
- **Distribution**: students download a **release zip** from GitHub Releases via a link on the Pages site. No git operations for students. See note `.notes/feedback_no-git-for-students.md`.
- **Library stack for corpus analysis** (locked 2026-05-21 via Day 1 AM port):
  - `nltk` — tokenisation + stopwords + `nltk.download("state_union" | "punkt" | "stopwords" | …)` data
  - `scikit-learn` — `CountVectorizer` for document-feature matrices; `LatentDirichletAllocation` for topic modelling
  - `scipy` — `scipy.cluster.hierarchy` (dendrograms), `scipy.spatial.distance` (Euclidean / cosine / Manhattan / …)
  - `numpy`, `pandas` 3.x. The old `pandas<3` cap came from `sotu`, our own package, so it was a decision of ours rather than an external constraint. `sotu` 0.1.1 (2026-07-28) lifted it to `pandas>=2.0`, and the course moved to pandas 3.0.5 the same day. Verified before the move: all five notebooks execute with zero errors, and seven figures spanning every kind the course draws were inspected by eye, because a byte-diff of a PNG says nothing useful. String columns now carry the dedicated `str` dtype in place of `object`.
  - `matplotlib` — plots + ColorBrewer-named colormaps via `matplotlib.colormaps[name]`
  - `seaborn` — the statistical layer over matplotlib; `scatterplot(hue=...)` colours by a column and builds the legend, which is most of what the course asks a plot to do
  - `scikit-misc` — `skmisc.loess`, the only loess in Python carrying standard errors, so `corpus_tools.loess_band` can draw a confidence band. `statsmodels`' lowess cannot.
  - `plotly` — the interactive twin of the static scatter in notebook 1a. The wheel installs a JupyterLab **mime renderer** into `<prefix>/share/jupyter/labextensions/`, so hover and legend filtering work offline with no second install step, and plotly detects Colab through `COLAB_NOTEBOOK_ID` on its own. Output is stored as `application/vnd.plotly.v1+json` (~18 KB per figure), not as an inlined copy of plotly.js.
  - `wordcloud` — word-cloud rendering
  - `networkx` — collocation networks (Day 2 PM)
  - **No spaCy.** It was in the 2026-05-21 lock and was dropped: the course teaches tokenising, stopword filtering and stemming as separate visible steps, which is what NLTK gives, whereas spaCy's `nlp(text)` does several at once and has no stemmer at all. Adding it would also mean per-language statistical models to download and verify on Day 1, for capability the lessons never use.
  - `sotu` — State of the Union corpus 1790–2026 (UCSB American Presidency Project; Peters & Woolley); the canonical demo dataset for Day 1 AM and Day 2 PM. Installed via PyPI; data ships bundled.
  - **Dev only**: `python-pptx` (image extraction from the 2025 deck), `pre-commit`, `pytest`.

## Pedagogy rules (hard)

These live in project-local notes under `.notes/` at the repo root. Read `.notes/README.md` and every linked file before authoring lesson content. (Migrated 2026-05-27 from the deprecated `~/.claude/projects/.../memory/` scheme.)

- **`no-unearned-python-idioms`** — every Python construct shown to learners must already have been explicitly taught. No comprehensions / f-string format specs / `with` blocks / type hints / etc. for elegance. Verbose-and-explicit beats clever. Enforced by `tools/check_taught_idioms.py`; the note carries what counts as a gloss.
- **`interjection-pedagogy`** — leave structural room in lessons for a second voice and Brian's live interjections over Mark's conceptual beats. Don't pack every minute; don't write as if one voice owns the lesson.
- **`no-git-for-students`** — no `git clone`, `git pull`, fork or branch references anywhere in student-facing material. Distribution is the release zip.
- **`liwc-dictionary-handling`** — the test is who wrote the dictionary. Dictionaries Brian and Mark built (`nietzsche.dic`, `macdvirtue.dic`, `nuke.dic`, and any they write later) are theirs to give away, so they ship in the repo as loose unencrypted files under CC-BY-NC 4.0, and people using them is the whole point. A third-party licensed dictionary is not ours to redistribute, so a loose `liwcdict.dic` never sits unencrypted in the repo, in any language, and `.gitignore` keeps it out. Distribution is set out in `.notes/feedback_liwc-dictionary-handling.md`.
- **`non-code-content-is-1-to-1`** — non-code slides (introductions, agenda, epigraphs, paper showcases, image-only slides) match the 2025 source 1:1. Only code-bearing content (R → Python translation, library-stack rewrites) is redesigned. No added headings, captions, or "framing prose" on slides whose 2025 originals were image-only.
- **`voice-when-authoring-new-prose`** — Mark's 2025 voice is preserved verbatim. His em-dashes stay. His discursive asides stay. His semantic colour cues, fragment-builds, lowercase casual titles all stay. The voice rules apply only when Claude is generating new prose for code-bridge cells. That should be rare. The diseased patterns are sentence structures, not characters. The parenthetical-aside cram. Triplets. Telling-about. Meta-conclusion. Staccato fragments. Unintroduced acronyms. Mechanical punctuation swaps do not fix a structure. Swapping `—` for `;` or `:` or parens leaves the cram intact. Real fixes split into two sentences. Or drop the aside. Or restructure so the second clause is the main clause. Calibrated against the INTS1301 *Bullet Voice* section at `/home/brian/people/Brian/INTS1301/CLAUDE.md`. Full rules and worked examples in `.notes/feedback_voice-when-authoring-new-prose.md`.
- **`class-based-layout-patterns`** — **retired 2026-07-29** along with `tools/slides.css`, which the classes lived in. It governed layout inside rendered decks, and nothing is rendered now. The note stays in `.notes/` as history.

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
├── pyproject.toml                           # SINGLE SOURCE for deps, Python 3.14, taught to students; uv reads it directly
├── uv.lock                                  # LOCAL ONLY — gitignored. Students reproduce from requirements.txt, so the lock is an instructor-side convenience uv regenerates on demand.
├── environment.yml                          # conda-side env spec; pins python=3.14 and pip-installs `-r requirements.txt`
└── requirements.txt                         # GENERATED from pyproject.toml by tools/sync_requirements.py; never hand-edited
```

There is intentionally **no `2026/` directory**. The repo is evergreen: `main` always carries the current edition's content, and each year is preserved as a **release tag** (`v2026.x`, `v2027.x`, …) with a release-zip asset. Future years evolve `main`; previous years live on as their release tags. The `2025-WinterSchool/` folder and the `.pdf`/`.pptx`/Carpentries HTML stay on local disk as source material. They DO NOT ship in the public `CorpusAnalysis` repo. A separate repo `DH-Oz/2025-corpus-analysis` archives the 2025 R/Rmd materials publicly (with `liwcdict.dic` stripped before push).

The `2025-slides/` folder is the one exception: it carries per-session PDF subsets of the 2025 deck (split by section-divider slides), is committed to this repo as a translation hand-off map for both instructors, and has a `MANIFEST.md` mapping each PDF to its 2026 notebook target. It is **not** student-facing — exclude it from the release zip alongside the other source materials.

## Distribution model

- **Public site**: GitHub Pages at `DH-Oz.github.io/CorpusAnalysis` (or similar — confirm with the instructor when the repo is created). Hosts the landing page and the student download link.
- **Student download**: release zip on GitHub Releases, linked from the landing page. Self-contained: notebooks, corpus, dictionaries, and a short README.
- **Year tracking**: years are carried by **release tags** (`v2026.x`, `v2027.x`, …), not by year-prefixed directories. `main` always holds the current edition's content; previous editions live on as their release tags and zip assets. Within-year versioning scheme is still open (see Open / deferred decisions).
- **Slides**: built by hand in Google Slides. There is no slide build path in this repo any more.

## Licences

- **Lesson content** (notebooks, slides, prose, dictionaries we own): **CC-BY-NC 4.0**.
- **Code** (any utility scripts, build tooling): **MIT**.
- The same split applies to the `DH-Oz/2025-corpus-analysis` archive repo.
- LIWC dictionaries are commercial and outside both licences — never redistribute.

## Commands

```bash
# Regenerate the lecture figures from the code-along notebooks. These land in
# figures/ (committed) and are what goes into the Google Slides deck.
uv run python tools/export_figures.py

# Extract images from the local .pptx (instructor-only; .pptx is gitignored).
uv run python tools/extract_pptx_images.py "Corpus Analysis Masterclass 2025.pptx" day-N/img --slides N N N

# Regenerate the matplotlib palette-families reference image used in §4 of D1-AM.
# Only needed if matplotlib's named-colormap set changes; output is committed.
uv run python tools/render_palettes_reference.py

# Run a notebook headless to verify it executes cleanly
uv run jupyter nbconvert --to notebook --execute day-1/D1-PM-wordcloud-hclust.ipynb --output /tmp/check.ipynb

# Re-run the code-along notebooks and write the outputs back into them, which is
# what the committed copies carry. Drop --all to run only what changed.
uv run python tools/preflight.py --inplace --all

# Assert the committed notebooks are each one clean top-to-bottom run.
uv run python tools/check_outputs.py

# Assert every Python construct is explained before a learner meets it.
uv run python tools/check_taught_idioms.py

# Build the student release zip locally. CI does this on a v* tag. See ADR 3.
uv run python tools/build_release.py --version v2026.1 --out dist
```

### Standing decisions live in `docs/decisions/`

Rationale and evidence belong in an ADR, not in this file. What matters here is what
to do; why it is that way is one link away.

- **[ADR 1](docs/decisions/0001-notebooks-ship-with-their-outputs.md) — notebooks
  carry their outputs.** The committed copies store one clean top-to-bottom run and
  ship that way, as answer keys; students type into a notebook they create
  themselves. **Re-running a notebook after editing it is part of editing it**,
  because `tools/notebook_cells.py` drops outputs when it replaces a cell. Notebook 2
  is executed with `dictionaries/liwcdict.dic` unpacked.
- **[ADR 2](docs/decisions/0002-3b-models-paragraphs-not-books.md) — 3b runs its
  topic model twice on purpose.** The book-level run is meant to fail. It reads as
  redundancy worth tidying; it is not. See
  `.notes/project_3b-book-topic-model-is-deliberate.md` before touching it.
- **[ADR 3](docs/decisions/0003-release-bundle-is-an-allowlist.md) — the release zip
  is an allowlist, verified after writing.** Tag `v2026.x` and
  `.github/workflows/release.yml` builds and attaches it. A new student-facing file
  must be added to the allowlist in `tools/build_release.py` or it will not ship.

### Slides are not built from notebooks (decided 2026-07-29)

The 2026 deck is built by hand in **Google Slides**. The notebooks-to-reveal.js
route was retired: `render_slides.py`, `render_stale.py`, `slides.css`,
`qa-rubric.md`, the auto-render Stop hook and the `jupyterlab-rise` dependency
are all gone, along with the visual-QA and click-to-reveal workflows that only
existed to serve them.

What stays, because it is what the Google deck is built *from*:

- `day-1/` … `day-4/` notebooks and their `img/` folders, now **internal notes
  and source material for the retrofit**, not deliverables. They are not
  rendered, not QA'd against a slide, and not shipped to students.
- `figures/` (committed) — figures harvested from the code-along notebooks by
  `tools/export_figures.py`. Drop these into slides.
- `2025-slides/` and `docs/2026-slide-translation.md` — the 2025 deck split by
  session, and the per-slide translation map.

Because the day-N notebooks are no longer presented, their content can drift
from the code-along without breaking anything. Do not spend QA effort
reconciling them, and do not treat a stale line in one as a defect in the
course.

### Notebook-cell editing

Edit lesson notebooks via `tools/notebook_cells.py` (append / insert / replace / delete with slideshow-metadata support, nbformat-validated, IDs auto-assigned). `slide_type` accepts `slide`, `subslide`, `fragment`, `notes`, `skip`, or `None` (continuation — cell joins the current slide with no slideshow metadata; how §4 image-then-code beats wire up). Smoke tests at `tools/test_notebook_cells.py`. Never hand-surger `.ipynb` JSON or use ad-hoc inline scripts:

```python
from tools.notebook_cells import append_cells, replace_cell

append_cells("day-1/D1-AM-intro.ipynb", [
    ("slide",    "![alt](img/p16-i0.png)"),
    ("subslide", "![alt](img/p17-i0.png)"),
])
replace_cell("day-1/D1-AM-intro.ipynb", 18, ("slide",
    '<div class="side-by-side">\n\n'
    '![cover](img/p18-i0.png)\n'
    '![dendrogram](img/p18-i1.png)\n\n'
    '</div>'
))
```

## Boundaries

- **Safe to author/edit**: `day-N/` lesson folders, `CLAUDE.md`, `README.md`, `.gitignore`, `pyproject.toml`, `environment.yml`, licence files, CI workflows.
- **Never hand-edit**: `requirements.txt` (generated from `pyproject.toml` by `tools/sync_requirements.py`, enforced by pre-commit), the `day-N/corpus_tools.py` copies (generated by `tools/sync_corpus_tools.py`), and `uv.lock` (managed by uv).
- **Read-only / source material**: `2025-WinterSchool/`, `Corpus Analysis Masterclass 2025.{pdf,pptx}`, `2025-slides/` (the committed split — regenerate via `MANIFEST.md`, don't hand-edit), `carpentriesCollabLessonTraining.html`. These inform the translation but do not ship.
- **Never commit**: a third-party licensed dictionary as a loose unencrypted file, in any language. Our own dictionaries are meant to be committed loose, and are. See `.notes/feedback_liwc-dictionary-handling.md` before changing dictionary distribution.
- **Never propose to students**: `git clone`, branches, forks, or any other git operation.

## Related repos

- `DH-Oz/CorpusAnalysis` (this repo) — evergreen 2026+ Python/Jupyter masterclass.
- `DH-Oz/2025-corpus-analysis` — historical archive of the 2025 R/Rmd masterclass. Live at https://github.com/DH-Oz/2025-corpus-analysis. Release `v2025` carries a bundled `corpusmasterclass2025-archive.zip` (LIWC stripped).

## Open / deferred decisions

These are not blockers but should be locked as work progresses. When one is settled, write it up as an ADR in `docs/decisions/` and leave this file a pointer.

1. **Within-year release versioning scheme** — major version is the calendar year (`v2026.x`, `v2027.x`); minor/patch format is open (e.g. `v2026.0.1` semver-ish, or `v2026-w1` week-of-instruction).

**Settled 2026-07-29, from the session transcripts: Mark reviews the code-along notebooks first, and gets the slides only once he is happy with them.** "I want him to start with the codealong, and once he's happy with that, give him slides. That gives us time to work with them." He reviews both artefacts, not slides alone: "Mark will review both the slides and the new jupyter notebooks for code along. He will do both." He works from a running Jupyter rather than a static render, so that he can load his own LIWC dictionary and confirm the LIWC-dependent cells actually execute.
