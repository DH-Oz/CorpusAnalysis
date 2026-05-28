"""Build scratch/1-sotu-first-look.ipynb.

Atomicity matches a typical literate-Python lesson at this scale: roughly one
code cell per teaching beat. Boilerplate that would otherwise repeat is
factored into a helper function defined once. Prose lives as comment blocks
at the top of each code cell, kept declarative and short.

Re-run from the repo root: `uv run python scratch/_build_rmd1.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.notebook_cells import append_cells

NOTEBOOK = "scratch/1-sotu-first-look.ipynb"


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
        "# Corpus Masterclass 1: A First Look at the State of the Union Corpus\n"
        "\n"
        "Each code cell below is one teaching beat. Press **Shift+Enter** to run it."
    ),

    md(
        "## Today's goal\n"
        "\n"
        "1. Load every State of the Union address (1790 to 2026) into a pandas DataFrame.\n"
        "2. Look at individual speeches; summarise the metadata.\n"
        "3. Plot speech length across two centuries, coloured by party.\n"
        "4. Build a document-feature matrix: counts of every word in every speech.\n"
        "5. Draw a word cloud of the most frequent corpus-wide terms.\n"
        "6. Discover hidden topics with Latent Dirichlet Allocation.\n"
        "7. Find each speech's most distinctive words.\n"
        "8. Draw hierarchical-clustering dendrograms; vary the metric and the time slice.\n"
        "9. Compare word clouds across presidential eras."
    ),

    code(
        "# Libraries used throughout the notebook.\n"
        "import sotu\n"
        "import pandas\n"
        "import numpy\n"
        "import matplotlib.pyplot as plt\n"
        "import sklearn.feature_extraction.text\n"
        "import sklearn.decomposition\n"
        "import scipy.spatial.distance\n"
        "import scipy.cluster.hierarchy\n"
        "import wordcloud\n"
        "\n"
        "print('Libraries imported.')"
    ),

    code(
        "# The sotu library exposes every U.S. State of the Union address from 1790 to 2026 as a\n"
        "# pandas DataFrame. Each row is one speech.\n"
        "df = sotu.load()\n"
        "print(f'{len(df)} speeches, {df[\"year\"].min()} to {df[\"year\"].max()}.')\n"
        "df[['year', 'president', 'party', 'sotu_type']].head(3)"
    ),

    code(
        "# Same data, the most recent few addresses.\n"
        "df[['year', 'president', 'party', 'sotu_type']].tail(3)"
    ),

    code(
        "# Washington's first address. The text column holds the full speech as a single string.\n"
        "first = df.iloc[0]\n"
        "print(f'{first[\"year\"]} {first[\"president\"]}')\n"
        "print(first['text'][:600] + ' ...')"
    ),

    code(
        "# Washington's second address.\n"
        "second = df.iloc[1]\n"
        "print(f'{second[\"year\"]} {second[\"president\"]}')\n"
        "print(second['text'][:600] + ' ...')"
    ),

    code(
        "# Metadata at a glance: column names and types.\n"
        "df.dtypes"
    ),

    code(
        "# How many speeches per party.\n"
        "df['party'].value_counts()"
    ),

    code(
        "# Speech length per address: tokens approximated by whitespace splitting.\n"
        "df['tokens'] = df['text'].str.split().str.len()\n"
        "df[['year', 'president', 'tokens']].head(5)"
    ),

    code(
        "# Length across two centuries. A single line follows the speeches in year order,\n"
        "# and the points are coloured by party. Drawing one line per party instead would\n"
        "# connect speeches across the decades between a party's terms, inventing trends\n"
        "# that are not there.\n"
        "by_year = df.sort_values('year')\n"
        "plt.figure(figsize=(13, 5))\n"
        "plt.plot(by_year['year'], by_year['tokens'], color='grey', linewidth=0.6, zorder=1)\n"
        "for party in df['party'].unique():\n"
        "    party_speeches = df[df['party'] == party]\n"
        "    plt.scatter(party_speeches['year'], party_speeches['tokens'], s=18, label=party, zorder=2)\n"
        "plt.xlabel('Year')\n"
        "plt.ylabel('Tokens')\n"
        "plt.title('State of the Union address length, 1790 to 2026')\n"
        "plt.legend(loc='upper left', fontsize=9, ncol=2)\n"
        "plt.show()"
    ),

    code(
        "# A document-feature matrix (DFM) holds the count of every word in every document.\n"
        "# sklearn.feature_extraction.text.CountVectorizer builds it in one call, with English\n"
        "# stop-word removal built in.\n"
        "vectorizer = sklearn.feature_extraction.text.CountVectorizer(\n"
        "    lowercase=True,\n"
        "    stop_words='english',\n"
        ")\n"
        "dfm = vectorizer.fit_transform(df['text'])\n"
        "features = vectorizer.get_feature_names_out()\n"
        "labels = (df['year'].astype(str) + ' ' + df['president']).tolist()\n"
        "\n"
        "print(f'DFM: {dfm.shape[0]} speeches by {dfm.shape[1]} unique features.')"
    ),

    code(
        "# Top 20 features across the whole corpus.\n"
        "dfm_df = pandas.DataFrame(dfm.toarray(), index=labels, columns=features)\n"
        "corpus_totals = dfm_df.sum(axis=0).sort_values(ascending=False)\n"
        "corpus_totals.head(20)"
    ),

    code(
        "# Word cloud of the corpus-wide top terms.\n"
        "wc = wordcloud.WordCloud(\n"
        "    width=900,\n"
        "    height=500,\n"
        "    background_color='white',\n"
        "    colormap='Dark2',\n"
        "    random_state=42,\n"
        ").generate_from_frequencies(corpus_totals.to_dict())\n"
        "\n"
        "plt.figure(figsize=(10, 5))\n"
        "plt.imshow(wc, interpolation='bilinear')\n"
        "plt.axis('off')\n"
        "plt.title('State of the Union: top terms (1790 to 2026)')\n"
        "plt.show()"
    ),

    code(
        "# Latent Dirichlet Allocation finds clusters of words that tend to co-occur across\n"
        "# documents. Each cluster is a topic; each speech is a mixture of topics.\n"
        "lda = sklearn.decomposition.LatentDirichletAllocation(\n"
        "    n_components=8,\n"
        "    random_state=42,\n"
        "    max_iter=20,\n"
        ").fit(dfm)\n"
        "\n"
        "topics = {}\n"
        "for topic_index, weights in enumerate(lda.components_):\n"
        "    top_indices = weights.argsort()[-10:][::-1]\n"
        "    top_words = []\n"
        "    for word_index in top_indices:\n"
        "        top_words.append(features[word_index])\n"
        "    topics[f'Topic {topic_index + 1}'] = top_words\n"
        "\n"
        "pandas.DataFrame(topics)"
    ),

    code(
        "# Top 10 words for each of the first three individual speeches.\n"
        "for row_index in range(3):\n"
        "    top = dfm_df.iloc[row_index].sort_values(ascending=False).head(10)\n"
        "    print(f'\\n{labels[row_index]}:')\n"
        "    for word, count in top.items():\n"
        "        print(f'    {word}: {int(count)}')"
    ),

    code(
        "# Row-normalisation: divide each row by its total so long speeches do not dominate\n"
        "# pairwise distances. After this every row sums to 1.\n"
        "dfm_dense = dfm.toarray().astype(float)\n"
        "row_totals = dfm_dense.sum(axis=1, keepdims=True)\n"
        "row_totals[row_totals == 0] = 1.0\n"
        "normalised = dfm_dense / row_totals\n"
        "print(f'Row-sum range: {normalised.sum(axis=1).min():.3f} to {normalised.sum(axis=1).max():.3f}')"
    ),

    code(
        "# Helper. Given a matrix slice and labels, draw the hierarchical-clustering\n"
        "# dendrogram. The metric and title vary; everything else is the same.\n"
        "def render_dendrogram(matrix, leaf_labels, metric, title, figsize=(14, 6), leaf_font_size=7):\n"
        "    distances = scipy.spatial.distance.pdist(matrix, metric=metric)\n"
        "    linkage = scipy.cluster.hierarchy.linkage(distances, method='average')\n"
        "    plt.figure(figsize=figsize)\n"
        "    scipy.cluster.hierarchy.dendrogram(\n"
        "        linkage,\n"
        "        labels=leaf_labels,\n"
        "        leaf_rotation=90,\n"
        "        leaf_font_size=leaf_font_size,\n"
        "    )\n"
        "    plt.title(title)\n"
        "    plt.show()"
    ),

    code(
        "# Every speech, Euclidean distance. With 240+ leaves the labels are tiny; the shape\n"
        "# of the tree is what matters at this scale.\n"
        "render_dendrogram(\n"
        "    normalised,\n"
        "    labels,\n"
        "    metric='euclidean',\n"
        "    title='State of the Union, 1790 to 2026: Euclidean distance',\n"
        "    figsize=(22, 7),\n"
        "    leaf_font_size=4,\n"
        ")"
    ),

    code(
        "# Modern subset, Euclidean distance.\n"
        "modern_mask = (df['year'] >= 1977).to_numpy()\n"
        "modern_matrix = normalised[modern_mask]\n"
        "modern_labels = []\n"
        "for label, keep in zip(labels, modern_mask):\n"
        "    if keep:\n"
        "        modern_labels.append(label)\n"
        "\n"
        "render_dendrogram(\n"
        "    modern_matrix,\n"
        "    modern_labels,\n"
        "    metric='euclidean',\n"
        "    title='Modern State of the Union (1977+): Euclidean distance',\n"
        ")"
    ),

    code(
        "# Same modern subset, cosine distance. Cosine measures the angle between two count\n"
        "# vectors and ignores their magnitude.\n"
        "render_dendrogram(\n"
        "    modern_matrix,\n"
        "    modern_labels,\n"
        "    metric='cosine',\n"
        "    title='Modern State of the Union (1977+): cosine distance',\n"
        ")"
    ),

    code(
        "# Founders era, Euclidean distance.\n"
        "founders_mask = (df['year'] < 1850).to_numpy()\n"
        "founders_matrix = normalised[founders_mask]\n"
        "founders_labels = []\n"
        "for label, keep in zip(labels, founders_mask):\n"
        "    if keep:\n"
        "        founders_labels.append(label)\n"
        "\n"
        "render_dendrogram(\n"
        "    founders_matrix,\n"
        "    founders_labels,\n"
        "    metric='euclidean',\n"
        "    title='Founders-era State of the Union (pre-1850): Euclidean distance',\n"
        "    figsize=(18, 6),\n"
        "    leaf_font_size=6,\n"
        ")"
    ),

    code(
        "# Founders era, cosine distance. Compare the four dendrograms above and ask which\n"
        "# pairs of speeches consistently cluster together regardless of metric and time slice.\n"
        "render_dendrogram(\n"
        "    founders_matrix,\n"
        "    founders_labels,\n"
        "    metric='cosine',\n"
        "    title='Founders-era State of the Union (pre-1850): cosine distance',\n"
        "    figsize=(18, 6),\n"
        "    leaf_font_size=6,\n"
        ")"
    ),

    code(
        "# Helper for the comparison-wordcloud beats. Takes one or more speaker names and lays\n"
        "# their first few addresses out as a grid of clouds.\n"
        "def comparison_clouds(speakers, take=4):\n"
        "    if isinstance(speakers, str):\n"
        "        speakers = [speakers]\n"
        "    rows = []\n"
        "    for name in speakers:\n"
        "        for _, row in df[df['president'] == name].head(take).iterrows():\n"
        "            rows.append(row)\n"
        "    if not rows:\n"
        "        print(f'No matches for {speakers!r}')\n"
        "        return\n"
        "    cols = 2 if len(speakers) == 1 else 4\n"
        "    nrows = int(numpy.ceil(len(rows) / cols))\n"
        "    fig, axes = plt.subplots(nrows, cols, figsize=(11, 3.2 * nrows))\n"
        "    flat = axes.flatten() if hasattr(axes, 'flatten') else [axes]\n"
        "    for ax, row in zip(flat, rows):\n"
        "        wc_local = wordcloud.WordCloud(\n"
        "            width=500,\n"
        "            height=350,\n"
        "            background_color='white',\n"
        "            colormap='tab10',\n"
        "            random_state=42,\n"
        "            stopwords=wordcloud.STOPWORDS,\n"
        "        ).generate(row['text'])\n"
        "        ax.imshow(wc_local, interpolation='bilinear')\n"
        "        ax.set_title(f'{row[\"year\"]} {row[\"president\"]}', fontsize=10)\n"
        "        ax.axis('off')\n"
        "    for ax in flat[len(rows):]:\n"
        "        ax.axis('off')\n"
        "    plt.tight_layout()\n"
        "    plt.show()"
    ),

    code(
        "# Washington's first four addresses.\n"
        "comparison_clouds('Washington')"
    ),

    code(
        "# Adams and Jefferson side by side.\n"
        "comparison_clouds(['Adams', 'Jefferson'])"
    ),

    code(
        "# Obama and Trump side by side.\n"
        "comparison_clouds(['Obama', 'Trump'])"
    ),

    md(
        "## What we've covered\n"
        "\n"
        "**Python:** library imports, pandas DataFrame inspection and column assignment, "
        "boolean masking, `for` loops, defining functions with default arguments, f-strings, "
        "matplotlib subplots.\n"
        "\n"
        "**Corpus linguistics:** loading a built-in corpus; document-feature matrix; English "
        "stop-word filtering; corpus-wide vs per-document top features; word clouds; Latent "
        "Dirichlet Allocation for topic discovery; hierarchical clustering with Euclidean and "
        "cosine distance; dendrograms; comparison word clouds across presidential eras."
    ),

    md(
        "## Read more\n"
        "\n"
        "- **NLTK Book**, Chapter 1: [https://www.nltk.org/book/ch01.html]("
        "https://www.nltk.org/book/ch01.html).\n"
        "- **scikit-learn user guide on text feature extraction**: [https://scikit-learn.org/"
        "stable/modules/feature_extraction.html]("
        "https://scikit-learn.org/stable/modules/feature_extraction.html).\n"
        "- **scikit-learn user guide on Latent Dirichlet Allocation**: [https://scikit-learn.org/"
        "stable/modules/decomposition.html#latent-dirichlet-allocation-lda]("
        "https://scikit-learn.org/stable/modules/decomposition.html#latent-dirichlet-allocation-lda).\n"
        "- **scipy hierarchical clustering**: [https://docs.scipy.org/doc/scipy/reference/"
        "cluster.hierarchy.html](https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html).\n"
        "- **matplotlib pyplot tutorial**: [https://matplotlib.org/stable/tutorials/pyplot.html]("
        "https://matplotlib.org/stable/tutorials/pyplot.html).\n"
        "- **wordcloud README**: [https://github.com/amueller/word_cloud]("
        "https://github.com/amueller/word_cloud).\n"
        "- **matplotlib named colormaps**: [https://matplotlib.org/stable/tutorials/colors/"
        "colormaps.html](https://matplotlib.org/stable/tutorials/colors/colormaps.html)."
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
