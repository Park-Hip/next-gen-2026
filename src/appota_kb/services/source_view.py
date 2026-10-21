"""What the "open the source" page shows: one cited version of a document, checked against the asker's scope.

No FastAPI and no LLM here, and nothing is written or logged.
The page opens only when every requested chunk is in the scope of the asker on the as-of date and all of
them belong to one document; every other case gives None, so the caller shows the same "not found" page
for a chunk that is out of scope and for one that does not exist (R10).
"""
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from appota_kb.models.scope import Scope
from appota_kb.services.card_text import NOTICE_LABEL, change_text, validity_window


@dataclass(frozen=True)
class SourceChunk:
    anchor: str          # "c-2", the fragment that scrolls to this chunk
    label: str | None    # "Điều 2", or None for a document without Điều
    text: str
    cited: bool


@dataclass(frozen=True)
class SourceView:
    title: str
    applies_to: str
    window: str          # "từ 01/01/2026 đến hết 31/12/2026", the same words as the card's source line
    notice: str | None   # "Sắp thay đổi: ...", from the rules only (ADR 0012)
    hr: str
    asker: str
    as_of: date
    chunks: tuple[SourceChunk, ...]   # the whole version, in order

    @property
    def first_cited(self) -> str:
        return next(c.anchor for c in self.chunks if c.cited)


def anchor_of(chunk_id: str) -> str:
    """The page anchor of a chunk id `<document id>#<n>`."""
    return "c-" + chunk_id.rsplit("#", 1)[-1]


def source_view(scope: Scope, chunk_ids: Sequence[str]) -> SourceView | None:
    cited = tuple(dict.fromkeys(chunk_ids))
    if not cited or not set(cited) <= scope.chunk_ids:
        return None
    by_id = {c.id: c for c in scope.chunks}
    document_ids = {by_id[cid].document_id for cid in cited}
    if len(document_ids) != 1:
        return None
    doc = next(d for d in scope.documents if d.id in document_ids)
    persona = scope.persona
    change = scope.change_for(doc.id)
    return SourceView(
        title=doc.title,
        applies_to=doc.applies_to,
        window=validity_window(doc, change),
        notice=NOTICE_LABEL + change_text(doc, change, persona.hr) if change is not None else None,
        hr=persona.hr,
        asker=f"nhân sự {persona.company}, {persona.unit}",
        as_of=scope.as_of,
        chunks=tuple(
            SourceChunk(anchor_of(c.id), c.label, c.text, c.id in cited)
            for c in scope.chunks
            if c.document_id == doc.id
        ),
    )

