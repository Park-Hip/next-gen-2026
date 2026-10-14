"""One search result of step 5, with the numbers behind its rank."""
from dataclasses import dataclass

from appota_kb.models.document import Chunk


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float
    bm25: float
    bm25_rank: int
    dense: float
    dense_rank: int
