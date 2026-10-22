"""The page through FastAPI's TestClient, with a real Answerer on offline fakes.

Each test injects an Answerer whose FakeGemini returns scripted replies, so the page
runs retrieval, the real with_structured_output path and step 7 end to end, offline.
Every test signs in first: the server decides who is asking from the signed session (ADR 0016).
"""
from datetime import datetime, timedelta, timezone
import html
import json
import logging
import re
import secrets
from urllib.parse import urlencode

import pytest
from fastapi.testclient import TestClient
from google.genai.errors import ServerError
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from builders import RETRIEVAL, chunk_text
from fakes import FakeGemini, SyllableEmbeddings, no_points, reply_citing

from appota_kb.api.page import BUSY_MESSAGE, build_app
from appota_kb.core.config import load_config
from appota_kb.evaluation.data_edit import with_edit
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.retrieval.index import build_index

LEAVE_QUESTION = "Phép năm của tôi là bao nhiêu ngày?"
SALARY_QUESTION = "Khung bậc lương của GameCo thế nào?"
# Throwaway values made on each run, so no credential-like literal sits in the repository.
PASSWORD = secrets.token_urlsafe(12)
SECRET = secrets.token_urlsafe(24)


def _app(answerer, **kwargs):
    return build_app(load_config(), answerer, session_secret=SECRET, demo_password=PASSWORD, **kwargs)


def _client(documents, reply="", error=None, monkeypatch=None):
    """A page over a FakeGemini; with `monkeypatch`, the page reads `documents` instead of data/ (edited data)."""
    if monkeypatch is not None:
        monkeypatch.setattr("appota_kb.api.page.load_documents", lambda: documents)
    index = build_index(documents, SyllableEmbeddings())
    chat = FakeGemini(reply=reply, error=error)
    answerer = Answerer(index, chat, RETRIEVAL)
    return TestClient(_app(answerer)), chat


def _sign_in(client, account, password=PASSWORD, next_path=None):
    """POST /signin the way the browser form does; the redirect is not followed."""
    fields = {"account": account, "password": password}
    if next_path is not None:
        fields["next"] = next_path
    return client.post(
        "/signin",
        content=urlencode(fields),
        headers={"content-type": "application/x-www-form-urlencoded"},
        follow_redirects=False,
    )


def _ask(client, account, as_of, q):
    """Sign in as `account` and ask as that account; the request carries no persona."""
    _sign_in(client, account)
    response = client.get("/", params={"as_of": as_of, "q": q})
    return response, html.unescape(response.text)


def _judge_ask(client, persona, as_of, q):
    """Sign in as the judge and ask as `persona`, chosen in the request."""
    _sign_in(client, "giam_khao")
    response = client.get("/", params={"persona": persona, "as_of": as_of, "q": q})
    return response, html.unescape(response.text)


def _names(page):
    return set(re.findall(r'<(?:input|select|textarea)[^>]*\sname="([^"]+)"', page))


def _card_text(page):
    """The visible text of the card, tags removed and whitespace collapsed."""
    article = re.search(r"<article.*?</article>", page, re.S).group(0)
    article = re.sub(r"</?a(?: [^>]*)?>", "", article)  # a link sits inside a sentence
    return " ".join(re.sub(r"<[^>]+>", " ", article).split())


@pytest.fixture(scope="module")
def page_app(documents):
    index = build_index(documents, SyllableEmbeddings())
    return _app(Answerer(index, FakeGemini(reply=""), RETRIEVAL))


@pytest.fixture
def page_client(page_app):
    """Signed out: each test gets a new client, so a new cookie jar and no inherited session."""
    return TestClient(page_app)


@pytest.fixture
def minh_client(page_client):
    assert _sign_in(page_client, "minh").status_code == 303
    return page_client


@pytest.fixture
def judge_client(page_client):
    assert _sign_in(page_client, "giam_khao").status_code == 303
    return page_client


# Sign-in, sign-out and the session.

def test_signed_out_pages_go_to_sign_in(page_client):
    for path in ("/", "/data", "/cases"):
        response = page_client.get(path, follow_redirects=False)
        assert response.status_code == 303, path
        assert response.headers["location"] == "/signin?" + urlencode({"next": path}), path


def test_sign_in_page_lists_every_account(page_client, personas):
    response = page_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    page = html.unescape(response.text)
    assert "giả lập" in page
    assert _names(page) == {"next", "account", "password"}
    assert 'type="password"' in page
    for persona in personas.values():
        assert f'value="{persona.id}"' in page
        assert persona.name in page
        assert ", ".join(persona.roles) in page
    assert "Studio, GameCo" in page
    assert "Nhân sự GameCo" in page
    assert "<article" not in page


