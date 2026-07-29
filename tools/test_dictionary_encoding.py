"""The German dictionary must survive whatever encoding the machine prefers.

`liwc.load_token_parser` opens the .dic file with no encoding, so Python falls back
to the machine's locale. Where that is not UTF-8, the UTF-8 bytes of `niederträch*`
are read as `niedertrÃ¤ch*`. Nothing raises. The pattern simply stops matching, and
every German category carrying an umlaut silently counts zero. `corpus_tools`
supplies its own reader that names UTF-8 explicitly.

These tests assert behaviour rather than implementation, so they fail if anyone
routes the notebooks back through the library's reader, and they say out loud which
platform and encoding they actually ran under. A matrix leg that does not report the
environment it got is a claim, not evidence.
"""

import locale
import platform
import sys
from pathlib import Path

import pytest

from corpus_tools import load_token_parser

GERMAN_DICTIONARY = Path(__file__).resolve().parent.parent / "dictionaries" / "nietzsche.dic"

# Terms carrying an umlaut, with the category each belongs to. Read off the .dic file
# by eye rather than by the code under test, so the expectation is independent of it.
UMLAUT_TERMS = [
    ("niederträchtig", "base"),
    ("schnöde", "base"),
    ("gefühle", "emotion"),
]


def test_reports_the_environment_it_ran_under():
    """Not a gate. This makes the matrix leg say what it actually got."""
    print(
        f"\n  platform: {platform.system()} {platform.machine()}"
        f"\n  python: {sys.version.split()[0]}"
        f"\n  sys.flags.utf8_mode: {sys.flags.utf8_mode}"
        f"\n  locale.getencoding(): {locale.getencoding()}"
    )
    with open(GERMAN_DICTIONARY, encoding="utf-8") as handle:
        handle.read(1)
    # What an unqualified open() would have chosen here, which is the whole risk.
    with open(GERMAN_DICTIONARY) as handle:
        print(f"  a bare open() on this machine chooses: {handle.encoding}")


def test_the_dictionary_really_contains_non_ascii():
    """If this file ever became pure ASCII the tests below could not fail."""
    raw = GERMAN_DICTIONARY.read_bytes()
    non_ascii = [byte for byte in raw if byte > 127]
    assert non_ascii, (
        "nietzsche.dic has no non-ASCII bytes, so the encoding tests below have "
        "nothing to detect and must be reconsidered rather than trusted."
    )


@pytest.mark.parametrize("term,expected_category", UMLAUT_TERMS)
def test_umlaut_terms_still_match(term, expected_category):
    parse_token, _ = load_token_parser(str(GERMAN_DICTIONARY))
    categories = list(parse_token(term))
    assert expected_category in categories, (
        f"{term!r} matched {categories}, expected {expected_category!r}. "
        f"This is what a non-UTF-8 read looks like: no error, no match. "
        f"locale.getencoding() here is {locale.getencoding()}."
    )


def test_category_count_is_stable():
    _, category_names = load_token_parser(str(GERMAN_DICTIONARY))
    assert len(category_names) == 54, (
        f"nietzsche.dic parsed to {len(category_names)} categories, expected 54."
    )
