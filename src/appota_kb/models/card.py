"""The card step 7 picks: answer, conflict or refusal."""
from dataclasses import dataclass
from typing import Literal

from appota_kb.models.document import Chunk, Document

LineKind = Literal["who", "claim", "lead", "quote", "source", "plain"]


@dataclass(frozen=True)
class CardLine:
    """One line of a card, with the role the template renders it as.

    The answer card has claim, quote and source lines per point (ADR 0011).
    The conflict card has lead, quote and plain lines; the refusal card has lead and plain lines.
    """
    kind: LineKind
    text: str


@dataclass(frozen=True)
class Card:
    kind: Literal["answer", "conflict", "refusal"]
    hr: str
    cited: tuple[Chunk, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    # For the log and #14; never shown (R10). A refusal's cause, or "model_flagged" on a conflict card
    # whose pair the rules did not declare (ADR 0014).
    reason: str | None = None
