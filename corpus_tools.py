"""liwcalike: per-document dictionary percentages, in the style of R's
quanteda.dictionaries::liwcalike.

A dictionary tags words with the categories they belong to. liwcalike applies
one to a collection of documents and returns a table with one row per document.
Each category column holds the percentage of that document's words that fall in
the category, so long speeches and short speeches can be compared directly.

This module ships beside the notebooks. The notebooks import it with
`from corpus_tools import liwcalike`.

Columns returned, in order:

- docname: the name passed in for the document.
- WC: word count. Words are runs of word characters, found with the same
  `re.findall(r"\\w+", ...)` pattern the notebooks use, so punctuation is not
  counted.
- WPS: words per sentence. Sentences are counted as runs of '.', '!', or '?'.
- Sixltr: percentage of words longer than six letters.
- Dic: percentage of word matches that land in any category. A word counts once
  for each category it belongs to, so Dic is the sum of the category columns.
- one column per dictionary category: the category's percentage of word count.

Percentage columns are rounded to `digits` places (2 by default). WC and WPS are
left unrounded, matching the R function.

The category matching is done by the `liwc` library, which reads the LIWC file
format and handles the trailing-'*' wildcard. We add only the per-document
normalisation that R's liwcalike performs.

This module also provides comparison_cloud, an R-style comparison word cloud
(R's textplot_wordcloud(comparison = TRUE)), built on the same wordcloud library.
"""

# This repo-root file is the single source. Copies sit beside each notebook in
# day-N/ and are generated from this one by tools/sync_corpus_tools.py. Edit only
# this file; never edit a day-N copy.

import re

import liwc
import matplotlib
import matplotlib.pyplot as plt
import networkx
import numpy
import pandas
import wordcloud


def liwcalike(texts, docnames, dictionary_path, tolower=True, digits=2):
    """Return a per-document dictionary-percentage table as a DataFrame.

    texts and docnames are equal-length lists. dictionary_path points at a
    LIWC-format .dic file. tolower lowercases each document before matching.
    """
    token_categories, category_names = liwc.load_token_parser(dictionary_path)

    rows = []
    for document_index, text in enumerate(texts):
        if tolower:
            tokens = re.findall(r"\w+", text.lower())
        else:
            tokens = re.findall(r"\w+", text)
        word_count = len(tokens)

        # Sentences are runs of terminal punctuation. A document with none is
        # treated as a single sentence.
        sentence_count = len(re.findall(r"[.!?]+", text))
        if sentence_count == 0:
            sentence_count = 1

        # Long words: strictly more than six letters.
        long_words = 0
        for token in tokens:
            if len(token) > 6:
                long_words = long_words + 1

        # Tally dictionary hits. A token adds to every category it matches.
        category_counts = {}
        for name in category_names:
            category_counts[name] = 0
        dictionary_hits = 0
        for token in tokens:
            for name in token_categories(token):
                category_counts[name] = category_counts[name] + 1
                dictionary_hits = dictionary_hits + 1

        row = {}
        row["docname"] = docnames[document_index]
        row["WC"] = word_count
        if word_count == 0:
            row["WPS"] = 0.0
            row["Sixltr"] = 0.0
            row["Dic"] = 0.0
            for name in category_names:
                row[name] = 0.0
        else:
            row["WPS"] = word_count / sentence_count
            row["Sixltr"] = round(long_words / word_count * 100, digits)
            row["Dic"] = round(dictionary_hits / word_count * 100, digits)
            for name in category_names:
                row[name] = round(category_counts[name] / word_count * 100, digits)
        rows.append(row)

    column_order = ["docname", "WC", "WPS", "Sixltr", "Dic"]
    for name in category_names:
        column_order.append(name)

    table = pandas.DataFrame(rows)
    table = table[column_order]
    return table


