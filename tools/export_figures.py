"""Regenerate the lecture figures from the code-along notebooks.

The notebooks are the single source: each figure is drawn by notebook code and
already seeded for reproducibility (wordcloud random_state, spring_layout seed,
LDA random_state). This tool executes each notebook with a real kernel and
harvests the PNG images its cells display, writing them to figures/ as
`<notebook-stem>-NN.png`.

figures/ is committed, so the change report after a regeneration is just:

    uv run python tools/export_figures.py
    git diff --stat figures/

The PNGs that changed are the slides whose images need re-pasting into Google
Slides. No bespoke diff tool — git is the diff.

Usage:
    uv run python tools/export_figures.py            # all code-along notebooks
    uv run python tools/export_figures.py 3a-collocations-dispersion.ipynb
"""

from __future__ import annotations

import argparse
import base64
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The five code-along notebooks at the repo root. Lecture figures come from
# these analyses; the day-N decks are conceptual and live in Google Slides.
DEFAULT_NOTEBOOKS = [
    "1a-sotu-corpus.ipynb",
    "1b-sotu-by-speech.ipynb",
    "2-dictionary-content.ipynb",
    "3a-collocations-dispersion.ipynb",
    "3b-nietzsche-german-paragraphs.ipynb",
]


def extract_pngs(notebook) -> list[bytes]:
    """Return the decoded PNG image of every code cell's output, in order.

    One cell can emit several images (the decade-network loop draws nine), so
    every image/png output is harvested, not just the first per cell.
    """
    pngs: list[bytes] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            png_b64 = output.get("data", {}).get("image/png")
            if png_b64 is None:
                continue
            pngs.append(base64.b64decode(png_b64))
    return pngs


def write_figures(pngs: list[bytes], out_dir: Path, stem: str) -> list[Path]:
    """Write PNGs to out_dir as `<stem>-NN.png`, returning the paths written."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, png in enumerate(pngs):
        path = out_dir / f"{stem}-{index:02d}.png"
        path.write_bytes(png)
        written.append(path)
    return written


def execute_notebook(path: str):
    """Run a notebook with a real kernel and return the executed notebook.

    The kernel's working directory is the notebook's folder, so relative paths
    in the lessons (corpus_tools, dictionaries/) resolve as they do in Jupyter.
    """
    import nbformat
    from nbclient import NotebookClient

    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=900,
        kernel_name="python3",
        resources={"metadata": {"path": str(Path(path).resolve().parent)}},
    )
    client.execute()
    return notebook


def export_one(path: str, out_dir: Path, execute=execute_notebook) -> list[Path]:
    """Execute one notebook and (re)write its figures, clearing any stale ones."""
    out_dir = Path(out_dir)
    stem = Path(path).stem
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.glob(f"{stem}-*.png"):
        stale.unlink()
    pngs = extract_pngs(execute(path))
    return write_figures(pngs, out_dir, stem)


def export_all(paths: list[str], out_dir: Path, execute=execute_notebook) -> dict[str, list[Path]]:
    """Export figures for several notebooks. Returns {notebook: [figure paths]}."""
    result: dict[str, list[Path]] = {}
    for path in paths:
        result[path] = export_one(path, out_dir, execute=execute)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate lecture figures from the code-along notebooks.")
    parser.add_argument("notebooks", nargs="*", default=DEFAULT_NOTEBOOKS, help="Notebook paths (default: the four code-along notebooks).")
    parser.add_argument("--out", default=str(REPO_ROOT / "figures"), help="Output directory (default: figures/).")
    args = parser.parse_args()

    out_dir = Path(args.out)
    notebooks = args.notebooks or DEFAULT_NOTEBOOKS
    for path in notebooks:
        print(f"Executing {path} ...")
        written = export_one(path, out_dir)
        print(f"  wrote {len(written)} figures")
    print(f"\nDone. Review changes with:  git diff --stat {out_dir.name}/")


if __name__ == "__main__":
    main()
