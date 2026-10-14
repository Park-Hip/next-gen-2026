"""services.guide: the view models of the judges' pages, on the real data and on small edits of it."""
from dataclasses import replace
from datetime import date
from urllib.parse import parse_qs, urlsplit

from appota_kb.services.guide import (
    STATUS_LABEL,
    access_label,
    applies_label,
    case_views,
    document_status,
    org_tree,
    persona_views,
    same_question_groups,
    series_views,
)
from appota_kb.services.scope import in_force, scope

DAY = date(2026, 10, 7)


def _status(documents, doc_id, day):
    doc = next(d for d in documents if d.id == doc_id)
    return document_status(doc, documents, day)


def test_org_tree_follows_org_yaml(org, personas):
    (root,) = org_tree(org, personas)
    assert root.name == "Tập đoàn"
    assert root.level == 1
    assert [c.name for c in root.children] == ["Nhân sự Tập đoàn", "GameCo", "PayCo"]
    by_name = {}

    def walk(unit):
        by_name[unit.name] = unit
        for child in unit.children:
            walk(child)

    walk(root)
    assert by_name["Studio"].level == 3
    assert by_name["Kế toán"].level == 3
    assert {n for n, u in by_name.items() if u.hr} == {"Tập đoàn", "GameCo", "PayCo"}
    assert by_name["GameCo"].hr == "HR GameCo"
    assert by_name["Studio"].personas == ("Minh",)
    assert by_name["Nhân sự Tập đoàn"].personas == ("Lan",)
    assert by_name["Kế toán"].personas == ("Hà",)


def test_document_status_on_known_dates(documents):
    assert _status(documents, "LEAVE-GAMECO-v1", DAY) == "superseded"
    assert _status(documents, "LEAVE-GAMECO-v2", DAY) == "in_force"
    assert _status(documents, "LEAVE-GAMECO-v3", DAY) == "not_yet"
    assert _status(documents, "LEAVE-GAMECO-v4-DRAFT", DAY) == "draft"
    new_year = date(2027, 1, 1)
    assert _status(documents, "LEAVE-GAMECO-v2", new_year) == "superseded"
    assert _status(documents, "LEAVE-GAMECO-v3", new_year) == "in_force"


def test_document_status_agrees_with_in_force(documents, dates):
    for day in dates:
        forced = {d.id for d in in_force(documents, day)}
        for doc in documents:
            assert (document_status(doc, documents, day) == "in_force") == (doc.id in forced), (doc.id, day)


def test_document_status_ended_and_no_date(documents):
    ended = [replace(d, effective_to=date(2026, 6, 30)) if d.id == "LEAVE-PAYCO-v1" else d for d in documents]
    assert _status(ended, "LEAVE-PAYCO-v1", DAY) == "ended"
    undated = [replace(d, effective_from=None) if d.id == "LEAVE-PAYCO-v1" else d for d in documents]
    assert _status(undated, "LEAVE-PAYCO-v1", DAY) == "no_date"


def test_every_status_has_a_label():
    assert set(STATUS_LABEL) == {"in_force", "superseded", "not_yet", "ended", "draft", "no_date"}


def test_access_and_applies_labels(documents, org):
    by_id = {d.id: d for d in documents}
    assert access_label(by_id["LEAVE-GAMECO-v2"]) == "Mọi nhân sự"
    assert access_label(by_id["SAL-BAND-GAMECO"]) == "Chỉ vai trò: hr_gameco"
    assert access_label(replace(by_id["LEAVE-GAMECO-v2"], access="unit:Kế toán")) == "Chỉ nhân sự thuộc Kế toán"
    assert applies_label(by_id["LEAVE-GAMECO-v2"], org) == "GameCo và đơn vị bên dưới: Studio"
    assert applies_label(replace(by_id["LEAVE-GAMECO-v2"], applies_to="Kế toán"), org) == "Kế toán"


