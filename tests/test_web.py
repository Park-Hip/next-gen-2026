"""The page through FastAPI's TestClient: form, cards, errors and the scope at the page level.

Most tests inject a fake answerer that cites fixed chunk ids, so they keep passing when #13
replaces the stub; the end-to-end tests at the bottom run the real stub.
"""
import html
import re

import pytest
from fastapi.testclient import TestClient

from app.config import load_config
from app.stub import Reply
from app.web import create_app

FAKE_TEXT = "FAKE ANSWERER TEXT"
LEAVE_QUESTION = "Phép năm của tôi là bao nhiêu ngày?"


def _client(retrieved=(), cited=()):
    def fake(scope, question):
        return Reply(tuple(retrieved), tuple(cited), FAKE_TEXT)

    return TestClient(create_app(load_config(), answerer=fake))


def _ask(client, persona, as_of, q):
    response = client.get("/", params={"persona": persona, "as_of": as_of, "q": q})
    return response, html.unescape(response.text)


def _card_text(page):
    """The visible text of the card, tags removed and whitespace collapsed."""
    article = re.search(r"<article.*?</article>", page, re.S).group(0)
    return " ".join(re.sub(r"<[^>]+>", " ", article).split())


@pytest.fixture(scope="module")
def stub_client():
    return TestClient(create_app(load_config()))


def test_form_without_question(stub_client):
    response = stub_client.get("/")
    assert response.status_code == 200
    page = html.unescape(response.text)
    assert 'lang="vi"' in page
    assert "Mọi đơn vị, nhân sự, văn bản và con số trên trang này đều là giả lập." in page
    assert "Minh - Studio, GameCo (giả lập)" in page
    assert "Lan - Nhân sự Tập đoàn (giả lập)" in page
    assert "Hà - Kế toán, PayCo (giả lập)" in page
    assert "<article" not in page


def test_no_unit_or_role_field(stub_client):
    page = stub_client.get("/").text
    names = set(re.findall(r'<(?:input|select|textarea)[^>]*\sname="([^"]+)"', page))
    assert names == {"persona", "as_of", "q"}


def test_question_limit_reaches_the_input(stub_client):
    page = stub_client.get("/").text
    assert f'maxlength="{load_config().page.question_max_chars}"' in page


def test_healthz(stub_client):
    response = stub_client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_answer_card_row_1():
    client = _client(["LEAVE-GAMECO-v2#2"], ["LEAVE-GAMECO-v2#2"])
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Trả lời Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.")
    assert "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo." in card
    assert FAKE_TEXT in card
    assert "Báo sai" not in page
    assert f"<q>{LEAVE_QUESTION}</q>" in page
    assert "Ngày áp dụng 07/10/2026" in page


def test_answer_card_row_2_next_version():
    client = _client(["LEAVE-GAMECO-v3#2"], ["LEAVE-GAMECO-v3#2"])
    response, page = _ask(client, "minh", "2027-01-01", LEAVE_QUESTION)
    assert response.status_code == 200
    assert "Quy chế nghỉ phép GameCo (bản 3)" in page
    assert "(bản 2)" not in page


def test_conflict_card_row_7():
    client = _client(["LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"], ["LEAVE-GROUP-v1#1"])
    response, page = _ask(client, "ha", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert "Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán." in card
    assert "Hệ thống không tự chọn." in card
    assert 'Tập đoàn, Điều 1 (từ 01/01/2024): "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."' in card
    assert 'PayCo, Điều 1 (từ 01/01/2025): "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."' in card
    assert card.endswith("Vui lòng hỏi HR PayCo.")
    assert FAKE_TEXT not in page
    assert "Đã ghi nhận" not in page


def test_refusals_are_identical_apart_from_hr():
    client = _client()
    _, row9 = _ask(client, "ha", "2026-10-07", "Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày?")
    _, row10 = _ask(client, "minh", "2026-10-07", "Khung bậc lương của GameCo thế nào?")
    card9, card10 = _card_text(row9), _card_text(row10)
    assert "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn." in card10
    assert FAKE_TEXT not in row10

    def neutral(card):
        card = card.split("Bạn đang hỏi với tư cách:", 1)[1].split(".", 1)[1]
        return card.replace("HR PayCo", "HR").replace("HR GameCo", "HR")

    assert neutral(card9) == neutral(card10)


def test_row_10_shows_nothing_forbidden(cases):
    row = next(c for c in cases if c["id"] == 10)
    _, page = _ask(_client(), row["persona"], str(row["as_of"]), row["questions"][0])
    card = _card_text(page)
    for text in row["must_not_contain"]:
        assert text not in card


def test_question_is_escaped():
    response = _client().get("/", params={"persona": "minh", "as_of": "2026-10-07", "q": "<b>x</b>"})
    assert "<b>x</b>" not in response.text
    assert "&lt;b&gt;x&lt;/b&gt;" in response.text


@pytest.mark.parametrize(
    "params, message",
    [
        ({"persona": "unknown", "as_of": "2026-10-07", "q": "abc"}, "Người hỏi không hợp lệ."),
        ({"persona": "minh", "as_of": "07/10/2026", "q": "abc"}, "Ngày không hợp lệ."),
        ({"persona": "minh", "as_of": "2026-10-07", "q": "x" * (load_config().page.question_max_chars + 1)},
         "Câu hỏi quá dài."),
    ],
)
def test_bad_input_is_400_without_traceback(params, message):
    response = _client().get("/", params=params)
    assert response.status_code == 400
    page = html.unescape(response.text)
    assert message in page
    assert "Traceback" not in page
    assert "<article" not in page


def test_unknown_persona_selects_the_placeholder():
    response = _client().get("/", params={"persona": "unknown", "as_of": "2026-10-07", "q": "abc"})
    assert '<option value="" disabled selected>' in response.text
    assert "<option value=\"minh\" selected>" not in response.text


# The real stub, end to end: the two rows in the issue's "How to verify", then R8 for every row.


def test_stub_row_1_minh(stub_client):
    _, page = _ask(stub_client, "minh", "2026-10-07", LEAVE_QUESTION)
    card = _card_text(page)
    assert card.startswith("Trả lời")
    assert "Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026" in card


def test_stub_row_7_ha(stub_client):
    _, page = _ask(stub_client, "ha", "2026-10-07", LEAVE_QUESTION)
    card = _card_text(page)
    assert card.startswith("Mâu thuẫn")
    assert "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm." in card
    assert "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm." in card


def test_stub_pages_show_no_forbidden_title(cases, documents, stub_client):
    titles = {d.id: d.title for d in documents}
    for row in cases:
        if "data_edit" in row:
            continue  # the page always runs on the real data
        for question in row["questions"]:
            _, page = _ask(stub_client, row["persona"], str(row["as_of"]), question)
            for doc_id in row["forbidden_by_rules"]:
                assert titles[doc_id] not in page, (row["id"], question, doc_id)
