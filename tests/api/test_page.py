"""The page through FastAPI's TestClient, with a real Answerer on offline fakes.

Each test injects an Answerer whose FakeGemini returns scripted replies, so the page
runs retrieval, the real with_structured_output path and step 7 end to end, offline.
"""
from datetime import datetime, timedelta, timezone
import html
import json
import re

import pytest
from fastapi.testclient import TestClient
from google.genai.errors import ServerError
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from builders import RETRIEVAL, chunk_text
from fakes import FakeGemini, SyllableEmbeddings, no_points, reply_citing

from appota_kb.api.page import BUSY_MESSAGE, build_app
from appota_kb.core.config import load_config
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.retrieval.index import build_index

LEAVE_QUESTION = "Phép năm của tôi là bao nhiêu ngày?"


def _client(documents, reply="", error=None):
    index = build_index(documents, SyllableEmbeddings())
    chat = FakeGemini(reply=reply, error=error)
    answerer = Answerer(index, chat, RETRIEVAL)
    return TestClient(build_app(load_config(), answerer)), chat


def _ask(client, persona, as_of, q):
    response = client.get("/", params={"persona": persona, "as_of": as_of, "q": q})
    return response, html.unescape(response.text)


def _card_text(page):
    """The visible text of the card, tags removed and whitespace collapsed."""
    article = re.search(r"<article.*?</article>", page, re.S).group(0)
    return " ".join(re.sub(r"<[^>]+>", " ", article).split())


@pytest.fixture(scope="module")
def page_client(documents):
    return _client(documents, reply="")[0]


def test_form_without_question(page_client):
    response = page_client.get("/")
    assert response.status_code == 200
    page = html.unescape(response.text)
    assert 'lang="vi"' in page
    assert "Mọi đơn vị, nhân sự, văn bản và con số trên trang này đều là giả lập." in page
    assert "Minh - Studio, GameCo (giả lập)" in page
    assert "Lan - Nhân sự Tập đoàn (giả lập)" in page
    assert "Hà - Kế toán, PayCo (giả lập)" in page
    assert "<article" not in page


def test_no_unit_or_role_field(page_client):
    page = page_client.get("/").text
    names = set(re.findall(r'<(?:input|select|textarea)[^>]*\sname="([^"]+)"', page))
    assert names == {"persona", "as_of", "q"}


def test_question_limit_reaches_the_input(page_client):
    page = page_client.get("/").text
    assert f'maxlength="{load_config().page.question_max_chars}"' in page


def test_healthz(page_client):
    response = page_client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_answer_card_row_1(documents):
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    claim = "Theo Quy chế nghỉ phép GameCo (bản 2), bạn được nghỉ phép năm 14 ngày mỗi năm."
    reply = reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
        claim_from={"LEAVE-GAMECO-v2#2": claim},
    )
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Trả lời Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.")
    # The model's sentence, then its verified quote, then the source line (ADR 0011).
    assert card.index(claim) < card.index(f'"{quote}"') < card.index("Nguồn:")
    assert "14 ngày" in card
    assert "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo." in card
    assert "Báo sai" not in page
    assert f"<q>{LEAVE_QUESTION}</q>" in page
    assert "Ngày áp dụng 07/10/2026" in page


def test_conflict_card_row_7(documents):
    quote = chunk_text(documents, "LEAVE-GROUP-v1#1")
    reply = reply_citing(
        "LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1",
        quote_from={
            "LEAVE-GROUP-v1#1": chunk_text(documents, "LEAVE-GROUP-v1#1"),
            "LEAVE-PAYCO-v1#1": chunk_text(documents, "LEAVE-PAYCO-v1#1"),
        },
        claim_from={
            "LEAVE-GROUP-v1#1": "MODEL TEXT MUST NOT APPEAR",
            "LEAVE-PAYCO-v1#1": "MODEL TEXT MUST NOT APPEAR",
        },
    )
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "ha", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Mâu thuẫn Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.")
    assert "Hệ thống không tự chọn." in card
    assert 'Tập đoàn, Điều 1 (từ 01/01/2024): "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."' in card
    assert 'PayCo, Điều 1 (từ 01/01/2025): "Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."' in card
    assert card.endswith("Vui lòng hỏi HR PayCo.")
    assert "MODEL TEXT MUST NOT APPEAR" not in page
    assert "Đã ghi nhận" not in page


