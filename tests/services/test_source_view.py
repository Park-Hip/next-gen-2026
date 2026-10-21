"""The "open the source" page's content: one cited version, only when the asker's scope holds every chunk."""
from datetime import date

from appota_kb.services.chunking import chunks
from appota_kb.services.scope import scope
from appota_kb.services.source_view import anchor_of, source_view

AS_OF = date(2026, 10, 7)


def test_anchor_of_a_chunk_id():
    assert anchor_of("LEAVE-GAMECO-v2#2") == "c-2"


def test_minh_opens_the_cited_clause_with_its_whole_version(personas, documents):
    view = source_view(scope(personas["minh"], AS_OF, documents), ["LEAVE-GAMECO-v2#2"])
    assert view.title == "Quy chế nghỉ phép GameCo (bản 2)"
    assert view.applies_to == "GameCo"
    assert view.window == "từ 01/01/2026 đến hết 31/12/2026"
    assert view.notice == "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."
    assert view.hr == "HR GameCo"
    assert view.asker == "nhân sự GameCo, Studio"
    assert view.as_of == AS_OF
    assert [(c.anchor, c.label, c.cited) for c in view.chunks] == [
        ("c-1", "Điều 1", False), ("c-2", "Điều 2", True), ("c-3", "Điều 3", False),
    ]
    assert view.chunks[1].text == "Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."
    assert view.first_cited == "c-2"


def test_two_clauses_of_one_document_are_both_cited(personas, documents):
    view = source_view(scope(personas["minh"], AS_OF, documents), ["LEAVE-GAMECO-v2#3", "LEAVE-GAMECO-v2#1"])
    assert [c.cited for c in view.chunks] == [True, False, True]
    assert view.first_cited == "c-1"


def test_a_document_without_dieu_highlights_the_cited_lines(personas, documents):
    ids = ["LEAVE-PROC-GAMECO-v1#1", "LEAVE-PROC-GAMECO-v1#2"]
    view = source_view(scope(personas["minh"], AS_OF, documents), ids)
    assert [(c.label, c.cited) for c in view.chunks] == [(None, True), (None, True), (None, False)]


def test_a_version_with_no_change_has_no_notice(personas, documents):
    view = source_view(scope(personas["lan"], AS_OF, documents), ["LEAVE-GROUP-v1#1"])
    assert view.window == "từ 01/01/2024"
    assert view.notice is None


def test_every_refused_request_gives_none(personas, documents):
    s = scope(personas["minh"], AS_OF, documents)
    refused = [
        [],
        ["SAL-BAND-GAMECO#1"],            # not readable by Minh
        ["LEAVE-GAMECO-v1#2"],            # replaced
        ["LEAVE-GAMECO-v3#2"],            # starts later
        ["LEAVE-GAMECO-v4-DRAFT#2"],      # draft
        ["LEAVE-GROUP-v1#1"],             # overridden by the GameCo policy
        ["NOPE#1"],
        ["LEAVE-GAMECO-v2#9"],            # a document in scope, a clause it does not have
        ["LEAVE-GAMECO-v2#2", "SAL-BAND-GAMECO#1"],
        ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"],  # two documents, both in scope
    ]
    for ids in refused:
        assert source_view(s, ids) is None, ids


def test_hoa_opens_the_salary_band_and_minh_does_not(personas, documents):
    assert source_view(scope(personas["hoa"], AS_OF, documents), ["SAL-BAND-GAMECO#1"]) is not None
    assert source_view(scope(personas["minh"], AS_OF, documents), ["SAL-BAND-GAMECO#1"]) is None


def test_sweep_a_chunk_opens_exactly_when_it_is_in_the_scope(employees, dates, documents):
    """Every account, every boundary date and every chunk: the page opens iff the scope holds the chunk."""
    all_chunk_ids = [c.id for d in documents for c in chunks(d)]
    assert len(all_chunk_ids) == 25
    opened = 0
    for persona in employees.values():
        for as_of in dates:
            s = scope(persona, as_of, documents)
            for chunk_id in all_chunk_ids:
                view = source_view(s, [chunk_id])
                assert (view is not None) == (chunk_id in s.chunk_ids), (persona.id, as_of, chunk_id)
                if view is not None:
                    opened += 1
                    assert [c.cited for c in view.chunks].count(True) == 1
    assert opened > 0
