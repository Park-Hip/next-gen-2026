"""The card step 7 picks: answer, conflict or refusal."""
from dataclasses import dataclass
from typing import Literal

from appota_kb.models.document import Chunk, Document


@dataclass(frozen=True)
class Card:
    kind: Literal["answer", "conflict", "refusal"]
    hr: str
    cited: tuple[Chunk, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    reason: str | None = None  # refusals only, for the log and #14; never shown (R10)
