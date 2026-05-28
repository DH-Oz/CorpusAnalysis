"""Build scratch/3a-collocations-dispersion.ipynb.

Matplotlib-only, minimal pyplot. Helper functions for repeated patterns
(dictionary parsing, lexical dispersion, decade networks). No list
comprehensions. Declarative prose, no cross-language framing.
Uses scratch/dictionaries/macdvirtue.dic and scratch/dictionaries/nuke.dic.

Re-run from the repo root: `uv run python scratch/_build_rmd3a.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.notebook_cells import append_cells

NOTEBOOK = "scratch/3a-collocations-dispersion.ipynb"


def md(source: str) -> tuple[None, str]:
    return (None, source)


def code(source: str) -> dict:
    return {"slide_type": None, "source": source, "cell_type": "code"}


def create_empty_notebook(path: str) -> None:
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.14"},
    }
    nbformat.write(nb, path)


CELLS: list = [
    md(
        "# Corpus Masterclass 3a: Collocations, Keyword Windows, Dispersion, Decade Networks\n"
        "\n"
        "Five techniques that look inside the corpus rather than summarising it whole: frequent "
        "two-word phrases, the context around a keyword, where a word falls within a speech, "
        "what is distinctive about that context, and how category co-occurrence shifts decade "
        "by decade."
    ),

    md(
        "## Today's goal\n"
        "\n"
        "1. Find the most frequent bigrams in the corpus.\n"
        "2. Replace selected multi-word phrases with single tokens.\n"
        "3. Capture the keyword windows around `atom`, `nuclear`, `nuke`.\n"
        "4. Rank what is distinctive inside those windows by keyness.\n"
        "5. Draw lexical-dispersion plots for a word across the corpus.\n"
        "6. Build a category co-occurrence network for each decade with a function and a loop."
    ),

    code(
        "# Libraries used throughout the notebook.\n"
        "import sotu\n"
        "import pandas\n"
        "import numpy\n"
        "import re\n"
        "import liwc\n"
        "import matplotlib.pyplot as plt\n"
        "import nltk.collocations\n"
        "import scipy.stats\n"
        "import networkx\n"
        "\n"
        "print('Libraries imported.')"
    ),

    code(
        "# Load the corpus.\n"
        "df = sotu.load()\n"
        "print(f'{len(df)} speeches, {df[\"year\"].min()} to {df[\"year\"].max()}.')"
    ),

    code(
        "# Collocations need every token in order. Tokenise each speech and collect the tokens\n"
        "# into one flat list. Keep the original capitalisation: the bigram step below selects\n"
        "# capitalised words, which are mostly proper nouns. extend adds the items of one list\n"
        "# to the end of another.\n"
        "all_tokens = []\n"
        "for text in df['text']:\n"
        "    all_tokens.extend(re.findall(r'\\w+', text))\n"
        "\n"
        "print(f'{len(all_tokens):,} tokens across the corpus.')"
    ),

    code(
        "# A bigram is a pair of consecutive tokens. We want phrases, not the most frequent word\n"
        "# pairs, which would just be 'of the' and 'in the'. Two steps get there. First, keep only\n"
        "# bigrams whose words both start with a capital letter and run two letters or more, which\n"
        "# skips stopwords, initials, and the lone pronoun I, surfacing proper-noun phrases. Second,\n"
        "# rank by a collocation statistic rather than raw count: the likelihood ratio is high when\n"
        "# two words occur together far more often than chance.\n"
        "def not_proper(word):\n"
        "    return len(word) < 2 or not word[:1].isupper()\n"
        "\n"
        "finder = nltk.collocations.BigramCollocationFinder.from_words(all_tokens)\n"
        "finder.apply_word_filter(not_proper)\n"
        "finder.apply_freq_filter(100)\n"
        "\n"
        "measures = nltk.collocations.BigramAssocMeasures()\n"
        "scored = finder.score_ngrams(measures.likelihood_ratio)\n"
        "for (first, second), score in scored[:20]:\n"
        "    print(f'{score:10.1f}  {first} {second}')"
    ),

    code(
        "# A replacement dictionary maps a two-token phrase to a single token. Treating 'united\n"
        "# states' as one token keeps it from scattering across two unrelated counts.\n"
        "replacements = {\n"
        "    ('united', 'states'): 'unitedstates',\n"
        "    ('federal', 'government'): 'federalgovernment',\n"
        "    ('soviet', 'union'): 'sovietunion',\n"
        "    ('world', 'war'): 'worldwar',\n"
        "    ('united', 'nations'): 'unitednations',\n"
        "    ('central', 'america'): 'centralamerica',\n"
        "    ('great', 'britain'): 'greatbritain',\n"
        "    ('supreme', 'court'): 'supremecourt',\n"
        "}\n"
        "print(f'{len(replacements)} replacement rules.')"
    ),

    code(
        "# apply_replacements walks a token list. When the current and next token match a rule,\n"
        "# it emits the single replacement token and skips ahead by two. A while loop is used\n"
        "# because we sometimes advance by one position and sometimes by two.\n"
        "def apply_replacements(tokens):\n"
        "    output = []\n"
        "    index = 0\n"
        "    while index < len(tokens):\n"
        "        if index + 1 < len(tokens):\n"
        "            pair = (tokens[index], tokens[index + 1])\n"
        "        else:\n"
        "            pair = None\n"
        "        if pair is not None and pair in replacements:\n"
        "            output.append(replacements[pair])\n"
        "            index = index + 2\n"
        "        else:\n"
        "            output.append(tokens[index])\n"
        "            index = index + 1\n"
        "    return output\n"
        "\n"
        "sample = ['the', 'united', 'states', 'and', 'the', 'soviet', 'union']\n"
        "print(apply_replacements(sample))"
    ),

    code(
        "# Re-tokenise every speech with phrase replacement applied. Keep one token list per\n"
        "# speech so we can locate words within their own document later.\n"
        "speech_tokens = []\n"
        "for text in df['text']:\n"
        "    speech_tokens.append(apply_replacements(re.findall(r'\\w+', text.lower())))\n"
        "\n"
        "print(f'{len(speech_tokens)} speeches re-tokenised.')"
    ),

    code(
        "# A keyword window is the run of tokens on either side of a target word. matches_pattern\n"
        "# returns True if a token starts with any of the given prefixes, so 'atom' also catches\n"
        "# 'atomic'.\n"
        "def matches_pattern(token, patterns):\n"
        "    for pattern in patterns:\n"
        "        if token.startswith(pattern):\n"
        "            return True\n"
        "    return False\n"
        "\n"
        "nuke_patterns = ['atom', 'nuclear', 'nuke']\n"
        "for word in ['atom', 'atomic', 'nuclear', 'apple']:\n"
        "    print(f'{word}: {matches_pattern(word, nuke_patterns)}')"
    ),

    code(
        "# split_inside_outside walks one speech. For each matching token it records the window\n"
        "# of tokens around it and marks those positions. Everything unmarked is the 'outside'.\n"
        "def split_inside_outside(tokens, patterns, window=10):\n"
        "    near_match = [False] * len(tokens)\n"
        "    inside_windows = []\n"
        "    for index, token in enumerate(tokens):\n"
        "        if matches_pattern(token, patterns):\n"
        "            start = max(0, index - window)\n"
        "            end = min(len(tokens), index + window + 1)\n"
        "            inside_windows.append(tokens[start:end])\n"
        "            for marker in range(start, end):\n"
        "                near_match[marker] = True\n"
        "    outside_tokens = []\n"
        "    for index, token in enumerate(tokens):\n"
        "        if not near_match[index]:\n"
        "            outside_tokens.append(token)\n"
        "    return inside_windows, outside_tokens"
    ),

    code(
        "# Apply to every speech and gather all inside-window tokens and all outside tokens. Drop\n"
        "# the keyword itself from the inside windows: it sits in every window by definition, so\n"
        "# leaving it in would just rank the search word at the top of its own keyness. We want\n"
        "# the words around it.\n"
        "all_inside = []\n"
        "all_outside = []\n"
        "for tokens in speech_tokens:\n"
        "    inside, outside = split_inside_outside(tokens, nuke_patterns, window=10)\n"
        "    for window_tokens in inside:\n"
        "        for token in window_tokens:\n"
        "            if matches_pattern(token, nuke_patterns):\n"
        "                continue\n"
        "            all_inside.append(token)\n"
        "    all_outside.extend(outside)\n"
        "\n"
        "print(f'Inside: {len(all_inside):,} tokens. Outside: {len(all_outside):,} tokens.')"
    ),

    code(
        "# Count each word in both groups. dict.get(word, 0) returns 0 when the word is not yet\n"
        "# a key.\n"
        "inside_counts = {}\n"
        "for token in all_inside:\n"
        "    inside_counts[token] = inside_counts.get(token, 0) + 1\n"
        "outside_counts = {}\n"
        "for token in all_outside:\n"
        "    outside_counts[token] = outside_counts.get(token, 0) + 1\n"
        "\n"
        "print(f'Distinct words inside: {len(inside_counts):,}.')"
    ),

    code(
        "# Keyness compares a word's inside frequency against its outside frequency. The\n"
        "# chi-squared statistic on a 2x2 contingency table is large when a word is much more\n"
        "# common inside the windows than outside.\n"
        "total_inside = len(all_inside)\n"
        "total_outside = len(all_outside)\n"
        "\n"
        "keyness = []\n"
        "for word, inside_count in inside_counts.items():\n"
        "    if inside_count < 5:\n"
        "        continue\n"
        "    outside_count = outside_counts.get(word, 0)\n"
        "    table = [\n"
        "        [inside_count, total_inside - inside_count],\n"
        "        [outside_count, total_outside - outside_count],\n"
        "    ]\n"
        "    statistic = scipy.stats.chi2_contingency(table).statistic\n"
        "    keyness.append((word, statistic, inside_count, outside_count))\n"
        "\n"
        "print(f'Keyness computed for {len(keyness):,} words.')"
    ),

    code(
        "# Sort by the statistic, highest first, and show the top 20. sort_key returns the\n"
        "# statistic from each tuple; passing it to sorted ranks by that value.\n"
        "def sort_key(entry):\n"
        "    return entry[1]\n"
        "\n"
        "ranked = sorted(keyness, key=sort_key, reverse=True)\n"
        "print('Top 20 keywords inside the nuclear windows:')\n"
        "for word, statistic, inside_count, outside_count in ranked[:20]:\n"
        "    print(f'  {word:18s}  chi-squared {statistic:8.1f}  inside {inside_count:4d}  outside {outside_count:5d}')"
    ),

    code(
        "# Restrict the dispersion analysis to speeches from 1908 onward, when nuclear vocabulary\n"
        "# enters the language.\n"
        "modern_indices = []\n"
        "for original_index, year in enumerate(df['year']):\n"
        "    if year >= 1908:\n"
        "        modern_indices.append(original_index)\n"
        "\n"
        "print(f'{len(modern_indices)} speeches from 1908 onward.')"
    ),

    code(
        "# A lexical-dispersion plot shows where in each speech a word appears. Only speeches\n"
        "# that use the word are shown. The x-axis is the absolute token position. Each grey\n"
        "# bar is the length of one speech, and each black mark is one occurrence.\n"
        "def dispersion_plot(prefix, title):\n"
        "    row_labels = []\n"
        "    row_lengths = []\n"
        "    row_positions = []\n"
        "    for original_index in modern_indices:\n"
        "        tokens = speech_tokens[original_index]\n"
        "        positions = []\n"
        "        for token_index, token in enumerate(tokens):\n"
        "            if token.startswith(prefix):\n"
        "                positions.append(token_index)\n"
        "        if len(positions) == 0:\n"
        "            continue\n"
        "        row_labels.append(f'{df.iloc[original_index][\"year\"]} {df.iloc[original_index][\"president\"]}')\n"
        "        row_lengths.append(len(tokens))\n"
        "        row_positions.append(positions)\n"
        "    plt.figure(figsize=(11, max(2.5, 0.30 * len(row_labels))))\n"
        "    for plot_row in range(len(row_labels)):\n"
        "        plt.hlines(plot_row, 0, row_lengths[plot_row], color='lightgray', linewidth=6, zorder=1)\n"
        "        marks = row_positions[plot_row]\n"
        "        plt.scatter(marks, [plot_row] * len(marks), marker='|', s=120, color='black', zorder=2)\n"
        "    plt.yticks(range(len(row_labels)), row_labels, fontsize=7)\n"
        "    plt.xlabel('Token index')\n"
        "    plt.title(title)\n"
        "    plt.gca().invert_yaxis()\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),

    code(
        "# Dispersion of words starting with 'atom'.\n"
        "dispersion_plot('atom', 'Lexical dispersion: words starting with \"atom\" (1908+)')"
    ),

    code(
        "# Dispersion of words starting with 'nuclear'.\n"
        "dispersion_plot('nuclear', 'Lexical dispersion: words starting with \"nuclear\" (1908+)')"
    ),

    code(
        "# The liwc library reads the dictionary and matches tokens, wildcards included. The nuke\n"
        "# dictionary has many categories (nuke, weapon, energy, suppliers, ...); the genuinely\n"
        "# nuclear words live in the 'nuke' category. We will count that category only.\n"
        "nuke_lookup, nuke_categories = liwc.load_token_parser('dictionaries/nuke.dic')\n"
        "print(f'{len(nuke_categories)} categories. nuke in them: {\"nuke\" in nuke_categories}')"
    ),

    code(
        "# Count only the 'nuke' category per speech and plot the rate per 1000 tokens over time.\n"
        "nuke_rows = []\n"
        "for original_index, tokens in enumerate(speech_tokens):\n"
        "    hits = 0\n"
        "    for token in tokens:\n"
        "        if 'nuke' in nuke_lookup(token):\n"
        "            hits = hits + 1\n"
        "    nuke_rows.append({\n"
        "        'year': df.iloc[original_index]['year'],\n"
        "        'rate': hits / len(tokens) * 1000 if tokens else 0,\n"
        "    })\n"
        "\n"
        "nuke_df = pandas.DataFrame(nuke_rows).sort_values('year')\n"
        "plt.figure(figsize=(13, 4))\n"
        "plt.plot(nuke_df['year'], nuke_df['rate'], marker='o', markersize=3, linewidth=0.6)\n"
        "plt.xlabel('Year')\n"
        "plt.ylabel('Nuclear vocabulary per 1000 tokens')\n"
        "plt.title('Nuclear vocabulary in State of the Union addresses')\n"
        "plt.show()"
    ),

    code(
        "# For the decade networks we need a category feature matrix. Apply the MAC virtue\n"
        "# dictionary to every speech, one row of category counts plus the year.\n"
        "mac_lookup, mac_names = liwc.load_token_parser('dictionaries/macdvirtue.dic')\n"
        "\n"
        "feature_rows = []\n"
        "for original_index, tokens in enumerate(speech_tokens):\n"
        "    counts = {}\n"
        "    for name in mac_names:\n"
        "        counts[name] = 0\n"
        "    for token in tokens:\n"
        "        for name in mac_lookup(token):\n"
        "            counts[name] = counts[name] + 1\n"
        "    counts['year'] = df.iloc[original_index]['year']\n"
        "    feature_rows.append(counts)\n"
        "\n"
        "feature_df = pandas.DataFrame(feature_rows)\n"
        "feature_df.head(3)"
    ),

    code(
        "# decade_network builds the co-occurrence network for one decade. Subset the speeches in\n"
        "# the year range, form the adjacency matrix, build the graph, and draw it with a\n"
        "# force-directed layout. Node size grows with how often a virtue appears, and faint edges\n"
        "# are weak co-occurrences.\n"
        "def decade_network(decade_start):\n"
        "    decade_end = decade_start + 9\n"
        "    mask = (feature_df['year'] >= decade_start) & (feature_df['year'] <= decade_end)\n"
        "    subset = feature_df[mask][mac_names]\n"
        "    if len(subset) == 0:\n"
        "        print(f'No speeches in the {decade_start}s.')\n"
        "        return\n"
        "    adjacency = subset.to_numpy().T @ subset.to_numpy()\n"
        "    graph = networkx.from_numpy_array(adjacency)\n"
        "    relabelling = {}\n"
        "    for node_index, name in enumerate(mac_names):\n"
        "        relabelling[node_index] = name\n"
        "    graph = networkx.relabel_nodes(graph, relabelling)\n"
        "    graph.remove_edges_from(list(networkx.selfloop_edges(graph)))\n"
        "    weights = []\n"
        "    for u, v in graph.edges():\n"
        "        weights.append(graph[u][v]['weight'])\n"
        "    largest = max(weights) if weights else 1\n"
        "    widths = []\n"
        "    edge_colors = []\n"
        "    for weight in weights:\n"
        "        widths.append(weight / largest * 8)\n"
        "        shade = 0.85 - 0.7 * (weight / largest)\n"
        "        edge_colors.append((shade, shade, shade))\n"
        "    category_totals = subset.sum(axis=0)\n"
        "    biggest = category_totals.max() if category_totals.max() > 0 else 1\n"
        "    node_sizes = []\n"
        "    for node in graph.nodes():\n"
        "        node_sizes.append(400 + category_totals[node] / biggest * 2400)\n"
        "    plt.figure(figsize=(8, 7))\n"
        "    networkx.draw(\n"
        "        graph,\n"
        "        pos=networkx.spring_layout(graph, seed=42, weight='weight'),\n"
        "        with_labels=True,\n"
        "        node_color='lightyellow',\n"
        "        node_size=node_sizes,\n"
        "        edge_color=edge_colors,\n"
        "        width=widths,\n"
        "        font_size=9,\n"
        "    )\n"
        "    plt.title(f'MAC virtues co-occurrence, the {decade_start}s ({len(subset)} speeches)')\n"
        "    plt.show()"
    ),

    code(
        "# One worked decade.\n"
        "decade_network(1940)"
    ),

    code(
        "# Every decade from the 1940s to the 2020s. range(1940, 2030, 10) steps by ten.\n"
        "for decade_start in range(1940, 2030, 10):\n"
        "    decade_network(decade_start)"
    ),

    md(
        "## What we've covered\n"
        "\n"
        "**Python:** `list.extend`; `nltk.collocations` frequency distributions; `while` loops "
        "with manual indexing; predicate helper functions; counting with `dict.get(key, 0)`; "
        "`scipy.stats.chi2_contingency`; `sorted` with a key function; `range(start, stop, step)`.\n"
        "\n"
        "**Corpus linguistics:** bigrams and collocations; phrase replacement; keyword windows; "
        "keyness with the chi-squared statistic; lexical-dispersion plots; per-decade "
        "co-occurrence networks."
    ),

    md(
        "## Read more\n"
        "\n"
        "- **NLTK collocations how-to**: [https://www.nltk.org/howto/collocations.html]("
        "https://www.nltk.org/howto/collocations.html).\n"
        "- **scipy.stats.chi2_contingency**: [https://docs.scipy.org/doc/scipy/reference/"
        "generated/scipy.stats.chi2_contingency.html]("
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html).\n"
        "- **NetworkX layouts**: [https://networkx.org/documentation/stable/reference/drawing.html"
        "#module-networkx.drawing.layout]("
        "https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout).\n"
        "- **MAC virtue dictionary**: Curry, Mullins & Whitehouse (2019), [https://doi.org/"
        "10.1086/701478](https://doi.org/10.1086/701478)."
    ),
]


def main() -> None:
    path = Path(NOTEBOOK)
    if path.exists():
        path.unlink()
    create_empty_notebook(NOTEBOOK)
    total = append_cells(NOTEBOOK, CELLS)
    print(f'Wrote {total} cells to {NOTEBOOK}')


if __name__ == '__main__':
    main()
