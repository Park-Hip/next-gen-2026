"""The Gemini clients: the embedding model (step 5) and the chat model (step 6).

The only code that reads GEMINI_API_KEY; the key comes from the environment only (decision 7).
"""
import os

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from appota_kb.core.config import Llm


def gemini_embeddings(model: str) -> GoogleGenerativeAIEmbeddings:
    """The embedding model, with the key read from GEMINI_API_KEY only (decision 7)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set; set it to a Gemini API key to build the index")
    return GoogleGenerativeAIEmbeddings(model=model, google_api_key=key)


def gemini_chat(settings: Llm) -> ChatGoogleGenerativeAI:
    """The chat model, with the key read from GEMINI_API_KEY only and no sampling (ADR 0003)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set; set it to a Gemini API key to answer questions")
    return ChatGoogleGenerativeAI(
        model=settings.model,
        google_api_key=key,
        thinking_level=settings.thinking_level,
        max_retries=settings.max_retries,
        timeout=settings.timeout_seconds,
        cache=False,
        rate_limiter=InMemoryRateLimiter(requests_per_second=settings.requests_per_minute / 60.0),
    )