def distinctive_terms(matrix, features):
    """For each document, the terms most distinctive of it.

    matrix is an (n_documents x n_terms) count array; features names the terms.
    A term's distinctiveness for a document is its rate there minus the term's
    mean rate across all the documents. Each term is assigned to the one
    document where that difference is largest. Returns a list with one dict per
    document, mapping each of its distinctive terms to its (positive)
    distinctiveness; terms with no positive difference anywhere are dropped.
    """
    n_documents = matrix.shape[0]
    rates = matrix.astype(float)
    totals = rates.sum(axis=1, keepdims=True)
    totals[totals == 0] = 1.0
    rates = rates / totals
    mean_rates = rates.mean(axis=0)
    deviations = rates - mean_rates
    assigned = deviations.argmax(axis=0)
    peak = deviations.max(axis=0)

    document_freqs = []
    for _ in range(n_documents):
        document_freqs.append({})
    for term_index in range(len(features)):
        if peak[term_index] > 0:
            document_freqs[assigned[term_index]][features[term_index]] = float(peak[term_index])
    return document_freqs


def comparison_cloud(matrix, features, labels, size=900, max_words=60):
    """Draw an R-style comparison word cloud: a disc split into wedges.

    matrix is an (n_documents x n_terms) count array; features names the terms
    and labels names the documents. The disc is divided into one angular wedge
    per document, and each wedge holds the terms most distinctive of that
    document. Distinctiveness is the term's rate in the document minus the
    term's mean rate across all the documents; term size grows with it, and the
    wedge colour identifies the document.

    This mirrors R's textplot_wordcloud(comparison = TRUE). The wordcloud library
    packs the words; we add the per-document wedge masks and the rim labels.
    """
    n_documents = matrix.shape[0]
    document_freqs = distinctive_terms(matrix, features)

    # Geometry: split the disc into equal wedges; each term packs into its wedge.
    centre = size / 2.0
    radius = size / 2.0 - 60
    grid_y, grid_x = numpy.mgrid[0:size, 0:size]
    angle = numpy.arctan2(-(grid_y - centre), grid_x - centre)
    angle = numpy.mod(angle, 2 * numpy.pi)
    distance = numpy.sqrt((grid_x - centre) ** 2 + (grid_y - centre) ** 2)
    wedge = 2 * numpy.pi / n_documents
    sector = numpy.floor(angle / wedge).astype(int)

    palette = matplotlib.colormaps["tab10"]
    plt.figure(figsize=(8, 8))
    axes = plt.gca()
    for document_index in range(n_documents):
        if len(document_freqs[document_index]) == 0:
            continue
        inside = (sector == document_index) & (distance < radius)
        mask = numpy.full((size, size), 255, dtype=numpy.uint8)
        mask[inside] = 0  # black marks the drawable wedge; white is masked out

        red, green, blue = palette(document_index % 10)[0:3]
        rgb = (int(red * 255), int(green * 255), int(blue * 255))

        def one_colour(*args, colour=rgb, **kwargs):
            return colour

        cloud = wordcloud.WordCloud(
            mask=mask,
            background_color=None,
            mode="RGBA",
            max_words=max_words,
            prefer_horizontal=0.95,
            relative_scaling=0.5,
            color_func=one_colour,
        ).generate_from_frequencies(document_freqs[document_index])
        axes.imshow(cloud, interpolation="bilinear")

        middle = (document_index + 0.5) * wedge
        label_x = centre + (radius + 30) * numpy.cos(middle)
        label_y = centre - (radius + 30) * numpy.sin(middle)
        axes.text(
            label_x,
            label_y,
            labels[document_index],
            color=(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255),
            fontsize=10,
            ha="center",
            va="center",
            fontweight="bold",
        )
    axes.set_xlim(0, size)
    axes.set_ylim(size, 0)
    axes.axis("off")
    plt.tight_layout()
    plt.show()


