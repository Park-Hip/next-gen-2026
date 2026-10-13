"""config.yaml loads into Config, and a bad file raises ValueError naming the key."""
from pathlib import Path

import pytest

from app.config import load_config


def test_real_config_loads():
    config = load_config()
    assert isinstance(config.retrieval.top_k, int) and config.retrieval.top_k > 0
    assert isinstance(config.stub.min_shared_tokens, int) and config.stub.min_shared_tokens > 0
    assert isinstance(config.stub.stopwords, frozenset)
    assert config.stub.stopwords and all(isinstance(s, str) for s in config.stub.stopwords)
    assert config.page.question_max_chars > 0
    assert config.page.utc_offset_hours > 0


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
        "stub:\n"
        "  min_shared_tokens: 2\n"
        "  stopwords: [tôi, và]\n"
        "page:\n"
        "  question_max_chars: 300\n"
        "  utc_offset_hours: 7\n"
    )


def test_missing_section_raises(tmp_path):
    path = _path(tmp_path, "retrieval:\n  top_k: 5\n")
    with pytest.raises(ValueError, match="missing section"):
        load_config(path)


def test_unknown_section_raises(tmp_path):
    path = _path(tmp_path, _valid() + "extra:\n  x: 1\n")
    with pytest.raises(ValueError, match="unknown section"):
        load_config(path)


def test_missing_key_raises(tmp_path):
    path = _path(tmp_path, "retrieval:\n  top_k: 5\nstub:\n  min_shared_tokens: 2\npage:\n  question_max_chars: 300\n  utc_offset_hours: 7\n")
    with pytest.raises(ValueError, match="stub: missing key"):
        load_config(path)


def test_unknown_key_raises(tmp_path):
    path = _path(
        tmp_path,
        "retrieval:\n  top_k: 5\nstub:\n  min_shared_tokens: 2\n  stopwords: [tôi]\n  extra: 1\n"
        "page:\n  question_max_chars: 300\n  utc_offset_hours: 7\n",
    )
    with pytest.raises(ValueError, match="stub: unknown key"):
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


def test_stopwords_not_a_list_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("stopwords: [tôi, và]", 'stopwords: "tôi"'))
    with pytest.raises(ValueError, match="stub.stopwords: must be a list of strings"):
        load_config(path)


def test_stopwords_item_not_a_string_raises(tmp_path):
    path = _path(tmp_path, _valid().replace("stopwords: [tôi, và]", "stopwords: [tôi, 1]"))
    with pytest.raises(ValueError, match="stub.stopwords: must be a list of strings"):
        load_config(path)