"""/source through FastAPI's TestClient: the link on each card, the page, and the 404 for everything else.

The server decides who is asking from the signed session (ADR 0016); the page is read-only and calls
neither the model nor the embedder.
"""
import html
import re
import secrets
from urllib.parse import parse_qs, unquote, urlencode, urlsplit

import pytest
from fastapi.testclient import TestClient

from builders import RETRIEVAL, chunk_text
from fakes import FakeGemini, SyllableEmbeddings, reply_citing

from appota_kb.api.page import build_app
from appota_kb.core.config import load_config
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.chunking import chunks
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.scope import scope

LEAVE_QUESTION = "Phép năm của tôi là bao nhiêu ngày?"
PASSWORD = secrets.token_urlsafe(12)
SECRET = secrets.token_urlsafe(24)
AS_OF = "2026-10-07"
NOTE = "Đoạn in đậm là câu trả lời của hệ thống; đoạn trong ngoặc kép là nguyên văn quy định đã được đối chiếu."


class CountingEmbeddings(SyllableEmbeddings):
    """Counts the questions embedded; documents are embedded once, when the index is built."""

    def __init__(self):
        self.queries = 0

    def embed_query(self, text):
        self.queries += 1
        return super().embed_query(text)


def _build(documents, reply="", embeddings=None):
    chat = FakeGemini(reply=reply)
    answerer = Answerer(build_index(documents, embeddings or SyllableEmbeddings()), chat, RETRIEVAL)
    app = build_app(load_config(), answerer, session_secret=SECRET, demo_password=PASSWORD)
    return TestClient(app), chat


@pytest.fixture(scope="module")
def parts(documents):
    embeddings = CountingEmbeddings()
    client, chat = _build(documents, embeddings=embeddings)
    return client.app, chat, embeddings


@pytest.fixture
def client(parts):
    """Signed out: each test gets a new client, so a new cookie jar."""
    return TestClient(parts[0])


def sign_in(client, account, next_path=None):
    fields = {"account": account, "password": PASSWORD}
    if next_path is not None:
        fields["next"] = next_path
    return client.post(
        "/signin",
        content=urlencode(fields),
        headers={"content-type": "application/x-www-form-urlencoded"},
        follow_redirects=False,
    )


def source(client, chunk_ids, as_of=AS_OF, persona=None):
    params = [("chunk", c) for c in chunk_ids]
    if as_of is not None:
        params.append(("as_of", as_of))
    if persona is not None:
        params.append(("persona", persona))
    return client.get("/source", params=params, follow_redirects=False)


def visible(response):
    return " ".join(re.sub(r"<[^>]+>", " ", html.unescape(response.text)).split())


def card_links(page):
    """[(href, link text)] of the links inside the card."""
    article = re.search(r"<article.*?</article>", page, re.S).group(0)
    return [(html.unescape(h), html.unescape(t)) for h, t in re.findall(r'<a href="([^"]+)">([^<]+)</a>', article)]


def ask(client, q=LEAVE_QUESTION, as_of=AS_OF, persona=None):
    params = {"as_of": as_of, "q": q}
    if persona is not None:
        params["persona"] = persona
    return client.get("/", params=params)


def signed_in_with_reply(documents, reply, account):
    client, _ = _build(documents, reply)
    sign_in(client, account)
    return client


def reply_for(documents, *ids):
    return reply_citing(*ids, quote_from={cid: chunk_text(documents, cid) for cid in ids})


def test_answer_card_source_links_to_the_cited_clause(documents):
    client = signed_in_with_reply(documents, reply_for(documents, "LEAVE-GAMECO-v2#2"), "minh")
    links = card_links(ask(client).text)
    assert links == [
        (f"/source?chunk=LEAVE-GAMECO-v2%232&as_of={AS_OF}#c-2", "Quy chế nghỉ phép GameCo (bản 2), Điều 2")
    ]
    opened = client.get(links[0][0])
    assert opened.status_code == 200
    text = visible(opened)
    assert "Bạn đang xem với tư cách: nhân sự GameCo, Studio. Ngày áp dụng 07/10/2026." in text
    assert "Quy chế nghỉ phép GameCo (bản 2) Hiệu lực từ 01/01/2026 đến hết 31/12/2026" in text
    assert "Hỏi thêm HR GameCo" in text
    assert "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027." in text
    # The whole version is shown, and only the cited clause is marked.
    items = re.findall(r'<li class="chunk( cited)?" id="(c-\d)">(.*?)</li>', opened.text, re.S)
    assert [(bool(cited), anchor) for cited, anchor, _ in items] == [(False, "c-1"), (True, "c-2"), (False, "c-3")]
    cited_text = " ".join(re.sub(r"<[^>]+>", " ", items[1][2]).split())
    assert cited_text == "Đoạn được trích Điều 2. Nhân sự GameCo được nghỉ phép năm 14 ngày mỗi năm."
    assert "Đơn nghỉ phép được gửi cho trưởng nhóm" in text


