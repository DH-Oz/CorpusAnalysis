"""Append, insert, and replace cells in a Jupyter notebook with slideshow metadata.

Designed for scaffolding lesson notebooks where every cell carries a
`slideshow.slide_type` (slide / subslide / fragment / notes / skip). Uses
nbformat so cell IDs, format version, and on-disk shape stay canonical.

Usage:
    from tools.notebook_cells import append_cells

    append_cells("day-1/D1-AM-intro.ipynb", [
        ("slide",    "## Title\\n\\n![alt](img/p16-i0.png)\\n\\nFraming sentence."),
        ("subslide", "## Continued\\n\\n![alt](img/p17-i0.png)\\n\\nMore framing."),
    ])

Each cell can be a `(slide_type, source)` tuple (markdown by default) or a dict
for finer control:

    {"slide_type": "slide", "source": "x = 1\\nprint(x)", "cell_type": "code"}
    {"slide_type": "notes", "source": "INSTRUCTOR NOTE — …"}
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell

VALID_SLIDE_TYPES = frozenset({"slide", "subslide", "fragment", "notes", "skip"})
VALID_CELL_TYPES = frozenset({"markdown", "code"})

# Sentinel for "no slide_type" — the cell continues the current slide
# vertically and has no `slideshow.slide_type` metadata at all. Pass
# slide_type=None in the dict form, or use the tuple (None, source).
CONTINUE = None

CellSpec = Union[tuple[str | None, str], dict]


def _normalise(spec: CellSpec) -> dict:
    if isinstance(spec, tuple):
        if len(spec) != 2:
            raise ValueError(f"tuple cell spec must be (slide_type, source); got {spec!r}")
        slide_type, source = spec
        return {"slide_type": slide_type, "source": source, "cell_type": "markdown"}
    if not isinstance(spec, dict):
        raise TypeError(f"cell spec must be tuple or dict; got {type(spec).__name__}")
    out = {"cell_type": "markdown", **spec}
    out.setdefault("slide_type", CONTINUE)
    return out


def _build_cell(spec: dict):
    slide_type = spec.get("slide_type", CONTINUE)
    if slide_type is not CONTINUE and slide_type not in VALID_SLIDE_TYPES:
        raise ValueError(
            f"invalid slide_type {slide_type!r}; expected None or one of {sorted(VALID_SLIDE_TYPES)}"
        )
    cell_type = spec.get("cell_type", "markdown")
    if cell_type not in VALID_CELL_TYPES:
        raise ValueError(
            f"invalid cell_type {cell_type!r}; expected one of {sorted(VALID_CELL_TYPES)}"
        )
    if "source" not in spec:
        raise ValueError("cell spec missing required 'source'")
    metadata: dict = {} if slide_type is CONTINUE else {"slideshow": {"slide_type": slide_type}}
    factory = new_markdown_cell if cell_type == "markdown" else new_code_cell
    return factory(source=spec["source"], metadata=metadata)


def _load(path: Path):
    nb = nbformat.read(path, as_version=4)
    nbformat.validator.normalize(nb)
    return nb


def _save(nb, path: Path) -> None:
    nbformat.validator.normalize(nb)
    nbformat.validate(nb)
    nbformat.write(nb, path)


def append_cells(notebook_path: str | Path, cells: list[CellSpec]) -> int:
    """Append cells to the end of a notebook on disk.

    Returns the new total cell count.
    """
    path = Path(notebook_path)
    nb = _load(path)
    for spec in cells:
        nb.cells.append(_build_cell(_normalise(spec)))
    _save(nb, path)
    return len(nb.cells)


def insert_cells(notebook_path: str | Path, index: int, cells: list[CellSpec]) -> int:
    """Insert cells starting at the given index, preserving order.

    `index` follows list semantics: 0 = before first cell, len(cells) = end.
    Returns the new total cell count.
    """
    path = Path(notebook_path)
    nb = _load(path)
    if not 0 <= index <= len(nb.cells):
        raise IndexError(f"index {index} out of range for notebook with {len(nb.cells)} cells")
    for offset, spec in enumerate(cells):
        nb.cells.insert(index + offset, _build_cell(_normalise(spec)))
    _save(nb, path)
    return len(nb.cells)


def replace_cell(notebook_path: str | Path, index: int, cell: CellSpec) -> None:
    """Replace the cell at `index` with a new one."""
    path = Path(notebook_path)
    nb = _load(path)
    if not 0 <= index < len(nb.cells):
        raise IndexError(f"index {index} out of range for notebook with {len(nb.cells)} cells")
    nb.cells[index] = _build_cell(_normalise(cell))
    _save(nb, path)


def delete_cells(notebook_path: str | Path, start: int, stop: int | None = None) -> int:
    """Delete cells in the half-open range [start, stop). Returns new total count.

    If `stop` is None, deletes only the cell at `start`.
    """
    path = Path(notebook_path)
    nb = _load(path)
    end = start + 1 if stop is None else stop
    if not 0 <= start < end <= len(nb.cells):
        raise IndexError(
            f"range [{start}, {end}) out of bounds for notebook with {len(nb.cells)} cells"
        )
    del nb.cells[start:end]
    _save(nb, path)
    return len(nb.cells)
