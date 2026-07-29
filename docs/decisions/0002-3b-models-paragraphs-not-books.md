# 2. 3b's topic model runs on paragraphs, and the book-level failure is the lesson

Date: 2026-07-29
Status: Accepted

## Context

3b ran Latent Dirichlet Allocation over the fifteen Nietzsche books at eight topics
and stopped there, with no document-mass column. Three topics carried zero weight
and repeated the same ten rare words, and those were presented as findings about
Nietzsche.

The obvious repair was the one notebook 1a already teaches: read the mass, then ask
for fewer topics. Measured on 3b's own matrix, that does not work here.

| topics | topics with zero mass | worst shared words between two topics |
|---|---|---|
| 2 | 0 | 7 of 10 |
| 3 | 0 | 6 of 10 |
| 4 | 1 | 6 of 10 |
| 5 | 1 | 4 of 10 |
| 6 | 2 | 7 of 10 |
| 8 | 3 | 10 of 10, three identical topics |

**Every setting from two to eight fails one test or the other.** Trimming rare words
with `min_df=3` makes it worse, not better. The reason is the documents: each is a
whole book, and *leben, macht, mensch, menschen, welt, giebt* and *selber* run
through all of them, so every topic drawn from a whole book gets a share of the same
vocabulary.

The notebook already argues this case against itself. It reshapes to paragraphs
further down precisely because books are too coarse for co-occurrence, then ran its
topic model on books six cells earlier.

The 7,265 paragraphs behave differently. No topic carries zero weight at any count
from four to eight, the smallest holds about a sixth of the corpus at five topics,
and the topics separate into things a reader recognises: Zarathustra's narration
(*sprach, sagte, kam*), its lyric passages (*oh, seele, ach, wahrlich*), the art and
music vocabulary (*kunst, musik*), and the moral vocabulary. The fit takes about
twelve seconds.

## Decision

**3b carries two topic models, and the first one is meant to fail.**

It runs eight topics on the books, where three come back with zero mass and
identical word lists, which is the failure notebook 1a diagnoses in the speeches. It
then runs three, where the dead topics go but topics 1 and 3 still share six of
their ten words. It concludes that the setting is not what is wrong, and runs the
real model after the paragraph reshape.

## Consequences

The book-level model looks redundant to anyone who has not measured it, and
"simplifying" it away would delete the lesson and leave a topic model that does not
work. `.notes/project_3b-book-topic-model-is-deliberate.md` carries the reproduction
command for a future session that is tempted.

`top_topics` takes the matrix and its feature names as arguments so the one helper
serves both models.

The prose must not claim the paragraph topics are distinct. Topics 4 and 5 share
five of ten words, and *menschen* appears in all five, because Nietzsche does write
about people everywhere. The notebook says so rather than hiding it. Three separate
drafts of this beat claimed a distinctness the output contradicted; see
`.notes/feedback_prose-must-match-the-executed-output.md`.

Notebook 1's own topic-model lesson stands, and 3b's prose points at it. Its claim
that at five topics "the duplicates are gone" was checked and holds in the sense it
means: the identical zero-mass pair at eight topics is genuinely gone, and all five
carry real weight.
