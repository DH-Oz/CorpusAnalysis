"""One plot type, one library.

Brian's rule, 2026-07-29: it is fine that scatters come from seaborn while networks
come from networkx and word clouds from matplotlib. What is not fine is one kind of
plot being drawn two different ways, because then the choice looks arbitrary to a
student and they have to learn both APIs to read the same picture twice.

The course had exactly that: the party-coloured scatter in notebook 1 used seaborn
while four identical scatters elsewhere used matplotlib.

Dispersion marks are deliberately their own type. They are drawn with ax.scatter and
marker='|', but a reader sees a dispersion plot rather than a scatter, and seaborn has
no equivalent. Classifying them as scatters produced three false positives the first
time this ran, so the distinction is load-bearing rather than cosmetic.

    uv run python tools/check_plot_libraries.py
"""

import collections
import json
import re
import sys
from pathlib import Path

# A dispersion mark is a scatter call wearing a bar marker. Checked before scatter.
DISPERSION_MARK = re.compile(r"(?:plt|axes|ax)\.scatter\([^\n]*marker\s*=\s*['\"]\|['\"]")

PATTERNS = [
    ("scatter", "seaborn", re.compile(r"seaborn\.scatterplot\(")),
    ("scatter", "matplotlib", re.compile(r"(?:plt|axes|ax)\.scatter\(")),
    ("bar", "seaborn", re.compile(r"seaborn\.barplot\(")),
    ("bar", "matplotlib", re.compile(r"(?:plt|axes|ax)\.bar\(")),
    ("line", "seaborn", re.compile(r"seaborn\.lineplot\(")),
    ("line", "matplotlib", re.compile(r"(?:plt|axes|ax)\.plot\(")),
    ("histogram", "seaborn", re.compile(r"seaborn\.histplot\(")),
    ("histogram", "matplotlib", re.compile(r"(?:plt|axes|ax)\.hist\(")),
    ("image", "matplotlib", re.compile(r"(?:plt|axes|ax)\.imshow\(")),
    ("dispersion", "matplotlib", re.compile(r"(?:plt|axes|ax)\.hlines\(")),
    ("network", "networkx", re.compile(r"networkx\.draw\(")),
    ("dendrogram", "scipy", re.compile(r"scipy\.cluster\.hierarchy\.dendrogram\(")),
]


def code_of(path):
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        parts = []
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                parts.append("".join(cell["source"]))
        return "\n".join(parts)
    return path.read_text(encoding="utf-8")


def main():
    root = Path(__file__).resolve().parent.parent
    files = sorted(root.glob("[0-9]*.ipynb")) + [root / "corpus_tools.py"]

    drawn_by = collections.defaultdict(lambda: collections.defaultdict(list))
    for path in files:
        text = code_of(path)
        # Dispersion marks first, so they are not counted as scatters.
        marks = DISPERSION_MARK.findall(text)
        if marks:
            drawn_by["dispersion"]["matplotlib"].append(f"{path.name}({len(marks)})")
            text = DISPERSION_MARK.sub("", text)
        for kind, library, pattern in PATTERNS:
            found = pattern.findall(text)
            if found:
                drawn_by[kind][library].append(f"{path.name}({len(found)})")

    split = []
    for kind in sorted(drawn_by):
        libraries = drawn_by[kind]
        summary = " | ".join(
            f"{library}: {', '.join(places)}" for library, places in sorted(libraries.items())
        )
        if len(libraries) > 1:
            split.append(kind)
            print(f"  SPLIT  {kind}: {summary}")
        else:
            print(f"  ok     {kind}: {summary}")

    if split:
        print(f"\n{len(split)} plot type(s) drawn by more than one library: "
              f"{', '.join(split)}.")
        print("Pick one library per plot type. A reader should not have to learn two")
        print("APIs to read the same kind of picture twice.")
        return 1

    print(f"\n{len(drawn_by)} plot types, each drawn by exactly one library.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
