"""The uvicorn factory: `uvicorn appota_kb.main:create_app --factory`.

create_app builds the index and the chat model eagerly, then the page, so a broken file or
a missing key fails the deploy's health check instead of failing on the first visitor.
Importing this module builds nothing.
"""
import logging

from fastapi import FastAPI

from appota_kb.api.page import build_app
from appota_kb.core.config import load_config
from appota_kb.integrations.data_files import load_documents
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings
from appota_kb.services.answering.answerer import Answerer
from appota_kb.services.retrieval.index import build_index


def create_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    documents = load_documents()
    index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
    answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
    return build_app(config, answerer)
