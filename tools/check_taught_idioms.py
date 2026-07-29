"""Every Python construct a learner meets must have been explained first.

The rule is `.notes/feedback_no-unearned-python-idioms.md`. It had no mechanical
check, and on 2026-07-29 a cell-by-cell read found it broken in four places at
once: `.iloc` used eight times across three notebooks with no explanation
anywhere, `enumerate` eleven times likewise, f-string format specs throughout with
their only gloss buried in a code comment, and three ternaries in a course that
otherwise writes an explicit `if`.

Two things are checked.

**Glosses.** For each construct, find where the course first uses it, and require a
markdown cell explaining it at or before that point. The notebooks are read in
teaching order, so notebook 1a explaining `.iloc` covers 3a's later use of it. The
gloss has to be markdown, because the same note's sibling rule says an explanation
buried in a code comment is the one a beginner skips.

**Banned constructs.** A few things are not to be used at all, however well
explained, because a plainer form exists and the course uses it everywhere else.

f-string format specs are handled by kind rather than by exact text. A cell
printing `{x:8.1f}` is satisfied by a gloss showing `:10.1f`, since both teach
width-plus-decimals, but not by one showing only `:,`.

    uv run python tools/check_taught_idioms.py
"""

import json
import re
import sys
from pathlib import Path

# Teaching order. A gloss counts if it lands at or before the first use.
COURSE_ORDER = [
    "0-setup-check.ipynb",
    "1a-sotu-corpus.ipynb",
    "1b-sotu-by-speech.ipynb",
    "2-dictionary-content.ipynb",
    "3a-collocations-dispersion.ipynb",
    "3b-nietzsche-german-paragraphs.ipynb",
]

# name -> (pattern in code, pattern that counts as a gloss in markdown)
CONSTRUCTS = {
    ".iloc": (r"\.iloc\[", r"`?\.?iloc"),
    "enumerate": (r"\benumerate\(", r"`?enumerate"),
    "dictionary": (r"^\s*\w+\s*=\s*\{\s*$|^\s*\w+\s*=\s*\{\}", r"dictionar"),
    "while loop": (r"^\s*while\s", r"`?while`? loop|a `while`"),
    "transpose": (r"\.T\s*@", r"transpos"),
    "tuple": (r"startswith\(\(", r"tuple"),
}

# Format specs, by kind: (how it looks in code, how it looks in a gloss).
# The two differ because in code a spec is closed by a brace and in a gloss it is
# quoted bare, as `:,` rather than as `{total:,}`.
SPEC_KINDS = {
    "thousands separator": (r":,(?=[}!])", r":,"),
    "text padded to a width": (r":\d+s", r":\d+s"),
    "whole number padded to a width": (r":\d+d", r":\d+d"),
    "fixed decimal places": (r":\.\d+f", r":\.\d+f"),
    "width and decimals together": (r":\d+\.\d+f", r":\d+\.\d+f"),
}

BANNED = {
    "ternary expression": (
        r"=\s*[^\n=]+\s+if\s+[^\n]+\s+else\s",
        "Write an explicit if. The course does everywhere else.",
    ),
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))["cells"]


def scan(notebooks):
    """Walk the course in order, yielding (position, notebook, index, cell)."""
    position = 0
    for name in notebooks:
        for index, cell in enumerate(load(name)):
            yield position, name, index, cell
            position = position + 1


def first_use_and_gloss(stream, code_pattern, gloss_pattern):
    """Return (first use, first gloss) as (position, notebook, index) or None."""
    use = None
    gloss = None
    for position, name, index, cell in stream:
        body = "".join(cell["source"])
        if cell["cell_type"] == "code" and use is None:
            if re.search(code_pattern, body, re.M):
                use = (position, name, index)
        elif cell["cell_type"] == "markdown" and gloss is None:
            if re.search(gloss_pattern, body, re.I):
                gloss = (position, name, index)
        if use is not None and gloss is not None:
            break
    return use, gloss


def main():
    root = Path(__file__).resolve().parent.parent
    notebooks = [root / name for name in COURSE_ORDER]
    missing = [p.name for p in notebooks if not p.exists()]
    if missing:
        print(f"Notebooks named in COURSE_ORDER are missing: {missing}")
        print("Update COURSE_ORDER, or this check is silently reading less than the course.")
        return 2

    failures = []

    checks = dict(CONSTRUCTS)
    for label, (in_code, in_gloss) in SPEC_KINDS.items():
        # The gloss has to show a spec of the same kind, inside backticks.
        checks[f"f-string spec, {label}"] = (in_code, r"`[^`]*" + in_gloss + r"[^`]*`")

    for label, (code_pattern, gloss_pattern) in checks.items():
        use, gloss = first_use_and_gloss(scan(notebooks), code_pattern, gloss_pattern)
        if use is None:
            continue
        if gloss is None:
            failures.append(
                f"{label}: first used in {Path(use[1]).name} cell {use[2]}, never explained")
        elif gloss[0] > use[0]:
            failures.append(
                f"{label}: used in {Path(use[1]).name} cell {use[2]}, but only explained "
                f"later, in {Path(gloss[1]).name} cell {gloss[2]}")

    for label, (pattern, advice) in BANNED.items():
        for _, name, index, cell in scan(notebooks):
            if cell["cell_type"] != "code":
                continue
            if re.search(pattern, "".join(cell["source"]), re.M):
                failures.append(f"{label} in {Path(name).name} cell {index}. {advice}")

    for line in failures:
        print(f"  {line}")

    if failures:
        print(f"\n{len(failures)} construct(s) a learner meets before anyone explains them.")
        print("See .notes/feedback_no-unearned-python-idioms.md.")
        return 1

    print(f"{len(checks)} constructs checked across {len(notebooks)} notebooks: "
          "each one is explained before it is used.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
