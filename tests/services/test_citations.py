"""Step 7: citations and quotes checked against the scope, and the card picked from them."""
from dataclasses import replace
from datetime import date

import pytest

from appota_kb.evaluation.data_edit import with_edit
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


def _point(chunk_id, documents, quote=None, claim=None):
    chunk = _chunk_by_id(documents, chunk_id)
    quote = chunk.text if quote is None else quote
    return Point(claim=claim or quote, quote=quote, chunks=(chunk_id,))


def test_conflict_quotes(personas, documents):
    ha = personas["ha"]
    as_of = date(2026, 10, 7)
    s = scope(ha, as_of, documents)
    group = next(d for d in documents if d.id == "LEAVE-GROUP-v1")
    payco = next(d for d in documents if d.id == "LEAVE-PAYCO-v1")
    group_chunks = tuple(chunks(group))
    payco_chunks = tuple(chunks(payco))

    def quoted(card, retrieved):
        return [(d.id, [c.id for c in doc_chunks]) for d, doc_chunks in conflict_quotes(card, retrieved)]

    # Citing only the Group side quotes the PayCo side from its top retrieved chunk.
    retrieved = (group_chunks[0], payco_chunks[0])
    card = pick_card(s, [c.id for c in retrieved], ["LEAVE-GROUP-v1#1"])
    assert quoted(card, retrieved) == [("LEAVE-GROUP-v1", ["LEAVE-GROUP-v1#1"]), ("LEAVE-PAYCO-v1", ["LEAVE-PAYCO-v1#1"])]

    # Citing both quotes both.
    card = pick_card(s, [c.id for c in retrieved], ["LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"])
    assert quoted(card, retrieved) == [("LEAVE-GROUP-v1", ["LEAVE-GROUP-v1#1"]), ("LEAVE-PAYCO-v1", ["LEAVE-PAYCO-v1#1"])]

    # Nothing retrieved from the PayCo side quotes all its chunks.
    retrieved_group_only = (group_chunks[0],)
    card = pick_card(s, [c.id for c in retrieved_group_only], ["LEAVE-GROUP-v1#1"])
    assert quoted(card, retrieved_group_only) == [
        ("LEAVE-GROUP-v1", ["LEAVE-GROUP-v1#1"]),
        ("LEAVE-PAYCO-v1", [c.id for c in payco_chunks]),
    ]


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
    points = (_point("LEAVE-GAMECO-v2#2", documents),)
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


def test_card_for_answer_one_bad_quote_refuses_the_whole_answer(personas, documents):
    s = scope(personas["minh"], date(2026, 10, 7), documents)
    retrieved = ("LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1")
    good = _point("LEAVE-GAMECO-v2#2", documents)
    bad = _point("LEAVE-PROC-GAMECO-v1#1", documents, quote="câu không có trong tài liệu")
    card = card_for_answer(s, retrieved, (good, bad))
    assert card.kind == "refusal" and card.reason == "quote_mismatch"


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


def test_card_for_answer_conflict_pair_document_retrieved_but_not_cited(cases, personas, documents):
    # Row 20: removing the "complements" declaration puts the leave procedure and the
    # GameCo policy in a declared conflict pair, and both are retrieved for an overtime
    # question. Only the overtime clause answers, so citing it must give an answer card.
    row = next(c for c in cases if c["id"] == 20)
    docs = with_edit(documents, row["data_edit"])
    s = scope(personas[row["persona"]], row["as_of"], docs)
    assert [tuple(sorted((a.id, b.id))) for a, b in s.conflicts] == [
        ("LEAVE-GAMECO-v2", "LEAVE-PROC-GAMECO-v1")
    ]
    retrieved = ("LEAVE-PROC-GAMECO-v1#1", "LEAVE-GAMECO-v2#1", "OT-GAMECO-v1#3")
    point = _point("OT-GAMECO-v1#3", docs)
    card = card_for_answer(s, retrieved, (point,))
    assert card.kind == "answer"
    assert [c.id for c in card.cited] == ["OT-GAMECO-v1#3"]


# --- The model's flag (ADR 0014) and a hidden partner (ADR 0015); all data is simulated ("giả lập").

LEAVE_RETRIEVED = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
AS_OF = date(2026, 10, 7)


def _wrong_topic(documents):
    """Row 19: LEAVE-PAYCO-v1 tagged nghi_phep_nam, so the rules form no pair for Hà."""
    return with_edit(documents, {"document": "LEAVE-PAYCO-v1", "set": {"topic": "nghi_phep_nam"}})


def _wrong_complement(documents):
    """#50 example 1: a "bổ sung" wrongly declared between the two leave policies."""
    return with_edit(documents, {"document": "LEAVE-PAYCO-v1", "set": {"complements": ["LEAVE-GROUP"]}})


def _both_points(docs, ids=LEAVE_RETRIEVED):
    return tuple(_point(cid, docs) for cid in ids)


def _pairs(card):
    return [(a.id, b.id) for a, b in card.conflicts]


