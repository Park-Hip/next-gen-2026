"""Load and validate config.yaml into frozen dataclasses.

Nothing is read at import time; web.py calls load_config() once at start-up.
Any missing key, unknown key or wrong type raises ValueError naming the key,
so a bad edit fails the deploy's health check instead of running with a wrong value.
"""
from dataclasses import dataclass
from pathlib import Path
import unicodedata

import yaml

CONFIG = Path(__file__).resolve().parent.parent / "config.yaml"


@dataclass(frozen=True)
class Retrieval:
    top_k: int


@dataclass(frozen=True)
class Stub:
    min_shared_tokens: int
    stopwords: frozenset[str]


@dataclass(frozen=True)
class Page:
    question_max_chars: int
    utc_offset_hours: int


@dataclass(frozen=True)
class Config:
    retrieval: Retrieval
    stub: Stub
    page: Page


def load_config(path: Path = CONFIG) -> Config:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path.name}: must be a mapping")
    expected = {"retrieval", "stub", "page"}
    unknown = set(raw) - expected
    if unknown:
        raise ValueError(f"{path.name}: unknown section(s) {', '.join(sorted(unknown))}")
    missing = expected - set(raw)
    if missing:
        raise ValueError(f"{path.name}: missing section(s) {', '.join(sorted(missing))}")
    return Config(
        retrieval=_load_retrieval(raw["retrieval"], path),
        stub=_load_stub(raw["stub"], path),
        page=_load_page(raw["page"], path),
    )


def _check_keys(path: Path, section: str, raw, expected: set[str]) -> None:
    if not isinstance(raw, dict):
        raise ValueError(f"{path.name} {section}: must be a mapping")
    unknown = set(raw) - expected
    if unknown:
        raise ValueError(f"{path.name} {section}: unknown key(s) {', '.join(sorted(unknown))}")
    missing = expected - set(raw)
    if missing:
        raise ValueError(f"{path.name} {section}: missing key(s) {', '.join(sorted(missing))}")


def _positive_int(path: Path, key: str, value) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{path.name} {key}: must be a positive integer, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{path.name} {key}: must be a positive integer")
    return value


def _stopwords(path: Path, key: str, value) -> frozenset[str]:
    if not isinstance(value, list) or any(not isinstance(s, str) for s in value):
        raise ValueError(f"{path.name} {key}: must be a list of strings")
    return frozenset(unicodedata.normalize("NFC", s).lower() for s in value)


def _load_retrieval(raw, path: Path) -> Retrieval:
    _check_keys(path, "retrieval", raw, {"top_k"})
    return Retrieval(top_k=_positive_int(path, "retrieval.top_k", raw["top_k"]))


def _load_stub(raw, path: Path) -> Stub:
    _check_keys(path, "stub", raw, {"min_shared_tokens", "stopwords"})
    return Stub(
        min_shared_tokens=_positive_int(path, "stub.min_shared_tokens", raw["min_shared_tokens"]),
        stopwords=_stopwords(path, "stub.stopwords", raw["stopwords"]),
    )


def _load_page(raw, path: Path) -> Page:
    _check_keys(path, "page", raw, {"question_max_chars", "utc_offset_hours"})
    return Page(
        question_max_chars=_positive_int(path, "page.question_max_chars", raw["question_max_chars"]),
        utc_offset_hours=_positive_int(path, "page.utc_offset_hours", raw["utc_offset_hours"]),
    )