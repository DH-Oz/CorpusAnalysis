# Rebuilding the lectures for 2026

The hand-off for turning the 2025 R/Rmd decks into the 2026 lectures. This is a
presentation pivot, not a redesign: the lessons keep the shape Mark and Brian
built over three deliveries; only the R becomes Python.

Three rules run through every page.

- **Non-code slides stay 1:1 with 2025.** Title cards, epigraphs, the agenda,
  paper showcases, photos, and memes carry over unchanged: same image, same
  words. Mark talks over them, so the slide stays the image.
- **Every analysis figure is live Python output.** Each one comes from
  `figures/`, regenerated from the corpus, so it runs 1790 to 2026 and includes
  Biden and Trump. The 2025 R PNGs stop around 1885 or pre-date Trump. None of
  them belong on a 2026 slide.
- **New prose is rare, and follows the voice rules.** Only the install steps,
  the tool names, and a few bridges are genuinely new. Keep them plain.

Lectures are rebuilt in Google Slides. Figures live in `figures/`: the
code-along notebooks make most of them (`tools/export_figures.py`), and
`slide-figures.ipynb` makes the three that no code-along notebook produces.
`dictionaries/liwcdict.dic` stays local and never ships.

Each session below lists its objectives, the slides that stay 1:1, then every
slide to change. New or edited slides carry the literal text; swapped images
carry a `figures/` path; text edits show before → after. Page numbers are within
each split PDF in `2025-slides/`.

---

## D1-AM — Mark — A first look at a corpus

*Objectives (≤3):* (1) say what counting words across a whole corpus shows that reading them one at a time cannot; (2) start Python and Jupyter and confirm the environment works; (3) load the State of the Union corpus and read its basic shape.

*Stays 1:1 (do not touch):* title, the McCarthy and Tempest epigraphs, the agenda layout, the introductions and sticky-note protocol, the PhilPapers and journal screenshots, Mark's three research figures (BLM networks, masculinity dendrogram, vaccine stacked-area), the "doing math" meme, the distance-metrics illustration, the feedback and closing slides.

### Slides to change

**Slide 5 — agenda (text).** "R installation" → "Python install". "quanteda" → "document-feature matrices".

**Slide 8 — "files available here" QR (logistics).** Still points at the 2025 zip. Repoint to the release link once the GitHub release exists.

**Slides 22–24 — the install sequence (new text).** The 2025 single "Installing the R environment" slide becomes three. Drop the R "Code Like a Pirate!" mascot. Full slide text:

> **Slide 22 — Installing Python**
> - Install Miniconda from https://www.anaconda.com/docs/getting-started/miniconda/main . It installs in your user folder and needs no admin rights.
> - Download the course zip from https://DH-Oz.github.io/CorpusAnalysis .
> - On a locked-down machine, run the notebooks in Google Colab: https://colab.research.google.com .
>
> *Spoken, not on the slide:* this replaces the five R bullets (R / RStudio / RMarkdown / RTools / Linux-see-Brian). Day-1 AM verifies an install students did before class. A Mac with admin can use `brew install --cask miniconda`; the direct `.pkg` needs no admin. Linux: see Brian.

> **Slide 23 — What is an environment?**
> - An environment bundles one copy of Python with the exact libraries a project needs.
> - It stays separate from the rest of your computer.
> - Different projects can need different versions of the same library. Each environment keeps its own.
> - `environment.yml` lists everything this course needs. Every student's `corpusanalysis` comes out identical.
> - You can delete and recreate it any time. Nothing else on your machine changes.
>
> *Spoken:* R students `install.packages` globally, so this idea is new. It explains what the launcher on slide 24 is building for them.

> **Slide 24 — Setting up and starting Jupyter** *(rewritten 2026-07-29: the terminal route is no longer the taught path)*
> 1. Unzip the course zip onto your Desktop.
> 2. Start it the way your machine wants:
>    - Windows: double-click `start-jupyter.bat`
>    - Mac: open Terminal, type `cd` and a space, drag the folder in, press Return, then run `sh start-jupyter.sh`
> 3. The first time, it asks whether to install Miniforge. Say yes. It goes in one folder in your home directory and needs no admin password.
> 4. It then builds the course environment, which takes a few minutes, and opens JupyterLab in your browser.
> 5. Leave the black window open while you work.
> 6. In the Day 1 notebook, type `print("Hello, world!")` and press Shift + Enter.
>
> *Spoken:* Mac users, do not double-click the launcher. macOS blocks anything that came off the internet, and the box it shows you offers only Delete and Close, which is a cruel pair of choices. Starting it from the Terminal walks around the whole problem, because the file is being read rather than launched. Two lines, once per session, and no password. There is also no `conda activate` to remember, which is the step that used to break people.

