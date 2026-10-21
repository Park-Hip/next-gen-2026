"""The prompt: system instruction, chunks in hit order, the asker, the question last."""
from langchain_core.messages import HumanMessage, SystemMessage

from builders import RETRIEVAL, minh_scope
from fakes import SyllableEmbeddings

from appota_kb.services.answering.prompt import SYSTEM_INSTRUCTION, build_messages
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.retrieval.search import retrieve


def test_build_messages_structure(personas, documents):
    s = minh_scope(personas, documents)
    question = "Phép năm của tôi là bao nhiêu ngày?"
    index = build_index(documents, SyllableEmbeddings())
    hits = retrieve(index, s, question, RETRIEVAL)
    messages = build_messages(hits, s, question)
    assert isinstance(messages[0], SystemMessage)
    assert messages[0].content == SYSTEM_INSTRUCTION
    user = messages[1].content
    assert isinstance(messages[1], HumanMessage)
    # The asker line (decision 1) and the question last.
    assert "<asker>Nhân sự GameCo, Studio.</asker>" in user
    assert "Based on the information above, answer this question:" in user
    assert user.rstrip().endswith(f"<question>{question}</question>")
    # Every hit chunk appears in hit order with id, title and Điều.
    positions = []
    for hit in hits:
        assert f'id="{hit.chunk.id}"' in user
        positions.append(user.index(f'id="{hit.chunk.id}"'))
    assert positions == sorted(positions)
    v2 = next(d for d in documents if d.id == "LEAVE-GAMECO-v2")
    assert f'document="{v2.title}"' in user
    assert 'clause="Điều 2"' in user
    # No chunk outside the hits appears (a procedure chunk is rarely in the top 5).
    for c in s.chunks:
        if c.id not in {h.chunk.id for h in hits}:
            assert f'id="{c.id}"' not in user


def test_prompt_rules_for_the_sentence_and_conflicts():
    # Issue #75: the sentence is checked by Hiep's reading, so the prompt must ask for
    # one plain sentence per clause, both sides of a disagreement, and no computation.
    text = SYSTEM_INSTRUCTION
    assert '"claim": one sentence' in text
    assert "names the document" in text
    assert "one point for each clause" in text
    assert "Never choose between them, merge them" in text
    assert "Do not return an empty list only because clauses disagree." in text
    assert "Never compute a date, an amount" in text


def test_prompt_refuses_a_personal_value_no_clause_states():
    # Row 11: a general yearly entitlement is not the employee's remaining balance.
    text = SYSTEM_INSTRUCTION
    assert "about the employee's own record" in text
    assert "general yearly entitlement" in text


def test_prompt_keeps_the_output_contract():
    text = SYSTEM_INSTRUCTION
    assert '"claim"' in text and '"quote"' in text and '"chunks"' in text
    assert 'return {"points": []}' in text
