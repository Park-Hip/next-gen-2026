"""services.ask: one question end to end, the same for the page and the harness, and the demo cache."""
from datetime import date

import pytest

from appota_kb.evaluation.data_edit import with_edit
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
    point = Point(
        claim="Theo Quy chế nghỉ phép GameCo (bản 2), bạn được nghỉ phép năm 14 ngày mỗi năm.",
        quote=c2.text,
        chunks=(c2.id,),
    )
    return Reply(retrieved=(c2.id,), points=(point,), raw="{}")


def test_ask_is_card_for_answer_plus_render(personas, documents):
    g1 = _chunk(documents, "LEAVE-GROUP-v1#1")
    conflict_point = Point(
        claim="Theo Quy chế nghỉ phép Tập đoàn, bạn được nghỉ 12 ngày.",
        quote=g1.text,
        chunks=(g1.id,),
    )
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


def test_ask_shows_the_claim_above_the_verified_quote(personas, documents):
    # Issue #75: the model's sentence is shown, but only above the quote step 7 checked.
    s = scope(personas["minh"], AS_OF, documents)
    point = Point(
        claim="Theo quy chế GameCo, bạn được nghỉ 14 ngày.",
        quote="ngày",
        chunks=("LEAVE-GAMECO-v2#2",),
    )
    reply = Reply(retrieved=("LEAVE-GAMECO-v2#2",), points=(point,), raw="{}")
    asked = ask(s, "q", CountingAnswerer(reply))
    assert asked.card.kind == "answer"
    assert [line.kind for line in asked.lines[:4]] == ["who", "claim", "quote", "source"]
    assert asked.lines[1].text == "Theo quy chế GameCo, bạn được nghỉ 14 ngày."
    assert asked.lines[2].text == '"ngày"'
    assert asked.lines[3].text.startswith("Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2")
    assert not hasattr(point, "text")


def test_ask_does_not_check_the_claim(personas, documents):
    # ADR 0011: no rule reads the sentence. A wrong number on top of a verified quote
    # still gets an answer card; Hiep's Faithfulness reading is the control.
    s = scope(personas["minh"], AS_OF, documents)
    point = Point(
        claim="Bạn được nghỉ 30 ngày mỗi năm.",
        quote="ngày",
        chunks=("LEAVE-GAMECO-v2#2",),
    )
    reply = Reply(retrieved=("LEAVE-GAMECO-v2#2",), points=(point,), raw="{}")
    asked = ask(s, "q", CountingAnswerer(reply))
    assert asked.card.kind == "answer"
    assert asked.lines[1].text == "Bạn được nghỉ 30 ngày mỗi năm."
    assert asked.lines[2].text == '"ngày"'


def test_ask_claim_never_changes_the_card_kind(personas, documents):
    # The sentence says PayCo applies, but the citation is the Group side of a declared pair:
    # only the rules decide, so the card is a conflict and shows no model text.
    s = scope(personas["ha"], AS_OF, documents)
    group = _chunk(documents, "LEAVE-GROUP-v1#1")
    point = Point(
        claim="Theo quy chế PayCo, bạn được nghỉ 13 ngày.",
        quote=group.text,
        chunks=(group.id,),
    )
    reply = Reply(retrieved=(group.id,), points=(point,), raw="{}")
    asked = ask(s, "q", CountingAnswerer(reply))
    assert asked.card.kind == "conflict"
    assert all("Theo quy chế PayCo" not in line.text for line in asked.lines)


def test_ask_refusal_hides_the_claim(personas, documents):
    s = scope(personas["minh"], AS_OF, documents)
    chunk = _chunk(documents, "LEAVE-GAMECO-v2#2")
    point = Point(
        claim="MODEL TEXT MUST NOT APPEAR",
        quote="câu không có trong tài liệu",
        chunks=(chunk.id,),
    )
    reply = Reply(retrieved=(chunk.id,), points=(point,), raw="{}")
    asked = ask(s, "q", CountingAnswerer(reply))
    assert asked.card.kind == "refusal"
    assert asked.card.reason == "quote_mismatch"
    assert all("MODEL TEXT MUST NOT APPEAR" not in line.text for line in asked.lines)


def _wrong_topic(documents):
    return with_edit(documents, {"document": "LEAVE-PAYCO-v1", "set": {"topic": "nghi_phep_nam"}})


def _both_leave_points(documents):
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
    points = tuple(
        Point(claim=f"Theo {cid}.", quote=_chunk(documents, cid).text, chunks=(cid,)) for cid in ids
    )
    return ids, points


def test_ask_shows_the_conflict_card_for_a_valid_flag(personas, documents):
    docs = _wrong_topic(documents)
    s = scope(personas["ha"], AS_OF, docs)
    ids, points = _both_leave_points(docs)
    flagged = Reply(retrieved=ids, points=points, raw="{}", disagreement=ids)
    unflagged = Reply(retrieved=ids, points=points, raw="{}")
    assert ask(s, "q", CountingAnswerer(unflagged)).card.kind == "answer"
    asked = ask(s, "q", CountingAnswerer(flagged))
    assert asked.card.kind == "conflict" and asked.card.reason == "model_flagged"
    quotes = [line.text for line in asked.lines if line.kind == "quote"]
    assert len(quotes) == 2
    assert "12 ngày" in quotes[0] and "13 ngày" in quotes[1]
    assert asked.lines[1].text.startswith("Có 2 quy định")
    assert asked.lines[-1].text == "Vui lòng hỏi HR PayCo."
    assert all("Theo LEAVE" not in line.text for line in asked.lines)


def test_the_same_chunks_on_two_dates_make_two_calls(personas, documents):
    """The prompt carries the as-of date (ADR 0012), so a reply written for one date is not served for another."""
    first = scope(personas["minh"], date(2026, 10, 7), documents)
    second = scope(personas["minh"], date(2026, 12, 15), documents)
    assert first.chunk_ids == second.chunk_ids
    answerer = CountingAnswerer(_row1_reply(documents))
    cache = ReplyCache(4)
    ask(first, "q", answerer, cache)
    assert ask(second, "q", answerer, cache).cache_hit is False
    assert ask(second, "q", answerer, cache).cache_hit is True
    assert answerer.calls == 2