def test_conflict_card_row_12_quotes_the_cited_clauses(documents, cases):
    row = next(c for c in cases if c["id"] == 12)
    ids = ("LEAVE-GROUP-v1#2", "LEAVE-PAYCO-v1#2")
    quotes = {cid: chunk_text(documents, cid) for cid in ids}
    reply = reply_citing(
        *ids,
        quote_from=quotes,
        claim_from={cid: "MODEL TEXT MUST NOT APPEAR" for cid in ids},
    )
    client, _ = _client(documents, reply=reply)
    _, page = _ask(client, row["persona"], str(row["as_of"]), row["questions"][0])
    card = _card_text(page)
    assert card.startswith("Mâu thuẫn Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.")
    for quote in quotes.values():
        assert f'"{quote}"' in card
    for text in row["must_show"]:
        assert text in card
    assert "MODEL TEXT MUST NOT APPEAR" not in page


def test_refusal_row_8_ha(documents):
    client, _ = _client(documents, reply=no_points())
    response, page = _ask(client, "ha", "2026-10-07", "Làm thêm giờ có cần ai duyệt trước không?")
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Từ chối")
    assert "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn." in card
    assert "Mâu thuẫn" not in card


def test_invented_citation_is_refused(documents):
    reply = json.dumps({"points": [{"chunks": ["SAL-BAND-GAMECO#2"], "quote": "x"}]})
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    assert "Hệ thống không tìm thấy quy định phù hợp" in _card_text(page)


def test_malformed_output_is_refused(documents):
    client, _ = _client(documents, reply="not json at all")
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    assert "Hệ thống không tìm thấy quy định phù hợp" in _card_text(page)


def test_unavailable_is_503_without_card_and_not_cached(documents):
    client, chat = _client(documents, error=ServerError(429, {"error": "rate limit"}))
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 503
    assert BUSY_MESSAGE in page
    assert "<article" not in page
    # The error is never cached, so the same question calls the model again.
    _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert chat.call_count == 2


def test_cache_same_question_one_call(documents):
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    reply = reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
    )
    client, chat = _client(documents, reply=reply)
    _, page1 = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    _, page2 = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert chat.call_count == 1
    # Step 7 still runs on the hit: the card is rendered on both responses.
    assert "14 ngày" in _card_text(page2)
    # A different persona has a different scope, so it misses the cache.
    _ask(client, "lan", "2026-10-07", LEAVE_QUESTION)
    assert chat.call_count == 2


def test_refusals_identical_apart_from_hr(documents):
    client, _ = _client(documents, reply=no_points())
    _, row9 = _ask(client, "ha", "2026-10-07", "Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày?")
    _, row10 = _ask(client, "minh", "2026-10-07", "Khung bậc lương của GameCo thế nào?")
    card9, card10 = _card_text(row9), _card_text(row10)
    assert "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn." in card10

    def neutral(card):
        card = card.split("Bạn đang hỏi với tư cách:", 1)[1].split(".", 1)[1]
        return card.replace("HR PayCo", "HR").replace("HR GameCo", "HR")

    assert neutral(card9) == neutral(card10)


def test_row_10_shows_nothing_forbidden(documents, cases):
    row = next(c for c in cases if c["id"] == 10)
    client, _ = _client(documents, reply=no_points())
    _, page = _ask(client, row["persona"], str(row["as_of"]), row["questions"][0])
    card = _card_text(page)
    for text in row["must_not_contain"]:
        assert text not in card


def test_question_is_escaped(page_client):
    response = page_client.get("/", params={"persona": "minh", "as_of": "2026-10-07", "q": "<b>x</b>"})
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
def test_bad_input_is_400_without_traceback(page_client, params, message):
    response = page_client.get("/", params=params)
    assert response.status_code == 400
    page = html.unescape(response.text)
    assert message in page
    assert "Traceback" not in page
    assert "<article" not in page


def test_unknown_persona_selects_the_placeholder(page_client):
    response = page_client.get("/", params={"persona": "unknown", "as_of": "2026-10-07", "q": "abc"})
    assert '<option value="" disabled selected>' in response.text
    assert "<option value=\"minh\" selected>" not in response.text


