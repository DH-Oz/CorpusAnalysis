"""Sync the canonical corpus_tools.py to a copy beside each day-N notebook.

corpus_tools.py at the repo root is the single source. The notebooks import it
with `from corpus_tools import ...`, which resolves to a copy sitting in the same
folder as the notebook. This script regenerates those copies from the canonical
file, so there is never a second version to maintain by hand.

The day-N copies are gitignored; only the root corpus_tools.py is tracked.

Usage:
    uv run python tools/sync_corpus_tools.py          # write the copies
    uv run python tools/sync_corpus_tools.py --check  # exit 1 if any copy is stale
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL = REPO_ROOT / "corpus_tools.py"


def target_dirs():
    """day-* folders that hold at least one notebook."""
    dirs = []
    for child in sorted(REPO_ROOT.glob("day-*")):
        if child.is_dir() and any(child.glob("*.ipynb")):
            dirs.append(child)
    return dirs


def main(check):
    source = CANONICAL.read_text(encoding="utf-8")
    stale = []
    written = []
    for day_dir in target_dirs():
        copy_path = day_dir / "corpus_tools.py"
        if check:
            current = ""
            if copy_path.exists():
                current = copy_path.read_text(encoding="utf-8")
            if current != source:
                stale.append(copy_path)
        else:
            copy_path.write_text(source, encoding="utf-8")
            written.append(copy_path)

    if check:
        if stale:
            print("Stale or missing corpus_tools.py copies:")
            for path in stale:
                print("  " + str(path.relative_to(REPO_ROOT)))
            print("Fix with: uv run python tools/sync_corpus_tools.py")
            return 1
        print("All corpus_tools.py copies match the canonical.")
        return 0

    for path in written:
        print("wrote " + str(path.relative_to(REPO_ROOT)))
    return 0


if __name__ == "__main__":
    check_mode = "--check" in sys.argv[1:]
    raise SystemExit(main(check_mode))
