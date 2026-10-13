"""Keyword stand-in for steps 5-6, until #12 (retrieval) and #13 (LLM) land. Deleted by #13.

The stub can only see the asker's Scope, so it can never return a chunk outside it (R8).
It matches the question's syllables against each in-scope chunk: the answer text is the
first cited chunk's text, word for word.
"""
import re
import unicodedata
from dataclasses import dataclass
from typing import Callable

from app.config import Config
from app.rules import Scope


@dataclass(frozen=True)
class Reply:
    retrieved: tuple[str, ...]  # chunk ids, best first
    cited: tuple[str, ...]      # chunk ids the answer cites
    text: str | None            # answer text; never shown on a conflict or refusal card


Answerer = Callable[[Scope, str], Reply]

_WORD = re.compile(r"\w+")


def _tokens(text: str, stopwords: frozenset[str]) -> set[str]:
    text = unicodedata.normalize("NFC", text).lower()
    return {word for word in _WORD.findall(text) if word not in stopwords}


def answer(scope: Scope, question: str, config: Config) -> Reply:
    question_tokens = _tokens(question, config.stub.stopwords)
    scored = []
    for chunk in scope.chunks:
        shared = len(question_tokens & _tokens(chunk.text, config.stub.stopwords))
        if shared >= config.stub.min_shared_tokens:
            scored.append((shared, chunk))
    scored.sort(key=lambda pair: (-pair[0], pair[1].id))
    top = scored[: config.retrieval.top_k]
    if not top:
        return Reply((), (), None)
    best_score = top[0][0]
    return Reply(
        retrieved=tuple(chunk.id for _, chunk in top),
        cited=tuple(chunk.id for score, chunk in top if score == best_score),
        text=top[0][1].text,
    )