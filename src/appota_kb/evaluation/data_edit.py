"""The data_edit of a test case row: a line removed and/or metadata fields set."""
from dataclasses import replace
from datetime import date

from appota_kb.models.document import Document


def _metadata_changes(doc_id: str, values: dict) -> dict:
    """The allowed metadata changes: topic (a string), complements (a list of series ids) and effective_to (a date)."""
    changes = {}
    for key, value in values.items():
        if key == "topic":
            if not isinstance(value, str) or not value:
                raise ValueError(f"{doc_id}: data_edit topic must be a non-empty string")
            changes["topic"] = value
        elif key == "complements":
            if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                raise ValueError(f"{doc_id}: data_edit complements must be a list of strings")
            changes["complements"] = tuple(value)
        elif key == "effective_to":
            if not isinstance(value, date):
                raise ValueError(f"{doc_id}: data_edit effective_to must be a date")
            changes["effective_to"] = value
        else:
            raise ValueError(f"{doc_id}: data_edit cannot set {key}")
    return changes


def with_edit(documents: list[Document], edit: dict) -> list[Document]:
    """A copy of documents with edit["remove"] removed and edit["set"] applied to edit["document"]."""
    doc_id = edit["document"]
    remove = edit.get("remove")
    values = edit.get("set") or {}
    if remove is None and not values:
        raise ValueError(f"{doc_id}: data_edit needs remove or set")
    changes = _metadata_changes(doc_id, values)
    found = False
    out = []
    for d in documents:
        if d.id != doc_id:
            out.append(d)
            continue
        found = True
        if "effective_to" in changes and (d.effective_from is None or changes["effective_to"] < d.effective_from):
            raise ValueError(f"{doc_id}: data_edit effective_to is before effective_from")
        body = d.body
        if remove is not None:
            if remove not in body.splitlines():
                raise ValueError(f"{doc_id}: data_edit line not found")
            body = "\n".join(line for line in body.splitlines() if line != remove)
        out.append(replace(d, body=body, **changes))
    if not found:
        raise ValueError(f"{doc_id}: not a loaded document")
    return out
