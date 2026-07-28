"""Regenerate requirements.txt from the dependency list in pyproject.toml.

pyproject.toml is the single source. requirements.txt is generated from it, and
environment.yml installs from requirements.txt, so one edit in pyproject reaches
both the conda path and the Colab path with nothing kept in step by hand.

requirements.txt holds only the direct dependencies rather than a full resolved
lock, because students read it. `uv export` produces every transitive package
with hashes, which is the right thing for reproducing an environment exactly and
the wrong thing for a file that doubles as teaching material.

Usage:
    uv run python tools/sync_requirements.py          # write requirements.txt
    uv run python tools/sync_requirements.py --check  # exit 1 if it is stale
"""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PYPROJECT = PROJECT / "pyproject.toml"
REQUIREMENTS = PROJECT / "requirements.txt"

HEADER = """\
# Corpus Analysis Masterclass — the dependency list students install.
#
# GENERATED FILE. Do not edit by hand: your change would be overwritten.
# The source is the `dependencies` list in pyproject.toml. Edit there, then run
#     uv run python tools/sync_requirements.py
#
# Install into a fresh Python 3.14 environment (Miniconda supplies only Python):
#     pip install -r requirements.txt
# environment.yml installs from this same file, so there is nothing to keep in sync.
"""


def render() -> str:
    with PYPROJECT.open("rb") as handle:
        data = tomllib.load(handle)
    dependencies = data["project"]["dependencies"]
    lines = [HEADER, ""]
    for dependency in dependencies:
        lines.append(dependency)
    return "\n".join(lines) + "\n"


def main(check: bool) -> int:
    wanted = render()
    current = REQUIREMENTS.read_text() if REQUIREMENTS.exists() else ""
    if current == wanted:
        if check:
            print("requirements.txt matches pyproject.toml")
        return 0
    if check:
        print("requirements.txt is stale against pyproject.toml", file=sys.stderr)
        print("Fix with: uv run python tools/sync_requirements.py", file=sys.stderr)
        return 1
    REQUIREMENTS.write_text(wanted)
    print(f"wrote {REQUIREMENTS.relative_to(PROJECT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main("--check" in sys.argv[1:]))
