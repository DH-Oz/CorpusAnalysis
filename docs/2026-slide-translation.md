# 2025 → 2026 slide translation

Per-deck change-list for the R → Python pivot. The 2026 lectures are rebuilt as
**Google Slides** by Mark; this document says, slide by slide, what each 2025
(R) slide becomes in 2026 — a `figures/` image, rewritten text, or unchanged.

**Figure source:** every teaching figure is regenerated from the course corpus
by `tools/export_figures.py` and lives in `figures/`. Run
`uv run python tools/export_figures.py`; `git diff --stat figures/` then names
any image that changed. Mark's own published research figures (his papers) are
*not* course-corpus figures and cannot be regenerated here — they are flagged
"keep (Mark's research)".

Page numbers are within each split PDF in `2025-slides/` (each file starts at
its own page 1).

Action tags: **FIG** (swap in a `figures/` image) · **TEXT** (rewrite prose) ·
**KEEP** (carries over unchanged) · **LOGISTICS** (links/QR) · **OUTPUT**
(R console output → screenshot of the Python notebook's output).

---

## D1-AM-intro (Mark) — `2025-slides/D1-AM-intro.pdf`, 45 pp

Mostly Mark's verbatim intro. The R content is the install section and the
"first corpus analysis" demo, whose plots are exactly notebook 1's ten figures.

### Figures — one-to-one with `1-sotu-first-look`

| 2025 p# | Slide | 2026 figure |
|---|---|---|
| 28 | Token-length over time (ggplot **line**, by party) | `figures/1-sotu-first-look-00.png` — note: ours is a **scatter**, not a line (speeches are discrete events) |
| 30 | SOTU word cloud (corpus-wide top terms) | `figures/1-sotu-first-look-01.png` |
| 35 | Dendrogram, every speech, Euclidean (237 leaves) | `figures/1-sotu-first-look-02.png` |
| 36 | Dendrogram, modern (1977+), Euclidean | `figures/1-sotu-first-look-03.png` |
| 37 | Dendrogram, modern (1977+), cosine | `figures/1-sotu-first-look-04.png` |
| 39 | Dendrogram, founders (pre-1850), Euclidean | `figures/1-sotu-first-look-05.png` |
| 40 | Dendrogram, founders (pre-1850), cosine | `figures/1-sotu-first-look-06.png` |
| 41 | Comparison cloud — Washington's 8 messages | `figures/1-sotu-first-look-07.png` |
| 42 | Comparison cloud — Adams + Jefferson | `figures/1-sotu-first-look-08.png` |
| 43 | Comparison cloud — Obama + Trump | `figures/1-sotu-first-look-09.png` |

### Text / tool-name changes

| 2025 p# | Slide | Action | Change |
|---|---|---|---|
| 5 | Agenda | TEXT | "R installation" → "Python install & verification"; "(re)introduction to quanteda" → "…to document-feature matrices"; "more quanteda and LIWC" → "more document-feature matrices and LIWC" |
| 9–12 | Beginner notes (otherwise verbatim) | TEXT | one phrase: "update **R** and all packages" → "update **Python** and your packages" |
| 21 | "Installing R" divider | TEXT | → "Installing Python" |
| 22 | Installing the R environment (R / RStudio / RMarkdown / RTools) | TEXT | → Miniconda + Jupyter install & verify; drop the R-pirate art (or a neutral image) |
| 23 | "Your first RMarkdown" — `install.packages(...)` chunk | TEXT | → "Verifying your environment": the notebook's import-check cell (`import sotu, pandas, …`) |
| 24 | "Follow along: corpusmasterclass0.Rmd" | TEXT | → "Follow along: **1-sotu-first-look.ipynb**" |
| 26 | SOTU bullets + `.rda` corpus list | TEXT | "Available natively in **quanteda.corpora**" → "Available via the **sotu** package"; drop the `data_corpus_*.rda` list (quanteda-only). Photos KEEP |
| 31 | `brewer.pal` R help | TEXT+FIG | → matplotlib colormaps; use `day-1/img/matplotlib-palettes.png` as the reference image |
| 29 | `head(dfmat_sotu)` / `topfeatures()` R console | OUTPUT | screenshot the Python DFM + top-20 output from notebook 1 |
| 34 | LDA `get_terms()` R console (8 topics) | OUTPUT | screenshot the Python `top_topics()` output (notebook 1 does 8- then 5-topic) |

### Keep (Mark's research or general concept — no change)

- p1 title · p2–4 McCarthy / *Tempest* epigraphs · p6 introductions · p7 sticky-note protocol · p13 divider · p25 "doing math" meme · p33 ColorBrewer palette theory · p38 distance-metrics diagram · p44 feedback · p45 thanks.
- **Mark's research figures (keep):** p17 BLM emoji/hashtag networks · p18 masculinity-extremism dendrogram · p20 vaccine-discourse stacked area. (p18 previews the dendrogram technique taught later.)
- p14–16, p19 PhilPapers / journal screenshots — KEEP.
- p32 ColorBrewer website — KEEP (tool-agnostic) or swap to a matplotlib reference, your call.

### Logistics

- p8 "Files available here" QR + `tinyurl.com/yc4awanh` → **LOGISTICS**: new release-zip link once the GitHub release exists.

---

## D1-PM-wordcloud-hclust (Brian, code-along) — `2025-slides/D1-PM-wordcloud-hclust.pdf`, 11 pp

Brian's first type-along. **No course-corpus figures** — this is the RStudio/RMarkdown setup ritual (Hello World, knit to a report) plus a live wordcloud. The 2026 equivalent is the Jupyter workflow + notebook 1.

| p# | Slide | Action | Change |
|---|---|---|---|
| 1 | "Day 1 PM: Type-along with Brian" divider | KEEP | |
| 2 | Agenda — follow-along demos | TEXT | "Technical Validation: making a markdown document; generating a PDF report" → reframe for Jupyter (run a notebook; export only if kept) |
| 3 | "Technical Validation" divider | KEEP | |
| 4 | Hello World in RMarkdown (RStudio screenshot) | TEXT+IMG | → Jupyter "Hello World": new notebook, run a cell; replace RStudio screenshot with Jupyter |
| 5 | "Run current chunk" (RStudio `plot(cars)`) | IMG | → Jupyter "run a cell" screenshot |
| 6 | "Add hello world" — `` ```{r} print("Hello World") `` | TEXT | → a Python cell: `print("Hello World")` |
| 7 | "Preview, then Publish" — knit to Word/PDF | TEXT+IMG | knit → nbconvert export, or drop the report-publishing beat. The Atlantic "scientific paper is obsolete" link KEEPS |
| 8 | "What is Markdown?" (Gruber) | KEEP | tool-agnostic |
| 9 | "Getting Started with Corpus Analysis" divider | KEEP | |
| 10 | "Code along … generate a wordcloud" | TEXT | code-along = notebook 1; the live wordcloud is `figures/1-sotu-first-look-01.png` if a static is wanted |
| 11 | Sticky-note feedback | KEEP | |

**Open decision:** the RMarkdown "knit to a PDF report" workflow (pp4–7) has no clean Jupyter equivalent students need. Likely simplify to "make a notebook, run cells, see output" and drop the report-publishing beat — Brian's call.

---

## D2-AM-demos (Brian) — `2025-slides/D2-AM-demos.pdf`, 5 pp

Brian's live-demo showcase. Tool-agnostic agenda + Brian's own research figures. **Essentially all KEEP** — no R tool-names, no course-corpus figures to swap.

| p# | Slide | Action | Note |
|---|---|---|---|
| 1 | "Day 2 AM: Live demos" divider | KEEP | |
| 2 | Agenda (wordcloud, topic models, hierarchical clustering, comparison clouds, dispersion) | KEEP | tool-agnostic; the techniques live in notebooks 1 and 3a |
| 3 | "Brian's Research" — Gab racial-superiority dispersion plot + topic table + Zenodo links | KEEP | Brian's published research (content-warning slide), not course corpus |
| 4 | "AI (LLMs) for data analysis" — BERTopic, sentiment, summarisation | KEEP | after-school; these are already Python-world tools |
| 5 | Sticky-note feedback | KEEP | |

Nothing to change — the demos draw on notebooks 1 and 3a, which already exist.

---

## D2-PM-dfm-collocations (Mark) — `2025-slides/D2-PM-dfm-collocations.pdf`, 37 pp

Mark's LIWC + dictionaries + matrices lecture. Maps to **notebook 2 (2-dictionary-content)**. The category-trend plots and the co-occurrence networks are notebook 2's figures, and ours are **scatter, not the 2025 lines** (speeches are discrete). `figures/` for notebook 2 was regenerated this session with `liwcdict.dic` in place, so it now carries the LIWC emotion plots too — **15 figures**: MAC trends `00–06`, networks `07–08`, LIWC emotions `09–14`.

### Figures → notebook 2 (all scatter, not lines)

| 2025 p# | Slide | 2026 figure |
|---|---|---|
| 8 | LIWC `liwcalike` table (WPS, WC, Sixltr, Dic, function, pronoun…) | OUTPUT: screenshot notebook 2's `liwcalike(...)` table — `corpus_tools.liwcalike` produces exactly these columns |
| 10 | WC (word count) over year | **GAP** — a LIWC *summary* metric, not a category %. Not plotted by notebook 2. Add it, or drop (≈ notebook 1's token-length plot) |
| 11 | WPS (words per sentence) over year | **GAP** — same; add or drop |
| 12 | Posemo over year | `figures/2-dictionary-content-10.png` (LIWC: Posemo) |
| 13 | Anx over year | `…-12.png` (Anx) |
| 14 | Anger over year | `…-13.png` (Anger) |
| 15 | Sad over year | `…-14.png` (Sad) |
| 20–26 | MAC-D trends: Family, Group, Reciprocity, Heroism, Deference, Fairness, Property | `figures/2-dictionary-content-00 … -06` (`plot_category` scatters, one per MAC virtue) |
| 35 | Two MAC co-occurrence networks (force-directed + circular) | `…-07.png` (spring) + `…-08.png` (circular) |

LIWC emotion set generated is Affect/Posemo/Negemo/Anx/Anger/Sad (`09–14`); the deck shows four of them. **Reconcile** which category trends Mark wants on slides so notebook 2 emits exactly that set. Keeping the WC/WPS summaries (pp10–11) means adding two plots; `liwcdict.dic` stays local/gitignored, the resulting PNGs are safe to ship.

### Text / tool changes

| p# | Slide | Action | Change |
|---|---|---|---|
| 1 | "Day 2 PM: **quanteda**" + "Follow along: corpusmasterclass2.Rmd" | TEXT | → "Day 2 PM: document-feature matrices"; "Follow along: **2-dictionary-content.ipynb**" |
| 2 | quanteda.io site ("R package by Kenneth Benoit") | TEXT+IMG | → the Python stack: `CountVectorizer` for the DFM, the `liwc` package for dictionaries; drop the quanteda.io screenshot |
| 34 | "Live demo!" + `tinyurl.com/bdz7chz2` | LOGISTICS | update the link |

### Keep

p3 "LIWCing at SOTUs" divider · p4 The Count · p5–7 LIWC / LIWC-22 sites + Cash (update to LIWC-22 if desired) · p9 dictionary category lists (same `.dic` files) · p16 "beyond base LIWC" divider · p17 custom-dictionaries intro · p18–19 Mark's MAC-D paper + the MAC-D-vs-MFD opinion · p27 "semantic networks" divider · p28 Firth "company it keeps" · p29 "RAMSIFY" · p30 "always has been" meme · p31 transpose diagram · p32 Top Gun · p33 "not commutative" · p36 feedback · p37 thanks.

---

## D3-AM-german-liwc (Mark) — `2025-slides/D3-AM-german-liwc.pdf`, 47 pp

The biggest deck, two halves: **nuclear / dispersion / decade-networks → notebook 3a**, then **German Nietzsche → notebook 3b**. Mark's "American presidents are war criminals :)" presidential banter (pp12–20) is the interjection device — **KEEP all of it**.

### Nuclear half → notebook 3a

| 2025 p# | Slide | 2026 |
|---|---|---|
| 5 | R collocations (united states, federal government…) | OUTPUT: notebook 3a's nltk bigram / likelihood-ratio output |
| 6 | keyness table (weapons, proliferation… chi²) | OUTPUT: 3a's chi-squared keyness output |
| 8 | dispersion `atom*` | `figures/3a-collocations-dispersion-00.png` |
| 9 | dispersion `nuclear*` | `…-01.png` |
| 10 | nuke category % over year | `…-02.png` |
| 11 | semantic network, **whole SOTU corpus** | **GAP** — 3a does per-decade only. Add a whole-corpus network, or use a decade |
| 12–19 | semantic networks, 1940s–2010s (one per decade) | `…-03/04 … -11` (decade_network loop; 1940 worked example is `03`/`04`) |

### German half → notebook 3b

| 2025 p# | Slide | 2026 |
|---|---|---|
| 23, 33 | Nietzsche book length (Tokens vs Year) | 3b book-length scatter |
| 24 | German wordcloud (menschen, leben, macht…) | 3b German wordcloud |
| 25 | `topfeatures` (German) | OUTPUT |
| 26 | LDA topics (German) | OUTPUT |
| 27 | per-book top features | OUTPUT |
| 28 | dendrogram (Nietzsche books) | 3b dendrogram |
| 29–30 | comparison clouds (early / late Nietzsche) | 3b comparison clouds (×2) |
| 31 | dispersion `scham*/schmach*/schand*` (shame) | 3b German dispersion (shame) |
| 32 | dispersion `vertrau*/misstrau*` (trust) | 3b German dispersion (trust) |
| 34 | Sixltr vs Year | 3b metric scatter |
| 35–37 | instinct / shame / virtue vs Year | 3b `nietzsche.dic` category scatters |
| 38–40 | concept network — book (force + circle), paragraph (circle) | 3b concept egonet (book + paragraph) |
| 42–44 | egonets: solitude / modesty / humility | 3b per-concept egonet loop |
| 45 | 'virtue' `[tugend*]` keyness + Google Translate | OUTPUT (3b `keyness_top`); KEEP the Google-Translate device |

All German figures are `figures/3b-nietzsche-german-paragraphs-*.png` (20 figures; exact index per figure reads off notebook 3b). The metric/category trends are **scatter** (the 2025 ones already are).

### Text / tool changes

| p# | Slide | Action | Change |
|---|---|---|---|
| 1 | "Day 3 AM…" + "Follow along: corpusmasterclass3a.Rmd / 3b.Rmd" | TEXT | → "Follow along: **3a-collocations-dispersion.ipynb**, **3b-nietzsche-german-paragraphs.ipynb**" |
| 2 | "State of the Union addresses" (quanteda.corpora) | TEXT | "quanteda.corpora" → "sotu" (same edit as D1-AM p26) |

### Keep

p3 nuclear-theme images (towers, bomb, Einstein, Oppenheimer) · p4 bigram pride-flag joke · p7 nuke.dic list · p20 conclusion + banter · p21 Monty Python · p22 nietzschesource.org · p38 Mark's *Nietzsche's Moral Psychology* cover · p41 Carly Simon "You're So Vain" · p46 feedback · p47 thanks · **all presidential war-criminal banter (pp12–20)**.

**German-LIWC note:** the title says "LIWC in German", but 2026 uses the **open `nietzsche.dic`** moral-psychology dictionary on the Nietzsche corpus instead of a commercial German LIWC — no gitignored dependency, and all 20 of notebook 3b's figures generate cleanly.

---

## D3-PM-custom-dict (Brian, code-along) — `2025-slides/D3-PM-custom-dict.pdf`, 3 pp

Code-along; the teaching is off-slide. **All KEEP** — no R, no figures.

| p# | Slide | Action |
|---|---|---|
| 1 | "building your own custom dictionary" divider | KEEP |
| 2 | "Who wants to be the lab rat?…" | KEEP |
| 3 | Sticky-note feedback | KEEP |

Students build a `.dic` live (same format as `nuke.dic` / `macdvirtue.dic`, which ship).

---

## D4-AM-corpus-construction (Brian/Mark, split class) — `2025-slides/D4-AM-corpus-construction.pdf`, 7 pp

Finding + building corpora with AI. Tool-agnostic; mostly KEEP. No figures.

| p# | Slide | Action | Change |
|---|---|---|---|
| 1 | "Day 4 AM: corpus construction" divider | KEEP | |
| 2 | Agenda (find data; LLM chat-driven dev; live demo) | KEEP | |
| 3 | "How to find data" (dataset sources) | KEEP | refresh any dead links (Twitter/X Powertrack pricing/status has changed) |
| 4 | "State Hansard" (NSW Hansard API; Copilot in VSCode) | TEXT | "nsw hansard api **r-lang**" → "…python"; rest KEEP |
| 5 | "Factiva RTF" download | KEEP | |
| 6 | "chat driven development… Demo with **Claude 3.5 Sonnet**" | TEXT | update model name to the current Claude |
| 7 | Sticky-note feedback | KEEP | |

---

## D4-PM-brainstorming (Brian/Mark) — `2025-slides/D4-PM-brainstorming.pdf`, 1 p

| p# | Slide | Action |
|---|---|---|
| 1 | Puck epilogue ("If we shadows have offended…") | KEEP |

No teaching content; goodbyes and reflection. No changes.

---

## Figure gaps to decide (the only things not already in `figures/`)

`figures/` now holds **58** images (1-sotu 10, 2-dictionary 15, 3a 13, 3b 20), all regenerated from the corpus. Three lecture figures have no current source:

1. **D2-PM pp10–11** — LIWC *summary* metrics WC + WPS over year. Notebook 2 plots category percentages, not these. Add two plots, or drop (WC ≈ notebook 1's token-length).
2. **D3-AM p11** — semantic network over the *whole* SOTU corpus. Notebook 3a builds per-decade networks only. Add a whole-corpus network, or use a decade.
3. **Category-set reconciliation** — the decks show specific category trends (7 MAC, 4 LIWC emotions, several Nietzsche categories). Decide exactly which Mark wants on slides and make notebooks 2/3b emit that set, so every figure-slide has a `figures/` image.

Everything else maps to an existing `figures/` image or a small text edit.

