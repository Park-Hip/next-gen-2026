"""Step 6 offline: the schema, the prompt, the built request, and the Answerer seam."""
from dataclasses import replace
from datetime import date
import json
import logging
import unicodedata

import pytest
from google.genai.errors import ServerError
from httpx import TimeoutException
from langchain_core.documents import Document as LCDocument
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.vectorstores import InMemoryVectorStore

from fakes import FakeGemini, SyllableEmbeddings, reply_citing

from appota_kb.answer import (
    AnswerUnavailable,
    Answerer,
    SYSTEM_INSTRUCTION,
    answer_schema,
    build_messages,
)
from appota_kb.core.config import Retrieval, load_config
from appota_kb.integrations.gemini import gemini_chat
from appota_kb.services.chunking import chunks as document_chunks
from appota_kb.retrieval import ScopeLeakError, build_index, retrieve
from appota_kb.rules import card_for_answer, scope as build_scope

RETRIEVAL = Retrieval(top_k=5, rrf_k=60, bm25_k1=1.2, bm25_b=0.75, embedding_model="test")


def _chunk_text(documents, chunk_id):
    doc_id, _ = chunk_id.rsplit("#", 1)
    doc = next(d for d in documents if d.id == doc_id)
    return next(c for c in document_chunks(doc) if c.id == chunk_id).text


def _minh_scope(personas, documents, as_of=date(2026, 10, 7)):
    return build_scope(personas["minh"], as_of, documents)


def test_answer_schema_enum_and_order():
    schema = answer_schema(("LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"))
    point = schema["$defs"]["Point"]
    assert list(point["properties"]) == ["chunks", "quote", "text"]
    chunks = point["properties"]["chunks"]
    assert chunks["type"] == "array"
    assert chunks["items"]["type"] == "string"
    assert chunks["items"]["enum"] == ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"]
    assert point["required"] == ["chunks", "quote", "text"]
    assert schema["properties"]["points"]["minItems"] == 1


def test_answer_schema_single_id_is_still_an_enum():
    schema = answer_schema(("LEAVE-GAMECO-v2#2",))
    assert schema["$defs"]["Point"]["properties"]["chunks"]["items"]["enum"] == ["LEAVE-GAMECO-v2#2"]


def test_answer_schema_empty_ids_raises():
    with pytest.raises(ValueError):
        answer_schema(())


def test_build_messages_structure(personas, documents):
    s = _minh_scope(personas, documents)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    index = build_index(documents, SyllableEmbeddings())
    hits = retrieve(index, s, question, RETRIEVAL)
    messages = build_messages(hits, s, question)
    assert isinstance(messages[0], SystemMessage)
    assert messages[0].content == SYSTEM_INSTRUCTION
    user = messages[1].content
    assert isinstance(messages[1], HumanMessage)
    # The asker line (decision 1) and the question last.
    assert "<asker>Nhân sự GameCo, Studio.</asker>" in user
    assert "Based on the information above, answer this question:" in user
    assert user.rstrip().endswith(f"<question>{question}</question>")
    # Every hit chunk appears in hit order with id, title and Điều.
    positions = []
    for hit in hits:
        assert f'id="{hit.chunk.id}"' in user
        positions.append(user.index(f'id="{hit.chunk.id}"'))
    assert positions == sorted(positions)
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    assert f'document="{v2.title}"' in user
    assert 'clause="Điều 2"' in user
    # No chunk outside the hits appears (a procedure chunk is rarely in the top 5).
    for c in s.chunks:
        if c.id not in {h.chunk.id for h in hits}:
            assert f'id="{c.id}"' not in user


def test_gemini_request_built_from_config(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    config = load_config()
    chat = gemini_chat(config.llm)
    request = chat._prepare_request([HumanMessage(content="hi")])
    assert request["model"] == "gemini-3.8-flash"
    cfg = request["config"]
    assert cfg.thinking_config.thinking_level.name == "LOW"
    assert cfg.temperature is None
    assert cfg.http_options.timeout == config.llm.timeout_seconds * 1000
    assert cfg.http_options.retry_options.attempts == config.llm.max_retries
    dumped = json.dumps(cfg.model_dump(exclude_none=True), default=str)
    for param in ("temperature", "top_p", "top_k", "seed"):
        assert param not in dumped


def test_gemini_chat_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    config = load_config()
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        gemini_chat(config.llm)


def test_gemini_chat_attributes(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    config = load_config()
    chat = gemini_chat(config.llm)
    assert chat.cache is False
    assert chat.model == config.llm.model
    assert chat.timeout == config.llm.timeout_seconds
    assert chat.max_retries == config.llm.max_retries
    assert chat.rate_limiter.requests_per_second == config.llm.requests_per_minute / 60.0


def test_answerer_row1_reply(personas, documents):
    s = _minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    chat = FakeGemini(reply=reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
        text="Bạn được nghỉ 14 ngày một năm.",
    ))
    answerer = Answerer(index, chat, RETRIEVAL)
    reply = answerer(s, "Phép năm của tôi là bao nhiêu ngày?")
    assert "LEAVE-GAMECO-v2#2" in reply.retrieved
    assert set(reply.retrieved) <= s.chunk_ids
    assert reply.points is not None and len(reply.points) == 1
    point = reply.points[0]
    assert point.chunks == ("LEAVE-GAMECO-v2#2",)
    assert point.quote == quote
    assert point.text == "Bạn được nghỉ 14 ngày một năm."


def test_answerer_out_of_enum_id_comes_through_as_data(personas, documents):
    s = _minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    chat = FakeGemini(reply=json.dumps(
        {"points": [{"chunks": ["SAL-BAND-GAMECO#2"], "quote": "x", "text": "y"}]}
    ))
    answerer = Answerer(index, chat, RETRIEVAL)
    reply = answerer(s, "Phép năm của tôi là bao nhiêu ngày?")
    assert reply.points is not None and reply.points[0].chunks == ("SAL-BAND-GAMECO#2",)
    card = card_for_answer(s, reply.retrieved, reply.points)
    assert card.kind == "refusal" and card.reason == "outside_retrieved"


def test_answerer_malformed_output_gives_none(personas, documents):
    s = _minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    bad_outputs = [
        "not json at all",
        json.dumps({"points": [{"chunks": ["LEAVE-GAMECO-v2#2"], "quote": "x"}]}),  # missing text
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
    s = _minh_scope(personas, documents)
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
    s = _minh_scope(personas, documents)
    answerer = Answerer(leaky, FakeGemini(reply=""), RETRIEVAL)
    with pytest.raises(ScopeLeakError):
        answerer(s, "Phép năm của tôi là bao nhiêu ngày?")


def test_answerer_called_twice_calls_model_twice(personas, documents):
    s = _minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    chat = FakeGemini(reply=reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}))
    answerer = Answerer(index, chat, RETRIEVAL)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    answerer(s, question)
    answerer(s, question)
    assert chat.call_count == 2


def test_answer_log_line(personas, documents, caplog):
    caplog.set_level(logging.INFO, logger="app.answer")
    s = _minh_scope(personas, documents)
    index = build_index(documents, SyllableEmbeddings())
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    chat = FakeGemini(reply=reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote}))
    answerer = Answerer(index, chat, RETRIEVAL)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    answerer(s, question)

    records = [r for r in caplog.records if r.name == "app.answer"]
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