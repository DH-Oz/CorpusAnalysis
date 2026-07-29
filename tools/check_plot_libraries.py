"""One plot type, one library, and the library is declared here.

Brian's rule, 2026-07-29: it is fine that scatters come from seaborn while networks
come from networkx and word clouds from matplotlib. What is not fine is one kind of
plot being drawn two different ways, because then the choice looks arbitrary to a
student and they have to learn two APIs to read the same picture twice.

The first version of this check only flagged a type drawn by *more than one* library.
That made it structurally unable to catch a type with a single instance: notebook 0's
party-count chart was matplotlib's `plt.bar` in a notebook that already imported
seaborn, and the check passed it without comment because `bar` appeared exactly once.
A rule enforced only where it is already broken twice is not enforced.

So the intended library for each plot type is written down below, and any call from
another library fails, whether or not anything disagrees with it.

Two kinds of call are deliberately not plot types. Dispersion marks are `ax.scatter`
with `marker='|'`, and the loess curve is `ax.plot(grid, fitted, ...)`. Both are
drawing primitives inside a helper rather than a plot a student chooses to make, and
seaborn has no equivalent for either. Classifying the first as a scatter produced
three false positives the day this was written.

    uv run python tools/check_plot_libraries.py
"""

import collections
import json
import re
import sys
from pathlib import Path

# What draws what. Change a value here and the notebooks must follow.
POLICY = {
    "scatter": "seaborn",
    "bar": "seaborn",
    "histogram": "seaborn",
    "line": "seaborn",
    "image": "matplotlib",
    "dispersion": "matplotlib",
    "network": "networkx",
    "dendrogram": "scipy",
}

# Primitives inside helpers, excised before anything is classified.
NOT_A_PLOT_TYPE = [
    ("dispersion mark", re.compile(r"(?:plt|axes|ax)\.scatter\([^\n]*marker\s*=\s*['\"]\|['\"]")),
    ("loess curve", re.compile(r"(?:plt|axes|ax)\.plot\(\s*grid,\s*fitted")),
]

CALLS = [
    ("scatter", "seaborn", re.compile(r"seaborn\.scatterplot\(")),
    ("scatter", "matplotlib", re.compile(r"(?:plt|axes|ax)\.scatter\(")),
    ("bar", "seaborn", re.compile(r"seaborn\.(?:barplot|countplot)\(")),
    ("bar", "matplotlib", re.compile(r"(?:plt|axes|ax)\.bar\(")),
    ("histogram", "seaborn", re.compile(r"seaborn\.histplot\(")),
    ("histogram", "matplotlib", re.compile(r"(?:plt|axes|ax)\.hist\(")),
    ("line", "seaborn", re.compile(r"seaborn\.lineplot\(")),
    ("line", "matplotlib", re.compile(r"(?:plt|axes|ax)\.plot\(")),
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
        for label, pattern in NOT_A_PLOT_TYPE:
            hits = pattern.findall(text)
            if hits and label == "dispersion mark":
                drawn_by["dispersion"]["matplotlib"].append(f"{path.name}({len(hits)})")
            text = pattern.sub("", text)
        for kind, library, pattern in CALLS:
            hits = pattern.findall(text)
            if hits:
                drawn_by[kind][library].append(f"{path.name}({len(hits)})")

    problems = []
    for kind in sorted(drawn_by):
        expected = POLICY.get(kind)
        for library in sorted(drawn_by[kind]):
            places = ", ".join(drawn_by[kind][library])
            if expected is None:
                print(f"  ?      {kind} via {library}: {places}   <-- no policy for this type")
                problems.append(f"{kind} has no declared library")
            elif library != expected:
                print(f"  WRONG  {kind} via {library}: {places}   <-- policy says {expected}")
                problems.append(f"{kind} drawn with {library} in {places}, policy is {expected}")
            else:
                print(f"  ok     {kind} via {library}: {places}")

    if problems:
        print(f"\n{len(problems)} plot(s) drawn against policy:\n")
        for problem in problems:
            print(f"  - {problem}")
        print("\nEither change the call or change POLICY in this file, deliberately.")
        return 1

    print(f"\n{len(drawn_by)} plot types, each drawn by its declared library.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
