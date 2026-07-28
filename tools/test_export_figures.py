"""Tests for tools.export_figures.

The figure builder executes each code-along notebook and harvests the PNG
images its cells display, so the lecture figures regenerate from the single
source (the notebooks) with no duplicated analysis code. The pure core —
pulling image/png outputs out of an executed notebook in order — is what these
tests pin. Execution itself (a real kernel) is verified by running the tool.

Run via: uv run pytest tools/test_export_figures.py -q
"""

import base64

from tools.export_figures import export_one, extract_pngs, write_figures

# A 1x1 transparent PNG. Used as a stand-in image so the tests stay pure and
# fast: no matplotlib, no kernel.
_PNG_1x1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
    "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


def _notebook(cells):
    return {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}


def _code_cell(outputs):
    return {"cell_type": "code", "source": "plt.show()", "metadata": {}, "outputs": outputs}


def _png_output():
    return {
        "output_type": "display_data",
        "data": {"image/png": base64.b64encode(_PNG_1x1).decode()},
        "metadata": {},
    }


def test_extract_pngs_returns_image_outputs_in_order():
    nb = _notebook(
        [
            {"cell_type": "markdown", "source": "# heading", "metadata": {}},
            _code_cell([_png_output()]),
            _code_cell([{"output_type": "stream", "name": "stdout", "text": "1\n"}]),
            _code_cell([_png_output()]),
        ]
    )

    pngs = extract_pngs(nb)

    assert pngs == [_PNG_1x1, _PNG_1x1]


def test_extract_pngs_handles_multiple_images_in_one_cell():
    # The decade-network loop draws nine graphs in a single cell, so one cell
    # can carry several image outputs. All of them, in order, must be harvested.
    nb = _notebook([_code_cell([_png_output(), _png_output(), _png_output()])])

    pngs = extract_pngs(nb)

    assert pngs == [_PNG_1x1, _PNG_1x1, _PNG_1x1]


def test_extract_pngs_ignores_markdown_and_non_image_outputs():
    nb = _notebook(
        [
            {"cell_type": "markdown", "source": "![](img/p1.png)", "metadata": {}},
            _code_cell([{"output_type": "execute_result", "data": {"text/plain": "42"}, "metadata": {}}]),
        ]
    )

    pngs = extract_pngs(nb)

    assert pngs == []


def test_write_figures_names_files_sequentially(tmp_path):
    written = write_figures([_PNG_1x1, _PNG_1x1], tmp_path, "1-sotu-first-look")

    assert [p.name for p in written] == [
        "1-sotu-first-look-00.png",
        "1-sotu-first-look-01.png",
    ]
    for path in written:
        assert path.read_bytes() == _PNG_1x1


def test_export_one_executes_then_writes_harvested_figures(tmp_path):
    # The kernel run is the external boundary; inject a fake executor so this
    # stays a fast unit test of the harvest-and-write orchestration.
    fake_nb = _notebook([_code_cell([_png_output()]), _code_cell([_png_output()])])

    def fake_execute(path):
        assert path == "3a-collocations-dispersion.ipynb"
        return fake_nb

    written = export_one("3a-collocations-dispersion.ipynb", tmp_path, execute=fake_execute)

    assert [p.name for p in written] == [
        "3a-collocations-dispersion-00.png",
        "3a-collocations-dispersion-01.png",
    ]


def test_export_one_clears_stale_figures_from_a_previous_run(tmp_path):
    # A run that now produces fewer figures must remove the leftovers, so the
    # figures/ directory (and thus the git diff) reflects reality.
    stale = tmp_path / "3a-collocations-dispersion-07.png"
    stale.write_bytes(b"old")

    def fake_execute(path):
        return _notebook([_code_cell([_png_output()])])

    export_one("3a-collocations-dispersion.ipynb", tmp_path, execute=fake_execute)

    assert not stale.exists()