def test_sign_in_calls_no_model(documents):
    client, chat = _client(documents, reply="")
    client.get("/", follow_redirects=True)
    _sign_in(client, "minh")
    assert chat.call_count == 0


def test_right_password_signs_in(page_client):
    response = _sign_in(page_client, "minh")
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert "Đang đăng nhập" in page_client.get("/").text


@pytest.mark.parametrize("attempt", ["wrong", "empty", "near_miss", "unknown_account", "no_account"])
def test_wrong_password_or_unknown_account_sets_no_session(page_client, attempt):
    account = {"unknown_account": "khong-co", "no_account": ""}.get(attempt, "minh")
    password = {"wrong": secrets.token_urlsafe(12), "empty": "", "near_miss": PASSWORD + "x"}.get(attempt, PASSWORD)
    response = _sign_in(page_client, account, password)
    assert response.status_code == 401
    page = html.unescape(response.text)
    assert "Sai mật khẩu." in page
    assert "set-cookie" not in response.headers
    assert page_client.get("/", follow_redirects=False).status_code == 303


def test_form_without_a_body_does_not_sign_in(page_client):
    response = page_client.post("/signin", follow_redirects=False)
    assert response.status_code == 401
    assert "set-cookie" not in response.headers


def test_password_is_never_logged_or_echoed(page_client, caplog):
    secret_try = secrets.token_urlsafe(12)
    with caplog.at_level(logging.DEBUG):
        wrong = _sign_in(page_client, "minh", secret_try)
        _sign_in(page_client, "minh")
        page_client.get("/", params={"as_of": "2026-10-07", "q": LEAVE_QUESTION})
    assert secret_try not in wrong.text
    assert secret_try not in caplog.text
    assert PASSWORD not in caplog.text


def test_password_is_not_accepted_in_the_url(page_client):
    response = page_client.get("/signin", params={"account": "minh", "password": PASSWORD}, follow_redirects=False)
    assert response.status_code == 200
    assert page_client.get("/", follow_redirects=False).status_code == 303


def test_sign_in_form_never_prefills_the_password(page_client):
    page = page_client.get("/signin").text
    assert 'name="password"' in page
    assert re.search(r'name="password"[^>]*value=', page) is None


def test_sign_in_page_shows_the_demo_password(page_client):
    """The demo password is published on purpose (ADR 0016), so the form shows it as a placeholder, never as a value."""
    page = page_client.get("/signin").text
    assert f'placeholder="{PASSWORD}"' in page
    assert f'value="{PASSWORD}"' not in page


def test_sign_in_returns_to_next(page_client):
    path = "/?" + urlencode({"as_of": "2026-10-07", "q": LEAVE_QUESTION})
    page = page_client.get("/signin", params={"next": path}).text
    assert f'name="next" value="{html.escape(path)}"' in page
    response = _sign_in(page_client, "minh", next_path=path)
    assert response.status_code == 303
    assert response.headers["location"] == path


@pytest.mark.parametrize(
    "next_path",
    ["https://evil.example", "//evil.example", "/\\evil.example", "/ok\nSet-Cookie: x=y", "/ok\x00", "evil", "javascript:alert(1)"],
)
def test_sign_in_never_redirects_off_site(page_client, next_path):
    response = _sign_in(page_client, "minh", next_path=next_path)
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    shown = page_client.get("/signin", params={"next": next_path}).text
    assert re.search(r'name="next" value="/"', shown)


def test_sign_in_wrong_password_keeps_next(page_client):
    response = _sign_in(page_client, "minh", "sai", next_path="/cases")
    assert 'name="next" value="/cases"' in response.text
    assert 'value="minh" checked' in response.text


def test_signing_in_again_replaces_the_account(page_client):
    _sign_in(page_client, "minh")
    _sign_in(page_client, "lan")
    page = page_client.get("/").text
    assert "Lan - Nhân sự Tập đoàn" in html.unescape(page)
    assert "Minh - Studio" not in html.unescape(page)


