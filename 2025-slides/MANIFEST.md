# 2025 Slides — split by session

This folder is the canonical hand-off map for the 2026 Python/Jupyter translation. Each file is a per-session subset of `Corpus Analysis Masterclass 2025.pdf` (the 2025 R/Rmd deck, which itself lives in the `DH-Oz/2025-corpus-analysis` archive repo, not this one). The split is by section-divider slides and end-of-session sticky-note slides found in the source deck.

Use these as the reference for translating each session into its 2026 Jupyter notebook. The 2026 notebook filenames match the PDF filenames below (with `.ipynb` instead of `.pdf`).

## Source

- **File**: `Corpus Analysis Masterclass 2025.pdf`
- **Total pages**: 156
- **Status in this repo**: gitignored (lives in `DH-Oz/2025-corpus-analysis` and on instructor laptops only)
- **Split tool**: `pdftk <source> cat <range> output <out>`

## Sessions

| # | File | Source pages | 2025 divider slide | 2026 notebook | Lead |
|---|---|---|---|---|---|
| 1 | `D1-AM-intro.pdf` | 1–45 | (course title; "Day 1 AM: Intro" at p13) | `D1-AM-intro.ipynb` | Mark |
| 2 | `D1-PM-wordcloud-hclust.pdf` | 46–56 | "Day 1 PM: Type-along with Brian" | `D1-PM-wordcloud-hclust.ipynb` | Brian (code-along) |
| 3 | `D2-AM-demos.pdf` | 57–61 | "Day 2 AM: Live demos" | `D2-AM-demos.ipynb` | Brian |
| 4 | `D2-PM-dfm-collocations.pdf` | 62–98 | "Day 2 PM: quanteda" | `D2-PM-dfm-collocations.ipynb` | Mark |
| 5 | `D3-AM-german-liwc.pdf` | 99–145 | "Day 3 AM: lexical dispersion / semantic networks / LIWC in German" | `D3-AM-german-liwc.ipynb` | Mark |
| 6 | `D3-PM-custom-dict.pdf` | 146–148 | "Day 3 PM: building your own custom dictionary" | `D3-PM-custom-dict.ipynb` | Brian (code-along) |
| 7 | `D4-AM-corpus-construction.pdf` | 149–155 | "Day 4 AM: corpus construction" | `D4-AM-corpus-construction.ipynb` | Brian/Mark (split class) |
| 8 | `D4-PM-brainstorming.pdf` | 156 | (no divider — single Puck epilogue page) | `D4-PM-brainstorming.ipynb` | Brian/Mark |

Pages sum to 156; no gaps, no overlaps.

## Notes

- The 2025 Day 2 PM divider says **"quanteda"** (R-only). The 2026 file is named `dfm-collocations` to stay tool-agnostic until the Python library stack is locked. See CLAUDE.md *Open / deferred decisions*.
- Day 3 PM (3 pages) and Day 4 PM (1 page) are intentionally small — these are code-along / brainstorming sessions where most teaching happens off-slide.
- Day 4 PM is the closing Puck epilogue from *A Midsummer Night's Dream* ("If we shadows have offended…"). No teaching content; goodbyes and reflection only.

## Regenerating

If the source PDF changes, re-run from the repo root:

```bash
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 1-45    output 2025-slides/D1-AM-intro.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 46-56   output 2025-slides/D1-PM-wordcloud-hclust.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 57-61   output 2025-slides/D2-AM-demos.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 62-98   output 2025-slides/D2-PM-dfm-collocations.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 99-145  output 2025-slides/D3-AM-german-liwc.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 146-148 output 2025-slides/D3-PM-custom-dict.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 149-155 output 2025-slides/D4-AM-corpus-construction.pdf
pdftk "Corpus Analysis Masterclass 2025.pdf" cat 156     output 2025-slides/D4-PM-brainstorming.pdf
```
