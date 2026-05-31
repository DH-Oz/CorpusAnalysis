# QA findings — `day-1/D1-AM-intro.ipynb` (revised)

Produced 2026-05-27, revised after the first pass's mechanical-replacement trap was caught. The rule fixed in this revision: diseased patterns are SENTENCE STRUCTURES, not characters; swapping `—` for `;` is not a fix.

**Status: proposed edits below. Awaiting sign-off.**

## Pre-flight (unchanged from first pass)

- 2025 source: `2025-slides/D1-AM-intro.pdf` pp.1-45, read cover-to-cover.
- 2026 notebook: 74 cells (44 markdown, 30 code).
- Open question decisions (you answered):
  - Meme p25 "Get In Losers": **drop** for now.
  - Alt-text em-dashes (cells 14-20, 48-50, 61): **clean** (real-fix rewrites, not char swaps).
  - McCarthy fragment-build (cell 1): not addressed; **deferred** as a separate decision. Cell 1 unchanged in this pass.

## Cell-page map and classification (unchanged from first pass)

See first revision; classifications still hold. No re-tabulation here.

## Voice findings — trap vs real fix

For each Claude-authored cell with a diseased sentence pattern, the trap (char swap) and the real fix (sentence rewrite) are shown side-by-side. The real-fix wording is what gets applied.

### Label-prefix em-dashes (legitimate label use; rewrite as proper labels)

| Cell | Current | Real fix |
|---:|---|---|
| 4 | `INSTRUCTOR NOTE — 2025 slide says "R installation" ...` | `**Note:** 2025 slide says "R installation" ...` (drop the em-dash-as-label; use proper bold-colon label) |
| 8 | `INSTRUCTOR NOTE — The 2025 link was ...` | `**Note:** The 2025 link was ...` |
| 35 | `INSTRUCTOR NOTE — 2025 named ...` | `**Note:** 2025 named ...` |

### Parenthetical-aside crams in Claude-authored sentences (rewrite the sentence)

| Cell | Trap | Fake fix (do NOT do) | Real fix |
|---:|---|---|---|
| 7 | `**https://github.com/...**\n\n*(QR code regenerated from the final release-tag URL before the masterclass opens.)*` | swap parens for em-dashes or remove parens only | **drop the parenthetical entirely** — the regen info already lives in cell 8 notes |
| 8 (body) | `Students download a zip from the release page — no git operations are ever taught.` | `... release page; no git operations are ever taught.` | **drop the aside**: stop after `Students download a zip from the release page.` (the "no git" claim is implied by the prior sentences and lives on its own in `.notes/feedback_no-git-for-students.md`) |
| 22 | `**Jupyter**: bundled with Miniconda — \`conda install -c conda-forge jupyterlab\` if missing` | swap `—` for `;` | **drop the aside** — Miniconda includes Jupyter; the install-if-missing case is rare. Bullet becomes: `**Jupyter**: bundled with Miniconda.` |
| 22 | `**For locked-down machines**: open the notebooks in Google Colab — every notebook ships with a Colab-compatible install cell` | swap `—` for `;` | **drop the aside**: `**For locked-down machines**: open the notebooks in Google Colab.` The install-cell promise is true of every notebook, not worth saying per-bullet. |
| 26 | `We now import the libraries this course uses. If any line raises \`ImportError\`, the conda environment is incomplete — fix it now rather than mid-lesson.` | swap `—` for `.` and keep imperative | **drop the imperative** (telling-about): `The course uses the libraries below. An \`ImportError\` means the conda environment is incomplete.` |
| 30 | `spaCy needs pre-trained language models. We use the small English and German models for this course — both are pulled in by \`environment.yml\`.` | swap `—` for `;` | **restructure**: `spaCy needs pre-trained language models. The small English and German models ship in \`environment.yml\`.` |
| 51 | `## ColorBrewer palettes in Python — via matplotlib` | `## ColorBrewer palettes in Python: via matplotlib` | **drop redundant qualifier**: `## ColorBrewer palettes via matplotlib` ("in Python" is implied by the whole course being Python) |

### Other Claude diseased patterns