class CiteAllGemini(FakeGemini):
    """A hostile model that cites every retrieved chunk, quoting each word for word."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self._calls.append((messages, kwargs))
        user = messages[-1].content
        points = []
        for match in re.finditer(r'<chunk id="([^"]+)"[^>]*>(.*?)</chunk>', user):
            quote = match.group(2)
            points.append({
                "claim": f"Theo tài liệu, {quote}",
                "quote": quote,
                "chunks": [match.group(1)],
            })
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=json.dumps({"points": points})))])


def test_page_never_shows_forbidden_title(documents, cases):
    titles = {d.id: d.title for d in documents}
    index = build_index(documents, SyllableEmbeddings())
    answerer = Answerer(index, CiteAllGemini(), RETRIEVAL)
    client = TestClient(build_app(load_config(), answerer))
    for row in cases:
        if "data_edit" in row:
            continue  # the page always runs on the real data
        for question in row["questions"]:
            _, page = _ask(client, row["persona"], str(row["as_of"]), question)
            for doc_id in row["forbidden_by_rules"]:
                assert titles[doc_id] not in page, (row["id"], question, doc_id)

# The judges' guide pages: /data and /cases are built from files and never call the model.

TABS = (("/", "Hỏi"), ("/data", "Dữ liệu giả lập"), ("/cases", "Tình huống kiểm thử"))


def _today_text():
    config = load_config()
    today = (datetime.now(timezone.utc) + timedelta(hours=config.page.utc_offset_hours)).date()
    return today.strftime("%d/%m/%Y")


CASE_START = '<section class="panel guide-panel case" id="case-'


def _case_html(page):
    """{row id: the HTML of its case panel}; a case panel holds no nested <section>."""
    out = {}
    for chunk in page.split(CASE_START)[1:]:
        row_id, rest = chunk.split('"', 1)
        out[int(row_id)] = rest.split("</section>", 1)[0]
    return out


def _case_panels(page):
    """{row id: the visible text of its case panel}, tags removed and whitespace collapsed."""
    return {i: " ".join(re.sub(r"<[^>]+>", " ", body).split()) for i, body in _case_html(page).items()}


def test_tabs_on_every_page(page_client):
    for path, label in TABS:
        page = page_client.get(path).text
        links = re.findall(r'<a href="([^"]+)"( aria-current="page")?>([^<]+)</a>', page.split("</nav>")[0])
        assert [(href, text) for href, _, text in links] == list(TABS), path
        assert [text for _, current, text in links if current] == [label], path
        assert f"<title>{label} - Tri thức nội bộ Appota (giả lập)</title>" in page


def test_banner_on_main_page_only(page_client):
    banner = 'Lần đầu dùng? Xem <a href="/data">dữ liệu</a> và <a href="/cases">tình huống mẫu</a>.'
    assert banner in page_client.get("/").text
    assert banner not in page_client.get("/data").text
    assert banner not in page_client.get("/cases").text


def test_data_page_lists_everything(page_client, documents, personas, org):
    response = page_client.get("/data")
    assert response.status_code == 200
    page = html.unescape(response.text)
    assert "Góc nhìn ban tổ chức" in page
    assert "kể cả văn bản bị giới hạn quyền xem" in page
    assert _today_text() in page
    for unit in org.parent:
        assert unit in page, unit
    for persona in personas.values():
        assert persona.name in page
        assert " > ".join(persona.path) in page
        assert ", ".join(persona.roles) in page
    for doc in documents:
        assert doc.id in page
        assert doc.title in page
    # Documents are listed with their clauses, the restricted one included, under the organiser label.
    assert "Bậc 3 có mức lương từ 18 đến 25 triệu đồng mỗi tháng (số liệu giả lập)." in page
    assert "Chỉ vai trò: hr_gameco" in page
    assert "Dự thảo, chưa ban hành" in page
    assert "<article" not in page


def test_cases_page_lists_every_row(page_client, cases, personas):
    response = page_client.get("/cases")
    assert response.status_code == 200
    page = html.unescape(response.text)
    panels = _case_panels(page)
    assert set(panels) == {row["id"] for row in cases}
    for row in cases:
        text = panels[row["id"]]
        assert " ".join(row["purpose"].split()) in text
        assert row["expected_answer"] in text
        assert personas[row["persona"]].name in text
        assert row["as_of"].strftime("%d/%m/%Y") in text
        for question in row["questions"]:
            assert question in text
    # The purpose is collapsed by default: a <details> with no open attribute, once per row.
    assert len(re.findall(r'<details class="purpose">', page)) == len(cases)
    assert "<details class=\"purpose\" open" not in page
    # The featured group comes first, then the other rows in file order, each once.
    order = [int(i) for i in re.findall(r'<section class="panel guide-panel case" id="case-(\d+)"', page)]
    assert order == [1, 5, 7] + [row["id"] for row in cases if row["id"] not in (1, 5, 7)]
    assert page.index("Bắt buộc theo đề") < page.index('id="case-1"')


def test_cases_page_try_links(page_client, cases):
    page = html.unescape(page_client.get("/cases").text)
    link = r'<a class="try" href="[^"]+" target="_blank" rel="noopener nofollow">Thử ngay</a>'
    bodies = _case_html(page)
    for row in cases:
        expected = 0 if "data_edit" in row else len(row["questions"])
        assert len(re.findall(link, bodies[row["id"]])) == expected, row["id"]
    note = _case_panels(page)[15]
    assert "Tình huống này chạy trên dữ liệu đã sửa" in note
    assert "Hạn chế đã biết, theo dõi ở issue #24" in note


def test_cases_page_without_run(documents, tmp_path):
    index = build_index(documents, SyllableEmbeddings())
    client = TestClient(build_app(load_config(), Answerer(index, FakeGemini(), RETRIEVAL), root=tmp_path))
    page = html.unescape(client.get("/cases").text)
    assert "Chưa có lần chạy đánh giá nào được ghi trong báo cáo kiểm thử." in page
    assert "Kết quả thực tế" not in page
    assert 'id="case-1"' in page


def test_cases_page_shows_committed_run(page_client, cases):
    from appota_kb.evaluation.committed import committed_run

    run = committed_run(cases)
    page = html.unescape(page_client.get("/cases").text)
    assert run.run_id in page
    assert run.commit in page
    assert run.model in page
    assert run.results_path in page
    panels = _case_panels(page)
    for row in cases:
        text = panels[row["id"]]
        assert "Kết quả thực tế" in text
        assert run.rows[row["id"]].verdict in text
        assert run.rows[row["id"]].lesson in text
    # Row 1 shows the card the employee saw, rendered by the main page's own template.
    assert "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2" in panels[1]
    assert "Hệ thống không tìm thấy quy định phù hợp" in panels[6]


def test_cases_page_marks_a_stale_run(page_client, cases):
    from appota_kb.evaluation.committed import committed_run

    page = html.unescape(page_client.get("/cases").text)
    stale = "Bộ kiểm thử đã thay đổi sau lần chạy này" in page
    assert stale == committed_run(cases).stale


def test_broken_committed_run_fails_start_up(documents, cases, personas, tmp_path):
    from builders import committed_fixture

    run_id = committed_fixture(tmp_path, documents, personas, cases)
    (tmp_path / "results" / f"{run_id}.jsonl").unlink()
    index = build_index(documents, SyllableEmbeddings())
    with pytest.raises(ValueError, match=run_id):
        build_app(load_config(), Answerer(index, FakeGemini(), RETRIEVAL), root=tmp_path)


def test_guide_pages_never_call_the_model(documents):
    client, chat = _client(documents, reply="")
    assert client.get("/data").status_code == 200
    assert client.get("/cases").status_code == 200
    assert chat.call_count == 0


def test_try_links_answer_on_the_main_page(documents):
    index = build_index(documents, SyllableEmbeddings())
    answerer = Answerer(index, CiteAllGemini(), RETRIEVAL)
    client = TestClient(build_app(load_config(), answerer))
    bodies = _case_html(html.unescape(client.get("/cases").text))
    href_of = {i: re.search(r'<a class="try" href="([^"]+)"', body).group(1) for i, body in bodies.items() if "<a class=\"try\"" in body}

    pages = {}
    for row_id, persona_id in ((1, "minh"), (5, "lan")):
        response = client.get(href_of[row_id])
        assert response.status_code == 200
        page = html.unescape(response.text)
        assert re.search(rf'<option value="{persona_id}" selected>', page)
        assert 'value="2026-10-07"' in page
        assert f'value="{LEAVE_QUESTION}"' in page
        pages[row_id] = _card_text(page)
    assert "nhân sự GameCo, Studio" in pages[1]
    assert "nhân sự Tập đoàn, Nhân sự Tập đoàn" in pages[5]
    assert pages[1] != pages[5]
