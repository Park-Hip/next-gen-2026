"""The Gemini clients: the key from GEMINI_API_KEY only, settings from config, no network."""
import json

from langchain_core.messages import HumanMessage
import pytest

from appota_kb.core.config import load_config
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings


def test_gemini_embeddings_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        gemini_embeddings("gemini-embedding-001")


def test_gemini_embeddings_constructs_without_network(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    embeddings = gemini_embeddings("gemini-embedding-001")
    assert embeddings.model == "gemini-embedding-001"


def test_gemini_request_built_from_config(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    config = load_config()
    chat = gemini_chat(config.llm)
    request = chat._prepare_request([HumanMessage(content="hi")])
    assert request["model"] == "gemini-3.5-flash-lite"
    cfg = request["config"]
    assert cfg.thinking_config.thinking_level.name == "MEDIUM"
    assert cfg.temperature is None
    assert cfg.http_options.timeout == config.llm.timeout_seconds * 1000
    assert cfg.http_options.retry_options.attempts == config.llm.max_retries
    dumped = json.dumps(cfg.model_dump(exclude_none=True), default=str)
    for param in ("temperature", "top_p", "top_k", "seed"):
        assert param not in dumped


def test_gemini_chat_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    config = load_config()
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
        gemini_chat(config.llm)


def test_gemini_chat_attributes(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    config = load_config()
    chat = gemini_chat(config.llm)
    assert chat.cache is False
    assert chat.model == config.llm.model
    assert chat.timeout == config.llm.timeout_seconds
    assert chat.max_retries == config.llm.max_retries
    assert chat.rate_limiter.requests_per_second == config.llm.requests_per_minute / 60.0
