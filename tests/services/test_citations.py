"""Step 7: citations and quotes checked against the scope, and the card picked from them."""
from datetime import date

import pytest

from appota_kb.models.answer import Point
from appota_kb.services.chunking import chunks
from appota_kb.services.citations import (
    card_for_answer,
    conflict_quotes,
    fold,
    pick_card,
)
from appota_kb.services.scope import scope


def _chunk_by_id(documents, chunk_id):
    doc_id, _ = chunk_id.rsplit("#", 1)
    return next(c for d in documents if d.id == doc_id for c in chunks(d) if c.id == chunk_id)


def _point(chunk_id, documents, quote=None, text="some text"):
    chunk = _chunk_by_id(documents, chunk_id)
    return Point(chunks=(chunk_id,), quote=chunk.text if quote is None else quote, text=text)


def test_conflict_quotes(personas, documents):
    ha = personas["ha"]
    as_of = date(2026, 10, 7)
    s = scope(ha, as_of, documents)
    group = next(d for d in documents if d.id == "LEAVE-GROUP-v1")
    payco = next(d for d in documents if d.id == "LEAVE-PAYCO-v1")
    group_chunks = tuple(chunks(group))
    payco_chunks = tuple(chunks(payco))

    # Citing only the Group side quotes the PayCo side from its top retrieved chunk.
    retrieved = (group_chunks[0], payco_chunks[0])
    card = pick_card(s, [c.id for c in retrieved], ["LEAVE-GROUP-v1#1"])
    left, right = conflict_quotes(card, retrieved)[0]
    assert [c.id for c in left] == ["LEAVE-GROUP-v1#1"]
    assert [c.id for c in right] == ["LEAVE-PAYCO-v1#1"]

    # Citing both quotes both.
    card = pick_card(s, [c.id for c in retrieved], ["LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"])
    left, right = conflict_quotes(card, retrieved)[0]
    assert [c.id for c in left] == ["LEAVE-GROUP-v1#1"]
    assert [c.id for c in right] == ["LEAVE-PAYCO-v1#1"]

    # Nothing retrieved from the PayCo side quotes all its chunks.
    retrieved_group_only = (group_chunks[0],)
    card = pick_card(s, [c.id for c in retrieved_group_only], ["LEAVE-GROUP-v1#1"])
    left, right = conflict_quotes(card, retrieved_group_only)[0]
    assert [c.id for c in left] == ["LEAVE-GROUP-v1#1"]
    assert [c.id for c in right] == [c.id for c in payco_chunks]


def test_conflict_quotes_only_for_conflict_cards(personas, documents):
    as_of = date(2026, 10, 7)
    s_minh = scope(personas["minh"], as_of, documents)
    s_ha = scope(personas["ha"], as_of, documents)
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    v2_chunks = tuple(chunks(v2))
    answer = pick_card(s_minh, [c.id for c in v2_chunks], ["LEAVE-GAMECO-v2#2"])
    assert conflict_quotes(answer, v2_chunks) == ()
    refusal = pick_card(s_ha, s_ha.chunk_ids, [])
    assert conflict_quotes(refusal, ()) == ()