def test_answer_card_has_the_note_under_the_asker_line(documents):
    client = signed_in_with_reply(documents, reply_for(documents, "LEAVE-GAMECO-v2#2"), "minh")
    page = ask(client).text
    assert page.count(NOTE) == 1
    assert page.index("Bạn đang hỏi với tư cách") < page.index(NOTE) < page.index('<p class="lead">')


def test_conflict_and_refusal_cards_have_no_note(documents):
    conflict = signed_in_with_reply(documents, reply_for(documents, "LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"), "ha")
    page = ask(conflict).text
    assert "Mâu thuẫn" in page
    assert NOTE not in page
    refusal = signed_in_with_reply(documents, '{"answer": "", "points": [], "disagreement": []}', "minh")
    page = ask(refusal).text
    assert "Hệ thống không tìm thấy quy định phù hợp" in page
    assert NOTE not in page
    assert "/source" not in page


def test_conflict_card_names_each_title_and_links_each_side(documents):
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
    client = signed_in_with_reply(documents, reply_for(documents, *ids), "ha")
    links = card_links(ask(client).text)
    assert [text for _, text in links] == ["Quy chế nghỉ phép Tập đoàn, Điều 1", "Quy chế nghỉ phép PayCo, Điều 1"]
    for (href, text), chunk_id in zip(links, ids):
        assert parse_qs(urlsplit(href).query)["chunk"] == [chunk_id]
        opened = client.get(href)
        assert opened.status_code == 200
        assert text.rsplit(",", 1)[0] in visible(opened)
        assert opened.text.count('class="chunk cited"') == 1


def test_procedure_source_highlights_its_lines(client):
    sign_in(client, "minh")
    response = source(client, ["LEAVE-PROC-GAMECO-v1#1", "LEAVE-PROC-GAMECO-v1#2"])
    assert response.status_code == 200
    items = re.findall(r'<li class="chunk( cited)?" id="(c-\d)">', response.text)
    assert [(bool(cited), anchor) for cited, anchor in items] == [(True, "c-1"), (True, "c-2"), (False, "c-3")]
    assert "Điều" not in visible(response)


def test_the_title_is_the_link_of_a_document_without_dieu(documents):
    ids = ("LEAVE-PROC-GAMECO-v1#1", "LEAVE-PROC-GAMECO-v1#3")
    client = signed_in_with_reply(documents, reply_for(documents, *ids), "minh")
    links = card_links(ask(client, "Tôi xin nghỉ phép ở đâu, ai duyệt?").text)
    assert len(links) == 2
    assert all(text == "Hướng dẫn đăng ký nghỉ phép trên hệ thống HR GameCo" for _, text in links)
    assert [parse_qs(urlsplit(href).query)["chunk"] for href, _ in links] == [[ids[0]], [ids[1]]]


def test_the_judges_links_carry_the_account_asked_as(documents):
    client = signed_in_with_reply(documents, reply_for(documents, "LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1"), "giam_khao")
    links = card_links(ask(client, persona="ha").text)
    assert len(links) == 2
    for href, _ in links:
        assert parse_qs(urlsplit(href).query)["persona"] == ["ha"]
        assert client.get(href).status_code == 200
    # As the judge asking as Hà, GameCo's policy is not in scope.
    assert source(client, ["LEAVE-GAMECO-v2#2"], persona="ha").status_code == 404


def test_an_employees_links_never_carry_a_persona(documents):
    client = signed_in_with_reply(documents, reply_for(documents, "LEAVE-GAMECO-v2#2"), "minh")
    href = card_links(ask(client, persona="lan").text)[0][0]
    assert "persona" not in href


def test_signed_out_goes_through_sign_in_and_back(client):
    path = f"/source?chunk=LEAVE-GAMECO-v2%232&as_of={AS_OF}"
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert unquote(response.headers["location"]) == "/signin?next=" + path
    back = sign_in(client, "minh", next_path=path)
    assert back.headers["location"] == path
    assert client.get(path).status_code == 200


LEAKS = [
    ["SAL-BAND-GAMECO#1"],
    ["LEAVE-GAMECO-v1#2"],
    ["LEAVE-GAMECO-v3#2"],
    ["LEAVE-GAMECO-v4-DRAFT#2"],
    ["NOPE#1"],
    ["LEAVE-GAMECO-v2#2", "SAL-BAND-GAMECO#1"],
    ["LEAVE-GAMECO-v2#2", "LEAVE-PROC-GAMECO-v1#1"],
    [],
]