def test_series_views(documents, org):
    views = series_views(documents, org, DAY)
    assert [name for name, _ in views][0] == "LEAVE-GAMECO"
    assert sum(len(v) for _, v in views) == len(documents)
    gameco = dict(views)["LEAVE-GAMECO"]
    # By effective_from, the undated draft last.
    assert [d.id for d in gameco] == [
        "LEAVE-GAMECO-v1", "LEAVE-GAMECO-v2", "LEAVE-GAMECO-v3", "LEAVE-GAMECO-v4-DRAFT",
    ]
    v2 = gameco[1]
    assert v2.validity == "Từ 01/01/2026"
    assert v2.relations == ("Dùng thay: LEAVE-GROUP",)
    assert v2.lines[1] == "Điều 2. Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."
    assert gameco[3].validity == "Chưa có ngày hiệu lực"
    proc = dict(views)["LEAVE-PROC-GAMECO"][0]
    assert proc.relations == ("Bổ sung: LEAVE-GAMECO",)


def test_persona_scope_matches_rules(personas, documents):
    views = {v.persona.id: v for v in persona_views(personas, documents, DAY)}
    for persona_id, view in views.items():
        scoped = scope(personas[persona_id], DAY, documents)
        assert view.scope_titles == tuple(d.title for d in scoped.documents)
    assert views["minh"].path == "Tập đoàn > GameCo > Studio"
    assert views["lan"].roles == "employee, hr_group"
    assert views["ha"].conflicts == ("Quy chế nghỉ phép Tập đoàn và Quy chế nghỉ phép PayCo",)
    assert views["minh"].conflicts == ()
    assert views["lan"].conflicts == ()


def test_same_question_groups(cases):
    assert same_question_groups(cases) == [[1, 5, 7]]

    other_day = [dict(r) for r in cases]
    other_day[4] = {**other_day[4], "as_of": date(2026, 10, 8)}
    assert same_question_groups(other_day) == [[1, 7]]

    # Row 15 shares row 12's question and date but has a data_edit, so it is never grouped.
    row_12, row_15 = (next(r for r in cases if r["id"] == i) for i in (12, 15))
    assert row_12["questions"][0] == row_15["questions"][0]
    assert all(15 not in g for g in same_question_groups(cases))


def test_case_views_order(cases, personas, documents):
    featured, rest = case_views(cases, personas, documents)
    assert [c.id for c in featured] == [1, 5, 7]
    assert [c.id for c in rest] == [i for i in range(1, 16) if i not in (1, 5, 7)]
    assert sorted(c.id for c in featured + rest) == [r["id"] for r in cases]


def test_try_links_match_rows(cases, personas, documents):
    featured, rest = case_views(cases, personas, documents)
    views = {c.id: c for c in featured + rest}
    for row in cases:
        view = views[row["id"]]
        assert [w.text for w in view.wordings] == row["questions"]
        if "data_edit" in row:
            assert all(w.href is None for w in view.wordings)
            continue
        for wording in view.wordings:
            query = parse_qs(urlsplit(wording.href).query)
            assert urlsplit(wording.href).path == "/"
            assert query == {
                "persona": [row["persona"]],
                "as_of": [row["as_of"].isoformat()],
                "q": [wording.text],
            }
    assert len(views[1].wordings) == 3


def test_data_edit_note_names_the_document_and_line(cases, personas, documents):
    _, rest = case_views(cases, personas, documents)
    view = next(c for c in rest if c.id == 15)
    edit = next(r for r in cases if r["id"] == 15)["data_edit"]
    title = next(d.title for d in documents if d.id == edit["document"])
    assert title in view.data_edit_note
    assert edit["remove"] in view.data_edit_note
    assert view.limitation_issue == "#24"
    assert view.kind_label == "Chưa xử lý tốt"
    assert view.as_of == "07/10/2026"
    assert next(c for c in rest if c.id == 2).data_edit_note is None
