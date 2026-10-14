"""The chunking rule: one chunk per Điều, or per line for a document without Điều."""
import re

from appota_kb.models.document import Chunk, Document

_DIEU = re.compile(r"^Điều (\d+)\. (.+)$")


def chunks(document: Document) -> list[Chunk]:
    """One chunk per non-empty body line; the procedure is chunked by plain line, the rest by Điều."""
    lines = [line for line in document.body.splitlines() if line.strip()]
    matches = [_DIEU.match(line) for line in lines]
    if any(matches):
        if not all(matches):
            raise ValueError(f"{document.id}: mixes Điều and plain lines")
        numbers = [m.group(1) for m in matches]
        if len(numbers) != len(set(numbers)):
            raise ValueError(f"{document.id}: repeated Điều number")
        return [
            Chunk(id=f"{document.id}#{n}", document_id=document.id, label=f"Điều {n}", text=m.group(2))
            for n, m in zip(numbers, matches)
        ]
    return [
        Chunk(id=f"{document.id}#{i}", document_id=document.id, label=None, text=line)
        for i, line in enumerate(lines, start=1)
    ]
