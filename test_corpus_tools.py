"""Tests for corpus_tools.liwcalike.

Hand-computed against the quanteda.dictionaries::liwcalike formulas
(kbenoit/quanteda.dictionaries R/liwcalike.R). Percentages are checked on a
tiny corpus and dictionary so every expected value can be derived by hand.

Run via: uv run pytest test_corpus_tools.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus_tools import comparison_cloud, distinctive_terms, liwcalike


def write_dic(tmp_path: Path, body: str) -> str:
    path = tmp_path / "tiny.dic"
    path.write_text(body, encoding="utf-8")
    return str(path)


# brave -> virtue, honest -> virtue, greed* -> vice (wildcard prefix).
TWO_CATEGORY_DIC = (
    "%\n"
    "1\tvirtue\n"
    "2\tvice\n"
    "%\n"
    "brave\t1\n"
    "honest\t1\n"
    "greed*\t2\n"
)


def test_columns_follow_the_spec_order(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Brave and honest leaders."], ["docA"], dic)
    assert list(result.columns) == [
        "docname", "WC", "WPS", "Sixltr", "Dic", "virtue", "vice",
    ]


def test_word_count_excludes_punctuation(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Brave and honest leaders."], ["docA"], dic)
    assert result.loc[0, "WC"] == 4


def test_category_percentage_is_count_over_word_count(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Brave and honest leaders."], ["docA"], dic)
    # brave + honest = 2 virtue hits over 4 words.
    assert result.loc[0, "virtue"] == 50.0
    assert result.loc[0, "vice"] == 0.0


def test_dic_equals_sum_of_category_percentages(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Brave and honest leaders."], ["docA"], dic)
    assert result.loc[0, "Dic"] == 50.0


def test_sixltr_counts_words_strictly_longer_than_six(tmp_path):
    # "honest" is exactly six letters and must NOT count; "leaders" (7) must.
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Brave and honest leaders."], ["docA"], dic)
    assert result.loc[0, "Sixltr"] == 25.0


def test_wps_counts_sentences_by_terminal_punctuation(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Greedy, greedier, and greed! Honesty?"], ["docB"], dic)
    # five word tokens, two sentences (! and ?).
    assert result.loc[0, "WC"] == 5
    assert result.loc[0, "WPS"] == 2.5


def test_wildcard_matches_prefix_only(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["Greedy, greedier, and greed! Honesty?"], ["docB"], dic)
    # greedy, greedier, greed all match greed*; honesty does NOT match honest.
    assert result.loc[0, "vice"] == 60.0
    assert result.loc[0, "virtue"] == 0.0


def test_token_in_two_categories_counts_in_both(tmp_path):
    body = (
        "%\n"
        "1\tvirtue\n"
        "2\tvice\n"
        "%\n"
        "proud\t1\t2\n"
    )
    dic = write_dic(tmp_path, body)
    result = liwcalike(["Proud."], ["docC"], dic)
    assert result.loc[0, "virtue"] == 100.0
    assert result.loc[0, "vice"] == 100.0
    # Dic counts the token once per category, matching quanteda's tokens_lookup.
    assert result.loc[0, "Dic"] == 200.0


def test_one_row_per_document(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(
        ["Brave and honest leaders.", "Greedy, greedier, and greed!"],
        ["docA", "docB"],
        dic,
    )
    assert len(result) == 2
    assert list(result["docname"]) == ["docA", "docB"]


def test_empty_document_yields_zero_without_error(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["!!!"], ["empty"], dic)
    assert result.loc[0, "WC"] == 0
    assert result.loc[0, "WPS"] == 0.0
    assert result.loc[0, "Sixltr"] == 0.0
    assert result.loc[0, "Dic"] == 0.0
    assert result.loc[0, "virtue"] == 0.0


def test_tolower_false_is_case_sensitive(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    # With tolower=False, capitalised "Brave" does not match the lowercase entry.
    result = liwcalike(["Brave brave"], ["docD"], dic, tolower=False)
    assert result.loc[0, "virtue"] == 50.0


def test_default_rounding_is_two_digits(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    # one virtue hit over three words -> 33.333... -> 33.33.
    result = liwcalike(["brave the day"], ["docE"], dic)
    assert result.loc[0, "virtue"] == 33.33


def test_digits_argument_controls_rounding(tmp_path):
    dic = write_dic(tmp_path, TWO_CATEGORY_DIC)
    result = liwcalike(["brave the day"], ["docE"], dic, digits=1)
    assert result.loc[0, "virtue"] == 33.3


def test_distinctive_terms_assigns_each_term_to_its_peak_document():
    # doc0 favours 'a' (rate 0.75 vs mean 0.5), doc1 favours 'b'; each peak is 0.25.
    freqs = distinctive_terms(numpy.array([[3, 1], [1, 3]]), ["a", "b"])
    assert freqs == [{"a": 0.25}, {"b": 0.25}]


def test_distinctive_terms_drops_terms_with_no_positive_difference():
    # Both terms occur equally in both documents, so neither is distinctive.
    freqs = distinctive_terms(numpy.array([[2, 2], [2, 2]]), ["a", "b"])
    assert freqs == [{}, {}]


def test_distinctive_terms_handles_a_document_only_term():
    freqs = distinctive_terms(numpy.array([[4, 0], [0, 4]]), ["a", "b"])
    assert freqs == [{"a": 0.5}, {"b": 0.5}]


def test_comparison_cloud_runs_without_error():
    matrix = numpy.array([[5, 1, 0, 2], [0, 1, 5, 2]])
    features = ["alpha", "beta", "gamma", "delta"]
    comparison_cloud(matrix, features, ["doc one", "doc two"], size=200, max_words=8)
    import matplotlib.pyplot as plt

    plt.close("all")