def test_step7(personas, documents):
    minh = personas["minh"]
    ha = personas["ha"]
    as_of = date(2026, 10, 7)
    s_minh = scope(minh, as_of, documents)
    s_ha = scope(ha, as_of, documents)

    assert pick_card(s_minh, s_minh.chunk_ids, ["LEAVE-GAMECO-v1#1"]).kind == "refusal"
    assert pick_card(s_minh, s_minh.chunk_ids, ["LEAVE-GAMECO-v2#2", "LEAVE-GAMECO-v1#1"]).kind == "refusal"
    v2_chunks = {c.id for c in chunks(next(d for d in documents if d.id == "LEAVE-GAMECO-v2"))}
    assert pick_card(s_minh, v2_chunks, ["OT-GAMECO-v1#3"]).kind == "refusal"
    assert pick_card(s_minh, s_minh.chunk_ids, []).kind == "refusal"

    card = pick_card(s_ha, s_ha.chunk_ids, ["LEAVE-GROUP-v1#1"])
    assert card.kind == "conflict"
    assert [(a.id, b.id) for a, b in card.conflicts] == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]

    card = pick_card(s_minh, s_minh.chunk_ids, ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"])
    assert card.kind == "answer"
    assert [c.id for c in card.cited] == ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"]

    with pytest.raises(ValueError):
        pick_card(s_minh, set(s_minh.chunk_ids) | {"SAL-BAND-GAMECO#2"}, ["LEAVE-GAMECO-v2#2"])


def test_fold_nfc_and_whitespace():
    assert fold("a   b\nc") == "a b c"
    assert fold("  x  ") == "x"
    assert fold("nghỉ") == fold("nghỉ")
    import unicodedata
    assert fold(unicodedata.normalize("NFD", "nghỉ")) == "nghỉ"


def test_card_for_answer_row_1_answer(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    points = (_point("LEAVE-GAMECO-v2#2", documents, text="Bạn được nghỉ 14 ngày."),)
    card = card_for_answer(s, ("LEAVE-GAMECO-v2#2",), points)
    assert card.kind == "answer"
    assert card.reason is None
    assert card.cited and card.cited[0].id == "LEAVE-GAMECO-v2#2"


def test_card_for_answer_malformed_and_no_points(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    malformed = card_for_answer(s, s.chunk_ids, None)
    assert malformed.kind == "refusal" and malformed.reason == "malformed"
    empty = card_for_answer(s, (), ())
    assert empty.kind == "refusal" and empty.reason == "no_points"


def test_card_for_answer_invented_id_is_refused(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    # In the scope but not retrieved.
    retrieved = ("LEAVE-GAMECO-v2#2",)
    in_scope_but_foreign = _point("LEAVE-PROC-GAMECO-v1#1", documents)
    card = card_for_answer(s, retrieved, (in_scope_but_foreign,))
    assert card.kind == "refusal" and card.reason == "outside_retrieved"
    # Outside the scope: reaching step 7 as data, not via the enum.
    outside = _point("SAL-BAND-GAMECO#2", documents)
    card = card_for_answer(s, retrieved, (outside,))
    assert card.kind == "refusal" and card.reason == "outside_retrieved"
    # One good point plus one invented still refuses the whole answer (R7).
    good = _point("LEAVE-GAMECO-v2#2", documents)
    card = card_for_answer(s, retrieved, (good, in_scope_but_foreign))
    assert card.kind == "refusal" and card.reason == "outside_retrieved"


def test_card_for_answer_quote_rules(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    retrieved = ("LEAVE-GAMECO-v2#2",)
    # Quote not in the cited chunk.
    bad = _point("LEAVE-GAMECO-v2#2", documents, quote="không có câu này")
    card = card_for_answer(s, retrieved, (bad,))
    assert card.kind == "refusal" and card.reason == "quote_mismatch"
    # Quote present in another retrieved chunk but not the one cited.
    proc = _chunk_by_id(documents, "LEAVE-PROC-GAMECO-v1#1")
    wrong = _point("LEAVE-GAMECO-v2#2", documents, quote=proc.text)
    card = card_for_answer(s, ("LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"), (wrong,))
    assert card.kind == "refusal" and card.reason == "quote_mismatch"
    # Empty and whitespace-only quotes fail ("" is a substring of everything).
    for quote in ("", "   ", "\n\t"):
        card = card_for_answer(s, retrieved, (_point("LEAVE-GAMECO-v2#2", documents, quote=quote),))
        assert card.kind == "refusal" and card.reason == "quote_mismatch"


def test_card_for_answer_quote_folding_accepted(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    chunk = _chunk_by_id(documents, "LEAVE-GAMECO-v2#2")
    import unicodedata
    nfd = unicodedata.normalize("NFD", chunk.text)
    widened = "  ".join(chunk.text.split())
    assert card_for_answer(s, (chunk.id,), (_point(chunk.id, documents, quote=nfd),)).kind == "answer"
    assert card_for_answer(s, (chunk.id,), (_point(chunk.id, documents, quote=widened),)).kind == "answer"


def test_card_for_answer_conflict_ha(personas, documents):
    s = scope(personas["ha"], date(2026, 10, 7), documents)
    group = _point("LEAVE-GROUP-v1#1", documents)
    card = card_for_answer(s, ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"), (group,))
    assert card.kind == "conflict"
    assert [(a.id, b.id) for a, b in card.conflicts] == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]
    payco = _point("LEAVE-PAYCO-v1#1", documents)
    card = card_for_answer(s, ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"), (payco,))
    assert card.kind == "conflict"


def test_card_for_answer_retrieved_outside_scope_raises(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    with pytest.raises(ValueError):
        card_for_answer(s, ("SAL-BAND-GAMECO#2",), None)
