"""config.yaml loads into Config, and a bad file raises ValueError naming the key."""
from pathlib import Path

import pytest

from appota_kb.config import load_config


def test_real_config_loads():
    config = load_config()
    assert isinstance(config.retrieval.top_k, int) and config.retrieval.top_k > 0
    assert isinstance(config.retrieval.rrf_k, int) and config.retrieval.rrf_k > 0
    assert isinstance(config.retrieval.bm25_k1, float) and config.retrieval.bm25_k1 > 0
    assert isinstance(config.retrieval.bm25_b, float) and 0 <= config.retrieval.bm25_b <= 1
    assert isinstance(config.retrieval.embedding_model, str) and config.retrieval.embedding_model
    assert config.llm.model == "gemini-3.8-flash"
    assert isinstance(config.llm.thinking_level, str) and config.llm.thinking_level
    assert isinstance(config.llm.max_retries, int) and config.llm.max_retries > 0
    assert isinstance(config.llm.timeout_seconds, float) and config.llm.timeout_seconds > 0
    assert isinstance(config.llm.requests_per_minute, float) and config.llm.requests_per_minute > 0
    assert config.page.question_max_chars > 0
    assert config.page.utc_offset_hours > 0
    assert config.page.answer_cache_size > 0
    assert 0 <= config.eval.over_cautious_max_share <= 1
    assert 0 <= config.eval.confidence <= 1


def test_only_config_py_mentions_config_yaml():
    root = Path(__file__).resolve().parent.parent / "app"
    for path in root.glob("*.py"):
        if path.name == "config.py":
            continue
        assert "config.yaml" not in path.read_text(encoding="utf-8"), path.name


def _path(tmp_path, text):
    path = tmp_path / "config.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def _valid():
    return (
        "retrieval:\n"
        "  top_k: 5\n"
        "  rrf_k: 60\n"
        "  bm25_k1: 1.2\n"
        "  bm25_b: 0.75\n"
        "  embedding_model: gemini-embedding-001\n"
        "llm:\n"
        "  model: gemini-3.8-flash\n"
        "  thinking_level: low\n"
        "  max_retries: 6\n"
        "  timeout_seconds: 30\n"
        "  requests_per_minute: 4\n"
        "page:\n"
        "  question_max_chars: 300\n"
        "  utc_offset_hours: 7\n"
        "  answer_cache_size: 256\n"
        "eval:\n"
        "  over_cautious_max_share: 0.10\n"
        "  confidence: 0.95\n"
    )


def test_missing_section_raises(tmp_path):
    path = _path(tmp_path, "retrieval:\n  top_k: 5\n")
    with pytest.raises(ValueError, match="missing section"):
        load_config(path)


def test_unknown_section_raises(tmp_path):
    path = _path(tmp_path, _valid() + "extra:\n  x: 1\n")
    with pytest.raises(ValueError, match="unknown section"):
        load_config(path)


def test_removed_stub_section_is_unknown(tmp_path):
    path = _path(tmp_path, _valid() + "stub:\n  min_shared_tokens: 2\n")
    with pytest.raises(ValueError, match="unknown section"):
        load_config(path)


def test_missing_key_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("  timeout_seconds: 30\n", ""))
    with pytest.raises(ValueError, match="llm: missing key"):
        load_config(path)


def test_unknown_key_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("  timeout_seconds: 30\n", "  timeout_seconds: 30\n  extra: 1\n"))
    with pytest.raises(ValueError, match="llm: unknown key"):
        load_config(path)


def test_string_integer_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("top_k: 5", 'top_k: "5"'))
    with pytest.raises(ValueError, match="retrieval.top_k: must be a positive integer"):
        load_config(path)


def test_bool_integer_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("top_k: 5", "top_k: true"))
    with pytest.raises(ValueError, match="retrieval.top_k: must be a positive integer"):
        load_config(path)


def test_non_positive_integer_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("utc_offset_hours: 7", "utc_offset_hours: 0"))
    with pytest.raises(ValueError, match="page.utc_offset_hours: must be a positive integer"):
        load_config(path)


def test_answer_cache_size_non_positive_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("answer_cache_size: 256", "answer_cache_size: 0"))
    with pytest.raises(ValueError, match="page.answer_cache_size: must be a positive integer"):
        load_config(path)


def test_retrieval_unknown_key_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("  embedding_model: gemini-embedding-001\n", "  embedding_model: gemini-embedding-001\n  extra: 1\n"))
    with pytest.raises(ValueError, match="retrieval: unknown key"):
        load_config(path)


