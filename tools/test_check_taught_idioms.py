"""Tests for tools/check_taught_idioms.py.

Run via: `uv run pytest tools/test_check_taught_idioms.py -q`

The thing worth testing is that the check reads the course as one sequence rather
than one notebook at a time, because that is the whole reason it can tell "explained
in notebook 1, used in 3a" apart from "never explained". The expectations here are
written from the rule, not read back from the checker.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from tools.check_taught_idioms import SPEC_KINDS, first_use_and_gloss, scan

USE = r"\.iloc\["
GLOSS = r"`?\.?iloc"


def write(path: Path, cells) -> Path:
    nb = new_notebook()
    nb.cells = cells
    nbformat.write(nb, path)
    return path


@pytest.fixture
def lesson(tmp_path: Path):
    def build(*specs):
        paths = []
        for number, cells in enumerate(specs):
            paths.append(write(tmp_path / f"{number}-lesson.ipynb", cells))
        return paths
    return build


def test_gloss_before_use_passes(lesson):
    paths = lesson([
        new_markdown_cell("`df.iloc[0]` takes a row by its position."),
        new_code_cell("first = df.iloc[0]"),
    ])
    use, gloss = first_use_and_gloss(scan(paths), USE, GLOSS)
    assert use is not None and gloss is not None
    assert gloss[0] < use[0]


def test_use_with_no_gloss_anywhere_is_caught(lesson):
    paths = lesson([new_code_cell("first = df.iloc[0]")])
    use, gloss = first_use_and_gloss(scan(paths), USE, GLOSS)
    assert use is not None
    assert gloss is None


def test_gloss_arriving_after_the_use_is_caught(lesson):
    paths = lesson([
        new_code_cell("first = df.iloc[0]"),
        new_markdown_cell("`df.iloc[0]` takes a row by its position."),
    ])
    use, gloss = first_use_and_gloss(scan(paths), USE, GLOSS)
    assert gloss[0] > use[0]


def test_a_gloss_in_an_earlier_notebook_covers_a_later_use(lesson):
    """The reason the check walks the course rather than each file separately."""
    paths = lesson(
        [new_markdown_cell("`df.iloc[0]` takes a row by its position.")],
        [new_code_cell("first = df.iloc[0]")],
    )
    use, gloss = first_use_and_gloss(scan(paths), USE, GLOSS)
    assert gloss[0] < use[0]
    assert Path(gloss[1]).name == "0-lesson.ipynb"
    assert Path(use[1]).name == "1-lesson.ipynb"


def test_an_explanation_in_a_code_comment_does_not_count(lesson):
    """A comment sits in the same monospace as the code, which is what gets skipped."""
    paths = lesson([new_code_cell("# .iloc takes a row by position\nfirst = df.iloc[0]")])
    use, gloss = first_use_and_gloss(scan(paths), USE, GLOSS)
    assert use is not None
    assert gloss is None


def test_a_gloss_for_one_spec_kind_does_not_satisfy_another(lesson):
    """`:,` teaches thousands; it says nothing about decimal places."""
    in_code, in_gloss = SPEC_KINDS["fixed decimal places"]
    paths = lesson([
        new_markdown_cell("Putting `:,` after the colon groups thousands."),
        new_code_cell("print(f'{value:.1f}')"),
    ])
    use, gloss = first_use_and_gloss(scan(paths), in_code, r"`[^`]*" + in_gloss + r"[^`]*`")
    assert use is not None
    assert gloss is None


def test_a_gloss_showing_the_same_spec_kind_does_satisfy_it(lesson):
    in_code, in_gloss = SPEC_KINDS["fixed decimal places"]
    paths = lesson([
        new_markdown_cell("`:.1f` prints one digit after the decimal point."),
        new_code_cell("print(f'{value:.3f}')"),
    ])
    use, gloss = first_use_and_gloss(scan(paths), in_code, r"`[^`]*" + in_gloss + r"[^`]*`")
    assert gloss[0] < use[0]