def cooccurrence_graph(counts, labels, top_edges=40):
    """Build a category co-occurrence graph and keep its strongest links.

    counts is an (n_documents x n_categories) array of non-negative values;
    labels names the categories. The co-occurrence weight between two categories
    is the matrix product counts.T @ counts: it grows with how often, and how
    strongly, the pair turns up in the same documents. This is the same feature
    co-occurrence matrix R's quanteda builds with fcm().

    Self-loops are dropped, only the `top_edges` heaviest links are kept, and any
    category left with no links is removed. Returns a networkx.Graph whose nodes
    are label strings and whose edges carry a 'weight'.
    """
    matrix = numpy.asarray(counts, dtype=float)
    adjacency = matrix.T @ matrix
    graph = networkx.from_numpy_array(adjacency)

    relabelling = {}
    for node_index in range(len(labels)):
        relabelling[node_index] = labels[node_index]
    graph = networkx.relabel_nodes(graph, relabelling)

    graph.remove_edges_from(list(networkx.selfloop_edges(graph)))

    # Rank the edges by weight, keep the strongest, and drop the rest.
    ranked_edges = []
    for u, v in graph.edges():
        ranked_edges.append((graph[u][v]["weight"], u, v))

    def by_weight(item):
        return item[0]

    ranked_edges = sorted(ranked_edges, key=by_weight, reverse=True)
    for weight, u, v in ranked_edges[top_edges:]:
        graph.remove_edge(u, v)

    graph.remove_nodes_from(list(networkx.isolates(graph)))
    return graph


def draw_cooccurrence_network(counts, labels, top_edges=40, node_color="lightyellow", title=""):
    """Draw the category co-occurrence network for a set of documents.

    counts is an (n_documents x n_categories) array; labels names the categories.
    The graph comes from cooccurrence_graph. Each node is sized by how often its
    category appears across the documents; each edge is widened and darkened by
    its co-occurrence weight. A fresh force-directed layout is computed every
    call. Nothing is drawn when no co-occurrences survive the pruning.
    """
    graph = cooccurrence_graph(counts, labels, top_edges)
    if graph.number_of_nodes() == 0:
        print("No co-occurrences to display.")
        return

    matrix = numpy.asarray(counts, dtype=float)
    category_totals = {}
    for column_index in range(len(labels)):
        category_totals[labels[column_index]] = matrix[:, column_index].sum()
    biggest = max(category_totals.values())
    if biggest <= 0:
        biggest = 1.0
    node_sizes = []
    for node in graph.nodes():
        node_sizes.append(300 + category_totals[node] / biggest * 1900)

    weights = []
    for u, v in graph.edges():
        weights.append(graph[u][v]["weight"])
    largest = max(weights) if weights else 1
    widths = []
    edge_colors = []
    for weight in weights:
        widths.append(weight / largest * 5)
        shade = 0.85 - 0.7 * (weight / largest)
        edge_colors.append((shade, shade, shade))

    plt.figure(figsize=(9, 8))
    networkx.draw(
        graph,
        pos=networkx.spring_layout(graph, seed=42, weight="weight"),
        with_labels=True,
        node_color=node_color,
        node_size=node_sizes,
        edge_color=edge_colors,
        width=widths,
        font_size=8,
    )
    plt.title(title)
    plt.show()


def dispersion_plot(labels, lengths, positions, title, mark_size=100):
    """Draw a lexical-dispersion plot, one row per document.

    labels, lengths, and positions are equal-length lists. For row i a grey bar
    runs from 0 to lengths[i] (the document's token count) and a black tick is
    drawn at each token index in positions[i] (every occurrence being traced).
    Rows read top to bottom in the order given.
    """
    plt.figure(figsize=(11, max(2.5, 0.30 * len(labels))))
    for plot_row in range(len(labels)):
        plt.hlines(plot_row, 0, lengths[plot_row], color="lightgray", linewidth=6, zorder=1)
        marks = positions[plot_row]
        plt.scatter(marks, [plot_row] * len(marks), marker="|", s=mark_size, color="black", zorder=2)
    plt.yticks(range(len(labels)), labels, fontsize=7)
    plt.xlabel("Token index")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
