"""Shipped notebooks must be the product of one clean top-to-bottom run.

Brian's ruling, 2026-07-29: the notebooks committed here carry their outputs, so
an instructor can read a notebook without running it and a reviewer can check
prose against results. Students receive their own copy and start from a blank
one, which is a separate build step.

The committed state drifted badly before this check existed. Notebook 3a had 2 of
23 code cells executed and 3b had 8 of 33, because `tools/notebook_cells.py`
builds a fresh cell whenever it replaces one and a fresh cell has no outputs. Every
cell edited across a session lost its result, silently, and the notebook still
opened and still looked fine.

The rule enforced here is stricter than "has outputs", deliberately. A cell that
assigns a variable and prints nothing has no output and is perfectly healthy, so
counting outputs would flag the wrong cells and miss the real fault. What actually
distinguishes a clean run is the execution counts: running a notebook top to bottom
in a fresh kernel numbers its code cells 1, 2, 3 and so on with no gaps. A partial
re-run, a cell executed twice, or a cell never executed all break that sequence.

    uv run python tools/check_outputs.py
"""

import json
import sys
from pathlib import Path


def faults(cells):
    """Return the ways this notebook's code cells depart from one clean run."""
    found = []
    expected = 0
    for index, cell in enumerate(cells):
        if cell["cell_type"] != "code":
            continue
        expected = expected + 1
        count = cell.get("execution_count")
        if count is None:
            found.append((index, f"never executed, expected count {expected}"))
        elif count != expected:
            found.append((index, f"execution count {count}, expected {expected}"))
    return found


def main():
    root = Path(__file__).resolve().parent.parent
    notebooks = sorted(root.glob("[0-9]*.ipynb"))
    if not notebooks:
        print("No code-along notebooks found, which is itself wrong.")
        return 1

    total = 0
    for path in notebooks:
        cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
        found = faults(cells)
        code_cells = sum(1 for cell in cells if cell["cell_type"] == "code")
        if not found:
            print(f"  {path.name}: {code_cells} code cells, one clean run")
            continue
        total = total + len(found)
        print(f"  {path.name}: {len(found)} of {code_cells} code cells off-sequence")
        for index, reason in found[:6]:
            print(f"      cell {index}: {reason}")
        if len(found) > 6:
            print(f"      ... and {len(found) - 6} more")

    if total:
        print(f"\n{total} code cell(s) are not part of a clean top-to-bottom run.")
        print("Re-run the notebook and commit the result:")
        print("  uv run python tools/preflight.py --inplace --all")
        return 1

    print(f"\n{len(notebooks)} notebooks: every one is a clean top-to-bottom run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