A `0-setup-check.ipynb` smoke test then runs before notebook 1.

**First-look figures → notebook 1's live output.** Each runs to 2026, including Biden and Trump:
- length scatter → `figures/1a-sotu-corpus-00.png` (points, not the 2025 line: speeches are discrete events)
- corpus wordcloud → `figures/1a-sotu-corpus-01.png`
- five dendrograms, metric × era → `figures/1b-sotu-by-speech-00.png` … `-04.png`
- three comparison clouds → `figures/1b-sotu-by-speech-05.png` … `-07.png`

**Console output → notebook output.** `head(dfmat_sotu)`, `topfeatures()`, the LDA term table (pp29, 34): screenshot the Python notebook running, not the R console.

**Palettes (p31).** `brewer.pal` → matplotlib colormaps. Reference image: `day-1/img/matplotlib-palettes.png`.

---

## D1-PM — Brian, code-along — your first wordcloud and clustering

*Objectives (≤3):* (1) run a Jupyter cell, read its output, and recover when it errors; (2) build a wordcloud and a hierarchical clustering from the corpus by typing along.

*Stays 1:1 (do not touch):* the dividers, the "What is Markdown?" explanation, the Atlantic "scientific paper is obsolete" link, the sticky-note slide.

### Slides to change

**Slides 4–7 — RStudio / RMarkdown screenshots (images).** Replace with Jupyter screenshots to capture → `day-1/img/jupyter-*.png` (a fresh notebook, a code cell, the run output). [screenshots not yet taken]

**Hello-World chunk (text).** The R chunk `print("Hello World")` → a Python cell: `print("Hello, world!")`.

**Follow-along pointer (text).** "Follow along: corpusmasterclass0.Rmd" → "Follow along: `1a-sotu-corpus.ipynb`, then `1b-sotu-by-speech.ipynb`".

**"Knit to PDF report" beat — drop.** No Jupyter equivalent students need. Cut the slide, or let "run cells, see output" stand in.

---

## D2-AM — Brian — demos of what corpus analysis can do

*Objectives (≤3):* (1) name the analyses the course will cover and say what question each one answers.

*Stays 1:1 (do not touch):* everything. The agenda, Brian's Gab dispersion plot and topic table from his published work, the "AI for data analysis" slide (BERTopic, sentiment, summarisation, already Python-world tools), the sticky-note slide.

### Slides to change

None. A showcase, not a build, so nothing changes in code. The agenda is tool-agnostic and the techniques live in notebooks 1 and 3a.

---

## D2-PM — Mark — dictionaries, matrices, and networks

*Objectives (≤3):* (1) apply a content-analysis dictionary to a corpus and read a category as a percentage over time; (2) explain a document-feature matrix and what its transpose-times-itself product measures; (3) read a category co-occurrence network.

*Stays 1:1 (do not touch):* the "LIWCing at SOTUs" divider, the Count, the LIWC and LIWC-22 website shots, the dictionary category lists, Mark's MAC-D paper and his MAC-D-versus-MFD opinion, the Firth quote, the transpose diagram, the Top Gun and "always has been" memes, the "not commutative" slide, the closing.

### Slides to change

**Slide 2 — dictionary intro (text).** `quanteda` → the Python stack: `CountVectorizer` for the matrix, the `liwc` package for dictionaries.

**Follow-along pointer (text).** "Follow along: corpusmasterclass2.Rmd" → "`2-dictionary-content.ipynb`".

**Category-trend figures → notebook 2's scatters** (line becomes points; each runs to 2026):
- seven MAC virtues (pp20–26) → `figures/2-dictionary-content-00.png` … `-06.png`
- LIWC emotion trends (pp12–15) → among `figures/2-dictionary-content-09.png` … `-14.png` (regenerated once `liwcdict.dic` was in place)

**Co-occurrence networks (p35) → notebook 2** (force-directed and circular): `figures/2-dictionary-content-07.png` and `-08.png`.

