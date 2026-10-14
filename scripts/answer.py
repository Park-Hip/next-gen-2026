"""Ask one question through steps 5-7 and print the retrieved ids, the raw reply, the points and the card.

Run by hand: `uv run python scripts/answer.py <persona> <as_of> <question>` (needs GEMINI_API_KEY).
"""
from datetime import date
import logging
import os
import sys

from appota_kb.core.config import load_config
from appota_kb.integrations.data_files import load_documents, load_org, load_personas
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings
from appota_kb.services.answering.answerer import Answerer, AnswerUnavailable
from appota_kb.services.citations import card_for_answer
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.scope import scope as build_scope


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    documents = load_documents()
    personas = load_personas(load_org())
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set; set it to a Gemini API key to run the manual check")
    if len(sys.argv) != 4:
        sys.exit("usage: python scripts/answer.py <persona> <as_of> <question>")
    persona_id, as_of_text, question = sys.argv[1], sys.argv[2], sys.argv[3]
    if persona_id not in personas:
        sys.exit(f"unknown persona {persona_id}")
    as_of = date.fromisoformat(as_of_text)
    index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
    scoped = build_scope(personas[persona_id], as_of, documents)
    answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
    try:
        reply = answerer(scoped, question)
    except AnswerUnavailable as exc:
        sys.exit(f"unavailable: {exc}")
    print(f"retrieved: {list(reply.retrieved)}")
    print(f"raw: {reply.raw}")
    if reply.points is None:
        print("points: malformed output")
    else:
        for point in reply.points:
            print(f"  chunks={list(point.chunks)} quote={point.quote!r} text={point.text!r}")
    card = card_for_answer(scoped, reply.retrieved, reply.points)
    print(f"card: {card.kind} reason={card.reason!r}")