def test_sign_out_ends_the_session(minh_client):
    assert minh_client.get("/", follow_redirects=False).status_code == 200
    response = minh_client.post("/signout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    after = minh_client.get("/", follow_redirects=True)
    assert after.status_code == 200
    assert 'name="password"' in after.text
    assert minh_client.get("/", follow_redirects=False).status_code == 303


def test_sign_out_is_post_only(minh_client):
    assert minh_client.get("/signout", follow_redirects=False).status_code in (404, 405)
    assert minh_client.get("/", follow_redirects=False).status_code == 200


def test_tampered_cookie_is_signed_out(minh_client):
    cookie = minh_client.cookies.get("session")
    assert cookie
    payload, rest = cookie.split(".", 1)
    minh_client.cookies.set("session", payload[:-2] + ("AA" if not payload.endswith("AA") else "BB") + "." + rest)
    assert minh_client.get("/", follow_redirects=False).status_code == 303
    minh_client.cookies.set("session", "not-a-cookie")
    assert minh_client.get("/", follow_redirects=False).status_code == 303


def test_cookie_signed_with_another_secret_is_signed_out(page_app, documents):
    index = build_index(documents, SyllableEmbeddings())
    other = TestClient(build_app(
        load_config(), Answerer(index, FakeGemini(reply=""), RETRIEVAL),
        session_secret=secrets.token_urlsafe(24), demo_password=PASSWORD,
    ))
    _sign_in(other, "giam_khao")
    forged = other.cookies.get("session")
    victim = TestClient(page_app)
    victim.cookies.set("session", forged)
    assert victim.get("/cases", follow_redirects=False).status_code == 303
    assert victim.get("/", follow_redirects=False).status_code == 303


def test_session_cookie_flags(page_client):
    response = _sign_in(page_client, "minh")
    cookie = response.headers["set-cookie"]
    assert "httponly" in cookie.lower()
    assert "samesite=lax" in cookie.lower()
    # A browser-session cookie: no Max-Age or Expires, so it ends when the browser closes.
    assert "max-age" not in cookie.lower() and "expires" not in cookie.lower()
    # The cookie holds the account id only, never the password, unit or roles.
    assert PASSWORD not in cookie


def test_healthz(page_client):
    response = page_client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# The ask page for an employee.

def test_employee_form(minh_client):
    response = minh_client.get("/")
    assert response.status_code == 200
    page = html.unescape(response.text)
    assert 'lang="vi"' in page
    assert "Mọi đơn vị, nhân sự, văn bản và con số trên trang này đều là giả lập." in page
    assert "Đang đăng nhập: <strong>Minh - Studio, GameCo (giả lập)</strong>" in page
    assert "Đổi tài khoản" in page and "Đăng xuất" in page
    assert "<article" not in page
    # No unit, role or account field: only the date and the question reach the server.
    assert _names(page) == {"as_of", "q"}


def test_employee_has_no_tabs_and_no_guide_banner(minh_client):
    page = minh_client.get("/").text
    assert "<nav" not in page
    assert "Lần đầu dùng?" not in page


def test_question_limit_reaches_the_input(minh_client):
    page = minh_client.get("/").text
    assert f'maxlength="{load_config().page.question_max_chars}"' in page


def test_as_of_is_labelled_as_a_demo_control(minh_client):
    page = html.unescape(minh_client.get("/").text)
    assert "Ngày áp dụng (demo)" in page
    assert "Ngày áp dụng là điều khiển của bản demo" in page
    assert "sản phẩm thật luôn dùng ngày hôm nay" in page


def test_answer_card_row_1(documents):
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    answer = "Theo Quy chế nghỉ phép GameCo (bản 2), bạn được nghỉ phép năm 14 ngày mỗi năm."
    reply = reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
        answer=answer,
    )
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Trả lời Bạn đang hỏi với tư cách: nhân sự GameCo, Studio.")
    # One answer, then its verified quote, then the source line (ADR 0018).
    assert card.index(answer) < card.index(f'"{quote}"') < card.index("Nguồn:")
    assert card.count(answer) == 1
    assert "14 ngày" in card
    assert (
        "Nguồn: Quy chế nghỉ phép GameCo (bản 2), Điều 2, hiệu lực từ 01/01/2026 đến hết 31/12/2026. Hỏi thêm: HR GameCo."
        " Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."
    ) in card
    assert "Báo sai" not in page
    assert f"<q>{LEAVE_QUESTION}</q>" in page
    assert "Ngày áp dụng 07/10/2026" in page
    assert "Minh - Studio, GameCo (giả lập)" in page


