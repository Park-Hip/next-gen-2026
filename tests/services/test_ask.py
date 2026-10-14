"""services.ask: one question end to end, the same for the page and the harness, and the demo cache."""
from datetime import date

import pytest

from appota_kb.models.answer import Point, Reply
from appota_kb.services.answering.answerer import AnswerUnavailable
from appota_kb.services.ask import ReplyCache, ask
from appota_kb.services.card_text import render
from appota_kb.services.chunking import chunks
from appota_kb.services.citations import card_for_answer
from appota_kb.services.scope import scope

AS_OF = date(2026, 10, 7)


def _chunk(documents, chunk_id):
    doc_id = chunk_id.rsplit("#", 1)[0]
    document = next(d for d in documents if d.id == doc_id)
    return next(c for c in chunks(document) if c.id == chunk_id)


class CountingAnswerer:
    """Returns a fixed reply, or raises, and counts the calls."""

    def __init__(self, reply=None, error=None):
        self.reply = reply
        self.error = error
        self.calls = 0

    def __call__(self, scope_obj, question):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.reply


def _row1_reply(documents):
    c2 = _chunk(documents, "LEAVE-GAMECO-v2#2")
    point = Point(chunks=(c2.id,), quote=c2.text)
    return Reply(retrieved=(c2.id,), points=(point,), raw="{}")


def test_ask_is_card_for_answer_plus_render(personas, documents):
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    conflict_point = Point(chunks=(g1.id,), quote=g1.text)
    cases = [
        (scope(personas["minh"], AS_OF, documents), _row1_reply(documents)),               # answer card (row 1)
        (scope(personas["ha"], AS_OF, documents),
         Reply(retrieved=(g1.id,), points=(conflict_point,), raw="{}")),                   # conflict card (row 7)
        (scope(personas["minh"], AS_OF, documents), Reply(retrieved=(), points=(), raw="")),  # refusal card
    ]
    for s, reply in cases:
        asked = ask(s, "q", CountingAnswerer(reply))
        card = card_for_answer(s, reply.retrieved, reply.points)
        by_id = {c.id: c for c in s.chunks}
        assert asked.reply == reply
        assert asked.card == card
        assert asked.lines == render(card, s, reply.points, tuple(by_id[cid] for cid in reply.retrieved))
        assert asked.cache_hit is False
    assert [ask(s, "q", CountingAnswerer(r)).card.kind for s, r in cases] == ["answer", "conflict", "refusal"]


def test_cache_hit_makes_no_call(personas, documents):
    s = scope(personas["minh"], AS_OF, documents)
    answerer = CountingAnswerer(_row1_reply(documents))
    cache = ReplyCache(2)
    first = ask(s, "q", answerer, cache)
    second = ask(s, "q", answerer, cache)
    assert answerer.calls == 1
    assert (first.cache_hit, second.cache_hit) == (False, True)
    assert second.card == first.card and second.lines == first.lines


def test_unavailable_is_not_cached(personas, documents):
    s = scope(personas["minh"], AS_OF, documents)
    cache = ReplyCache(2)
    with pytest.raises(AnswerUnavailable):
        ask(s, "q", CountingAnswerer(error=AnswerUnavailable("busy")), cache)
    answerer = CountingAnswerer(_row1_reply(documents))
    assert ask(s, "q", answerer, cache).cache_hit is False
    assert answerer.calls == 1


def test_cache_evicts_the_least_recently_used(personas, documents):
    s = scope(personas["minh"], AS_OF, documents)
    answerer = CountingAnswerer(_row1_reply(documents))
    cache = ReplyCache(2)
    ask(s, "a", answerer, cache)
    ask(s, "b", answerer, cache)
    ask(s, "a", answerer, cache)  # a is now the most recently used
    ask(s, "c", answerer, cache)  # evicts b
    assert answerer.calls == 3
    assert ask(s, "a", answerer, cache).cache_hit is True
    assert ask(s, "b", answerer, cache).cache_hit is False
    assert answerer.calls == 4


def test_ask_never_shows_text_the_model_added(personas, documents):
    # Issue #47: a one-word quote used to carry an invented sentence onto the card.
    # Pydantic drops a stray "text" at parse time; here the point has no such field at all.
    s = scope(personas["minh"], AS_OF, documents)
    point = Point(chunks=("LEAVE-GAMECO-v2#2",), quote="ngày")
    reply = Reply(retrieved=("LEAVE-GAMECO-v2#2",), points=(point,), raw="{}")
    asked = ask(s, "q", CountingAnswerer(reply))
    assert asked.card.kind == "answer"
    assert asked.lines[1] == '"ngày"'
    assert asked.lines[2].startswith("Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2")
    assert not hasattr(point, "text")
