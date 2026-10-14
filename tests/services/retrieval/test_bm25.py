"""Syllable tokens and Okapi BM25, checked by hand on small texts."""
import math
import unicodedata

import pytest

from appota_kb.services.retrieval.bm25 import bm25_scores, tokens


def test_tokens_normalises_and_lowercases():
    assert tokens(unicodedata.normalize("NFD", "nghỉ")) == tokens("nghỉ")
    assert tokens("Leave NĂM") == ["leave", "năm"]
    assert tokens("a.b,c?") == ["a", "b", "c"]
    assert tokens("nghỉ") == ["nghỉ"]
    assert tokens("nghỉ") != tokens("nghi")


def test_bm25_two_texts_checked_by_hand():
    # k1 = 1, b = 0 collapses to score = idf * tf * 2 / (tf + 1); idf(a) over two texts = log(1.2).
    scores = bm25_scores(["a"], [["a"], ["a", "a"]], k1=1.0, b=0.0)
    idf = math.log(1.2)
    assert scores == pytest.approx([idf, idf * 4 / 3])


def test_bm25_common_token_stays_positive():
    # Lucene's IDF log(1 + (N - df + 0.5) / (df + 0.5)) never goes zero or negative.
    scores = bm25_scores(["a"], [["a"], ["a", "b"], ["a", "c"]], k1=1.2, b=0.75)
    assert all(score > 0 for score in scores)


def test_bm25_no_shared_token_scores_zero():
    scores = bm25_scores(["a"], [["a"], ["b"]], k1=1.2, b=0.75)
    assert scores[0] > 0
    assert scores[1] == 0


def test_bm25_query_tokens_counted_once():
    texts = [["a"], ["a", "b"]]
    assert bm25_scores(["a"], texts, 1.2, 0.75) == pytest.approx(bm25_scores(["a", "a"], texts, 1.2, 0.75))
