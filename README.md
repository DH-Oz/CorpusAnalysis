# Corpus Analysis Masterclass — code-along notebooks (review copy)

The four hands-on "type-along" notebooks for the 2026 Python edition, for review.
Each is the audited, working version of the analysis.

1. `1-sotu-first-look.ipynb` — State of the Union corpus: word cloud, hierarchical
   clustering, topic models (LDA), comparison clouds.
2. `2-dictionary-content.ipynb` — content-analysis dictionaries: per-document
   category percentages on the open MAC dictionary, plus an instructor-only LIWC
   section (needs a licensed `liwcdict.dic` — see the note in the notebook).
3. `3a-collocations-dispersion.ipynb` — collocation networks, lexical dispersion,
   keyness.
4. `3b-nietzsche-german-paragraphs.ipynb` — German dictionary analysis, concept
   networks, keyness, moral scatters.

## Reading and running

Open any notebook on GitHub to read it with its saved outputs. To run them, open
in Jupyter from this folder: `corpus_tools.py` and the data sit beside them, and
`sotu` installs from PyPI. The open dictionaries (macdvirtue, nietzsche, nuke) and
the Nietzsche corpus are included; the commercial `liwcdict.dic` is not.
