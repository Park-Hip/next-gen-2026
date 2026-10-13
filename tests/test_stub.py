"""The keyword stub: the demo rows get the right card, and no id ever leaves the scope (R8)."""
from app.config import load_config
from app.data import with_edit
from app.rules import pick_card, scope
from app.stub import answer

CONFIG = load_config()


def _documents_for(documents, row):
    if "data_edit" in row:
        return with_edit(documents, row["data_edit"])
    return documents


def test_row_1_is_an_answer_citing_gameco_v2(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 1)
    s = scope(personas[row["persona"]], row["as_of"], documents)
    reply = answer(s, row["questions"][0], CONFIG)
    assert "LEAVE-GAMECO-v2#2" in reply.cited
    assert reply.cited and reply.text
    assert pick_card(s, reply.retrieved, reply.cited).kind == "answer"


def test_row_7_is_a_conflict(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 7)
    s = scope(personas[row["persona"]], row["as_of"], documents)
    reply = answer(s, row["questions"][0], CONFIG)
    assert pick_card(s, reply.retrieved, reply.cited).kind == "conflict"


def test_row_10_is_a_refusal(personas, documents, cases):
    row = next(c for c in cases if c["id"] == 10)
    s = scope(personas[row["persona"]], row["as_of"], documents)
    reply = answer(s, row["questions"][0], CONFIG)
    assert reply.retrieved == ()
    assert reply.cited == ()
    assert reply.text is None
    assert pick_card(s, reply.retrieved, reply.cited).kind == "refusal"


def test_stub_never_leaves_the_scope(personas, documents, cases):
    for row in cases:
        docs = _documents_for(documents, row)
        s = scope(personas[row["persona"]], row["as_of"], docs)
        for question in row["questions"]:
            reply = answer(s, question, CONFIG)
            assert set(reply.retrieved) <= s.chunk_ids, row["id"]
            assert set(reply.cited) <= set(reply.retrieved), row["id"]