def test_flag_adds_a_pair_the_rules_did_not_form(personas, documents):
    docs = _wrong_topic(documents)
    s = scope(personas["ha"], AS_OF, docs)
    assert s.conflicts == ()
    assert card_for_answer(s, LEAVE_RETRIEVED, _both_points(docs)).kind == "answer"
    card = card_for_answer(s, LEAVE_RETRIEVED, _both_points(docs), LEAVE_RETRIEVED)
    assert card.kind == "conflict" and card.reason == "model_flagged"
    assert _pairs(card) == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]
    assert [c.id for c in card.cited] == list(LEAVE_RETRIEVED)


def test_flag_order_does_not_matter(personas, documents):
    docs = _wrong_topic(documents)
    s = scope(personas["ha"], AS_OF, docs)
    card = card_for_answer(s, LEAVE_RETRIEVED, _both_points(docs), LEAVE_RETRIEVED[::-1])
    assert card.kind == "conflict"
    assert _pairs(card) == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]


def test_flag_across_a_wrongly_declared_complement(personas, documents):
    docs = _wrong_complement(documents)
    s = scope(personas["ha"], AS_OF, docs)
    assert s.conflicts == ()
    card = card_for_answer(s, LEAVE_RETRIEVED, _both_points(docs), LEAVE_RETRIEVED)
    assert card.kind == "conflict" and card.reason == "model_flagged"
    assert _pairs(card) == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]


def test_flag_repeating_a_declared_pair_leaves_reason_empty(personas, documents):
    s = scope(personas["ha"], AS_OF, documents)
    assert len(s.conflicts) == 1
    card = card_for_answer(s, LEAVE_RETRIEVED, _both_points(documents), LEAVE_RETRIEVED)
    assert card.kind == "conflict" and card.reason is None
    assert card == card_for_answer(s, LEAVE_RETRIEVED, _both_points(documents))


def test_flag_never_removes_a_declared_pair(personas, documents):
    s = scope(personas["ha"], AS_OF, documents)
    group_only = (_point("LEAVE-GROUP-v1#1", documents),)
    for flag in ((), ("LEAVE-GROUP-v1#1",), ("LEAVE-GROUP-v1#1", "LEAVE-GROUP-v1#2"), ("x", "y")):
        card = card_for_answer(s, LEAVE_RETRIEVED, group_only, flag)
        assert card.kind == "conflict", flag
        assert _pairs(card) == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]


