"""Tests for scratch/corpus_tools.liwcalike.

Hand-computed against the quanteda.dictionaries::liwcalike formulas
(kbenoit/quanteda.dictionaries R/liwcalike.R). Percentages are checked on a
tiny corpus and dictionary so every expected value can be derived by hand.

Run via: uv run pytest scratch/test_corpus_tools.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus_tools import liwcalike


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
