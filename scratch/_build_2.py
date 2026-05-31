"""Build scratch/2-dictionary-content.ipynb.

Matplotlib-only, minimal pyplot. Repeated patterns (dictionary parsing,
per-category plotting, network drawing) are factored into helper functions
defined once. Prose comments are declarative and short. No list comprehensions
(explicit loops only). Uses scratch/dictionaries/macdvirtue.dic.

Re-run from the repo root: `uv run python scratch/_build_rmd2.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.notebook_cells import append_cells

NOTEBOOK = "scratch/2-dictionary-content.ipynb"


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
        "# Corpus Masterclass 2: Dictionary-Based Content Analysis and Networks\n"
        "\n"
        "A dictionary tags words with the categories they belong to. Applying one to a corpus "
        "tells us how much of each category appears in each document. This notebook applies the "
        "MAC virtue dictionary to the State of the Union corpus, plots category trends over time, "
        "and turns those percentages into a co-occurrence network. A final section repeats the "
        "analysis with the commercial LIWC dictionary on the instructor's local machine."
    ),

    md(
        "## Today's goal\n"
        "\n"
        "1. Read a LIWC-format dictionary file.\n"
        "2. Apply it to the State of the Union corpus for a per-speech table of category percentages.\n"
        "3. Plot one moral-vocabulary category across two centuries.\n"
        "4. Plot the remaining categories with a function called in a loop.\n"
        "5. Compute an adjacency matrix: which categories co-occur across speeches.\n"
        "6. Draw that adjacency as a network, with two layouts.\n"
        "\n"
        "Dictionary: `dictionaries/macdvirtue.dic`, the Curry et al. MAC virtue dictionary."
    ),

    code(
        "# Libraries used throughout the notebook.\n"
        "import sotu\n"
        "import pandas\n"
        "import numpy\n"
        "import re\n"
        "import liwc\n"
        "import matplotlib.pyplot as plt\n"
        "import networkx\n"
        "from pathlib import Path\n"
        "\n"
        "print('Libraries imported.')"
    ),

    code(
        "# A LIWC-format dictionary has two parts. Between two lines that contain only '%', an\n"
        "# id-to-name table declares the categories. After the second '%', each line is a term\n"
        "# followed by the category ids it belongs to, all tab-separated. Look at the top of the\n"
        "# file to see the shape.\n"
        "with open('dictionaries/macdvirtue.dic') as f:\n"
        "    line_number = 0\n"
        "    for line in f:\n"
        "        print(line.rstrip())\n"
        "        line_number = line_number + 1\n"
        "        if line_number >= 14:\n"
        "            break"
    ),

    code(
        "# The liwc library reads the dictionary and handles the matching rules for us, including\n"
        "# the trailing '*' wildcard (a term like 'tugend*' matches tugend, tugendhaft, and so on).\n"
        "# load_token_parser returns a lookup function and the list of category names.\n"
        "token_categories, category_names = liwc.load_token_parser('dictionaries/macdvirtue.dic')\n"
        "print(f'Categories: {category_names}')"
    ),

    code(
        "# The lookup function returns the categories a token belongs to. A token can belong to\n"
        "# none, one, or several categories.\n"
        "for term in ['family', 'fair', 'brave', 'reciprocate']:\n"
        "    print(f'{term}: {list(token_categories(term))}')"
    ),

    code(
        "# Load the State of the Union corpus.\n"
        "df = sotu.load()\n"
        "print(f'{len(df)} speeches loaded.')"
    ),

    code(
        "# Tokenise one speech and count how many tokens fall into each category. re.findall\n"
        "# with the word pattern is a quick tokeniser for dictionary look-up.\n"
        "first_tokens = re.findall(r'\\w+', df.iloc[0]['text'].lower())\n"
        "\n"
        "first_counts = {}\n"
        "for name in category_names:\n"
        "    first_counts[name] = 0\n"
        "for token in first_tokens:\n"
        "    for name in token_categories(token):\n"
        "        first_counts[name] = first_counts[name] + 1\n"
        "\n"
        "print(f'Washington 1790, category counts:')\n"
        "print(first_counts)"
    ),

    md(
        "`liwcalike` runs that same tally over every speech at once. It comes from "
        "`corpus_tools.py`. That file sits beside this notebook, and `import` brings its code in."
    ),

    code(
        "# import takes a name from another file and makes it usable here. corpus_tools.py sits in\n"
        "# the same folder as this notebook. From it we take the liwcalike function.\n"
        "from corpus_tools import liwcalike\n"
        "\n"
        "# liwcalike tokenises each speech and tallies its dictionary categories, then divides every\n"
        "# count by the speech's word count. A long speech uses more category words just by being\n"
        "# longer, so comparing percentages rather than counts puts every speech on equal footing.\n"
        "# liwcalike needs three things: the texts, a name for each speech, and the dictionary file.\n"
        "docnames = []\n"
        "for _, speech in df.iterrows():\n"
        "    docnames.append(f\"{speech['president']}_{speech['year']}\")\n"
        "\n"
        "virtue_df = liwcalike(list(df['text']), docnames, 'dictionaries/macdvirtue.dic')\n"
        "virtue_df['year'] = list(df['year'])\n"
        "virtue_df['president'] = list(df['president'])\n"
        "print(f'{len(virtue_df)} speeches processed.')\n"
        "virtue_df[['docname', 'WC', 'Family', 'Group']].head(3)"
    ),

    code(
        "# Helper. Plot one category's percentage across the years.\n"
        "def plot_category(category_name):\n"
        "    ordered = virtue_df.sort_values('year')\n"
        "    plt.figure(figsize=(13, 4))\n"
        "    plt.plot(ordered['year'], ordered[category_name], marker='o', markersize=3, linewidth=0.6)\n"
        "    plt.xlabel('Year')\n"
        "    plt.ylabel(f'{category_name} (% of words)')\n"
        "    plt.title(f'MAC virtue: {category_name} in State of the Union addresses')\n"
        "    plt.show()"
    ),

    code(
        "# Family across two centuries.\n"
        "plot_category('Family')"
    ),

    code(
        "# Every remaining category, one call each, via a loop.\n"
        "for name in ['Group', 'Reciprocity', 'Heroism', 'Deference', 'Fairness', 'Property']:\n"
        "    plot_category(name)"
    ),

    code(
        "# An adjacency matrix is a square table where rows and columns are the same items, here\n"
        "# the seven virtues. Subset to the seven percentage columns and convert to a numpy array.\n"
        "virtue_matrix = virtue_df[category_names].to_numpy()\n"
        "print(f'Matrix shape: {virtue_matrix.shape}')"
    ),

    code(
        "# Multiply the matrix transpose by the matrix. The result is 7 by 7. Each cell is large\n"
        "# when two categories tend to appear in the same speeches.\n"
        "adjacency = virtue_matrix.T @ virtue_matrix\n"
        "pandas.DataFrame(adjacency, index=category_names, columns=category_names).round(2)"
    ),

    code(
        "# Build a network from the adjacency matrix. Relabel the integer nodes with category\n"
        "# names and drop the self-loops created by the matrix diagonal.\n"
        "graph = networkx.from_numpy_array(adjacency)\n"
        "relabelling = {}\n"
        "for node_index, name in enumerate(category_names):\n"
        "    relabelling[node_index] = name\n"
        "graph = networkx.relabel_nodes(graph, relabelling)\n"
        "graph.remove_edges_from(list(networkx.selfloop_edges(graph)))\n"
        "print(f'{graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges.')"
    ),

    code(
        "# Helper. Draw the network with a given layout and title. Co-occurrence weights vary\n"
        "# widely, so scale every edge against the largest weight: the thickest edge is 8 points,\n"
        "# the rest proportional. Edge transparency keeps overlapping lines readable.\n"
        "def draw_network(graph, positions, title):\n"
        "    weights = []\n"
        "    for u, v in graph.edges():\n"
        "        weights.append(graph[u][v]['weight'])\n"
        "    largest = max(weights)\n"
        "    widths = []\n"
        "    for weight in weights:\n"
        "        widths.append(weight / largest * 8)\n"
        "    # Node area grows with strength: the total co-occurrence weight on a virtue, scaled\n"
        "    # against the busiest virtue so the sizes stay sensible on percentage inputs.\n"
        "    strengths = []\n"
        "    for node in graph.nodes():\n"
        "        strengths.append(graph.degree(node, weight='weight'))\n"
        "    biggest = max(strengths) if max(strengths) > 0 else 1\n"
        "    node_sizes = []\n"
        "    for value in strengths:\n"
        "        node_sizes.append(400 + value / biggest * 2600)\n"
        "    plt.figure(figsize=(9, 8))\n"
        "    networkx.draw(\n"
        "        graph,\n"
        "        pos=positions,\n"
        "        with_labels=True,\n"
        "        node_color='lightpink',\n"
        "        node_size=node_sizes,\n"
        "        edge_color='gray',\n"
        "        width=widths,\n"
        "        font_size=11,\n"
        "    )\n"
        "    plt.title(title)\n"
        "    plt.show()"
    ),

    code(
        "# A force-directed layout treats edges as springs. Connected nodes pull together;\n"
        "# unconnected nodes drift apart.\n"
        "spring_positions = networkx.spring_layout(graph, seed=42, weight='weight')\n"
        "draw_network(graph, spring_positions, 'MAC virtues: co-occurrence (force-directed layout)')"
    ),

    code(
        "# A circular layout puts nodes evenly around a ring. Position carries no meaning here, so\n"
        "# the eye reads edge thickness instead.\n"
        "circular_positions = networkx.circular_layout(graph)\n"
        "draw_network(graph, circular_positions, 'MAC virtues: co-occurrence (circular layout)')"
    ),

    md(
        "## The commercial LIWC dictionary (instructor demo)\n"
        "\n"
        "LIWC is the standard licensed psycholinguistic dictionary. The instructor runs it locally "
        "on `dictionaries/liwcdict.dic`. Because the file is commercial, it is never bundled in "
        "the public download; if it is not present here, the cells below skip themselves and the "
        "MAC analysis above stands in as the open-dictionary version of the same method."
    ),

    code(
        "# Try to load the LIWC dictionary. Path.exists() returns True if the file is on disk.\n"
        "liwc_path = Path('dictionaries/liwcdict.dic')\n"
        "have_liwc = liwc_path.exists()\n"
        "if have_liwc:\n"
        "    _, liwc_names = liwc.load_token_parser(str(liwc_path))\n"
        "    print(f'LIWC dictionary loaded: {len(liwc_names)} categories.')\n"
        "else:\n"
        "    print('liwcdict.dic is commercial and not bundled in this public download.')\n"
        "    print('The LIWC cells below are skipped; the MAC analysis above shows the same method.')"
    ),

    code(
        "# liwcalike works with any LIWC-format dictionary, so the commercial file goes through the\n"
        "# very same function. Six emotion categories mirror the 2025 lesson: overall affect,\n"
        "# positive and negative emotion, then the three negative subtypes.\n"
        "if have_liwc:\n"
        "    emotion_categories = ['Affect', 'Posemo', 'Negemo', 'Anx', 'Anger', 'Sad']\n"
        "    liwc_df = liwcalike(list(df['text']), docnames, str(liwc_path))\n"
        "    liwc_df['year'] = list(df['year'])\n"
        "    liwc_df = liwc_df.sort_values('year')\n"
        "    print(liwc_df[['year', 'Affect', 'Posemo', 'Negemo']].head(3))\n"
        "else:\n"
        "    print('LIWC counts skipped.')"
    ),

    code(
        "# Plot each emotion category across the years, via a function and a for loop. Same shape\n"
        "# as plot_category above, applied to the LIWC categories.\n"
        "if have_liwc:\n"
        "    def plot_liwc(category_name):\n"
        "        plt.figure(figsize=(13, 3.5))\n"
        "        plt.plot(liwc_df['year'], liwc_df[category_name], linewidth=0.6)\n"
        "        plt.xlabel('Year')\n"
        "        plt.ylabel(f'{category_name} (% of words)')\n"
        "        plt.title(f'LIWC: {category_name} in State of the Union addresses')\n"
        "        plt.show()\n"
        "\n"
        "    for name in ['Affect', 'Posemo', 'Negemo', 'Anx', 'Anger', 'Sad']:\n"
        "        plot_liwc(name)\n"
        "else:\n"
        "    print('LIWC plots skipped.')"
    ),

    md(
        "## What we've covered\n"
        "\n"
        "**Python:** file reading with `with open`; `re.findall` for tokenisation; importing a "
        "function from a helper module with `import`; defining functions and calling them in a "
        "loop; numpy matrix transpose `.T` and matrix multiplication `@`; networkx graphs, "
        "layouts, and drawing.\n"
        "\n"
        "**Corpus linguistics:** LIWC-format dictionaries; dictionary-based content analysis; "
        "per-document normalisation to a percentage; adjacency matrices from feature matrices; "
        "force-directed and circular network layouts."
    ),

    md(
        "## Read more\n"
        "\n"
        "- **MAC virtue dictionary**: Curry, Mullins & Whitehouse (2019), [https://doi.org/"
        "10.1086/701478](https://doi.org/10.1086/701478).\n"
        "- **NumPy linear algebra basics**: [https://numpy.org/doc/stable/user/quickstart.html"
        "#linear-algebra](https://numpy.org/doc/stable/user/quickstart.html#linear-algebra).\n"
        "- **NetworkX tutorial**: [https://networkx.org/documentation/stable/tutorial.html]("
        "https://networkx.org/documentation/stable/tutorial.html).\n"
        "- **NetworkX layouts**: [https://networkx.org/documentation/stable/reference/drawing.html"
        "#module-networkx.drawing.layout]("
        "https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout).\n"
        "- **Python re module**: [https://docs.python.org/3/library/re.html]("
        "https://docs.python.org/3/library/re.html)."
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
