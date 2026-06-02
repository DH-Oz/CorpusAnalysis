"""Render a Jupyter notebook to reveal.js slides (HTML) and a print-PDF for QA.

Usage:
    uv run python tools/render_slides.py NOTEBOOK.ipynb

Produces, next to the notebook:
    NOTEBOOK.slides.html  — nbconvert reveal.js output, with tools/slides.css
                            injected into <head> for project-wide styling.
    NOTEBOOK.slides.pdf   — Chrome-headless print of that HTML in reveal.js
                            print-pdf mode, one slide per page.

The PDF is the file the instructor (or Claude) reads for visual QA. The CSS
file gives us a single place to control image scaling, bullet spacing, and
heading sizes — no inline styles in lesson markdown.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
SLIDES_CSS = TOOLS_DIR / "slides.css"

# Click-to-reveal + lightbox JS, injected before </body>.
#
# - Click an *input* image (in a markdown cell) to toggle `.show-code` on the
#   parent section — this drives the click-to-reveal-code pattern.
# - Click an *output* image (one produced by code execution — inside
#   .jp-OutputArea) to open it in a fullscreen lightbox so dense plots like
#   the 237-leaf dendrogram are actually readable. Click anywhere on the
#   overlay (or press Escape) to dismiss.
# - Print-pdf rendering is unaffected — no events fire during headless print.
CLICK_REVEAL_JS = """
<style>
.lightbox-overlay {
    position: fixed; inset: 0; background: rgba(0, 0, 0, 0.92);
    display: flex; align-items: center; justify-content: center;
    z-index: 99999; cursor: zoom-out;
}
.lightbox-overlay img {
    max-width: 96vw; max-height: 96vh;
    object-fit: contain; background: white;
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.4);
}
.reveal .jp-OutputArea img { cursor: zoom-in; }
</style>
<script>
window.addEventListener("load", function () {
    // (1) Click input-cell images to toggle code visibility on the slide.
    var inputImgs = document.querySelectorAll(
        ".reveal section > .jp-Cell.jp-MarkdownCell img"
    );
    inputImgs.forEach(function (img) {
        img.addEventListener("click", function (event) {
            event.stopPropagation();
            var section = img.closest("section");
            if (section) section.classList.toggle("show-code");
        });
    });

    // (2) Click output images to open a fullscreen lightbox.
    var outputImgs = document.querySelectorAll(".reveal .jp-OutputArea img");
    outputImgs.forEach(function (img) {
        img.addEventListener("click", function (event) {
            event.stopPropagation();
            var overlay = document.createElement("div");
            overlay.className = "lightbox-overlay";
            var big = document.createElement("img");
            big.src = img.src;
            overlay.appendChild(big);
            overlay.addEventListener("click", function () {
                overlay.remove();
            });
            document.body.appendChild(overlay);
        });
    });

    // (3) Escape closes any open lightbox.
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            document.querySelectorAll(".lightbox-overlay").forEach(function (o) {
                o.remove();
            });
        }
    });
});
</script>
"""


def render_html(notebook: Path) -> Path:
    """Convert notebook to reveal.js slides HTML via `jupyter nbconvert`, then
    inject the project-wide CSS into the head.

    Cells are executed (`--execute`) so figure outputs (word clouds, dendrograms,
    tokens-over-time plot, …) are baked into the slides as live Python output
    rather than stale 2025 reference PNGs. The source .ipynb is NOT modified —
    nbconvert keeps the executed version in memory for the conversion only.
    Failed cells abort the render so we never ship a deck with broken outputs.
    """
    cmd = [
        "jupyter", "nbconvert", "--to", "slides",
        "--execute",
        "--ExecutePreprocessor.timeout=300",
        str(notebook),
    ]
    print(f"running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    html = notebook.with_suffix(".slides.html")
    if not html.exists():
        raise SystemExit(f"expected output {html} not found")
    inject_css(html, SLIDES_CSS)
    inject_click_reveal_js(html)
    return html


def inject_css(html: Path, css: Path) -> None:
    """Inject the contents of css into html's <head> as an inline <style>."""
    if not css.exists():
        print(f"  (note: {css} not found; skipping CSS injection)")
        return
    css_text = css.read_text()
    html_text = html.read_text()
    style_tag = f"<style>\n/* injected from {css.name} */\n{css_text}\n</style>"
    if "</head>" not in html_text:
        raise SystemExit(f"no </head> tag found in {html}; cannot inject CSS")
    html_text = html_text.replace("</head>", f"{style_tag}\n</head>", 1)
    html.write_text(html_text)
    print(f"  injected: {css.name} -> {html.name}")


def inject_click_reveal_js(html: Path) -> None:
    """Append the click-to-reveal JS just before </body>."""
    html_text = html.read_text()
    if "</body>" not in html_text:
        raise SystemExit(f"no </body> tag found in {html}; cannot inject JS")
    html_text = html_text.replace("</body>", f"{CLICK_REVEAL_JS}\n</body>", 1)
    html.write_text(html_text)
    print(f"  injected: click-reveal JS -> {html.name}")


def html_to_pdf(html: Path) -> Path:
    """Print reveal.js slides HTML to a multipage PDF via Chrome headless."""
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if chrome is None:
        raise SystemExit("no google-chrome / chromium binary on PATH")
    pdf = html.with_suffix(".pdf")
    url = f"file://{html.resolve()}?print-pdf"
    cmd = [
        chrome,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf}",
        url,
    ]
    print(f"running: chrome --print-to-pdf={pdf.name} {url}")
    subprocess.run(cmd, check=True)
    if not pdf.exists():
        raise SystemExit(f"expected PDF {pdf} not produced")
    return pdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    args = parser.parse_args()
    html = render_html(args.notebook)
    print(f"  HTML: {html}")
    pdf = html_to_pdf(html)
    print(f"  PDF:  {pdf} ({pdf.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