| Cell | Issue | Real fix |
|---:|---|---|
| 47 | Whole cell is invented colour-aside transition with stacked triplets (*"...sequential, diverging, and qualitative. The next slide is the picker; the slide after that is the catalogue; the slide after that is how to pull one in Python."*) | **delete cell entirely**; cell 48 already opens its own slide |
| 36 | Claude rewrote Mark's 2025 SoU bullets with added detail (237 number, specific years, attribution), inserting two em-dashed asides | **restore 2025 wording verbatim** with library substitution only (full body in Proposed Edits below) |
| 53 | `## Topic modelling — Latent Dirichlet Allocation` (British spelling + em-dash; 2025 used American "modeling" and no dash) | **match 2025 verbatim**: `## Topic modeling using Latent Dirichlet Allocation` |
| 40, 43, 45, 55, 57, 59, 62, 64, 66, 68, 70 | Claude-invented `## Heading — Subhead` lines on slides where 2025 had NO heading | **strip to `<!-- demo slide -->` placeholder** (preserves slide_type:slide for reveal.js boundary; removes invented heading; lets the live code output be the visual per `demo-slides-show-live-output`) |

### 2025-verbatim cells where Claude introduced char drift (restore Mark's chars)

| Cell | Drift | Restore to |
|---:|---|---|
| 3 | `**Day 4 AM (Brian/Mark) — *splitting class*:**` (Claude's em-dash restructuring) | 2025 pattern: `**Day 4 AM (Brian/Mark): Splitting class:** finding and constructing corpora with AI \| how to download things other people have built` |
| 6 | `"I'd like some help" — the person not speaking will head over to help you` (em-dash) | Mark's en-dash: `"I'd like some help" – the person not speaking will head over to help you` |
| 12 | `... isn't set correctly, you just need to **update** your Python or conda packages, or just **restart** Jupyter.` (lost en-dash, lost "or you just need to" structure) | Restore Mark's structure (with Python substitutions only): `... isn't set correctly, or you just need to **update** your Python or conda packages – or just **restart** Jupyter.` |

### Alt-text rewrites (cells 14-20, 48-50, 61) — drop em-dashes by simplifying descriptions

Alt text isn't on-slide content, but the user said clean. Default: shorter, no parenthetical-aside crams.

| Cell | Current alt text | Real fix |
|---:|---|---|
| 0 | `Title image — illustrated cover scene for the Corpus Analysis Masterclass: a path of text emerging from open books toward a horizon of word-node constellations.` | `Cover image for the Corpus Analysis Masterclass.` |
| 14 | `PhilPapers search for "corpus linguistics" — 56 hits, including Mejía-Ramos et al. (2019) ...` | `PhilPapers search results for "corpus linguistics".` |
| 15 | `PhilPapers search for "corpus analysis" — 26 hits, including Magro (2010) ...` | `PhilPapers search results for "corpus analysis".` |
| 16 | `Social Science Computer Review (2022), "The Affiliative Use of Emoji and Hashtags ..." — Alfano, Reimann, ...` | `Journal article: "The Affiliative Use of Emoji and Hashtags in the Black Lives Matter Movement in Twitter" (Social Science Computer Review, 2022).` |
| 17 | `Four collocation networks from the BLM paper — each panel is a different Twitter community ...` | `Four collocation networks from the BLM paper, one per Twitter community, showing hashtag-emoji co-occurrence.` |
| 18 (second image) | `Hierarchical clustering dendrogram — Euclidean distance on normalised token frequency across six documents (Rodger.pdf, AMRA.docx, MRA.docx, Tarrant.pdf, Lads.docx, MGTOW.docx).` | `Hierarchical clustering dendrogram of six documents using Euclidean distance on normalised token frequency.` |
| 19 | `*PLOS ONE* (open access), "Polarization and trust in the evolution of vaccine discourse on Twitter during COVID-19" — Ojea Quintana, Reimann, Cheong, Alfano & Klein.` | `Journal article: "Polarization and trust in the evolution of vaccine discourse on Twitter during COVID-19" (PLOS ONE, open access).` |
| 20 | `Stacked-area chart of daily word counts across five community labels — Unorth (purple), ... — with a vertical reference line marking a key inflection.` | `Stacked-area chart of daily word counts across five community labels (Unorth, Health, Dem, Antivax, Repub) with a vertical reference line marking a key inflection.` |
| 48 | `Matplotlib's named-palette families — Sequential / Diverging / Qualitative. Any name shown here is reachable in code via \`matplotlib.colormaps[name]\`.` | `Matplotlib's named palette families (Sequential, Diverging, Qualitative). Any name is reachable in code via \`matplotlib.colormaps[name]\`.` |
| 49 | `colorbrewer2.org — interactive palette picker for sequential, diverging, and qualitative colour schemes (language-agnostic; both R and Python users use this).` | `colorbrewer2.org, an interactive palette picker for sequential, diverging, and qualitative colour schemes.` |
| 50 | `ColorBrewer palette descriptions — Sequential / Diverging / Qualitative families with palette names and value ranges. Language-agnostic reference; the same family names appear as matplotlib colormaps.` | `ColorBrewer palette description page covering Sequential, Diverging, and Qualitative families.` |
| 61 | `Distance metrics illustrated — nine panels covering Euclidean, Cosine, Hamming, Manhattan, Minkowski, Chebyshev, Jaccard, Haversine, and Sørensen-Dice. Language-agnostic conceptual reference.` | `Nine-panel illustration of distance metrics: Euclidean, Cosine, Hamming, Manhattan, Minkowski, Chebyshev, Jaccard, Haversine, Sørensen-Dice.` |

## Layout findings

No findings (unchanged from first pass).

## Structural findings

1. **2025 p25 meme**: deferred per your call.
2. **Cell 1 McCarthy fragment-build**: deferred (separate decision).

## Proposed edits (ordered for safe application)

Working in descending cell-index order so deletions don't shift indices of earlier cells. Tool: `tools/notebook_cells.py`.

1. **Cell 70** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
2. **Cell 68** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
3. **Cell 66** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
4. **Cell 64** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
5. **Cell 62** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
6. **Cell 61** → alt-text rewrite per table above
7. **Cell 59** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
8. **Cell 57** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
9. **Cell 55** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
10. **Cell 53** → `replace_cell(slide_type=slide, "## Topic modeling using Latent Dirichlet Allocation")`
11. **Cell 51** → `replace_cell(slide_type=slide, "## ColorBrewer palettes via matplotlib\n\nMatplotlib ships the ColorBrewer palettes as named colormaps. Anything you'd pick on \`colorbrewer2.org\` is reachable by name (\`\"Blues\"\`, \`\"YlGnBu\"\`, \`\"Set1\"\`, …).")`
12. **Cell 50** → alt-text rewrite
13. **Cell 49** → alt-text rewrite
14. **Cell 48** → alt-text rewrite
15. **Cell 47** → `delete_cells([47])`
16. **Cell 45** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
17. **Cell 43** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
18. **Cell 40** → `replace_cell(slide_type=slide, "<!-- demo slide -->")`
19. **Cell 38** → `replace_cell(slide_type=slide, "## Washington-1790")` (drop the blockquote prose; cell 39's code output is the visual)
20. **Cell 36** → `replace_cell(slide_type=slide, "## State of the Union addresses\n\n- From 1790 to present\n- Yearly (unlike inaugurals)\n- Mixed format (written vs spoken)\n- Varying lengths (1k-35k)\n- Available natively in the \`sotu\` Python package\n\n<div class=\"image-grid\">\n\n![SoU photo 1](img/p26-i0.png)\n![SoU photo 2](img/p26-i1.png)\n![SoU photo 3](img/p26-i2.png)\n![SoU photo 4](img/p26-i5.png)\n\n</div>")`
21. **Cell 35** → `replace_cell(slide_type=notes, "**Note:** 2025 named \`corpusmasterclass0.Rmd\`. 2026 placeholder; demo content likely merges into \`day-1/D1-PM-wordcloud-hclust.ipynb\` for Brian's code-along.")`
22. **Cell 30** → `replace_cell(slide_type=slide, "spaCy needs pre-trained language models. The small English and German models ship in \`environment.yml\`.")`
23. **Cell 26** → `replace_cell(slide_type=slide, "The course uses the libraries below. An \`ImportError\` means the conda environment is incomplete.")`
24. **Cell 22** → `replace_cell(slide_type=slide, "## Installing the Python environment:\n\n- **Miniconda** (or Anaconda): https://docs.conda.io/en/latest/miniconda.html\n- **Jupyter**: bundled with Miniconda.\n- **This course's env**: download the release zip, then in the unpacked folder run \`conda env create -f environment.yml\` and \`conda activate corpusanalysis\`\n- **For locked-down machines**: open the notebooks in Google Colab.\n- **For Linux**: talk to Brian\n\n*Always look on the bright side of code.*")`
25. **Cell 20** → alt-text rewrite
26. **Cell 19** → alt-text rewrite
27. **Cell 18** → second-image alt-text rewrite (first image alt text already clean)
28. **Cell 17** → alt-text rewrite
29. **Cell 16** → alt-text rewrite
30. **Cell 15** → alt-text rewrite
31. **Cell 14** → alt-text rewrite
32. **Cell 12** → `replace_cell` restoring Mark's structure (full body below):
    ```
    - **Google** your error messages! You're almost certainly not the first person to run into this problem.
    - Maybe the problem is that the **working directory** isn't set correctly, or you just need to **update** your Python or conda packages – or just **restart** Jupyter.
    - **Stack Overflow** is your friend, but only post there if you can give them a **minimal, reproducible example**; otherwise they will be **very very mean** to you.
    - Perhaps most importantly, most code is **not always built from scratch but copy-pasted, then tailored to purpose**.
    ```
33. **Cell 8** → `replace_cell(slide_type=notes, "**Note:** The 2025 link was \`tinyurl.com/yc4awanh\`. For 2026, replace the placeholder above with the GitHub Releases asset URL once \`v2026\` is tagged. Regenerate the QR code from the new URL. Students download a zip from the release page.")`
34. **Cell 7** → `replace_cell(slide_type=slide, "## Files (code, corpora, etc.) available here:\n\n**https://github.com/DH-Oz/CorpusAnalysis/releases**")` (drop the parenthetical)
35. **Cell 6** → `replace_cell(slide_type=slide, "## Sticky Note protocol\n\n- **Green** sticky note on your laptop: *\"I'm done and my code has run successfully.\"*\n- **No** sticky note: *\"Currently working on it!\"*\n- **Red** sticky note: *\"I'd like some help\"* – the person not speaking will head over to help you")` (em-dash → en-dash to match Mark)
36. **Cell 4** → `replace_cell(slide_type=notes, "**Note:** 2025 slide says \"R installation\" (D1 AM) and \"quanteda\" (D2 PM / D3 AM). 2026 wording: \"Python install verification\" and the tool-agnostic \"document-feature matrices\" / \"more corpus work\". Python library stack is \`nltk\` + \`scikit-learn\` + \`scipy\` + \`numpy\` + \`pandas\` + \`matplotlib\` + \`wordcloud\` + \`networkx\` + \`spacy\` (with \`en_core_web_sm\` and \`de_core_news_sm\` models). f-strings are the only taught idiom; list comprehensions and type hints never appear.")`
37. **Cell 3** → `replace_cell(slide_type=slide, ...)` restoring 2025 Day 4 AM bullet pattern (full body below):
    ```
    ## Agenda

    - **Day 1 AM (Mark):** introductions, examples of what's to come, Python install verification
    - **Day 1 PM (Brian):** follow-along typing; your first word cloud and hierarchical clustering
    - **Day 2 AM (Brian):** demos of various corpus analyses we've done
    - **Day 2 PM (Mark):** (re)introduction to document-feature matrices; matrices and their multiplication; collocation networks
    - **Day 3 AM (Mark):** more corpus work and LIWC, this time in German!
    - **Day 3 PM (Brian):** follow-along typing; building your own custom dictionary
    - **Day 4 AM (Brian/Mark): Splitting class:** finding and constructing corpora with AI | how to download things other people have built
    - **Day 4 PM (Brian/Mark):** brainstorming, planning collaborations, goodbyes
    ```
38. **Cell 0** → `replace_cell(slide_type=slide, "# Corpus Analysis Masterclass\n\n![Cover image for the Corpus Analysis Masterclass.](img/p1-cover.png)\n\n### Mark Alfano & Brian Ballsun-Stanton, Macquarie University")`

After all edits land, the Stop hook will auto-render the slides PDF. Walk every page per the rubric.
