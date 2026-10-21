"""What steps 1-4 leave for one asker on one date."""
from dataclasses import dataclass
from datetime import date, timedelta

from appota_kb.models.document import Chunk, Document
from appota_kb.models.org import Persona


@dataclass(frozen=True)
class Change:
    """The first date a document in the scope leaves it, and the documents that replace it for this asker.

    `successors` holds only documents in the asker's scope on the next day, so a document the asker
    may not read is never named. It is empty when nothing the asker can be told about replaces it.
    """
    document_id: str
    last_day: date
    successors: tuple[Document, ...]

    @property
    def next_day(self) -> date:
        return self.last_day + timedelta(days=1)


@dataclass(frozen=True)
class Scope:
    persona: Persona
    as_of: date
    documents: tuple[Document, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    chunks: tuple[Chunk, ...]
    changes: tuple[Change, ...] = ()

    @property
    def chunk_ids(self) -> frozenset[str]:
        return frozenset(c.id for c in self.chunks)

    def change_for(self, document_id: str) -> Change | None:
        return next((c for c in self.changes if c.document_id == document_id), None)