def test_each_invalid_flag_is_ignored(personas, documents):
    docs = _wrong_topic(documents)
    s = scope(personas["ha"], AS_OF, docs)
    both = _both_points(docs)
    group2, payco2 = "LEAVE-GROUP-v1#2", "LEAVE-PAYCO-v1#2"
    only_group_quote = Point(claim="c", quote=_chunk_by_id(docs, "LEAVE-GROUP-v1#1").text, chunks=LEAVE_RETRIEVED)
    cases = [
        ("one id", LEAVE_RETRIEVED, both, ("LEAVE-GROUP-v1#1",)),
        ("three ids", LEAVE_RETRIEVED + (payco2,), both, LEAVE_RETRIEVED + (payco2,)),
        ("the same id twice", LEAVE_RETRIEVED, both, ("LEAVE-GROUP-v1#1", "LEAVE-GROUP-v1#1")),
        ("not retrieved", LEAVE_RETRIEVED, both, ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#2")),
        ("outside the scope", LEAVE_RETRIEVED, both, ("LEAVE-GROUP-v1#1", "SAL-BAND-GAMECO#2")),
        ("retrieved but not cited", LEAVE_RETRIEVED + (payco2,), both, ("LEAVE-GROUP-v1#1", payco2)),
        ("cited, but the quote is in the other chunk", LEAVE_RETRIEVED, (only_group_quote,), LEAVE_RETRIEVED),
        (
            "two chunks of the same document",
            ("LEAVE-GROUP-v1#1", group2),
            _both_points(docs, ("LEAVE-GROUP-v1#1", group2)),
            ("LEAVE-GROUP-v1#1", group2),
        ),
    ]
    for name, retrieved, points, flag in cases:
        without = card_for_answer(s, retrieved, points)
        with_flag = card_for_answer(s, retrieved, points, flag)
        assert with_flag == without, name
        assert with_flag.kind == "answer" and with_flag.reason is None, name


def test_a_point_citing_two_chunks_validates_only_the_chunk_holding_its_quote(personas, documents):
    docs = _wrong_topic(documents)
    s = scope(personas["ha"], AS_OF, docs)
    both_cited = Point(claim="c", quote=_chunk_by_id(docs, "LEAVE-GROUP-v1#1").text, chunks=LEAVE_RETRIEVED)
    # The PayCo chunk is cited but never quoted: the flag is ignored.
    assert card_for_answer(s, LEAVE_RETRIEVED, (both_cited,), LEAVE_RETRIEVED).kind == "answer"
    # With a second point quoting the PayCo chunk itself, the flag holds.
    payco = _point("LEAVE-PAYCO-v1#1", docs)
    assert card_for_answer(s, LEAVE_RETRIEVED, (both_cited, payco), LEAVE_RETRIEVED).kind == "conflict"


def test_flag_does_not_change_a_refusal(personas, documents):
    docs = _wrong_topic(documents)
    s = scope(personas["ha"], AS_OF, docs)
    assert card_for_answer(s, LEAVE_RETRIEVED, None, LEAVE_RETRIEVED).reason == "malformed"
    assert card_for_answer(s, LEAVE_RETRIEVED, (), LEAVE_RETRIEVED).reason == "no_points"
    bad_quote = (_point("LEAVE-GROUP-v1#1", docs), _point("LEAVE-PAYCO-v1#1", docs, quote="không có trong tài liệu"))
    card = card_for_answer(s, LEAVE_RETRIEVED, bad_quote, LEAVE_RETRIEVED)
    assert card.kind == "refusal" and card.reason == "quote_mismatch"
    outside = (_point("LEAVE-GROUP-v1#1", docs), _point("LEAVE-PAYCO-v1#2", docs))
    card = card_for_answer(s, LEAVE_RETRIEVED, outside, LEAVE_RETRIEVED)
    assert card.kind == "refusal" and card.reason == "outside_retrieved"


def test_flag_on_the_false_alarm_watch_row_is_ignored(cases, personas, documents):
    """Row 20 cites one document alone, so a flag naming it and an uncited chunk is invalid."""
    row = next(c for c in cases if c["id"] == 20)
    docs = with_edit(documents, row["data_edit"])
    s = scope(personas[row["persona"]], row["as_of"], docs)
    retrieved = ("LEAVE-PROC-GAMECO-v1#1", "LEAVE-GAMECO-v2#1", "OT-GAMECO-v1#3")
    card = card_for_answer(s, retrieved, (_point("OT-GAMECO-v1#3", docs),), ("OT-GAMECO-v1#3", "LEAVE-GAMECO-v2#1"))
    assert card.kind == "answer" and card.reason is None


def _hr_payco_only(documents):
    return [replace(d, access="roles:hr_payco") if d.id == "LEAVE-PAYCO-v1" else d for d in documents]


def test_p8_hidden_partner_refuses_ha(personas, documents):
    """P8: LEAVE-PAYCO-v1 readable only by hr_payco, and still in a pair with the Group policy."""
    docs = _hr_payco_only(documents)
    s = scope(personas["ha"], AS_OF, docs)
    assert [d.id for d in s.documents] == ["LEAVE-GROUP-v1"] and s.conflicts == ()
    assert s.hidden_partners == ("LEAVE-GROUP-v1",)
    group = (_point("LEAVE-GROUP-v1#1", docs),)
    card = card_for_answer(s, ("LEAVE-GROUP-v1#1",), group)
    assert card.kind == "refusal" and card.reason == "hidden_conflict"
    assert card.cited == () and card.conflicts == ()
    # A flag cannot turn the refusal into something else.
    flag = ("LEAVE-GROUP-v1#1", "LEAVE-GROUP-v1#2")
    assert card_for_answer(s, ("LEAVE-GROUP-v1#1",), group, flag).reason == "hidden_conflict"


def test_p8_a_reader_with_hr_payco_gets_the_conflict_card(personas, documents):
    docs = _hr_payco_only(documents)
    reader = replace(personas["ha"], roles=("employee", "hr_payco"))
    s = scope(reader, AS_OF, docs)
    assert s.hidden_partners == ()
    card = card_for_answer(s, LEAVE_RETRIEVED, (_point("LEAVE-GROUP-v1#1", docs),))
    assert card.kind == "conflict" and card.reason is None
    assert _pairs(card) == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]


def test_hidden_check_comes_before_the_declared_pairs(personas, documents):
    """A document paired with both a readable and a hidden document is refused."""
    group = _doc(documents, "LEAVE-GROUP-v1")
    payco = _doc(documents, "LEAVE-PAYCO-v1")
    secret = replace(payco, id="LEAVE-SECRET-v1", series="LEAVE-SECRET", access="roles:hr_payco")
    s = scope(personas["ha"], AS_OF, [group, payco, secret])
    assert [(a.id, b.id) for a, b in s.conflicts] == [("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")]
    assert s.hidden_partners == ("LEAVE-GROUP-v1", "LEAVE-PAYCO-v1")
    for cid in ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"):
        card = pick_card(s, LEAVE_RETRIEVED, [cid])
        assert card.kind == "refusal" and card.reason == "hidden_conflict"


def test_a_question_citing_an_unpaired_document_is_not_refused(personas, documents):
    docs = _hr_payco_only(documents)
    minh = scope(personas["minh"], AS_OF, docs)
    card = card_for_answer(minh, ("LEAVE-GAMECO-v2#2",), (_point("LEAVE-GAMECO-v2#2", docs),))
    assert card.kind == "answer"


def _doc(documents, doc_id):
    return next(d for d in documents if d.id == doc_id)
