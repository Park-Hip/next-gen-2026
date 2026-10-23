"""The committed run the demo's "Test cases" page shows: the run the committed report names.

Reads only committed files (docs/test_report.md, results/<run_id>.jsonl and its
review YAML), scores them offline and calls no model. The page and the report therefore
cannot disagree: both are built from the same records, checks and review file.
"""
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re

from appota_kb.core.paths import ROOT
from appota_kb.evaluation.report import REPORT_REL, failures
from appota_kb.evaluation.review import lesson_of, load_reviews
from appota_kb.evaluation.score import load_run, score_all, verdicts
from appota_kb.integrations.data_files import cases_sha256

PENDING = "[chờ Hiệp]"
NO_RESULT = "Chưa có kết quả"
_RESULTS_FILE = re.compile(r"`(results/[^`]+\.jsonl)`")


def report_run_path(text: str) -> str | None:
    """The `results/<run_id>.jsonl` the report header names, or None."""
    match = _RESULTS_FILE.search(text)
    return match.group(1) if match else None


@dataclass(frozen=True)
class RowResult:
    card: dict | None            # record["card"]: {"kind", "lines", ...}; None when the row has no card
    verdict: str                 # "Đạt", "Chưa đạt", "[chờ Hiệp]" or "Chưa có kết quả"
    failures: tuple[str, ...]    # the failed checks, as the report lists them
    lesson: str                  # Hiep's lesson, or "[chờ Hiệp]"


def card_with_line_kinds(card: dict) -> dict:
    """A card whose lines are {kind, text}, including cards saved before ADR 0011.

    Old records stored flat strings: who, then a lead, then quotes or sources.
    The fallback lets /cases keep showing a run made before the line kinds existed.
    """
    lines = card.get("lines") or []
    if not lines or isinstance(lines[0], dict):
        return card
    kind = card.get("kind")
    converted = []
    for i, text in enumerate(lines):
        if i == 0:
            line_kind = "who"
        elif kind == "conflict" and i > 1:
            line_kind = "quote" if text.endswith('"') else "plain"
        elif kind == "answer":
            line_kind = "quote" if text.startswith('"') else "source"
        elif kind == "refusal" and i > 1:
            line_kind = "plain"
        else:
            line_kind = "lead"
        converted.append({"kind": line_kind, "text": text})
    return {**card, "lines": converted}


@dataclass(frozen=True)
class RunView:
    run_id: str
    started: str                 # "14/10/2026 13:17"
    commit: str                  # first 7 characters
    dirty: bool
    model: str                   # "gemini-3.5-flash-lite, medium"
    results_path: str            # "results/<run_id>.jsonl"
    stale: bool                  # the test file changed after this run
    rows: dict[int, RowResult]
    counts: tuple[tuple[str, int], ...]   # verdict and number of rows, in a fixed order


def committed_run(rows: list[dict], root: Path = ROOT) -> RunView | None:
    """The run the committed report names, or None when no report is committed.

    A report that names a results file that is not there is a broken deploy: ValueError.
    """
    report = root / REPORT_REL
    if not report.exists():
        return None
    rel = report_run_path(report.read_text(encoding="utf-8"))
    if rel is None:
        raise ValueError(f"{REPORT_REL.as_posix()}: names no results file")
    results = root / rel
    if not results.exists():
        raise ValueError(f"{REPORT_REL.as_posix()} names {rel}, which does not exist")

    run_id = results.stem
    records = load_run(results)
    scores = score_all(rows, records)
    reviews = load_reviews(root / "results" / f"{run_id}.review.yaml")
    marks = verdicts(scores, reviews)

    result_rows: dict[int, RowResult] = {}
    for score in scores:
        row_id = score.row["id"]
        record = score.record
        card = record.get("card") if record else None
        result_rows[row_id] = RowResult(
            card=card_with_line_kinds(card) if card else None,
            verdict=marks[row_id] or NO_RESULT,
            failures=tuple(failures(score)) if record else (),
            lesson=lesson_of(reviews.get(row_id)),
        )

    first = records[0] if records else {}
    started = ""
    if first.get("started_at"):
        started = datetime.fromisoformat(first["started_at"]).strftime("%d/%m/%Y %H:%M")
    tally = [r.verdict for r in result_rows.values()]
    counts = tuple(
        (name, tally.count(name)) for name in ("Đạt", "Chưa đạt", PENDING, NO_RESULT) if name in tally
    )
    return RunView(
        run_id=run_id,
        started=started,
        commit=str(first.get("commit", "?"))[:7],
        dirty=bool(first.get("dirty")),
        model=f"{first.get('model', '?')}, {first.get('thinking_level', '?')}",
        results_path=rel,
        stale=bool(first.get("cases_sha256")) and first["cases_sha256"] != cases_sha256(),
        rows=result_rows,
        counts=counts,
    )
