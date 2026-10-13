"""Load and validate the simulated data in data/.

Every unit, person, document and number here is simulated ("giả lập").
Nothing is loaded at import time; callers load what they need.
Malformed data raises ValueError naming the offending file or unit.
"""
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path
import re

import yaml

DATA = Path(__file__).resolve().parent.parent / "data"

_FRONT_MATTER = re.compile(r"---\n(.*?)\n---\n\n(.*)", re.S)
_FIELDS = frozenset({
    "id", "title", "owner", "series", "topic", "access",
    "applies_to", "status", "effective_from", "effective_to", "overrides", "complements",
})
_DIEU = re.compile(r"^Điều (\d+)\. (.+)$")


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    owner: str
    series: str
    topic: str
    access: str
    applies_to: str
    status: str
    effective_from: date | None
    effective_to: date | None
    overrides: str | None
    complements: tuple[str, ...]
    body: str


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    label: str | None
    text: str


@dataclass(frozen=True)
class Persona:
    id: str
    name: str
    unit: str
    path: tuple[str, ...]
    roles: tuple[str, ...]
    hr: str


@dataclass(frozen=True)
class Org:
    parent: dict[str, str | None]
    hr: dict[str, str]

    def path(self, unit: str) -> tuple[str, ...]:
        path = []
        while unit is not None:
            path.insert(0, unit)
            unit = self.parent[unit]
        return tuple(path)

    def hr_for(self, unit: str) -> str:
        for name in reversed(self.path(unit)):
            if name in self.hr:
                return self.hr[name]
        raise ValueError(f"{unit}: no HR contact on its path")


def _load_document(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    match = _FRONT_MATTER.match(text)
    if match is None:
        raise ValueError(f"{path.name}: no front matter")
    meta = yaml.safe_load(match.group(1))
    if set(meta) != _FIELDS:
        raise ValueError(f"{path.name}: front matter keys are not exactly the metadata fields")
    if meta["id"] != path.stem:
        raise ValueError(f"{path.name}: file name is not the id {meta['id']}")
    if meta["status"] not in ("published", "draft"):
        raise ValueError(f"{path.name}: status {meta['status']!r} is not published or draft")
    access = meta["access"]
    if access != "all_staff" and not access.startswith(("unit:", "roles:")):
        raise ValueError(f"{path.name}: access {access!r} has an unknown form")
    effective_from = meta["effective_from"]
    effective_to = meta["effective_to"]
    if effective_from is not None and effective_to is not None and effective_to < effective_from:
        raise ValueError(f"{path.name}: effective_to is before effective_from")
    return Document(
        id=meta["id"],
        title=meta["title"],
        owner=meta["owner"],
        series=meta["series"],
        topic=meta["topic"],
        access=access,
        applies_to=meta["applies_to"],
        status=meta["status"],
        effective_from=effective_from,
        effective_to=effective_to,
        overrides=meta["overrides"],
        complements=tuple(meta["complements"] or []),
        body=match.group(2).strip(),
    )


def load_documents(root: Path = DATA) -> list[Document]:
    documents = [_load_document(path) for path in sorted((root / "documents").glob("*.md"))]
    series = {d.series for d in documents}
    for d in documents:
        if d.overrides is not None and d.overrides not in series:
            raise ValueError(f"{d.id}: overrides names an unknown series {d.overrides}")
        for name in d.complements:
            if name not in series:
                raise ValueError(f"{d.id}: complements names an unknown series {name}")
    return documents


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


def load_org(root: Path = DATA) -> Org:
    units = yaml.safe_load((root / "org.yaml").read_text(encoding="utf-8"))
    parent = {u["name"]: u["parent"] for u in units}
    hr = {u["name"]: u["hr"] for u in units if u.get("hr")}
    for name, up in parent.items():
        if up is not None and up not in parent:
            raise ValueError(f"org.yaml: {name} has unknown parent {up}")
    for name in parent:
        seen = set()
        cur = name
        while cur is not None:
            if cur in seen:
                raise ValueError(f"org.yaml: cycle through {cur}")
            seen.add(cur)
            cur = parent[cur]
    org = Org(parent=parent, hr=hr)
    for name in parent:
        if all(u not in hr for u in org.path(name)):
            raise ValueError(f"org.yaml: {name} has no HR contact on its path")
    return org


def load_personas(org: Org, root: Path = DATA) -> dict[str, Persona]:
    raw = yaml.safe_load((root / "personas.yaml").read_text(encoding="utf-8"))
    personas = {}
    for p in raw:
        unit = p["unit"]
        if unit not in org.parent:
            raise ValueError(f"personas.yaml: {p['id']} has unknown unit {unit}")
        personas[p["id"]] = Persona(
            id=p["id"],
            name=p["name"],
            unit=unit,
            path=org.path(unit),
            roles=tuple(p["roles"]),
            hr=org.hr_for(unit),
        )
    return personas


def load_test_cases(root: Path = DATA) -> list[dict]:
    return yaml.safe_load((root / "test_cases.yaml").read_text(encoding="utf-8"))


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