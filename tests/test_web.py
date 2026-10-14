"""The page through FastAPI's TestClient, with a real Answerer on offline fakes.

Each test injects an Answerer whose FakeGemini returns scripted replies, so the page
runs retrieval, the real with_structured_output path and step 7 end to end, offline.
"""
import html
import json
import re

import pytest
from fastapi.testclient import TestClient
from google.genai.errors import ServerError
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from fakes import FakeGemini, SyllableEmbeddings, no_points, reply_citing

from app.answer import Answerer
from app.config import Retrieval, load_config
from app.data import chunks as document_chunks
from app.retrieval import build_index
from app.web import BUSY_MESSAGE, create_app

RETRIEVAL = Retrieval(top_k=5, rrf_k=60, bm25_k1=1.2, bm25_b=0.75, embedding_model="test")
LEAVE_QUESTION = "Phép năm của tôi là bao nhiêu ngày?"


def _chunk_text(documents, chunk_id):
    doc_id, _ = chunk_id.rsplit("#", 1)
    doc = next(d for d in documents if d.id == doc_id)
    return next(c for c in document_chunks(doc) if c.id == chunk_id).text


def _client(documents, reply="", error=None):
    index = build_index(documents, SyllableEmbeddings())
    chat = FakeGemini(reply=reply, error=error)
    answerer = Answerer(index, chat, RETRIEVAL)
    return TestClient(create_app(load_config(), answerer)), chat


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
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    reply = reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
        text="Bạn được nghỉ phép năm 14 ngày mỗi năm.",
    )
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Trả lời Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.")
    assert "14 ngày" in card
    assert "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026. Hỏi thêm: HR GameCo." in card
    assert "Báo sai" not in page
    assert f"<q>{LEAVE_QUESTION}</q>" in page
    assert "Ngày áp dụng 07/10/2026" in page


def test_conflict_card_row_7(documents):
    quote = _chunk_text(documents, "LEAVE-GROUP-v1#1")
    reply = reply_citing(
        "LEAVE-GROUP-v1#1",
        quote_from={"LEAVE-GROUP-v1#1": quote},
        text="LLM TEXT MUST NOT APPEAR",
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
    assert "LLM TEXT MUST NOT APPEAR" not in page
    assert "Đã ghi nhận" not in page


def test_refusal_row_8_ha(documents):
    client, _ = _client(documents, reply=no_points())
    response, page = _ask(client, "ha", "2026-10-07", "Làm thêm giờ có cần ai duyệt trước không?")
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Từ chối")
    assert "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn." in card
    assert "Mâu thuẫn" not in card


def test_invented_citation_is_refused(documents):
    reply = json.dumps({"points": [{"chunks": ["SAL-BAND-GAMECO#2"], "quote": "x", "text": "y"}]})
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
    quote = _chunk_text(documents, "LEAVE-GAMECO-v2#2")
    reply = reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
        text="Bạn được nghỉ phép năm 14 ngày mỗi năm.",
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


def test_import_web_builds_nothing():
    import app.web
    # Import must not trigger expensive initialization (Gemini calls, network).
    # app is a lazy proxy; the real app is only built on first request.
    assert hasattr(app.web, "app")
    assert isinstance(app.web.app, app.web._LazyApp)


class CiteAllGemini(FakeGemini):
    """A hostile model that cites every retrieved chunk, quoting each word for word."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self._calls.append((messages, kwargs))
        user = messages[-1].content
        points = []
        for match in re.finditer(r'<chunk id="([^"]+)"[^>]*>(.*?)</chunk>', user):
            points.append({"chunks": [match.group(1)], "quote": match.group(2), "text": f"MARKER {match.group(1)}"})
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=json.dumps({"points": points})))])


def test_page_never_shows_forbidden_title(documents, cases):
    titles = {d.id: d.title for d in documents}
    index = build_index(documents, SyllableEmbeddings())
    answerer = Answerer(index, CiteAllGemini(), RETRIEVAL)
    client = TestClient(create_app(load_config(), answerer))
    for row in cases:
        if "data_edit" in row:
            continue  # the page always runs on the real data
        for question in row["questions"]:
            _, page = _ask(client, row["persona"], str(row["as_of"]), question)
            for doc_id in row["forbidden_by_rules"]:
                assert titles[doc_id] not in page, (row["id"], question, doc_id)