**LIWC output table (p8) → notebook output.** Use the notebook's own `liwcalike()` table, not the R screenshot.

**Optional new figures — summary metrics (pp10–11).** The 2025 deck plots LIWC word count and words-per-sentence. These are not category percentages, so they are not in notebook 2. `slide-figures.ipynb` makes them: `figures/slide-sotu-wc.png`, `figures/slide-sotu-wps.png`. Use them only if the lecture wants them.

---

## D3-AM — Mark — dispersion, networks, and German

*Objectives (≤3):* (1) read a lexical-dispersion plot and say where in a text a word concentrates; (2) read a semantic network and how it shifts across decades; (3) carry the whole pipeline into German with a custom dictionary.

*Stays 1:1 (do not touch):* the nuclear-theme images, the bigram pride-flag joke, the nuke.dic list, the Monty Python turn, the nietzschesource.org page, Mark's *Nietzsche's Moral Psychology* cover, the Carly Simon sleeve, the closing, and all of the presidential "war criminals" banter.

### Slides to change

**Nuclear half → notebook 3a** (each figure runs to 2026):
- `atom` / `nuclear` dispersions (pp8–9) → `figures/3a-collocations-dispersion-00.png`, `-01.png`
- nuke trend (p10) → `figures/3a-collocations-dispersion-02.png`
- decade networks 1940s–2010s (pp12–19) → `figures/3a-collocations-dispersion-03.png` … `-11.png`
- collocation and keyness tables (pp5–6) → notebook printed output

**German half → notebook 3b.** The German wordcloud, dendrogram, two comparison clouds, the `scham*` / `vertrau*` dispersions, the moral-category scatters (instinct, shame, virtue), and the concept egonets (book, paragraph, and per-concept: solitude, modesty, humility) all come from `figures/3b-nietzsche-german-paragraphs-*.png`. The German topic and per-book tables → notebook printed output. The 'virtue' `[tugend*]` keyness slide keeps its Google-Translate panel.

**Optional new figure — whole-corpus nuclear network (p11).** The 2025 slide shows the nuclear network over the whole corpus; notebook 3a builds only per-decade ones. `slide-figures.ipynb` makes it: `figures/slide-sotu-nuke-network.png`.

**On "LIWC in German".** 2026 uses the open `nietzsche.dic` on the Nietzsche corpus, not a commercial German LIWC. Nothing gitignored, and all of notebook 3b's figures generate cleanly.

---

## D3-PM — Brian, code-along — build your own dictionary

*Objectives (≤3):* (1) write a small content-analysis dictionary for a question of their own and run it.

*Stays 1:1 (do not touch):* all of it.

### Slides to change

None. A code-along that happens off the slides. The class builds a `.dic` file in the same format as `nuke.dic` and `macdvirtue.dic`, which ship.

---

## D4-AM — Brian and Mark — finding and building corpora

*Objectives (≤3):* (1) find corpus data from public sources and bring it in; (2) use a language model to help clean and shape that data.

*Stays 1:1 (do not touch):* the dataset-source list, the Hansard and Factiva walk-throughs, the closing.

### Slides to change

**Slide 4 — search term (text).** "nsw hansard api r-lang" → "nsw hansard api python".

**Slide 6 — model name (text).** "Demo with Claude 3.5 Sonnet" → the current Claude model (e.g. Opus 4.8 for the 2026 delivery).

**Source links (logistics).** Refresh any dead links; the Twitter/X access terms have changed.

---

## D4-PM — Brian and Mark — brainstorming and goodbyes

*Stays 1:1 (do not touch):* the single Puck epilogue from *A Midsummer Night's Dream*. Reflection and goodbyes.

### Slides to change

None.

---

## The three figures only `slide-figures.ipynb` makes

Two lecture slides and one network had no figure in any code-along notebook.
`slide-figures.ipynb` makes all three from the corpus:

- `figures/slide-sotu-wc.png` — words per State of the Union address over time (D2-PM)
- `figures/slide-sotu-wps.png` — words per sentence over time (D2-PM)
- `figures/slide-sotu-nuke-network.png` — nuclear co-occurrence across the whole corpus (D3-AM)

What remains is a choice, not a gap: which category trends Mark actually puts on
slides. The notebooks emit a superset of what the decks show, so he selects
rather than waits for anything to be built.
