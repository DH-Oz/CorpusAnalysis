"""Smoke tests for tools/notebook_cells.py.

Run via: `uv run pytest tools/test_notebook_cells.py -q`
"""

from __future__ import annotations

from pathlib import Path

import nbformat
import pytest
from nbformat.v4 import new_markdown_cell, new_notebook

from tools.notebook_cells import (
    append_cells,
    delete_cells,
    insert_cells,
    replace_cell,
)


@pytest.fixture
def notebook(tmp_path: Path) -> Path:
    """A 3-cell scratch notebook written to a tmp file, returns its path."""
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# Title", metadata={"slideshow": {"slide_type": "slide"}}),
        new_markdown_cell("body 1", metadata={"slideshow": {"slide_type": "subslide"}}),
        new_markdown_cell("body 2", metadata={"slideshow": {"slide_type": "fragment"}}),
    ]
    path = tmp_path / "scratch.ipynb"
    nbformat.write(nb, path)
    return path


def _slide_types(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    return [c.metadata["slideshow"]["slide_type"] for c in nb.cells]


def _sources(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    return [c.source for c in nb.cells]


def test_append_tuple_form(notebook: Path) -> None:
    total = append_cells(notebook, [("slide", "## New"), ("subslide", "more")])
    assert total == 5
    assert _slide_types(notebook)[-2:] == ["slide", "subslide"]
    assert _sources(notebook)[-2:] == ["## New", "more"]


def test_append_dict_form_with_code_cell(notebook: Path) -> None:
    append_cells(notebook, [{"slide_type": "fragment", "source": "x = 1", "cell_type": "code"}])
    nb = nbformat.read(notebook, as_version=4)
    assert nb.cells[-1].cell_type == "code"
    assert nb.cells[-1].source == "x = 1"
    assert nb.cells[-1].metadata["slideshow"]["slide_type"] == "fragment"


def test_insert_preserves_order(notebook: Path) -> None:
    insert_cells(notebook, index=1, cells=[("notes", "first"), ("notes", "second")])
    assert _sources(notebook)[:4] == ["# Title", "first", "second", "body 1"]


def test_insert_at_end_equals_append(notebook: Path) -> None:
    insert_cells(notebook, index=3, cells=[("slide", "tail")])
    assert _sources(notebook)[-1] == "tail"


def test_replace_cell(notebook: Path) -> None:
    replace_cell(notebook, index=1, cell=("slide", "swapped"))
    assert _sources(notebook)[1] == "swapped"
    assert _slide_types(notebook)[1] == "slide"


def test_delete_single(notebook: Path) -> None:
    remaining = delete_cells(notebook, start=1)
    assert remaining == 2
    assert _sources(notebook) == ["# Title", "body 2"]


def test_delete_range(notebook: Path) -> None:
    remaining = delete_cells(notebook, start=1, stop=3)
    assert remaining == 1
    assert _sources(notebook) == ["# Title"]


def test_invalid_slide_type_raises(notebook: Path) -> None:
    with pytest.raises(ValueError, match="invalid slide_type"):
        append_cells(notebook, [("bogus", "x")])


def test_invalid_cell_type_raises(notebook: Path) -> None:
    with pytest.raises(ValueError, match="invalid cell_type"):
        append_cells(notebook, [{"slide_type": "slide", "source": "x", "cell_type": "raw"}])


def test_missing_source_raises(notebook: Path) -> None:
    with pytest.raises(ValueError, match="missing required 'source'"):
        append_cells(notebook, [{"slide_type": "slide"}])


def test_bad_tuple_length_raises(notebook: Path) -> None:
    with pytest.raises(ValueError, match="tuple cell spec"):
        append_cells(notebook, [("slide", "x", "extra")])  # type: ignore[list-item]


def test_insert_index_out_of_range_raises(notebook: Path) -> None:
    with pytest.raises(IndexError):
        insert_cells(notebook, index=99, cells=[("slide", "x")])


def test_appended_cells_get_ids(notebook: Path) -> None:
    append_cells(notebook, [("slide", "fresh")])
    nb = nbformat.read(notebook, as_version=4)
    assert all(c.get("id") for c in nb.cells), "nbformat should assign IDs to every cell"


def test_continue_via_none_tuple_omits_slideshow_metadata(notebook: Path) -> None:
    append_cells(notebook, [(None, "continuation cell")])
    nb = nbformat.read(notebook, as_version=4)
    last = nb.cells[-1]
    assert "slideshow" not in last.metadata, f"slide_type=None should leave no slideshow metadata; got {last.metadata!r}"
    assert last.source == "continuation cell"


def test_continue_via_dict_without_slide_type(notebook: Path) -> None:
    append_cells(notebook, [{"source": "x = 1", "cell_type": "code"}])
    nb = nbformat.read(notebook, as_version=4)
    last = nb.cells[-1]
    assert last.cell_type == "code"
    assert "slideshow" not in last.metadata


def test_continue_via_explicit_none_in_dict(notebook: Path) -> None:
    append_cells(notebook, [{"slide_type": None, "source": "noop"}])
    nb = nbformat.read(notebook, as_version=4)
    assert "slideshow" not in nb.cells[-1].metadata
