"""Render a static palette-families reference image for the colour-aside slide.

Pedagogical purpose: the same as R's `brewer.pal()` help page in 2025 — show
students the named-palette UI for picking colours. matplotlib organises its
named colormaps into Sequential / Diverging / Qualitative families that map
1:1 onto ColorBrewer's families, so the same conceptual point lands.

Output: day-1/img/matplotlib-palettes.png — embedded as a slide image in the
§4 colour-aside section.

Usage:
    uv run python tools/render_palettes_reference.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy

OUT_PATH = Path("day-1/img/matplotlib-palettes.png")

FAMILIES = {
    "Sequential": [
        "Blues", "BuGn", "GnBu", "Greens", "Oranges", "PuBu",
        "PuRd", "Purples", "Reds", "YlGn", "YlGnBu", "YlOrBr",
    ],
    "Diverging": [
        "BrBG", "PiYG", "PRGn", "PuOr", "RdBu", "RdGy", "RdYlBu", "RdYlGn", "Spectral",
    ],
    "Qualitative": [
        "Accent", "Dark2", "Paired", "Pastel1", "Pastel2", "Set1", "Set2", "Set3", "tab10", "tab20",
    ],
}


def render_family(ax, family: str, palettes: list[str]) -> None:
    gradient = numpy.linspace(0, 1, 256)
    n = len(palettes)
    canvas = numpy.zeros((n * 10, 256, 4))
    for i, name in enumerate(palettes):
        cmap = matplotlib.colormaps[name]
        canvas[i * 10:(i + 1) * 10] = cmap(gradient)
    ax.imshow(canvas, aspect="auto", interpolation="nearest")
    ax.set_yticks([i * 10 + 5 for i in range(n)])
    ax.set_yticklabels(palettes, fontsize=10, family="monospace")
    ax.set_xticks([])
    ax.set_title(family, loc="left", fontsize=14, fontweight="bold", pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)


def main() -> None:
    max_palettes = max(len(p) for p in FAMILIES.values())
    fig, axes = plt.subplots(
        nrows=1, ncols=len(FAMILIES),
        figsize=(14, 0.42 * max_palettes + 1.2),
        gridspec_kw={"width_ratios": [1, 1, 1]},
    )
    for ax, (family, palettes) in zip(axes, FAMILIES.items()):
        render_family(ax, family, palettes)
    plt.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
