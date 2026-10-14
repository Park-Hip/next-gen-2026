"""Hiep's reading of a run: the review YAML he fills in and the review sheet he reads (decision D6).

The YAML holds `faithful` (answer cards) and `lesson` (every row); the sheet shows, per row,
the question, the expectation, the card, the raw reply and the points against the cited chunks.
"""
from pathlib import Path

import yaml

from appota_kb.evaluation.score import CHECKS, RowScore, faithful_of

KIND_LABEL = {"good": "good", "hard": "hard", "limitation": "limitation"}
CARD_LABEL = {"answer": "Trả lời", "conflict": "Mâu thuẫn", "refusal": "Từ chối"}


def review_skeleton(run_id: str, rows: list[dict]) -> str:
    """The review YAML Hiep fills in: faithful (answer cards) and lesson (every row)."""
    lines = [
        f"# Hiep's reading of run {run_id} (decision D6). faithful: yes or no, answer cards only. "
        "lesson: in Vietnamese.",
    ]
    for row in rows:
        lines.append(f"- row: {row['id']}")
        lines.append("  faithful:")
        lines.append("  lesson:")
        lines.append("  note:")
    return "\n".join(lines) + "\n"


def load_reviews(path: Path) -> dict:
    """The review YAML as {row_id: entry}; an empty faithful is None."""
    if not path.exists():
        return {}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    return {entry["row"]: entry for entry in raw}


def lesson_of(review: dict | None) -> str:
    if not review:
        return "[chờ Hiệp]"
    lesson = review.get("lesson")
    return lesson.strip() if isinstance(lesson, str) and lesson.strip() else "[chờ Hiệp]"


def build_review_sheet(run_id: str, scores: list[RowScore], reviews: dict) -> str:
    """The sheet Hiep reads: per row the question, expectation, card, raw reply and points."""
    out = [f"# Review sheet for run {run_id}", ""]
    out.append("Read every answer card against the cited chunks; mark `faithful` in the review YAML.")
    out.append("")
    for score in scores:
        row = score.row
        out.append(f"## Row {row['id']} ({KIND_LABEL[row['kind']]}, {CARD_LABEL[row['card']]})")
        out.append("")
        out.append(f"- Question: {row['questions'][0]}")
        out.append(f"- Kỳ vọng: {row['expected_answer']}")
        if score.record is None:
            out.append("- Kết quả: chỉ có lỗi, không có thẻ.")
            out.append("")
            continue
        card = score.record.get("card")
        lines = card.get("lines") or [] if card else []
        out.append("- Thẻ:")
        for line in lines:
            out.append(f"  - {line}")
        out.append(f"- Raw reply: {score.record.get('raw') or '(empty)'}")
        points = score.record.get("points")
        if points:
            out.append("- Points:")
            for point in points:
                out.append(f"  - quote: {point['quote']}")
                for cid in point.get("chunks", []):
                    full = score.record.get("retrieved_text") or {}
                    out.append(f"    chunk {cid}: {full.get(cid, '(not retrieved)')}")
        elif points is None:
            out.append("- Points: malformed output.")
        failed = [name for name in CHECKS if name in score.checks and not score.checks[name]]
        out.append("- Checks: " + (", ".join(f"{name}: FAIL" for name in failed) if failed else "all applied checks pass"))
        out.append(f"- Faithful: {faithful_of(reviews.get(row['id'])) or '[chờ Hiệp]'}")
        out.append(f"- Lesson: {lesson_of(reviews.get(row['id']))}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"
