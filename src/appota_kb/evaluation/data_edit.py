"""The data_edit of a test case row: the documents with one line removed."""
from dataclasses import replace

from appota_kb.models.document import Document


def with_edit(documents: list[Document], edit: dict) -> list[Document]:
    """A copy of documents with the line edit["remove"] removed from edit["document"]."""
    doc_id = edit["document"]
    remove = edit["remove"]
    found = False
    out = []
    for d in documents:
        if d.id != doc_id:
            out.append(d)
            continue
        found = True
        if remove not in d.body.splitlines():
            raise ValueError(f"{doc_id}: data_edit line not found")
        body = "\n".join(line for line in d.body.splitlines() if line != remove)
        out.append(replace(d, body=body))
    if not found:
        raise ValueError(f"{doc_id}: not a loaded document")
    return out
