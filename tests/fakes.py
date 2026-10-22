"""Offline stand-ins for Gemini: a lexical embedder and a scripted chat model.

FakeGemini subclasses ChatGoogleGenerativeAI and overrides only _generate, so the real
with_structured_output path (schema binding, request building, parsing) runs offline.
"""
import hashlib
import json
import math
import re

from langchain_core.embeddings import Embeddings
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import PrivateAttr

from appota_kb.services.retrieval.bm25 import tokens

DIM = 256


class SyllableEmbeddings(Embeddings):
    """Deterministic, lexical stand-in: each syllable hashes into a 256-d L2-normalised vector.

    Not Gemini; it ranks by shared syllables, so it checks the retrieval plumbing.
    """

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * DIM
        for syllable in tokens(text):
            digest = hashlib.sha256(syllable.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % DIM
            vector[index] += 1.0
        norm = math.sqrt(sum(v * v for v in vector))
        if norm == 0:
            return vector
        return [v / norm for v in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


class FakeGemini(ChatGoogleGenerativeAI):
    """A chat model whose _generate returns scripted replies; everything else is real."""

    _reply: str = PrivateAttr(default="")
    _error: Exception | None = PrivateAttr(default=None)
    _calls: list = PrivateAttr(default_factory=list)

    def __init__(self, reply: str = "", error: Exception | None = None):
        super().__init__(model="gemini-3.8-flash", google_api_key="dummy")
        self._reply = reply
        self._error = error

    @property
    def call_count(self) -> int:
        return len(self._calls)

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self._calls.append((messages, kwargs))
        if self._error is not None:
            raise self._error
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=self._reply))]
        )


def reply_citing(
    *ids: str,
    quote_from: dict[str, str],
    answer: str | None = None,
    disagreement: tuple[str, ...] = (),
) -> str:
    """JSON {answer, points: [...], disagreement: [...]}: one point per id, quoting quote_from[id] word for word.

    The answer defaults to one sentence that repeats the quotes; tests that check wording pass `answer`.
    `disagreement` is the model's flag, empty unless a test sets it.
    """
    text = answer if answer is not None else " ".join(f"Theo tài liệu, {quote_from[cid]}" for cid in ids)
    return json.dumps(
        {
            "answer": text,
            "points": [
                {"quote": quote_from[cid], "chunks": [cid]}
                for cid in ids
            ],
            "disagreement": list(disagreement),
        },
        ensure_ascii=False,
    )


def no_points() -> str:
    return json.dumps({"answer": "", "points": [], "disagreement": []})


def _question_of(messages) -> str:
    """The question in the user turn, for scripted models keyed by it."""
    for message in reversed(messages):
        content = message.content if isinstance(message.content, str) else str(message.content)
        match = re.search(r"<question>(.*?)</question>", content, re.S)
        if match:
            return match.group(1)
    return ""


class ScriptedGemini(FakeGemini):
    """A chat model whose reply (or exception) is chosen by the question in the user turn."""

    _script: dict = PrivateAttr(default_factory=dict)

    def __init__(self, replies: dict):
        super().__init__(reply="")
        self._script = replies

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self._calls.append((messages, kwargs))
        action = self._script.get(_question_of(messages), "")
        if isinstance(action, Exception):
            raise action
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=action))]
        )


class CountingEmbeddings(SyllableEmbeddings):
    """Records how many embed_documents and embed_query calls retrieval makes."""

    def __init__(self):
        super().__init__()
        self.document_calls = 0
        self.query_calls = 0

    def embed_documents(self, texts):
        self.document_calls += 1
        return super().embed_documents(texts)

    def embed_query(self, text):
        self.query_calls += 1
        return super().embed_query(text)
