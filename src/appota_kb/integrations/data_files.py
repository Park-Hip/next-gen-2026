"""Load and validate the simulated data in data/; the only code that reads data/.

Every unit, person, document and number here is simulated ("giả lập").
Nothing is loaded at import time; callers load what they need.
Malformed data raises ValueError naming the offending file or unit.
"""
from datetime import date
import hashlib
from pathlib import Path
import re

import yaml

from appota_kb.core.paths import DATA
from appota_kb.models.document import Document
from appota_kb.models.org import Org, Persona

_FRONT_MATTER = re.compile(r"---\n(.*?)\n---\n\n(.*)", re.S)
_FIELDS = frozenset({
    "id", "title", "owner", "series", "topic", "access",
    "applies_to", "status", "effective_from", "effective_to", "overrides", "complements",
})


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


def _check_versions_and_overrides(documents: list[Document]) -> None:
    """Publish-time checks on published documents; a draft is checked when it is published.

    A tie on effective_from, a self-override and an override cycle each make the rules
    pick by file name or drop a series, so they fail the load instead.
    """
    published = [d for d in documents if d.status == "published"]
    versions: dict[tuple[str, date], list[str]] = {}
    for d in published:
        if d.effective_from is not None:
            versions.setdefault((d.series, d.effective_from), []).append(d.id)
    for (series, effective_from), ids in versions.items():
        if len(ids) > 1:
            raise ValueError(
                f"series {series} has two published versions with effective_from {effective_from}: "
                + ", ".join(sorted(ids))
            )
    edges: dict[str, dict[str, list[str]]] = {}
    for d in published:
        if d.overrides is None:
            continue
        if d.overrides == d.series:
            raise ValueError(f"{d.id}: overrides names its own series {d.series}")
        edges.setdefault(d.series, {}).setdefault(d.overrides, []).append(d.id)
    finished: set[str] = set()

    def visit(series: str, path: list[str]) -> None:
        if series in path:
            cycle = path[path.index(series):] + [series]
            ids = sorted({i for a, b in zip(cycle, cycle[1:]) for i in edges[a][b]})
            raise ValueError(f"overrides cycle: {' -> '.join(cycle)} ({', '.join(ids)})")
        if series in finished:
            return
        for target in sorted(edges.get(series, {})):
            visit(target, path + [series])
        finished.add(series)

    for series in sorted(edges):
        visit(series, [])


def load_documents(root: Path = DATA) -> list[Document]:
    documents = [_load_document(path) for path in sorted((root / "documents").glob("*.md"))]
    series = {d.series for d in documents}
    for d in documents:
        if d.overrides is not None and d.overrides not in series:
            raise ValueError(f"{d.id}: overrides names an unknown series {d.overrides}")
        for name in d.complements:
            if name not in series:
                raise ValueError(f"{d.id}: complements names an unknown series {name}")
    _check_versions_and_overrides(documents)
    return documents


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
            company=org.hr_unit(unit),
            path=org.path(unit),
            roles=tuple(p["roles"]),
            hr=org.hr_for(unit),
        )
    return personas


def load_test_cases(root: Path = DATA) -> list[dict]:
    return yaml.safe_load((root / "test_cases.yaml").read_text(encoding="utf-8"))


def cases_sha256(root: Path = DATA) -> str:
    """The hash of data/test_cases.yaml, recorded with every run to detect a changed test file."""
    return hashlib.sha256((root / "test_cases.yaml").read_bytes()).hexdigest()
