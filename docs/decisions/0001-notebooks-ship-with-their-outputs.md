# 1. Notebooks ship with their outputs, as answer keys

Date: 2026-07-29
Status: Accepted

## Context

The committed notebooks had drifted into a state that was neither one thing nor the
other. Counted directly: `0-setup-check` had 4 of 5 code cells executed,
`1-sotu-first-look` 33 of 36, `2-dictionary-content` 3 of 20, `3a` 2 of 23, and `3b`
8 of 33. All five still opened, still rendered, and still looked finished.

The cause was `tools/notebook_cells.py`, which builds a fresh cell whenever it
replaces one. A fresh cell has no outputs, so every cell edited during a session
silently lost its result. Nothing checked, so nothing said.

That forced a decision that had never actually been taken: should the shipped
notebooks carry results at all?

Both answers are defensible. Empty notebooks suit a code-along, because a learner
runs a cell and watches the result appear, which does not happen when the result is
already sitting there, and nothing can go stale. Full outputs let an instructor read
a lesson without running it, and let a reviewer check prose against results. The
mixed state we had was the one option that was certainly wrong.

A second question sat underneath it: what does a learner type into? The Carpentries
model is that they start from nothing.

## Decision

**The notebooks store the outputs of one clean top-to-bottom run, and ship that way.
They are the answer keys.**

Learners are told to make their own notebook (File, New, saved under the lesson's
name) and type along into that. The shipped copy is what lets someone catch up after
falling behind, or stop typing altogether and still follow the session.

There is therefore **no stripped student copy and no build step producing one**. A
`tools/strip_outputs.py` was written on the assumption that students received a
blanked version of these files, and deleted once that proved wrong.

**Notebook 2 is executed with `dictionaries/liwcdict.dic` unpacked**, so its stored
outputs include the six LIWC emotion plots and the Affect/Posemo/Negemo table.
Derived percentages are not the dictionary, and published LIWC work prints exactly
these. The dictionary itself stays gitignored and reaches students only inside
`resources.zip`.

## Consequences

Re-running a notebook after editing it is part of editing it.
`uv run python tools/preflight.py --inplace --all` does that, and
`tools/check_outputs.py` gates it in CI so the drift cannot recur silently.

That check asserts the code cells' execution counts run 1, 2, 3 with no gaps, rather
than asserting each cell has output. A cell that assigns a variable and prints
nothing is perfectly healthy and has no output, so counting outputs would flag the
wrong cells while missing the real fault, which is a notebook edited and never
re-run.

The repository carries the figures inline. Notebook 1 is about 2.75 MB and the five
together about 6.5 MB, which sets the floor for the release zip.

Every number, rank and quoted word in a markdown cell is now a claim sitting
directly above the output that can contradict it, in front of people who cannot tell
which to believe. See `.notes/feedback_prose-must-match-the-executed-output.md`.

Notebook 2's stored output for the extraction cell reads `liwcdict.dic is already in
place`, which is not the branch a student meets first. No single stored output is
correct for every reader of a cell that behaves differently depending on what is on
disk; this was accepted knowingly.

Related: `.notes/feedback_liwc-dictionary-handling.md`, ADR 3 for what reaches
students.
