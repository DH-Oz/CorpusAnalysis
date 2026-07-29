# 4. `corpus_tools.py` ships as a local file, not a package and not an R bridge

Date: 2026-05-31 (decided), 2026-07-29 (recorded)
Status: Accepted

## Context

The 2025 course used quanteda's `liwcalike()` in R, which returns per-document
dictionary category percentages. The Python port needed the same behaviour, and
three ways to get it were considered in the same exchange:

- call the real thing through **rpy2**, bridging to R and quanteda;
- **publish a package to PyPI**, as had already been done for `sotu`;
- **ship a plain `.py` file** alongside the notebooks.

The goal was never to reinvent LIWC: "The goal here is to use all the liwc tools,
not to reinvent from scratch." The `liwc` package does the dictionary matching, and
what was missing was only the percentage normalisation quanteda wrapped around it.

## Decision

**A local file, `corpus_tools.py`, distributed beside the notebooks.**

Brian raised and settled it in one turn: *"shipped module, yes. and full. Or do we
just pypi it properly like we did sotc? Or do we intorduce rpy2?"*, then *"let's
just have it be a shipped module so we can discuss what that implies."*

The reason given at the time was pedagogical. A file the student can see next to the
notebook is what makes `import` teachable: *"we can just provide scripts or locally
written packages to make the beahviour the same. Allows us to discuss what import
does?"*

Notebook 2 still carries that beat, at cells 2 to 4: *"`import` takes a name from
another file and makes it usable here"*, then *"`corpus_tools.py` is ours, and sits
in the same folder as this notebook."*

## A note on the recorded rationale

A fuller justification for rejecting rpy2 and PyPI exists in the transcripts — rpy2
needing a local R and quanteda install and so breaking the locked-down-machine and
Colab backstops, PyPI being premature packaging for one function. **That text was
written by a previous Claude session and pasted back in as a resume prompt.** It is
not Brian's wording and was not verified against him, so it is recorded here as a
plausible reconstruction rather than as the decision's stated grounds.

What is confirmed from Brian's own words is the decision itself, the two rejected
alternatives, and the `import`-teaching reason.

The reconstructed reasons are consistent with constraints recorded elsewhere: Colab
is the documented backstop and about half the room is on restricted machines, both
of which an rpy2 dependency would break.

## Consequences

`corpus_tools.py` travels in the release bundle (ADR 3) and must be uploaded
alongside the notebooks on Colab, which `README.md` tells students to do.

It has grown well past `liwcalike` — it now holds `load_token_parser`,
`comparison_cloud`, `distinctive_terms`, `cooccurrence_graph`,
`draw_cooccurrence_network`, `dispersion_plot`, `linear_band` and `loess_band`.
What belongs in it rather than inline in a notebook is a cognitive-load judgement
about the code-along, not a line-count rule; see
`.notes/feedback_notebooks-serve-the-instructor-and-the-lagging-student.md`.

Revisiting PyPI is reasonable if the file proves reusable across years. That would
cost the `import` beat, which is the thing to weigh.
