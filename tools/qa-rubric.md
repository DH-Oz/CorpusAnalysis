# Per-Session QA Rubric

Invoke against one session at a time, e.g. *"Run the QA rubric against day-1/D1-AM-intro.ipynb"*. This is a checklist Claude executes turn-by-turn, not a script. Every block below has to produce a written finding before the next block runs.

## Pre-flight

1. Identify the 2025-slides PDF that corresponds to the notebook (see `2025-slides/MANIFEST.md`).
2. Read the PDF cover to cover (no skimming, no spot-checks). Page-by-page note each slide's content: heading present or absent, prose present or absent, image-only, code-screenshot, layout, semantic colour, fragment-build structure.
3. Enumerate every markdown cell in the notebook with its index and `slide_type`.
4. Build the cell↔page map: for each markdown cell, which 2025 page (or page range) is the source, or "no 2025 source — Claude-authored bridge".

Stop and report the map before doing any edits.

## Per-cell classification

Mark each markdown cell as one of:

- **Verbatim-2025**: the cell corresponds to a 2025 slide with prose/headings. The 2026 cell text matches that slide's text word-for-word, including em-dashes, lowercase casual titles, ellipses, "shitty sentence" register, fragment builds, and semantic colour cues. Voice rules below do NOT apply to this cell.
- **Image-only-2025**: the cell corresponds to a 2025 slide that was just an image (or just an image + title). The 2026 cell should be image-only or image+title only. No invented markdown heading, no caption, no transition sentence.
- **Code-bridge**: there is no 2025 source slide; the cell exists because a code section needs a bridge that did not exist in R. Voice rules below apply hard. Keep the smallest amount of prose possible.
- **Instructor-note**: `slide_type: notes` cell Claude authored to document a 2025→2026 substitution. Voice rules apply.

A cell that 2025 left image-only and 2026 has labelled with `## Some Heading — Some Subtitle` is by definition wrong. The right action is to drop the heading cell, not to rewrite it.

## Voice checks (only for Code-bridge and Instructor-note cells)

The diseased patterns below are sentence structures. The character used to hinge a structure is incidental. Mechanical replacements do not fix structures. Swapping `—` for `;` or `:` or parens leaves the cram intact. A proposed remedy must be a sentence-level rewrite. If a proposed remedy reads identically to the original except for a punctuation character, it is wrong and gets re-done.

For each Claude-authored cell, check and report.

### Parenthetical-aside cram

Reject if the sentence has shape *"Statement A. Plus extra fact B about A. Crammed into one breath."* The hinge can be `—`, `;`, `:`, or `(`. Mark's 2025 verbatim cells are exempt.

Fix: split into two declarative sentences. Or drop the aside. The reader usually already gets it. Or restructure so the second clause is the main one.

### Triplets

Reject three-clause patterns separated by periods, semicolons, or commas-and-conjunction. Example: *"X, Y, and Z; A, B, and C"*.

Fix: pick the most important pair. Or restructure as a list. Or drop the enumeration.

### Meta-conclusion

Reject sentences describing other slides. Examples: *"The next slide is..."*, *"The slide after that..."*, *"In what follows..."*.

Fix: delete the sentence.

### Telling-about

Reject sentences describing what the student does or has built. Mark's own *"Google your error messages!"* is fine. Mark wrote it. Claude inventing *"We now import..."* is not fine.

Fix: be the slide. Say the thing, not what the student does about the thing.

### Staccato fragments

Reject period-separated short fragments. Example: *"Twenty-seven-page report. No methods. Billion-pound deals."*

Fix: rejoin into one complete sentence with commas.

### Unintroduced acronyms

Reject any acronym appearing before it is spelled out. Examples: `RAG`, `LDA`, `NLP`, `ML`, `LLM`. Check the 2025 source. Mark spelled out "Latent Dirichlet Allocation" as a slide title. The 2026 cell should match.

Fix: spell out on first use.

### Term-quoting

Reject any technical term defined inline without the phrase being quoted and the attribution being visible.

Fix: quote the phrase. Show the source on the slide.

### Trap-vs-real-fix worked example

- Trap (Claude original): *"We use the small English and German models for this course — both are pulled in by environment.yml."*
- Fake fix, mechanical char swap: *"We use the small English and German models for this course; both are pulled in by environment.yml."* Same diseased structure. Do not propose this.
- Fake fix, mechanical paren wrap: *"We use the small English and German models for this course (both are pulled in by environment.yml)."* Same diseased structure. Do not propose this.
- Real fix, drop the aside: *"The small English and German spaCy models ship in environment.yml."*
- Real fix, split into two: *"We use spaCy's small English and German models. Both are already in environment.yml."*

Cross-reference the calibration: `/home/brian/people/Brian/INTS1301/CLAUDE.md` § *Bullet Voice*. Note (in `.notes/`): `voice-when-authoring-new-prose`.

## Layout checks (every markdown cell, regardless of source)

| Check | Reject if |
|---|---|
| Inline style | `style="..."` attribute on any HTML tag |
| Inline sizing | `width=` or `height=` attribute on any HTML tag |
| Inline CSS | `<style>` block inside a cell |
| Ad-hoc class | Class name used in a cell that is not defined in `tools/slides.css` |

Reusable layouts (side-by-side image pairs, image grids, two-column bodies) use named classes from `tools/slides.css`. Note (in `.notes/`): `class-based-layout-patterns`.

## Structural checks (whole notebook)

- 2025 slide sequence preserved: every 2025 slide has a corresponding 2026 cell or cell-group, in order, no inserted "framing" cells between Mark's beats.
- §4-style image-then-code beats use live Python outputs as the slide visual, not 2025 R reference PNGs. Note (in `.notes/`): `demo-slides-show-live-output`.
- Code cells silently obey PEP 8; no formatting rules taught as a beat. Note (in `.notes/`): `silent-pep8-formatting`.
- Code cells use only idioms already explicitly taught. No comprehensions / type hints / `with` blocks unless earned. Note (in `.notes/`): `no-unearned-python-idioms`.
- Code-explainer markdown cells (the literate prose between code beats) are ≤ 240 chars. General slideshow markdown is unbounded. Note (in `.notes/`): `literate-markdown-cells`.

## Render check

1. Run `uv run python tools/render_stale.py` (or `tools/render_slides.py` for a single notebook). The Stop hook also fires this automatically; either is fine.
2. Open the resulting `.slides.pdf` and walk every page (not a spot-check).
3. Verify on each page: text fits, images render, fragment builds don't overflow, sub-slide stacks navigate sanely, live Python output is present on image-then-code beats.
4. If a slide looks empty in HTML but fine in PDF, check the click-to-reveal input-hide rule (see CLAUDE.md § *Click-to-reveal + lightbox*).

The session is not "done" until step 3 passes for every page.

## Output

Produce a single findings file per session, e.g. `day-1/D1-AM-intro.qa.md`, listing:

- Cell-page map (table)
- Per-cell classification (table)
- Voice-rule findings (one row per violation, with the offending text quoted)
- Layout findings
- Structural findings
- Render-walk notes (any page that didn't pass)

Edits are proposed in the findings file, then applied via `tools/notebook_cells.py` (`replace_cell`, `delete_cell`), then the render check re-runs.

## How to invoke

Type: *"Run tools/qa-rubric.md against day-N/<notebook>.ipynb"*

Claude reads this file, the corresponding 2025-slides PDF, and the notebook, and produces the findings file. No edits until findings are agreed.
