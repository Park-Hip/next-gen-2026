"""The uvicorn factory: `uvicorn appota_kb.main:create_app --factory`.

create_app builds the index and the chat model eagerly, then the page, so a broken file or
a missing key, session secret or demo password fails the deploy's health check instead of
failing on the first visitor.
Importing this module builds nothing.
"""
import logging
import os

from fastapi import FastAPI

from appota_kb.api.page import build_app
from appota_kb.core.config import load_config
from appota_kb.integrations.data_files import load_documents
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.retrieval.index import build_index


def _required_env(name: str, purpose: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is not set; set it to {purpose}")
    return value


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    # Neither value is read from the repository; the demo password is published in
    # the README on purpose (ADR 0016), but the code still reads it only from the environment.
    session_secret = _required_env("SESSION_SECRET", "a long random string that signs the session cookie")
    demo_password = _required_env("DEMO_PASSWORD", "the password shared by the simulated accounts")
    config = load_config()
    documents = load_documents()
    index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
    answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
    return build_app(config, answerer, session_secret=session_secret, demo_password=demo_password)