def test_conflict_card_row_7(documents):
    reply = reply_citing(
        "LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1",
        quote_from={
            "LEAVE-GROUP-v1#1": chunk_text(documents, "LEAVE-GROUP-v1#1"),
            "LEAVE-PAYCO-v1#1": chunk_text(documents, "LEAVE-PAYCO-v1#1"),
        },
        answer="MODEL TEXT MUST NOT APPEAR",
    )
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "ha", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Mâu thuẫn Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.")
    assert "Hệ thống không tự chọn." in card
    assert (
        'Quy chế nghỉ phép Tập đoàn, Điều 1 (từ 01/01/2024, áp dụng cho Tập đoàn): '
        '"Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm."'
    ) in card
    assert (
        'Quy chế nghỉ phép PayCo, Điều 1 (từ 01/01/2025, áp dụng cho PayCo): '
        '"Nhân sự PayCo được nghỉ phép năm 13 ngày mỗi năm."'
    ) in card
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
        answer="MODEL TEXT MUST NOT APPEAR",
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


NOT_FOUND = "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn."
NOT_VERIFIED = "Hệ thống không đối chiếu được câu trả lời với nguyên văn quy định nên không đưa ra câu trả lời."
SYSTEM_ERROR = "Hệ thống gặp lỗi khi tạo câu trả lời."


def test_invented_citation_is_refused(documents):
    reply = json.dumps({"answer": "c", "points": [{"chunks": ["SAL-BAND-GAMECO#2"], "quote": "x"}]})
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert NOT_VERIFIED in card
    assert NOT_FOUND not in card
    assert "SAL-BAND" not in card and "lương" not in card.lower()


def test_malformed_output_is_refused_as_a_system_error(documents):
    client, _ = _client(documents, reply="not json at all")
    response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Từ chối")
    assert SYSTEM_ERROR in card
    assert "Vui lòng thử lại; nếu vẫn lỗi, liên hệ HR GameCo." in card
    assert NOT_FOUND not in card


def test_p6_the_four_replies_give_three_texts(documents):
    """Probe P6 of gaps.md: Minh, 07/10/2026, the leave question; each reply the model may give."""
    c2 = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    replies = {
        "no points": (no_points(), NOT_FOUND),
        "malformed": ("not json at all", SYSTEM_ERROR),
        "quote not in its chunk": (
            reply_citing(
                "LEAVE-GAMECO-v2#2",
                quote_from={"LEAVE-GAMECO-v2#2": "Nhân sự GameCo được nghỉ phép năm 30 ngày."},
                answer="MODEL TEXT MUST NOT APPEAR",
            ),
            NOT_VERIFIED,
        ),
        "cites a chunk that was not retrieved": (
            reply_citing(
                "OT-GAMECO-v1#1",
                quote_from={"OT-GAMECO-v1#1": c2},
                answer="MODEL TEXT MUST NOT APPEAR",
            ),
            NOT_VERIFIED,
        ),
    }
    texts = set()
    for name, (reply, lead) in replies.items():
        client, _ = _client(documents, reply=reply)
        response, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
        card = _card_text(page)
        assert response.status_code == 200, name
        assert card.startswith("Từ chối Bạn đang hỏi với tư cách: nhân sự GameCo, Studio."), name
        assert lead in card, name
        assert "HR GameCo" in card, name
        assert "MODEL TEXT MUST NOT APPEAR" not in page, name
        assert "30 ngày" not in card and c2 not in card, name
        texts.add(card)
    assert len(texts) == 3


def test_no_points_refusal_text_is_unchanged(documents):
    client, _ = _client(documents, reply=no_points())
    _, page = _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert _card_text(page) == (
        "Từ chối Bạn đang hỏi với tư cách: nhân sự GameCo, Studio. "
        f"{NOT_FOUND} "
        "Hệ thống chỉ trả lời các quy định áp dụng cho bạn. Vui lòng liên hệ HR GameCo."
    )


@pytest.mark.parametrize("reply", ["not json at all", json.dumps({"answer": "", "points": [{"chunks": ["OT-GAMECO-v1#1"], "quote": "x"}]})])
def test_a_refused_model_fault_is_asked_again(documents, reply):
    # "Thử lại" or "hỏi lại" on the page must reach the model, not replay the cached failure.
    client, chat = _client(documents, reply=reply)
    _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert chat.call_count == 2


def test_a_no_points_refusal_is_cached(documents):
    client, chat = _client(documents, reply=no_points())
    _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    _ask(client, "minh", "2026-10-07", LEAVE_QUESTION)
    assert chat.call_count == 1


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
    # A different account has a different scope, so it misses the cache.
    _ask(client, "lan", "2026-10-07", LEAVE_QUESTION)
    assert chat.call_count == 2


