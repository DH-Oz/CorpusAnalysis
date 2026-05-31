"""Per-cell code-along complexity score for Jupyter notebooks and R Markdown.

Estimates how heavy a code cell is for a student to type along with live. The
output is a single number per cell. Sum across a notebook to compare against
the 2025 R source totals when budgeting a translation.

Score is the weighted sum of seven structural features:

    char_count            — raw text length (the floor)
    indent_depth_max      — deepest indentation level in the cell
    indent_changes        — number of lines where indentation level changed
    non_word_chars        — count of [^\\w\\s]; punctuation-as-syntax load
    distinct_identifiers  — distinct identifier tokens in the cell
    branch_loop_heads     — count of if/elif/else/for/while/with/def/class
                            (Python) or if/else/for/while/function (R)
    method_chain_max      — longest .foo().bar().baz() chain (Python)
                            or longest %>% chain (R)

Weights are an initial guess and intended to be tuned by hand-scoring
representative cells. Edit WEIGHTS below.

Usage:
    uv run python tools/code_along_score.py day-1/D1-AM-intro.ipynb
    uv run python tools/code_along_score.py "2025-WinterSchool/20250504 corpusmasterclass1.Rmd"

Prints a per-cell breakdown and a file total. Auto-detects R vs Python from
the file extension.
"""

from __future__ import annotations

import json
import re
import sys
import tokenize
from io import BytesIO
from pathlib import Path

# Initial weights. Tune by hand-scoring representative cells.
WEIGHTS = {
    "char_count": 1.0,
    "indent_depth_max": 8.0,
    "indent_changes": 2.0,
    "non_word_chars": 0.5,
    "distinct_identifiers": 4.0,
    "branch_loop_heads": 5.0,
    "method_chain_max": 3.0,
}

PYTHON_BRANCH_KEYWORDS = frozenset({
    "if", "elif", "else", "for", "while", "with",
    "def", "class", "try", "except", "finally",
})

R_BRANCH_KEYWORDS = frozenset({
    "if", "else", "for", "while", "repeat", "function",
})

