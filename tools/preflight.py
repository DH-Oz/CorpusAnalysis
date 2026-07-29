"""Run the notebooks you just edited and show what their cells returned.

The Stop hook used to re-render the day-N slide decks, and walking those PDFs was
how anyone actually saw a cell's output. The decks are gone, and replacing that with
static checks alone would have been a downgrade: linting notebook source never
executes a cell, so an edit that silently breaks an output looks identical to one
that works.

So this executes any code-along notebook whose file is newer than its last clean run,
and prints what each cell returned: errors in full, text output per cell, and the
number of figures drawn. A notebook that has not changed is not re-run, which keeps
the usual turn near-instant.

The fast static checks run afterwards, and cost about four seconds together.

Silent when everything passes and nothing changed, because a hook that prints on
every turn stops being read.

    uv run python tools/preflight.py            # what the hook runs
    uv run python tools/preflight.py --all      # re-run every notebook
    uv run python tools/preflight.py --quiet    # errors only, no cell output
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

STAMP = Path(".preflight-stamps.json")

STATIC_CHECKS = [
    ("tests", ["pytest", "-q"]),
    ("requirements match pyproject", ["python", "tools/sync_requirements.py", "--check"]),
    ("one plot type, one library", ["python", "tools/check_plot_libraries.py"]),
    ("explanations in markdown", ["python", "tools/check_markdown_convention.py"]),
]


def load_stamps(root):
    path = root / STAMP
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_stamps(root, stamps):
    (root / STAMP).write_text(json.dumps(stamps, indent=2, sort_keys=True) + "\n",
                              encoding="utf-8")


def stale_notebooks(root, stamps, run_all):
    stale = []
    for path in sorted(root.glob("[0-9]*.ipynb")):
        mtime = path.stat().st_mtime
        if run_all or stamps.get(path.name) != mtime:
            stale.append((path, mtime))
    return stale


def execute(path, workdir):
    result = subprocess.run(
        ["uv", "run", "jupyter", "nbconvert", "--to", "notebook", "--execute",
         str(path), "--output-dir", str(workdir), "--output", path.name],
        cwd=path.parent, capture_output=True, text=True,
    )
    executed = workdir / path.name
    if not executed.exists():
        return None, result
    return json.loads(executed.read_text(encoding="utf-8")), result


def report(notebook, quiet):
    """Print what the cells returned. Returns the number of errors."""
    errors = 0
    figures = 0
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        for output in cell.get("outputs", []):
            kind = output["output_type"]
            if kind == "error":
                errors = errors + 1
                print(f"    cell {index}: {output['ename']}: {output['evalue']}")
                for line in output.get("traceback", [])[-4:]:
                    print(f"      {line}")
            elif kind == "stream" and not quiet:
                text = "".join(output["text"]).rstrip()
                for line in text.splitlines()[:6]:
                    print(f"    cell {index}: {line}")
            elif "data" in output:
                if "image/png" in output["data"]:
                    figures = figures + 1
                elif not quiet and "text/plain" in output["data"]:
                    text = "".join(output["data"]["text/plain"]).rstrip()
                    first = text.splitlines()[0] if text.splitlines() else ""
                    print(f"    cell {index}: {first[:100]}")
    if figures:
        print(f"    {figures} figures drawn")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Re-run every notebook.")
    parser.add_argument("--quiet", action="store_true", help="Errors only.")
    arguments = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    stamps = load_stamps(root)
    stale = stale_notebooks(root, stamps, arguments.all)

    failed = 0

    if stale:
        names = ", ".join(path.name for path, _ in stale)
        print(f"\nRunning {len(stale)} changed notebook(s): {names}")
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            for path, mtime in stale:
                print(f"\n  {path.name}")
                notebook, result = execute(path, workdir)
                if notebook is None:
                    failed = failed + 1
                    print("    did not execute at all:")
                    for line in (result.stdout + result.stderr).splitlines()[-8:]:
                        print(f"      {line}")
                    continue
                errors = report(notebook, arguments.quiet)
                if errors:
                    failed = failed + 1
                else:
                    stamps[path.name] = mtime
        save_stamps(root, stamps)

    static_failures = []
    for label, command in STATIC_CHECKS:
        result = subprocess.run(["uv", "run", *command], cwd=root,
                                capture_output=True, text=True)
        if result.returncode != 0:
            static_failures.append((label, command, result))

    if static_failures:
        print(f"\n{len(static_failures)} static check(s) failed:\n")
        for label, command, result in static_failures:
            print(f"  --- {label} ---")
            print(f"      uv run {' '.join(command)}")
            for line in (result.stdout + result.stderr).rstrip().splitlines()[-12:]:
                print(f"      {line}")
            print()

    if failed or static_failures:
        return 1
    if stale:
        print("\nAll changed notebooks ran clean, and the static checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
