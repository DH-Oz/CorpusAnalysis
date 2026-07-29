"""Count the figures in a directory of executed notebooks, and insist there are some.

A notebook can exit zero while silently drawing nothing, which is the case this
guards. The subtler case is this checker looking in the wrong place and reporting
zero, which is indistinguishable from the first unless it is ruled out separately.
That happened on the Windows CI leg: Git Bash rewrites /tmp when handing it to
nbconvert, Python's pathlib does not, so the notebooks were written to the Windows
temp directory while the counter looked in D:\\tmp and found nothing.

So an empty or missing directory is a distinct, loudly-named failure rather than a
figure count of zero.

    uv run python tools/check_executed_figures.py executed --min-figures 40
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="Directory holding the executed notebooks.")
    parser.add_argument("--min-figures", type=int, default=40,
                        help="Fail below this many figures in total.")
    parser.add_argument("--expect-notebooks", type=int, default=5,
                        help="Fail unless this many notebooks are present.")
    arguments = parser.parse_args()

    directory = Path(arguments.directory)
    if not directory.is_dir():
        print(f"No such directory: {directory.resolve()}")
        print("This is a broken check, not a broken notebook. Nothing was counted.")
        return 2

    notebooks = sorted(directory.glob("*.ipynb"))
    if len(notebooks) != arguments.expect_notebooks:
        print(f"Found {len(notebooks)} notebooks in {directory.resolve()}, "
              f"expected {arguments.expect_notebooks}.")
        print("This is a broken check, not a broken notebook. Nothing was counted.")
        return 2

    total = 0
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        count = 0
        for cell in notebook["cells"]:
            for output in cell.get("outputs", []):
                if "image/png" in output.get("data", {}):
                    count = count + 1
        print(f"  {path.name}: {count} figures")
        total = total + count

    print(f"{total} figures across {len(notebooks)} notebooks")

    if total < arguments.min_figures:
        print(f"Only {total} figures, expected around 45 with LIWC skipped.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
