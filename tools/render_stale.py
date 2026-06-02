"""Render any day-N notebook whose .slides.pdf is stale (or missing).

Designed as a Claude Code Stop-hook target so QA renders trigger automatically
after notebook edits — no manual command needed. Silent when nothing is stale.

Usage:
    uv run python tools/render_stale.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    notebooks = sorted(project.glob("day-*/*.ipynb"))
    if not notebooks:
        return 0

    render = project / "tools" / "render_slides.py"
    rendered: list[Path] = []
    failed: list[tuple[Path, str]] = []

    for nb in notebooks:
        pdf = nb.with_suffix(".slides.pdf")
        stale = (not pdf.exists()) or (nb.stat().st_mtime > pdf.stat().st_mtime)
        if not stale:
            continue
        result = subprocess.run(
            ["uv", "run", "python", str(render), str(nb)],
            cwd=project,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            rendered.append(pdf)
        else:
            failed.append((nb, result.stderr.strip() or result.stdout.strip()))

    if rendered:
        print("Auto-rendered fresh slide decks (stop-hook):")
        for pdf in rendered:
            size = pdf.stat().st_size
            print(f"  {pdf.relative_to(project)}  ({size:,} bytes)")
        print()
        print(
            "QA reminder — slides are not 'done' until visually inspected. "
            "Read each rendered PDF and check that text, images, and bullet "
            "fragments fit on their slides without overflow."
        )

    if failed:
        print("WARN: render failed for:", file=sys.stderr)
        for nb, err in failed:
            print(f"  {nb.relative_to(project)}: {err[:200]}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