def test_every_refusal_is_the_same_404(client):
    """A chunk out of scope, an unknown id, two documents, no chunk, a bad date and an unknown path look alike."""
    sign_in(client, "minh")
    responses = [source(client, ids) for ids in LEAKS]
    responses += [source(client, ["LEAVE-GAMECO-v2#2"], as_of=value) for value in (None, "", "07/10/2026", "2026-13-40")]
    responses += [client.get("/nope"), client.get("/data")]
    assert {r.status_code for r in responses} == {404}
    bodies = {r.text for r in responses}
    assert len(bodies) == 1
    body = bodies.pop()
    assert "Không tìm thấy trang này" in body
    for leaked in ("Khung bậc lương", "SAL-BAND", "LEAVE-GAMECO", "NOPE", "bản 1", "bản 3", "bản 4"):
        assert leaked not in body


def test_a_persona_in_the_url_changes_nothing_for_an_employee(client):
    sign_in(client, "minh")
    assert source(client, ["LEAVE-GROUP-v1#1"], persona="lan").status_code == 404  # Minh's scope has GameCo's policy
    assert source(client, ["LEAVE-GAMECO-v2#2"], persona="lan").status_code == 200
    assert source(client, ["SAL-BAND-GAMECO#1"], persona="hoa").status_code == 404


def test_the_judge_opens_only_the_chosen_accounts_scope(client):
    sign_in(client, "giam_khao")
    assert source(client, ["LEAVE-GROUP-v1#1"], persona="lan").status_code == 200
    assert source(client, ["LEAVE-GAMECO-v2#2"], persona="lan").status_code == 404
    assert source(client, ["SAL-BAND-GAMECO#1"], persona="hoa").status_code == 200
    assert source(client, ["SAL-BAND-GAMECO#1"], persona="minh").status_code == 404
    for persona in (None, "", "nobody", "giam_khao"):
        assert source(client, ["LEAVE-GROUP-v1#1"], persona=persona).status_code == 404, persona


def test_hoa_opens_the_salary_band_and_minh_does_not(client):
    sign_in(client, "hoa")
    assert source(client, ["SAL-BAND-GAMECO#1"]).status_code == 200
    sign_in(client, "minh")
    assert source(client, ["SAL-BAND-GAMECO#1"]).status_code == 404


def test_the_page_opens_exactly_when_the_scope_holds_the_chunk(client, documents, employees, dates):
    all_ids = [c.id for d in documents for c in chunks(d)]
    for account, persona in employees.items():
        sign_in(client, account)
        for as_of in dates:
            allowed = scope(persona, as_of, documents).chunk_ids
            for chunk_id in all_ids:
                status = source(client, [chunk_id], as_of=as_of.isoformat()).status_code
                assert status == (200 if chunk_id in allowed else 404), (account, as_of, chunk_id)


def test_the_page_calls_neither_the_model_nor_the_embedder(parts, client):
    _, chat, embeddings = parts
    before = embeddings.queries
    sign_in(client, "minh")
    assert source(client, ["LEAVE-GAMECO-v2#2"]).status_code == 200
    assert source(client, ["SAL-BAND-GAMECO#1"]).status_code == 404
    assert chat.call_count == 0
    assert embeddings.queries == before


def test_a_new_date_in_the_link_shows_that_dates_scope(client):
    sign_in(client, "minh")
    assert source(client, ["LEAVE-GAMECO-v2#2"], as_of="2026-12-31").status_code == 200
    assert source(client, ["LEAVE-GAMECO-v2#2"], as_of="2027-01-01").status_code == 404
    page = source(client, ["LEAVE-GAMECO-v3#2"], as_of="2027-01-01")
    assert page.status_code == 200
    assert "Hiệu lực từ 01/01/2027" in visible(page)
    assert "Sắp thay đổi" not in visible(page)


def test_the_back_link_returns_to_the_ask_page(client):
    sign_in(client, "minh")
    assert f'<a href="/?as_of={AS_OF}">Về trang Hỏi</a>' in source(client, ["LEAVE-GAMECO-v2#2"]).text
    sign_in(client, "giam_khao")
    page = source(client, ["LEAVE-GROUP-v1#1"], persona="lan").text
    assert f'<a href="/?as_of={AS_OF}&amp;persona=lan">Về trang Hỏi</a>' in page


def test_cases_page_keeps_plain_text_cards(client):
    sign_in(client, "giam_khao")
    page = client.get("/cases")
    assert page.status_code == 200
    assert "/source" not in page.text
