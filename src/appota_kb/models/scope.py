"""What steps 1-4 leave for one asker on one date."""
from dataclasses import dataclass
from datetime import date

from appota_kb.models.document import Chunk, Document
from appota_kb.models.org import Persona


@dataclass(frozen=True)
class Scope:
    persona: Persona
    as_of: date
    documents: tuple[Document, ...]
    conflicts: tuple[tuple[Document, Document], ...]
    chunks: tuple[Chunk, ...]

    @property
    def chunk_ids(self) -> frozenset[str]:
        return frozenset(c.id for c in self.chunks)
