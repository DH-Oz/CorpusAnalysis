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
"""

import re

import liwc
import pandas


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
