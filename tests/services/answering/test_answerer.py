"""The Answerer on offline fakes: one call, points as data, errors as AnswerUnavailable."""
from dataclasses import replace
from datetime import date
import json
import logging

from google.genai.errors import ServerError
from httpx import TimeoutException
from langchain_core.documents import Document as LCDocument
from langchain_core.vectorstores import InMemoryVectorStore
import pytest

from builders import RETRIEVAL, chunk_text, minh_scope
from fakes import FakeGemini, SyllableEmbeddings, reply_citing

from appota_kb.services.answering.answerer import Answerer, AnswerUnavailable
from appota_kb.services.citations import card_for_answer
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.retrieval.search import ScopeLeakError
from appota_kb.services.scope import scope as build_scope


def test_answerer_row1_reply(personas, documents):
    s = minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    chat = FakeGemini(reply=reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
    ))
    answerer = Answerer(index, chat, RETRIEVAL)
    reply = answerer(s, "Phép năm của tôi là bao nhiêu ngày?")
    assert "LEAVE-GAMECO-v2#2" in reply.retrieved
    assert set(reply.retrieved) <= s.chunk_ids
    assert reply.points is not None and len(reply.points) == 1
    point = reply.points[0]
    assert point.chunks == ("LEAVE-GAMECO-v2#2",)
    assert point.quote == quote
    assert not hasattr(point, "text")


def test_answerer_out_of_enum_id_comes_through_as_data(personas, documents):
    s = minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    chat = FakeGemini(reply=json.dumps(
        {"points": [{"chunks": ["SAL-BAND-GAMECO#2"], "quote": "x"}]}
    ))
    answerer = Answerer(index, chat, RETRIEVAL)
    reply = answerer(s, "Phép năm của tôi là bao nhiêu ngày?")
    assert reply.points is not None and reply.points[0].chunks == ("SAL-BAND-GAMECO#2",)
    card = card_for_answer(s, reply.retrieved, reply.points)
    assert card.kind == "refusal" and card.reason == "outside_retrieved"


def test_answerer_malformed_output_gives_none(personas, documents):
    s = minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    bad_outputs = [
        "not json at all",
        json.dumps({"points": [{"chunks": ["LEAVE-GAMECO-v2#2"], "text": "x"}]}),  # missing quote
        json.dumps({"points": "nope"}),
    ]
    for bad in bad_outputs:
        chat = FakeGemini(reply=bad)
        answerer = Answerer(index, chat, RETRIEVAL)
        reply = answerer(s, "Phép năm của tôi là bao nhiêu ngày?")
        assert reply.points is None, bad


def test_answerer_empty_scope_makes_no_call(personas, documents):
    s = build_scope(personas["ha"], date(2023, 6, 1), documents)
    assert s.chunks == ()
    index = build_index(documents, SyllableEmbeddings())
    chat = FakeGemini(reply="")
    answerer = Answerer(index, chat, RETRIEVAL)
    reply = answerer(s, "Phép năm của tôi là bao nhiêu ngày?")
    assert reply.retrieved == ()
    assert reply.points == ()
    assert chat.call_count == 0


def test_answerer_errors_become_unavailable(personas, documents):
    s = minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    for error in (ServerError(429, {"error": "rate limit"}), TimeoutException("timeout")):
        chat = FakeGemini(error=error)
        answerer = Answerer(index, chat, RETRIEVAL)
        with pytest.raises(AnswerUnavailable):
            answerer(s, "Phép năm của tôi là bao nhiêu ngày?")


def test_answerer_leak_raises_scope_leak_error(personas, documents):
    class LeakyStore(InMemoryVectorStore):
        def similarity_search_with_score_by_vector(self, embedding, k=4, filter=None, **_):
            return [(LCDocument(id="SAL-BAND-GAMECO#1", page_content="foreign"), 1.0)]

    index = build_index(documents, SyllableEmbeddings())
    leaky = replace(index, store=LeakyStore(index.store.embedding))
    s = minh_scope(personas, documents)
    answerer = Answerer(leaky, FakeGemini(reply=""), RETRIEVAL)
    with pytest.raises(ScopeLeakError):
        answerer(s, "Phép năm của tôi là bao nhiêu ngày?")


def test_answerer_called_twice_calls_model_twice(personas, documents):
    s = minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    chat = FakeGemini(reply=reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}))
    answerer = Answerer(index, chat, RETRIEVAL)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    answerer(s, question)
    answerer(s, question)
    assert chat.call_count == 2


def test_answer_log_line(personas, documents, caplog):
    caplog.set_level(logging.INFO, logger="appota_kb.services.answering.answerer")
    s = minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    chat = FakeGemini(reply=reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}))
    answerer = Answerer(index, chat, RETRIEVAL)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    answerer(s, question)

    records = [r for r in caplog.records if r.name == "appota_kb.services.answering.answerer"]
    assert len(records) == 1
    payload = json.loads(records[0].getMessage())
    assert payload["persona"] == "minh"
    assert payload["as_of"] == "2026-10-07"
    assert payload["question"] == question
    assert payload["model"] == "gemini-3.8-flash"
    assert set(payload["retrieved"]) <= s.chunk_ids
    assert payload["points"] and payload["points"][0]["chunks"] == ["LEAVE-GAMECO-v2#2"]
    assert payload["raw"]
    assert isinstance(payload["latency_ms"], (int, float))
