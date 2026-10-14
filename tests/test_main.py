"""The uvicorn factory: importing it builds nothing, and a missing key fails at start-up."""
import pytest


def test_import_main_builds_nothing():
    # Sockets are blocked in the tests, so an import that called Gemini would fail here.
    import appota_kb.main

    assert callable(appota_kb.main.create_app)
    assert not hasattr(appota_kb.main, "app")


def test_create_app_without_key_fails_before_serving(monkeypatch):
    from appota_kb.main import create_app

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY is not set"):
        create_app()
