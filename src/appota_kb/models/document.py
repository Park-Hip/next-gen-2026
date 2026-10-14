"""A simulated ("giả lập") document with its metadata, and one chunk of its body."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    owner: str
    series: str
    topic: str
    access: str
    applies_to: str
    status: str
    effective_from: date | None
    effective_to: date | None
    overrides: str | None
    complements: tuple[str, ...]
    body: str


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    label: str | None
    text: str
