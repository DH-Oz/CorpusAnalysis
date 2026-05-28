"""Build scratch/3b-nietzsche-german-paragraphs.ipynb.

Matplotlib-only, minimal pyplot. Helper functions for repeated patterns
(dictionary parsing, lexical dispersion, concept egonets, keyness). No list
comprehensions. Declarative prose, no cross-language framing.
Uses scratch/nietzsche/*.txt and scratch/dictionaries/nietzsche.dic.

Re-run from the repo root: `uv run python scratch/_build_rmd3b.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.notebook_cells import append_cells

NOTEBOOK = "scratch/3b-nietzsche-german-paragraphs.ipynb"


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
        "# Corpus Masterclass 3b: Nietzsche, German, and Paragraph-Level Networks\n"
        "\n"
        "The corpus is fifteen of Nietzsche's books in German, read from a folder of text files. "
        "The pipeline is familiar from the earlier notebooks, with three differences: the corpus "
        "comes from disk rather than a library, the language is German with historic spellings, "
        "and the unit of analysis switches from whole books to individual paragraphs for the "
        "concept networks."
    ),

    md(
        "## Today's goal\n"
        "\n"
        "1. Load fifteen Nietzsche books from a folder of text files.\n"
        "2. Run the standard pipeline in German: stopwords, document-feature matrix, word cloud, "
        "topics, dendrogram.\n"
        "3. Draw lexical-dispersion plots for German moral-vocabulary roots, via a function.\n"
        "4. Apply a moral-psychology dictionary at the book level.\n"
        "5. Reshape the corpus to one row per paragraph.\n"
        "6. Build a concept egonet: a co-occurrence network restricted to paragraphs that "
        "mention a chosen concept, via a function called in a loop."
    ),

    code(
        "# Libraries used throughout the notebook.\n"
        "from pathlib import Path\n"
        "import pandas\n"
        "import numpy\n"
        "import re\n"
        "import liwc\n"
        "import matplotlib.pyplot as plt\n"
        "import nltk\n"
        "import nltk.corpus\n"
        "import sklearn.feature_extraction.text\n"
        "import sklearn.decomposition\n"
        "import scipy.spatial.distance\n"
        "import scipy.cluster.hierarchy\n"
        "import wordcloud\n"
        "import networkx\n"
        "\n"
        "print('Libraries imported.')"
    ),

    code(
        "# pathlib.Path points at the corpus folder. glob('*.txt') lists every text file; sorted\n"
        "# makes the order stable.\n"
        "txt_paths = sorted(Path('nietzsche').glob('*.txt'))\n"
        "print(f'{len(txt_paths)} files.')\n"
        "for path in txt_paths[:3]:\n"
        "    print(f'  {path.name}')"
    ),

    code(
        "# Each filename is 'YEAR CODE.txt', for example '1885 Z.txt' for Thus Spake Zarathustra.\n"
        "# Read every book, splitting the filename stem to recover the year and book code.\n"
        "rows = []\n"
        "for path in txt_paths:\n"
        "    pieces = path.stem.split(' ')\n"
        "    rows.append({\n"
        "        'year': int(pieces[0]),\n"
        "        'book_code': pieces[1],\n"
        "        'text': path.read_text(encoding='utf-8'),\n"
        "    })\n"
        "\n"
        "nietzsche_df = pandas.DataFrame(rows)\n"
        "nietzsche_df[['year', 'book_code']]"
    ),

    code(
        "# Book length in characters, labelled by book code.\n"
        "nietzsche_df['characters'] = nietzsche_df['text'].str.len()\n"
        "\n"
        "plt.figure(figsize=(11, 5))\n"
        "plt.scatter(nietzsche_df['year'], nietzsche_df['characters'])\n"
        "for _, row in nietzsche_df.iterrows():\n"
        "    plt.annotate(row['book_code'], (row['year'], row['characters']), fontsize=9)\n"
        "plt.xlabel('Year')\n"
        "plt.ylabel('Characters')\n"
        "plt.title('Nietzsche book length over time')\n"
        "plt.show()"
    ),

    code(
        "# Tokenise every book. The word pattern handles German letters.\n"
        "nietzsche_tokens = []\n"
        "for text in nietzsche_df['text']:\n"
        "    nietzsche_tokens.append(re.findall(r'\\w+', text.lower()))\n"
        "\n"
        "print(f'{len(nietzsche_tokens[0]):,} tokens in the first book.')"
    ),

    code(
        "# German stopwords ship with nltk. The download is a one-time fetch.\n"
        "nltk.download('stopwords', quiet=True)\n"
        "german_stop = set(nltk.corpus.stopwords.words('german'))\n"
        "print(f'{len(german_stop)} standard German stopwords.')"
    ),

    code(
        "# The standard list misses 19th-century forms. update adds several at once.\n"
        "german_stop.update(['dass', 'mehr', 'immer', 'ja', 'wer', 'sei', 'diess'])\n"
        "print(f'{len(german_stop)} stopwords after adding historic forms.')"
    ),

    code(
        "# Build the document-feature matrix with the extended German stopword set.\n"
        "vectorizer = sklearn.feature_extraction.text.CountVectorizer(\n"
        "    lowercase=True,\n"
        "    stop_words=list(german_stop),\n"
        ")\n"
        "dfm = vectorizer.fit_transform(nietzsche_df['text'])\n"
        "features = vectorizer.get_feature_names_out()\n"
        "print(f'DFM: {dfm.shape[0]} books by {dfm.shape[1]} features.')"
    ),

    code(
        "# Top 20 features across the corpus.\n"
        "totals = dfm.toarray().sum(axis=0)\n"
        "order = totals.argsort()[::-1]\n"
        "for rank in range(20):\n"
        "    word_index = order[rank]\n"
        "    print(f'{features[word_index]:20s}  {totals[word_index]}')"
    ),

    code(
        "# Word cloud of the corpus. Build the frequency dict with an explicit loop.\n"
        "word_freq = {}\n"
        "for word_index, total in enumerate(totals):\n"
        "    word_freq[features[word_index]] = int(total)\n"
        "\n"
        "wc = wordcloud.WordCloud(\n"
        "    width=900,\n"
        "    height=500,\n"
        "    background_color='white',\n"
        "    colormap='Dark2',\n"
        "    random_state=100,\n"
        ").generate_from_frequencies(word_freq)\n"
        "\n"
        "plt.figure(figsize=(11, 6))\n"
        "plt.imshow(wc, interpolation='bilinear')\n"
        "plt.axis('off')\n"
        "plt.title('Nietzsche corpus: top terms')\n"
        "plt.show()"
    ),

    code(
        "# Topic models over the German corpus.\n"
        "lda = sklearn.decomposition.LatentDirichletAllocation(\n"
        "    n_components=8,\n"
        "    random_state=100,\n"
        "    max_iter=20,\n"
        ").fit(dfm)\n"
        "\n"
        "for topic_index, weights in enumerate(lda.components_):\n"
        "    top_indices = weights.argsort()[-10:][::-1]\n"
        "    top_words = []\n"
        "    for word_index in top_indices:\n"
        "        top_words.append(features[word_index])\n"
        "    print(f'Topic {topic_index + 1}: {top_words}')"
    ),

    code(
        "# Hierarchical clustering of the fifteen books. Row-normalise, then dendrogram.\n"
        "dense = dfm.toarray().astype(float)\n"
        "row_totals = dense.sum(axis=1, keepdims=True)\n"
        "row_totals[row_totals == 0] = 1.0\n"
        "normalised = dense / row_totals\n"
        "\n"
        "book_labels = []\n"
        "for _, row in nietzsche_df.iterrows():\n"
        "    book_labels.append(f'{row[\"year\"]} {row[\"book_code\"]}')\n"
        "\n"
        "distances = scipy.spatial.distance.pdist(normalised, metric='euclidean')\n"
        "linkage = scipy.cluster.hierarchy.linkage(distances, method='average')\n"
        "plt.figure(figsize=(13, 5))\n"
        "scipy.cluster.hierarchy.dendrogram(linkage, labels=book_labels, leaf_rotation=45, leaf_font_size=10)\n"
        "plt.title('Nietzsche books: Euclidean distance on normalised token frequency')\n"
        "plt.show()"
    ),

    code(
        "# dispersion_plot shows where a set of word-roots appear within each book, in absolute\n"
        "# token position. A token counts if it starts with any of the prefixes. The grey bar is\n"
        "# the length of the book, and each black mark is one occurrence.\n"
        "def dispersion_plot(prefixes, title):\n"
        "    plt.figure(figsize=(11, 5))\n"
        "    for plot_row, tokens in enumerate(nietzsche_tokens):\n"
        "        plt.hlines(plot_row, 0, len(tokens), color='lightgray', linewidth=6, zorder=1)\n"
        "        marks = []\n"
        "        for token_index, token in enumerate(tokens):\n"
        "            for prefix in prefixes:\n"
        "                if token.startswith(prefix):\n"
        "                    marks.append(token_index)\n"
        "                    break\n"
        "        plt.scatter(marks, [plot_row] * len(marks), marker='|', s=80, color='black', zorder=2)\n"
        "    plt.yticks(range(len(book_labels)), book_labels, fontsize=8)\n"
        "    plt.xlabel('Token index')\n"
        "    plt.title(title)\n"
        "    plt.gca().invert_yaxis()\n"
        "    plt.show()"
    ),

    code(
        "# Shame: scham, schmach, schand.\n"
        "dispersion_plot(['scham', 'schmach', 'schand'], 'Nietzsche on shame')"
    ),

    code(
        "# Virtue: tugend.\n"
        "dispersion_plot(['tugend'], 'Nietzsche on virtue')"
    ),

    code(
        "# Trust and mistrust: vertrau, misstrau.\n"
        "dispersion_plot(['vertrau', 'misstrau'], 'Nietzsche on trust and mistrust')"
    ),

    code(
        "# Culture: kultur, cultur.\n"
        "dispersion_plot(['kultur', 'cultur'], 'Nietzsche on culture')"
    ),

    code(
        "# Load the Nietzsche moral-psychology dictionary with the liwc library. It has 54\n"
        "# categories (virtue, shame, culture, solitude, ...). The library handles the wildcard\n"
        "# matching, including the historic-spelling stems.\n"
        "n_lookup, n_names = liwc.load_token_parser('dictionaries/nietzsche.dic')\n"
        "print(f'{len(n_names)} categories: {n_names[:8]} ...')"
    ),

    code(
        "# count_categories tallies dictionary hits per category for one token list. Reused for\n"
        "# books here and paragraphs later.\n"
        "def count_categories(tokens):\n"
        "    counts = {}\n"
        "    for name in n_names:\n"
        "        counts[name] = 0\n"
        "    for token in tokens:\n"
        "        for name in n_lookup(token):\n"
        "            counts[name] = counts[name] + 1\n"
        "    return counts\n"
        "\n"
        "book_rows = []\n"
        "for original_index, tokens in enumerate(nietzsche_tokens):\n"
        "    counts = count_categories(tokens)\n"
        "    counts['book_code'] = nietzsche_df.iloc[original_index]['book_code']\n"
        "    counts['year'] = nietzsche_df.iloc[original_index]['year']\n"
        "    book_rows.append(counts)\n"
        "\n"
        "book_feature_df = pandas.DataFrame(book_rows)\n"
        "book_feature_df.head(3)"
    ),

    code(
        "# Plot a few moral terms across the books, labelled by book code.\n"
        "for name in ['virtue', 'shame', 'culture']:\n"
        "    if name not in book_feature_df.columns:\n"
        "        continue\n"
        "    ordered = book_feature_df.sort_values('year')\n"
        "    plt.figure(figsize=(11, 3.5))\n"
        "    plt.scatter(ordered['year'], ordered[name])\n"
        "    for _, row in ordered.iterrows():\n"
        "        plt.annotate(row['book_code'], (row['year'], row[name]), fontsize=8)\n"
        "    plt.xlabel('Year')\n"
        "    plt.ylabel(f'{name} count')\n"
        "    plt.title(f'Nietzsche on \"{name}\" across books')\n"
        "    plt.show()"
    ),

    code(
        "# Reshape to paragraphs. Splitting on blank lines turns fifteen long books into thousands\n"
        "# of short documents, so a concept that appears in one paragraph does not register as\n"
        "# co-occurring with concepts elsewhere in the same book.\n"
        "paragraph_rows = []\n"
        "for _, book in nietzsche_df.iterrows():\n"
        "    for paragraph in book['text'].split('\\n\\n'):\n"
        "        cleaned = paragraph.strip()\n"
        "        if len(cleaned) < 50:\n"
        "            continue\n"
        "        paragraph_rows.append({'book_code': book['book_code'], 'text': cleaned})\n"
        "\n"
        "paragraph_df = pandas.DataFrame(paragraph_rows)\n"
        "print(f'{len(paragraph_df)} paragraphs from {len(nietzsche_df)} books.')"
    ),

    code(
        "# Category counts per paragraph, reusing count_categories.\n"
        "paragraph_feature_rows = []\n"
        "for text in paragraph_df['text']:\n"
        "    tokens = re.findall(r'\\w+', text.lower())\n"
        "    paragraph_feature_rows.append(count_categories(tokens))\n"
        "\n"
        "paragraph_feature_df = pandas.DataFrame(paragraph_feature_rows)\n"
        "paragraph_feature_df.head(3)"
    ),

    code(
        "# concept_egonet restricts to paragraphs that mention a concept, then builds the\n"
        "# co-occurrence network among all categories there. The graph is nearly complete, so we\n"
        "# keep only the strongest links and drop categories left isolated. A force-directed\n"
        "# layout shapes the rest; node size grows with frequency and faint edges are weaker.\n"
        "def concept_egonet(concept_name, top_edges=50):\n"
        "    if concept_name not in paragraph_feature_df.columns:\n"
        "        print(f'{concept_name}: not a dictionary category.')\n"
        "        return\n"
        "    subset = paragraph_feature_df[paragraph_feature_df[concept_name] > 0]\n"
        "    if len(subset) < 5:\n"
        "        print(f'{concept_name}: only {len(subset)} paragraphs match.')\n"
        "        return\n"
        "    matrix = subset[n_names].to_numpy()\n"
        "    adjacency = matrix.T @ matrix\n"
        "    graph = networkx.from_numpy_array(adjacency)\n"
        "    relabelling = {}\n"
        "    for node_index, name in enumerate(n_names):\n"
        "        relabelling[node_index] = name\n"
        "    graph = networkx.relabel_nodes(graph, relabelling)\n"
        "    graph.remove_edges_from(list(networkx.selfloop_edges(graph)))\n"
        "    # Rank the edges by weight, keep the strongest, and drop nodes left with none.\n"
        "    ranked_edges = []\n"
        "    for u, v in graph.edges():\n"
        "        ranked_edges.append((graph[u][v]['weight'], u, v))\n"
        "    def by_weight(item):\n"
        "        return item[0]\n"
        "    ranked_edges = sorted(ranked_edges, key=by_weight, reverse=True)\n"
        "    for weight, u, v in ranked_edges[top_edges:]:\n"
        "        graph.remove_edge(u, v)\n"
        "    graph.remove_nodes_from(list(networkx.isolates(graph)))\n"
        "    weights = []\n"
        "    for u, v in graph.edges():\n"
        "        weights.append(graph[u][v]['weight'])\n"
        "    largest = max(weights) if weights else 1\n"
        "    widths = []\n"
        "    edge_colors = []\n"
        "    for weight in weights:\n"
        "        widths.append(weight / largest * 5)\n"
        "        shade = 0.85 - 0.7 * (weight / largest)\n"
        "        edge_colors.append((shade, shade, shade))\n"
        "    category_totals = subset[n_names].sum(axis=0)\n"
        "    biggest = category_totals.max() if category_totals.max() > 0 else 1\n"
        "    node_sizes = []\n"
        "    for node in graph.nodes():\n"
        "        node_sizes.append(250 + category_totals[node] / biggest * 1900)\n"
        "    plt.figure(figsize=(10, 9))\n"
        "    networkx.draw(\n"
        "        graph,\n"
        "        pos=networkx.spring_layout(graph, seed=42, weight='weight'),\n"
        "        with_labels=True,\n"
        "        node_color='lightgray',\n"
        "        node_size=node_sizes,\n"
        "        edge_color=edge_colors,\n"
        "        width=widths,\n"
        "        font_size=8,\n"
        "    )\n"
        "    plt.title(f'Concept egonet: {concept_name} ({len(subset)} paragraphs, top {top_edges} links)')\n"
        "    plt.show()"
    ),

    code(
        "# One worked concept.\n"
        "concept_egonet('virtue')"
    ),

    code(
        "# Several concepts, one call each.\n"
        "for concept in ['shame', 'culture', 'style', 'modesty', 'humility']:\n"
        "    concept_egonet(concept)"
    ),

    code(
        "# split_inside_outside captures the keyword windows around a set of prefixes. Reused for\n"
        "# both kultur and tugend below.\n"
        "def split_inside_outside(tokens, prefixes, window=10):\n"
        "    near_match = [False] * len(tokens)\n"
        "    for index, token in enumerate(tokens):\n"
        "        for prefix in prefixes:\n"
        "            if token.startswith(prefix):\n"
        "                start = max(0, index - window)\n"
        "                end = min(len(tokens), index + window + 1)\n"
        "                for marker in range(start, end):\n"
        "                    near_match[marker] = True\n"
        "                break\n"
        "    inside = []\n"
        "    outside = []\n"
        "    for index, token in enumerate(tokens):\n"
        "        if near_match[index]:\n"
        "            inside.append(token)\n"
        "        else:\n"
        "            outside.append(token)\n"
        "    return inside, outside"
    ),

    code(
        "# keyness_top ranks the words most distinctive of the inside windows by chi-squared.\n"
        "import scipy.stats\n"
        "\n"
        "def keyness_top(inside, outside, top=15):\n"
        "    inside_counts = {}\n"
        "    for token in inside:\n"
        "        inside_counts[token] = inside_counts.get(token, 0) + 1\n"
        "    outside_counts = {}\n"
        "    for token in outside:\n"
        "        outside_counts[token] = outside_counts.get(token, 0) + 1\n"
        "    total_inside = len(inside)\n"
        "    total_outside = len(outside)\n"
        "    scored = []\n"
        "    for word, inside_count in inside_counts.items():\n"
        "        if inside_count < 5:\n"
        "            continue\n"
        "        outside_count = outside_counts.get(word, 0)\n"
        "        table = [[inside_count, total_inside - inside_count], [outside_count, total_outside - outside_count]]\n"
        "        statistic = scipy.stats.chi2_contingency(table).statistic\n"
        "        scored.append((word, statistic))\n"
        "    def sort_key(entry):\n"
        "        return entry[1]\n"
        "    return sorted(scored, key=sort_key, reverse=True)[:top]"
    ),

    code(
        "# Gather kultur windows across the whole corpus and rank their keywords.\n"
        "kultur_inside = []\n"
        "kultur_outside = []\n"
        "for tokens in nietzsche_tokens:\n"
        "    inside, outside = split_inside_outside(tokens, ['kultur', 'cultur'])\n"
        "    kultur_inside.extend(inside)\n"
        "    kultur_outside.extend(outside)\n"
        "\n"
        "print('Keywords inside kultur windows:')\n"
        "for word, statistic in keyness_top(kultur_inside, kultur_outside):\n"
        "    print(f'  {word:18s}  chi-squared {statistic:8.1f}')"
    ),

    code(
        "# The same for tugend.\n"
        "tugend_inside = []\n"
        "tugend_outside = []\n"
        "for tokens in nietzsche_tokens:\n"
        "    inside, outside = split_inside_outside(tokens, ['tugend'])\n"
        "    tugend_inside.extend(inside)\n"
        "    tugend_outside.extend(outside)\n"
        "\n"
        "print('Keywords inside tugend windows:')\n"
        "for word, statistic in keyness_top(tugend_inside, tugend_outside):\n"
        "    print(f'  {word:18s}  chi-squared {statistic:8.1f}')"
    ),

    md(
        "## What we've covered\n"
        "\n"
        "**Python:** `pathlib.Path`, `.glob`, `.read_text`; parsing filenames; building a corpus "
        "from disk; extending a set with `.update`; reusing helper functions across books and "
        "paragraphs; the function-and-loop pattern for concept egonets.\n"
        "\n"
        "**Corpus linguistics:** working in German; custom stopwords for historic spellings; "
        "paragraph-level reshape; concept egonets; bottom-up collocation with keyness across "
        "morphological roots."
    ),

    md(
        "## Read more\n"
        "\n"
        "- **NLTK multilingual stopwords**: [https://www.nltk.org/howto/corpus.html#stopwords]("
        "https://www.nltk.org/howto/corpus.html#stopwords).\n"
        "- **pathlib**: [https://docs.python.org/3/library/pathlib.html]("
        "https://docs.python.org/3/library/pathlib.html).\n"
        "- **NetworkX layouts**: [https://networkx.org/documentation/stable/reference/drawing.html"
        "#module-networkx.drawing.layout]("
        "https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout).\n"
        "- **scipy.stats.chi2_contingency**: [https://docs.scipy.org/doc/scipy/reference/"
        "generated/scipy.stats.chi2_contingency.html]("
        "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html)."
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
