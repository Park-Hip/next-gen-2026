"""View models for the judges' guide pages: the simulated company and the test cases.

Pure functions over loaded data: no file reads, no model, no network. Status, scope and
conflicts come from services.scope, so these pages can never disagree with the rules.
Every date is formatted dd/mm/yyyy here, so the templates only print strings.
"""
from dataclasses import dataclass
from datetime import date
from typing import Literal
from urllib.parse import urlencode

from appota_kb.evaluation.report import LIMITATION_ISSUES
from appota_kb.evaluation.review import CARD_LABEL
from appota_kb.models.document import Document
from appota_kb.models.org import Org, Persona
from appota_kb.services.citations import fold
from appota_kb.services.scope import in_force, scope

DocStatus = Literal["in_force", "superseded", "not_yet", "ended", "draft", "no_date"]

STATUS_LABEL: dict[str, str] = {
    "in_force": "Đang hiệu lực",
    "superseded": "Đã có bản mới hơn",
    "not_yet": "Chưa đến ngày hiệu lực",
    "ended": "Hết hiệu lực",
    "draft": "Dự thảo, chưa ban hành",
    "no_date": "Đã ban hành nhưng chưa có ngày hiệu lực",
}
KIND_LABEL: dict[str, str] = {"good": "Làm tốt", "hard": "Khó", "limitation": "Chưa xử lý tốt"}


def format_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


@dataclass(frozen=True)
class UnitView:
    name: str
    level: int                      # 1 for the top unit
    hr: str | None                  # only on units that have their own HR contact
    personas: tuple[str, ...]       # names of the personas whose unit this is
    children: tuple["UnitView", ...]


def org_tree(org: Org, personas: dict[str, Persona]) -> tuple[UnitView, ...]:
    """The units as a tree, children in org.yaml order."""

    def build(name: str, level: int) -> UnitView:
        return UnitView(
            name=name,
            level=level,
            hr=org.hr.get(name),
            personas=tuple(p.name for p in personas.values() if p.unit == name),
            children=tuple(build(child, level + 1) for child, up in org.parent.items() if up == name),
        )

    return tuple(build(name, 1) for name, up in org.parent.items() if up is None)


def document_status(doc: Document, documents: list[Document], day: date) -> DocStatus:
    """Why a document is or is not in force on `day`; reuses scope.in_force, so it agrees with the rules."""
    if doc.status == "draft":
        return "draft"
    if doc.effective_from is None:
        return "no_date"
    if doc.effective_from > day:
        return "not_yet"
    if doc.id in {d.id for d in in_force(documents, day)}:
        return "in_force"
    if doc.effective_to is not None and day > doc.effective_to:
        return "ended"
    return "superseded"


def access_label(doc: Document) -> str:
    access = doc.access
    if access == "all_staff":
        return "Mọi nhân sự"
    if access.startswith("roles:"):
        return "Chỉ vai trò: " + ", ".join(access[6:].split(","))
    return "Chỉ nhân sự thuộc " + access[5:]


def _below(org: Org, unit: str) -> list[str]:
    """Every unit under `unit`, in org.yaml order."""
    return [name for name in org.parent if name != unit and unit in org.path(name)]


def applies_label(doc: Document, org: Org) -> str:
    below = _below(org, doc.applies_to)
    if not below:
        return doc.applies_to
    return f"{doc.applies_to} và đơn vị bên dưới: {', '.join(below)}"


def validity_label(doc: Document) -> str:
    if doc.effective_from is None:
        return "Chưa có ngày hiệu lực"
    text = "Từ " + format_date(doc.effective_from)
    if doc.effective_to is not None:
        text += " đến " + format_date(doc.effective_to)
    return text


@dataclass(frozen=True)
class DocumentView:
    id: str
    title: str
    owner: str
    status: DocStatus
    status_label: str
    validity: str
    applies_to: str
    access: str
    relations: tuple[str, ...]      # "Dùng thay: LEAVE-GROUP", "Bổ sung: LEAVE-GAMECO"
    lines: tuple[str, ...]          # the body, one line per clause


def series_views(documents: list[Document], org: Org, day: date) -> list[tuple[str, list[DocumentView]]]:
    """Documents grouped by series; series by their first id, versions by effective_from (undated last)."""
    grouped: dict[str, list[Document]] = {}
    for doc in documents:
        grouped.setdefault(doc.series, []).append(doc)
    out = []
    for series in sorted(grouped, key=lambda s: min(d.id for d in grouped[s])):
        versions = sorted(
            grouped[series],
            key=lambda d: (d.effective_from is None, d.effective_from or date.min, d.id),
        )
        views = []
        for doc in versions:
            status = document_status(doc, documents, day)
            relations = []
            if doc.overrides:
                relations.append(f"Dùng thay: {doc.overrides}")
            if doc.complements:
                relations.append("Bổ sung: " + ", ".join(doc.complements))
            views.append(
                DocumentView(
                    id=doc.id,
                    title=doc.title,
                    owner=doc.owner,
                    status=status,
                    status_label=STATUS_LABEL[status],
                    validity=validity_label(doc),
                    applies_to=applies_label(doc, org),
                    access=access_label(doc),
                    relations=tuple(relations),
                    lines=tuple(doc.body.splitlines()),
                )
            )
        out.append((series, views))
    return out