R_CHUNK_PATTERN = re.compile(r"^```\{r[^}]*\}\s*$(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
PYTHON_CHAIN_PATTERN = re.compile(r"(?:\.\w+\([^)]*\))+")
R_PIPE_PATTERN = re.compile(r"(?:%>%\s*\w+\([^)]*\))+")
NON_WORD_PATTERN = re.compile(r"[^\w\s]")
R_IDENTIFIER_PATTERN = re.compile(r"\b[A-Za-z_][A-Za-z_0-9.]*\b")


def score_features(features: dict[str, float]) -> float:
    return sum(features[k] * WEIGHTS[k] for k in WEIGHTS)


def indent_features(text: str) -> tuple[int, int]:
    """Return (max indent depth in 4-space units, count of indent-level changes)."""
    depths = []
    for line in text.splitlines():
        if not line.strip():
            continue
        spaces = len(line) - len(line.lstrip(" "))
        depths.append(spaces // 4)
    if not depths:
        return (0, 0)
    max_depth = max(depths)
    changes = sum(1 for a, b in zip(depths, depths[1:]) if a != b)
    return (max_depth, changes)


def python_identifiers_and_keywords(text: str) -> tuple[set[str], int]:
    """Tokenise Python source. Return (distinct identifier names, branch/loop head count)."""
    idents: set[str] = set()
    heads = 0
    try:
        tokens = tokenize.tokenize(BytesIO(text.encode("utf-8")).readline)
        for tok in tokens:
            if tok.type == tokenize.NAME:
                if tok.string in PYTHON_BRANCH_KEYWORDS:
                    heads += 1
                else:
                    idents.add(tok.string)
    except tokenize.TokenizeError:
        # Partial cell or malformed snippet; fall back to regex
        for match in R_IDENTIFIER_PATTERN.finditer(text):
            name = match.group(0)
            if name in PYTHON_BRANCH_KEYWORDS:
                heads += 1
            else:
                idents.add(name)
    return (idents, heads)


def r_identifiers_and_keywords(text: str) -> tuple[set[str], int]:
    """Regex-tokenise R source. Return (distinct identifier names, branch/loop head count)."""
    idents: set[str] = set()
    heads = 0
    for match in R_IDENTIFIER_PATTERN.finditer(text):
        name = match.group(0)
        if name in R_BRANCH_KEYWORDS:
            heads += 1
        else:
            idents.add(name)
    return (idents, heads)


def chain_depth(text: str, pattern: re.Pattern[str]) -> int:
    """Longest method-call chain in the cell."""
    longest = 0
    for match in pattern.finditer(text):
        chain = match.group(0)
        depth = chain.count("(")
        if depth > longest:
            longest = depth
    return longest


def strip_comments(text: str, language: str) -> str:
    """Remove comments before scoring.

    Prose comments are reading time, not typing-along complexity. Stripping
    them before feature extraction keeps the score focused on the executable
    portion of the cell.
    """
    if language == "python":
        try:
            tokens = list(tokenize.tokenize(BytesIO(text.encode("utf-8")).readline))
        except tokenize.TokenizeError:
            return _strip_hash_comments_lineby(text)
        lines = text.splitlines(keepends=True)
        for tok in tokens:
            if tok.type != tokenize.COMMENT:
                continue
            row = tok.start[0] - 1
            col_start = tok.start[1]
            col_end = tok.end[1]
            if 0 <= row < len(lines):
                line = lines[row]
                lines[row] = line[:col_start] + line[col_end:]
        return "".join(lines)
    return _strip_hash_comments_lineby(text)


def _strip_hash_comments_lineby(text: str) -> str:
    output_lines = []
    for line in text.splitlines(keepends=True):
        hash_position = line.find("#")
        if hash_position == -1:
            output_lines.append(line)
        else:
            output_lines.append(line[:hash_position].rstrip() + "\n")
    return "".join(output_lines)


def features_for_cell(text: str, language: str) -> dict[str, float]:
    text = strip_comments(text, language)
    char_count = len(text)
    max_depth, changes = indent_features(text)
    non_word_chars = len(NON_WORD_PATTERN.findall(text))
    if language == "python":
        idents, heads = python_identifiers_and_keywords(text)
        chain = chain_depth(text, PYTHON_CHAIN_PATTERN)
    else:
        idents, heads = r_identifiers_and_keywords(text)
        chain = chain_depth(text, R_PIPE_PATTERN)
    return {
        "char_count": char_count,
        "indent_depth_max": max_depth,
        "indent_changes": changes,
        "non_word_chars": non_word_chars,
        "distinct_identifiers": len(idents),
        "branch_loop_heads": heads,
        "method_chain_max": chain,
    }


def extract_ipynb_cells(path: Path) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)
            cells.append(source)
    return cells


def extract_rmd_cells(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group(1).strip("\n") for match in R_CHUNK_PATTERN.finditer(text)]


def detect_language(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".ipynb":
        return "python"
    if suffix == ".rmd":
        return "r"
    raise ValueError(f"Unsupported extension: {path.suffix}. Use .ipynb or .Rmd")


def score_file(path: Path) -> tuple[list[dict], float]:
    language = detect_language(path)
    cells = extract_ipynb_cells(path) if language == "python" else extract_rmd_cells(path)
    rows = []
    total = 0.0
    for index, source in enumerate(cells):
        feats = features_for_cell(source, language)
        score = score_features(feats)
        rows.append({"index": index, "score": score, "features": feats, "preview": preview(source)})
        total += score
    return (rows, total)


def preview(source: str, width: int = 60) -> str:
    first_line = source.strip().splitlines()[0] if source.strip() else ""
    if len(first_line) > width:
        return first_line[:width - 3] + "..."
    return first_line


def format_row(row: dict) -> str:
    feats = row["features"]
    return (
        f"cell {row['index']:3d}  "
        f"score {row['score']:8.1f}  "
        f"chars {feats['char_count']:4d}  "
        f"ind {feats['indent_depth_max']:2d}/{feats['indent_changes']:2d}  "
        f"nw {feats['non_word_chars']:4d}  "
        f"id {feats['distinct_identifiers']:3d}  "
        f"br {feats['branch_loop_heads']:2d}  "
        f"ch {feats['method_chain_max']:2d}  "
        f"| {row['preview']}"
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <path.ipynb|path.Rmd>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"not found: {path}", file=sys.stderr)
        return 1
    rows, total = score_file(path)
    print(f"# {path}")
    print(f"# {len(rows)} code cells, total score {total:.1f}")
    print(f"# columns: chars  ind(depth/changes)  nw(non-word)  id(idents)  br(branches)  ch(chain)")
    for row in rows:
        print(format_row(row))
    print(f"# TOTAL  {total:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
