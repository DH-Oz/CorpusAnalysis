"""Guard the markdown-over-comments convention in the code-along notebooks.

The rule, from .notes/feedback_markdown-cells-over-code-comments.md: when a code cell
needs explaining, the explanation goes in a markdown cell above it. A comment block
sits inside the thing it explains, in the same monospace as the code, which is exactly
what an inexperienced reader skips. The denser the block, the more reliably it is
skipped, so the hardest cells end up with the most-ignored explanations.

Short line-local remarks stay as comments. This only flags a preamble, meaning a run
of comment lines at the very top of a code cell, which is the shape that carries a
whole explanation.

    uv run python tools/check_markdown_convention.py
"""

import json
import sys
from pathlib import Path

# A single leading comment is a label, not an explanation, so the threshold is two.
MAX_PREAMBLE_LINES = 1


def preamble_length(source):
    count = 0
    for line in source.splitlines():
        if line.startswith("#"):
            count += 1
        else:
            break
    return count


def main():
    root = Path(__file__).resolve().parent.parent
    notebooks = sorted(root.glob("[0-9]*.ipynb"))
    if not notebooks:
        print("No code-along notebooks found, which is itself wrong.")
        return 1

    offenders = []
    for path in notebooks:
        cells = json.loads(path.read_text())["cells"]
        for index, cell in enumerate(cells):
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            length = preamble_length(source)
            if length > MAX_PREAMBLE_LINES:
                first = source.splitlines()[0][:70]
                offenders.append((path.name, index, length, first))

    for name, index, length, first in offenders:
        print(f"  {name} cell {index}: {length}-line comment preamble | {first}")

    if offenders:
        print(f"\n{len(offenders)} code cell(s) explain themselves in a comment block.")
        print("Move the explanation into a markdown cell above the code. Keep only")
        print("line-local remarks inside the cell.")
        return 1

    print(f"{len(notebooks)} notebooks: every explanation is in a markdown cell.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