@dataclass(frozen=True)
class PersonaView:
    persona: Persona
    path: str                       # "Tập đoàn > GameCo > Studio"
    roles: str                      # "employee, hr_group"
    scope_titles: tuple[str, ...]   # the documents the rules leave this person on `day`
    conflicts: tuple[str, ...]      # "Quy chế A và Quy chế B"


def persona_views(personas: dict[str, Persona], documents: list[Document], day: date) -> list[PersonaView]:
    out = []
    for persona in personas.values():
        scoped = scope(persona, day, documents)
        out.append(
            PersonaView(
                persona=persona,
                path=" > ".join(persona.path),
                roles=", ".join(persona.roles),
                scope_titles=tuple(d.title for d in scoped.documents),
                conflicts=tuple(f"{a.title} và {b.title}" for a, b in scoped.conflicts),
            )
        )
    return out


@dataclass(frozen=True)
class Wording:
    text: str
    href: str | None                # the main page filled in with this case; None for a data_edit row


@dataclass(frozen=True)
class CaseView:
    id: int
    kind: str
    kind_label: str
    card_label: str
    purpose: str
    persona: Persona
    as_of: str                      # dd/mm/yyyy
    wordings: tuple[Wording, ...]
    expected_answer: str
    data_edit_note: str | None
    limitation_issue: str | None


def same_question_groups(rows: list[dict]) -> list[list[int]]:
    """Row ids that share a question and a date but come from at least two askers, by first row id.

    A data_edit row runs on other data than the page, so it is never part of a group.
    """
    by_key: dict[tuple[str, date], list[dict]] = {}
    for row in rows:
        if "data_edit" in row:
            continue
        by_key.setdefault((fold(row["questions"][0]), row["as_of"]), []).append(row)
    groups = [
        [r["id"] for r in group]
        for group in by_key.values()
        if len({r["persona"] for r in group}) >= 2
    ]
    return sorted(groups, key=lambda g: g[0])


def _case_view(row: dict, personas: dict[str, Persona], documents: list[Document]) -> CaseView:
    edit = row.get("data_edit")
    note = None
    if edit:
        title = next(d.title for d in documents if d.id == edit["document"])
        changes = []
        if edit.get("remove"):
            changes.append(f'bỏ dòng "{edit["remove"]}"')
        for key, value in (edit.get("set") or {}).items():
            if key == "topic":
                changes.append(f'đổi chủ đề thành "{value}"')
            elif key == "complements":
                if value:
                    changes.append("khai báo bổ sung: " + ", ".join(value))
                else:
                    changes.append("bỏ khai báo bổ sung")
        note = (
            "Tình huống này chạy trên dữ liệu đã sửa: "
            + " và ".join(changes)
            + f" trong {title}. "
            'Trang "Ask" dùng dữ liệu gốc nên không thử trực tiếp được.'
        )
    wordings = tuple(
        Wording(
            text=question,
            href=None
            if edit
            else "/?" + urlencode({"persona": row["persona"], "as_of": row["as_of"].isoformat(), "q": question}),
        )
        for question in row["questions"]
    )
    return CaseView(
        id=row["id"],
        kind=row["kind"],
        kind_label=KIND_LABEL[row["kind"]],
        card_label=CARD_LABEL[row["card"]],
        purpose=row["purpose"],
        persona=personas[row["persona"]],
        as_of=format_date(row["as_of"]),
        wordings=wordings,
        expected_answer=row["expected_answer"],
        data_edit_note=note,
        limitation_issue=LIMITATION_ISSUES.get(row["id"]),
    )


def case_views(
    rows: list[dict], personas: dict[str, Persona], documents: list[Document]
) -> tuple[list[CaseView], list[CaseView]]:
    """(the featured same-question rows, the rest in file order); every row appears exactly once."""
    featured_ids = [i for group in same_question_groups(rows) for i in group]
    views = {row["id"]: _case_view(row, personas, documents) for row in rows}
    featured = [views[i] for i in featured_ids]
    rest = [views[row["id"]] for row in rows if row["id"] not in featured_ids]
    return featured, rest
