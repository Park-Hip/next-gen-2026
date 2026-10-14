"""The keyword side of step 5: Vietnamese syllable tokens and Okapi BM25 (ADR 0002)."""
import math
import re
import unicodedata


def tokens(text: str) -> list[str]:
    """NFC, lowercased, split into syllables on \\w+; diacritics are kept (ADR 0002)."""
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).lower())


def bm25_scores(query: list[str], texts: list[list[str]], k1: float, b: float) -> list[float]:
    """Okapi BM25 with Lucene's IDF log(1 + (N - df + 0.5) / (df + 0.5)).

    Each distinct query token counts once; statistics (N, df, average length) are
    computed over the given texts only, which is the asker's scope (ADR 0002).
    """
    n = len(texts)
    avgdl = sum(len(t) for t in texts) / n
    df: dict[str, int] = {}
    for t in texts:
        for word in set(t):
            df[word] = df.get(word, 0) + 1
    scores = []
    for t in texts:
        tf: dict[str, int] = {}
        for word in t:
            tf[word] = tf.get(word, 0) + 1
        score = 0.0
        for word in dict.fromkeys(query):
            if word not in tf:
                continue
            idf = math.log(1 + (n - df[word] + 0.5) / (df[word] + 0.5))
            length = len(t)
            score += idf * tf[word] * (k1 + 1) / (tf[word] + k1 * (1 - b + b * length / avgdl))
        scores.append(score)
    return scores