def test_rrf_k_non_positive_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("rrf_k: 60", "rrf_k: 0"))
    with pytest.raises(ValueError, match="retrieval.rrf_k: must be a positive integer"):
        load_config(path)


def test_bm25_k1_negative_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("bm25_k1: 1.2", "bm25_k1: -1.2"))
    with pytest.raises(ValueError, match="retrieval.bm25_k1: must be above 0"):
        load_config(path)


def test_bm25_k1_string_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("bm25_k1: 1.2", 'bm25_k1: "1.2"'))
    with pytest.raises(ValueError, match="retrieval.bm25_k1: must be a number"):
        load_config(path)


def test_bm25_k1_bool_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("bm25_k1: 1.2", "bm25_k1: true"))
    with pytest.raises(ValueError, match="retrieval.bm25_k1: must be a number"):
        load_config(path)


def test_bm25_k1_int_becomes_float(tmp_path):
    config = load_config(_path(tmp_path, _valid().replace("bm25_k1: 1.2", "bm25_k1: 1")))
    assert config.retrieval.bm25_k1 == 1.0
    assert isinstance(config.retrieval.bm25_k1, float)


def test_bm25_b_out_of_range_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("bm25_b: 0.75", "bm25_b: 1.5"))
    with pytest.raises(ValueError, match="retrieval.bm25_b: must be between 0 and 1"):
        load_config(path)


def test_bm25_b_bool_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("bm25_b: 0.75", "bm25_b: false"))
    with pytest.raises(ValueError, match="retrieval.bm25_b: must be a number"):
        load_config(path)


def test_bm25_b_int_boundary_becomes_float(tmp_path):
    config = load_config(_path(tmp_path, _valid().replace("bm25_b: 0.75", "bm25_b: 1")))
    assert config.retrieval.bm25_b == 1.0
    assert isinstance(config.retrieval.bm25_b, float)


def test_embedding_model_empty_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("embedding_model: gemini-embedding-001", 'embedding_model: ""'))
    with pytest.raises(ValueError, match="retrieval.embedding_model: must be a non-empty string"):
        load_config(path)


def test_eval_value_above_one_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("over_cautious_max_share: 0.10", "over_cautious_max_share: 1.5"))
    with pytest.raises(ValueError, match="eval.over_cautious_max_share"):
        load_config(path)


def test_eval_bool_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("over_cautious_max_share: 0.10", "over_cautious_max_share: true"))
    with pytest.raises(ValueError, match="eval.over_cautious_max_share"):
        load_config(path)


def test_eval_missing_key_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("  confidence: 0.95\n", ""))
    with pytest.raises(ValueError, match="eval: missing key"):
        load_config(path)


def test_eval_unknown_key_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("  confidence: 0.95\n", "  confidence: 0.95\n  extra: 1\n"))
    with pytest.raises(ValueError, match="eval: unknown key"):
        load_config(path)


def test_llm_thinking_level_minimal_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("thinking_level: low", "thinking_level: minimal"))
    with pytest.raises(ValueError, match="llm.thinking_level: must be low, medium or high"):
        load_config(path)


def test_llm_thinking_level_unknown_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("thinking_level: low", "thinking_level: none"))
    with pytest.raises(ValueError, match="llm.thinking_level: must be low, medium or high"):
        load_config(path)


def test_llm_max_retries_zero_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("max_retries: 6", "max_retries: 0"))
    with pytest.raises(ValueError, match="llm.max_retries: must be a positive integer"):
        load_config(path)


def test_llm_timeout_seconds_string_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("timeout_seconds: 30", 'timeout_seconds: "30"'))
    with pytest.raises(ValueError, match="llm.timeout_seconds: must be a number"):
        load_config(path)


def test_llm_requests_per_minute_string_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("requests_per_minute: 4", 'requests_per_minute: "4"'))
    with pytest.raises(ValueError, match="llm.requests_per_minute: must be a number"):
        load_config(path)


def test_llm_timeout_seconds_int_becomes_float(tmp_path):
    config = load_config(_path(tmp_path, _valid().replace("timeout_seconds: 30", "timeout_seconds: 1")))
    assert config.llm.timeout_seconds == 1.0
    assert isinstance(config.llm.timeout_seconds, float)


def test_llm_requests_per_minute_int_becomes_float(tmp_path):
    config = load_config(_path(tmp_path, _valid().replace("requests_per_minute: 4", "requests_per_minute: 1")))
    assert config.llm.requests_per_minute == 1.0
    assert isinstance(config.llm.requests_per_minute, float)