def test_refusals_identical_apart_from_hr(documents):
    client, _ = _client(documents, reply=no_points())
    _, row9 = _ask(client, "ha", "2026-10-07", "Đi công tác được hỗ trợ ăn uống bao nhiêu một ngày?")
    _, row10 = _ask(client, "minh", "2026-10-07", SALARY_QUESTION)
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


def test_question_is_escaped(minh_client):
    response = minh_client.get("/", params={"as_of": "2026-10-07", "q": "<b>x</b>"})
    assert "<b>x</b>" not in response.text
    assert "&lt;b&gt;x&lt;/b&gt;" in response.text


@pytest.mark.parametrize(
    "params, message",
    [
        ({"as_of": "07/10/2026", "q": "abc"}, "Ngày không hợp lệ."),
        ({"as_of": "2026-10-07", "q": "x" * (load_config().page.question_max_chars + 1)}, "Câu hỏi quá dài."),
    ],
)
def test_bad_input_is_400_without_traceback(minh_client, params, message):
    response = minh_client.get("/", params=params)
    assert response.status_code == 400
    page = html.unescape(response.text)
    assert message in page
    assert "Traceback" not in page
    assert "<article" not in page


class CiteAllGemini(FakeGemini):
    """A hostile model that cites every retrieved chunk, quoting each word for word."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self._calls.append((messages, kwargs))
        user = messages[-1].content
        points = []
        for match in re.finditer(r'<chunk id="([^"]+)"[^>]*>(.*?)</chunk>', user):
            quote = match.group(2)
            points.append({
                "quote": quote,
                "chunks": [match.group(1)],
            })
        answer = " ".join(f"Theo tài liệu, {point['quote']}" for point in points)
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=json.dumps({"answer": answer, "points": points})))])


def _cite_all_client(documents):
    index = build_index(documents, SyllableEmbeddings())
    return TestClient(_app(Answerer(index, CiteAllGemini(), RETRIEVAL)))


def test_page_never_shows_forbidden_title(documents, cases):
    titles = {d.id: d.title for d in documents}
    client = _cite_all_client(documents)
    for row in cases:
        if "data_edit" in row:
            continue  # the page always runs on the real data
        for question in row["questions"]:
            _, page = _ask(client, row["persona"], str(row["as_of"]), question)
            # A notice may name the next version, which is outside the scope today (ADR 0012).
            page = re.sub(r'<p class="change-notice">.*?</p>', "", page, flags=re.S)
            for doc_id in row["forbidden_by_rules"]:
                assert titles[doc_id] not in page, (row["id"], question, doc_id)


# Identity comes from the session, never from the request (P1).

def _logged(caplog):
    return [json.loads(r.getMessage()) for r in caplog.records if r.name == "appota_kb.api.page"]


@pytest.mark.parametrize("persona", ["lan", "unknown", "", "giam_khao", "ha"])
def test_employee_cannot_change_who_is_asking(documents, caplog, persona):
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    reply = reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote})
    client, _ = _client(documents, reply=reply)
    _sign_in(client, "minh")
    with caplog.at_level(logging.INFO, logger="appota_kb.api.page"):
        plain = client.get("/", params={"as_of": "2026-10-07", "q": LEAVE_QUESTION})
        forged = client.get("/", params={"persona": persona, "as_of": "2026-10-07", "q": LEAVE_QUESTION})
    assert forged.status_code == 200
    assert _card_text(html.unescape(forged.text)) == _card_text(html.unescape(plain.text))
    assert "nhân sự GameCo, Studio" in _card_text(html.unescape(forged.text))
    for line in _logged(caplog):
        assert line["account"] == "minh" and line["persona"] == "minh"


def test_employee_cannot_claim_a_role_or_unit(documents):
    client, _ = _client(documents, reply=no_points())
    _sign_in(client, "minh")
    params = {"as_of": "2026-10-07", "q": SALARY_QUESTION, "roles": "hr_gameco", "role": "hr_gameco", "unit": "Nhân sự GameCo"}
    page = html.unescape(client.get("/", params=params).text)
    card = _card_text(page)
    assert card.startswith("Từ chối")
    assert "triệu" not in card and "Khung bậc lương GameCo" not in card


def test_the_log_line_names_the_account(documents, caplog):
    client, _ = _client(documents, reply=no_points())
    _sign_in(client, "ha")
    with caplog.at_level(logging.INFO, logger="appota_kb.api.page"):
        client.get("/", params={"as_of": "2026-10-07", "q": LEAVE_QUESTION})
    (line,) = _logged(caplog)
    assert line["account"] == "ha" and line["persona"] == "ha"
    assert line["as_of"] == "2026-10-07" and line["question"] == LEAVE_QUESTION
    assert set(line) == {"account", "persona", "as_of", "question", "card", "reason", "cache_hit"}


# The judge account asks as any employee account.

def test_judge_asks_as_the_chosen_account(documents, caplog):
    quote = chunk_text(documents, "LEAVE-GROUP-v1#1")
    reply = reply_citing("LEAVE-GROUP-v1#1", quote_from={"LEAVE-GROUP-v1#1": quote})
    client, _ = _client(documents, reply=reply)
    with caplog.at_level(logging.INFO, logger="appota_kb.api.page"):
        response, page = _judge_ask(client, "lan", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Trả lời Bạn đang hỏi với tư cách: nhân sự Tập đoàn, Nhân sự Tập đoàn.")
    assert "12 ngày" in card
    assert "Giám khảo</strong> - đang hỏi với tư cách <strong>Lan</strong>" in page
    assert re.search(r'<option value="lan" selected>', page)
    (line,) = _logged(caplog)
    assert line["account"] == "giam_khao" and line["persona"] == "lan"


@pytest.mark.parametrize("persona", ["giam_khao", "", "unknown"])
def test_judge_must_choose_an_employee_account(judge_client, persona):
    """The server never guesses whom the judge asks as: the judge, a missing and an unknown id are all 400."""
    response = judge_client.get("/", params={"persona": persona, "as_of": "2026-10-07", "q": "abc"})
    assert response.status_code == 400
    page = html.unescape(response.text)
    assert "Người hỏi không hợp lệ." in page
    assert "<article" not in page
    assert '<option value="" disabled selected>' in page


def test_judge_form_has_the_account_picker(judge_client, employees):
    page = html.unescape(judge_client.get("/").text)
    assert _names(page) == {"persona", "as_of", "q"}
    select = re.search(r"<select.*?</select>", page, re.S).group(0)
    assert re.findall(r'<option value="([^"]*)"', select) == ["", *employees]
    assert "Hoa - Nhân sự GameCo (giả lập)" in page
    # The judge is not an employee, so it is not an account to ask as.
    assert "giam_khao" not in select
    assert '<option value="" disabled selected>' in select


def test_hoa_gets_the_salary_band_that_minh_is_refused(documents):
    """Access is granted, not only refused (G2.4): the same question, the same date, two accounts."""
    ids = ("SAL-BAND-GAMECO#2",)
    quote = chunk_text(documents, ids[0])
    reply = reply_citing(*ids, quote_from={ids[0]: quote})
    client, _ = _client(documents, reply=reply)
    _, hoa = _ask(client, "hoa", "2026-10-07", SALARY_QUESTION)
    card = _card_text(hoa)
    assert card.startswith("Trả lời Bạn đang hỏi với tư cách: nhân sự GameCo, Nhân sự GameCo.")
    assert "18 đến 25 triệu" in card
    assert "Nguồn: Khung bậc lương GameCo, Điều 2" in card
    _, minh = _ask(client, "minh", "2026-10-07", SALARY_QUESTION)
    refused = _card_text(minh)
    assert refused.startswith("Từ chối")
    assert "triệu" not in refused and "Khung bậc lương GameCo" not in refused


# The judges' guide pages: /data and /cases are built from files, never call the model, and
# open to the judge account only.

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


@pytest.mark.parametrize("account", ["minh", "lan", "ha", "hoa"])
@pytest.mark.parametrize("path", ["/data", "/cases"])
def test_employee_gets_404_on_the_judges_pages(page_client, account, path):
    """P2: no restricted title and no case text reaches a page an employee can open."""
    _sign_in(page_client, account)
    response = page_client.get(path)
    assert response.status_code == 404
    page = html.unescape(response.text)
    assert "Khung bậc lương GameCo" not in page
    assert "Tình huống #" not in page
    assert "SAL-BAND-GAMECO" not in page
    assert "<nav" not in page
    assert "Đăng xuất" in page


def test_judge_opens_both_pages(judge_client):
    assert judge_client.get("/data").status_code == 200
    assert judge_client.get("/cases").status_code == 200


def test_judge_tabs_on_every_page(judge_client):
    for path, label in TABS:
        page = judge_client.get(path).text
        nav = re.search(r"<nav.*?</nav>", page, re.S).group(0)
        links = re.findall(r'<a href="([^"]+)"( aria-current="page")?>([^<]+)</a>', nav)
        assert [(href, text) for href, _, text in links] == list(TABS), path
        assert [text for _, current, text in links if current] == [label], path
        assert f"<title>{label} - Tri thức nội bộ Appota (giả lập)</title>" in page


def test_judge_header_says_who_is_signed_in(judge_client):
    page = judge_client.get("/").text
    assert "<strong>Giám khảo</strong>" in page
    assert "đang hỏi với tư cách" not in page  # nobody chosen yet


def test_data_page_lists_everything(judge_client, documents, employees, org):
    response = judge_client.get("/data")
    assert response.status_code == 200
    page = html.unescape(response.text)
    assert "Góc nhìn ban tổ chức" in page
    assert "kể cả văn bản bị giới hạn quyền xem" in page
    assert _today_text() in page
    for unit in org.parent:
        assert unit in page, unit
    for persona in employees.values():
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
    # The judge is not an employee, so the page lists no account scope for it.
    assert 'id="persona-giam_khao"' not in page
    assert f"{len(employees)} tài khoản nhân sự và {len(documents)} văn bản" in page


def test_data_page_shows_hoa_reading_the_restricted_document(judge_client):
    page = html.unescape(judge_client.get("/data").text)
    hoa = re.search(r'id="persona-hoa".*?</section>', page, re.S).group(0)
    minh = re.search(r'id="persona-minh".*?</section>', page, re.S).group(0)
    assert "Khung bậc lương GameCo" in hoa
    assert "Khung bậc lương GameCo" not in minh


def test_cases_page_lists_every_row(judge_client, cases, personas):
    response = judge_client.get("/cases")
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
    assert order == [1, 5, 7, 10, 22] + [row["id"] for row in cases if row["id"] not in (1, 5, 7, 10, 22)]
    assert page.index("Bắt buộc theo đề") < page.index('id="case-1"')


def test_cases_page_try_links(judge_client, cases):
    page = html.unescape(judge_client.get("/cases").text)
    link = r'<a class="try" href="[^"]+" target="_blank" rel="noopener nofollow">Thử ngay</a>'
    bodies = _case_html(page)
    for row in cases:
        expected = 0 if "data_edit" in row else len(row["questions"])
        assert len(re.findall(link, bodies[row["id"]])) == expected, row["id"]
    panels = _case_panels(page)
    assert "Tình huống này chạy trên dữ liệu đã sửa" in panels[15]
    assert "Hạn chế đã biết" not in panels[15]
    assert "Hạn chế đã biết, theo dõi ở issue #51" in panels[16]


def test_cases_page_without_run(documents, tmp_path):
    index = build_index(documents, SyllableEmbeddings())
    client = TestClient(_app(Answerer(index, FakeGemini(), RETRIEVAL), root=tmp_path))
    _sign_in(client, "giam_khao")
    page = html.unescape(client.get("/cases").text)
    assert "Chưa có lần chạy đánh giá nào được ghi trong báo cáo kiểm thử." in page
    assert "Kết quả thực tế" not in page
    assert 'id="case-1"' in page


def test_cases_page_shows_committed_run(judge_client, cases):
    from appota_kb.evaluation.committed import committed_run

    run = committed_run(cases)
    page = html.unescape(judge_client.get("/cases").text)
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


def test_cases_page_marks_a_stale_run(judge_client, cases):
    from appota_kb.evaluation.committed import committed_run

    page = html.unescape(judge_client.get("/cases").text)
    stale = "Bộ kiểm thử đã thay đổi sau lần chạy này" in page
    assert stale == committed_run(cases).stale


def test_broken_committed_run_fails_start_up(documents, cases, personas, tmp_path):
    from builders import committed_fixture

    run_id = committed_fixture(tmp_path, documents, personas, cases)
    (tmp_path / "results" / f"{run_id}.jsonl").unlink()
    index = build_index(documents, SyllableEmbeddings())
    with pytest.raises(ValueError, match=run_id):
        _app(Answerer(index, FakeGemini(), RETRIEVAL), root=tmp_path)


def test_guide_pages_never_call_the_model(documents):
    client, chat = _client(documents, reply="")
    _sign_in(client, "giam_khao")
    assert client.get("/data").status_code == 200
    assert client.get("/cases").status_code == 200
    assert chat.call_count == 0


def test_try_links_answer_as_the_cases_account_for_the_judge(documents):
    client = _cite_all_client(documents)
    _sign_in(client, "giam_khao")
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


def test_flagged_conflict_card_on_the_wrong_topic_data(documents, monkeypatch):
    """Row 19 on the page: the model cites both Điều 1 and flags them; the rules show the conflict card."""
    docs = with_edit(documents, {"document": "LEAVE-PAYCO-v1", "set": {"topic": "nghi_phep_nam"}})
    ids = ("LEAVE-GROUP-v1#1", "LEAVE-PAYCO-v1#1")
    reply = reply_citing(
        *ids,
        quote_from={cid: chunk_text(docs, cid) for cid in ids},
        answer="MODEL TEXT MUST NOT APPEAR",
        disagreement=ids,
    )
    client, _ = _client(docs, reply=reply, monkeypatch=monkeypatch)
    # Without the flag the edited data gives the answer card; the flag alone makes it a conflict.
    unflagged, _ = _client(docs, reply=reply_citing(*ids, quote_from={cid: chunk_text(docs, cid) for cid in ids}), monkeypatch=monkeypatch)
    assert _card_text(_ask(unflagged, "ha", "2026-10-07", LEAVE_QUESTION)[1]).startswith("Trả lời")
    response, page = _ask(client, "ha", "2026-10-07", LEAVE_QUESTION)
    assert response.status_code == 200
    card = _card_text(page)
    assert card.startswith("Mâu thuẫn Bạn đang hỏi với tư cách: nhân sự PayCo, Kế toán.")
    assert "Có 2 quy định cùng áp dụng cho bạn" in card
    assert "12 ngày" in card and "13 ngày" in card
    assert card.endswith("Vui lòng hỏi HR PayCo.")
    assert "MODEL TEXT MUST NOT APPEAR" not in page
    assert "model_flagged" not in page


def test_try_link_signed_out_goes_through_sign_in_and_back(documents):
    client = _cite_all_client(documents)
    _sign_in(client, "giam_khao")
    href = re.search(r'<a class="try" href="([^"]+)"', html.unescape(client.get("/cases").text)).group(1)
    client.post("/signout")

    redirect = client.get(href, follow_redirects=False)
    assert redirect.status_code == 303
    location = redirect.headers["location"]
    assert location.startswith("/signin?next=")
    shown = html.unescape(client.get(location).text)
    assert f'name="next" value="{href}"' in shown
    back = _sign_in(client, "giam_khao", next_path=href)
    assert back.headers["location"] == href
    assert client.get(href).status_code == 200


def test_try_link_for_an_employee_ignores_the_persona(documents):
    client = _cite_all_client(documents)
    _sign_in(client, "giam_khao")
    href = re.search(r'<a class="try" href="([^"]+)"', html.unescape(client.get("/cases").text)).group(1)
    assert "persona=lan" in href or "persona=minh" in href
    _sign_in(client, "ha")
    card = _card_text(html.unescape(client.get(href).text))
    assert "nhân sự PayCo, Kế toán" in card


def test_answer_card_row_18_shows_the_window_and_the_notice(documents, cases):
    row = next(c for c in cases if c["id"] == 18)
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    answer = "Theo Quy chế nghỉ phép GameCo (bản 2), 14 ngày chỉ áp dụng đến hết 31/12/2026."
    reply = reply_citing(
        "LEAVE-GAMECO-v2#2",
        quote_from={"LEAVE-GAMECO-v2#2": quote},
        answer=answer,
    )
    client, _ = _client(documents, reply=reply)
    response, page = _ask(client, row["persona"], str(row["as_of"]), row["questions"][0])
    assert response.status_code == 200
    card = _card_text(page)
    source = "hiệu lực từ 01/01/2026 đến hết 31/12/2026. Hỏi thêm: HR GameCo."
    notice = "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."
    assert card.index(answer) < card.index(f'"{quote}"') < card.index(source) < card.index(notice)
    assert '<p class="change-notice"><strong>Sắp thay đổi:</strong>' in page
    for text in row["must_show"]:
        assert text in card
    assert "15 ngày" not in card


def test_answer_card_on_the_day_of_the_change_has_no_notice(documents):
    quote = chunk_text(documents, "LEAVE-GAMECO-v3#2")
    reply = reply_citing("LEAVE-GAMECO-v3#2", quote_from={"LEAVE-GAMECO-v3#2": quote})
    client, _ = _client(documents, reply=reply)
    _, page = _ask(client, "minh", "2027-01-01", LEAVE_QUESTION)
    card = _card_text(page)
    assert "hiệu lực từ 01/01/2027. Hỏi thêm: HR GameCo." in card
    assert "Sắp thay đổi" not in page and "đến hết" not in card
