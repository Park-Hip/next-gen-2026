"""The card step 7 picks: answer, conflict or refusal."""
from dataclasses import dataclass
from typing import Literal

from appota_kb.models.document import Chunk, Document

LineKind = Literal["who", "note", "claim", "lead", "quote", "source", "notice", "plain"]


@dataclass(frozen=True)
class CardLine:
    """One line of a card, with the role the template renders it as.

    The answer card has claim, quote and source lines per point (ADR 0011), and a notice line under the
    source line of a document that changes later (ADR 0012).
    The answer card also has one fixed note line under the asker line (#77).
    The conflict card has lead, quote, notice and plain lines; the refusal card has lead and plain lines.

    A source line or a conflict quote links to the version it cites: `chunks` holds the cited chunk ids and
    `ref` the part of `text` that becomes the link. No URL is built here; the page builds it.
    """
    kind: LineKind
    text: str
    chunks: tuple[str, ...] = ()
    ref: str = ""


@dataclass(frozen=True)
class Card:
    kind: Literal["answer", "conflict", "refusal"]
    hr: str
    cited: tuple[Chunk, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    # A refusal's cause, or "model_flagged" on a conflict card whose pair the rules did not declare (ADR 0014).
    # It picks the refusal text (ADR 0017) and goes to the log and #14; it is never shown itself.
    reason: str | None = None
