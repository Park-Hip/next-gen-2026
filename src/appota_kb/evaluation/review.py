"""Hiep's reading of a run: the review YAML he fills in and the review sheet he reads (decision D6).

The YAML holds `faithful` (answer cards) and `lesson` (every row); the sheet shows, per row,
the question, the expectation, the card, the raw reply and the answer above its quotes
against the cited chunks.
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


def answer_of(record: dict) -> str:
    """The model's answer; a run from before ADR 0018 stored one claim per point instead."""
    answer = record.get("answer")
    if isinstance(answer, str) and answer.strip():
        return answer
    claims = [p.get("claim") for p in record.get("points") or [] if isinstance(p, dict)]
    joined = " ".join(claim for claim in claims if isinstance(claim, str) and claim.strip())
    return joined or "(none)"


def build_review_sheet(run_id: str, scores: list[RowScore], reviews: dict) -> str:
    """The sheet Hiep reads: per row the question, expectation, card, raw reply, answer and quotes."""
    out = [f"# Review sheet for run {run_id}", ""]
    out.append("Read the answer against each quote and the cited chunks; mark `faithful` in the review YAML.")
    out.append("If the answer is unfaithful, name the error: a changed number, a dropped condition, an added fact, a flipped meaning, the wrong people, or deciding which rule applies.")
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
            text = line.get("text", "") if isinstance(line, dict) else line
            out.append(f"  - {text}")
        out.append(f"- Raw reply: {score.record.get('raw') or '(empty)'}")
        answer = answer_of(score.record)
        if answer != "(none)":
            out.append(f"- Answer: {answer}")
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
        if card and card["kind"] == "answer":
            faithful = faithful_of(reviews.get(row["id"])) or "[chờ Hiệp]"
        else:
            faithful = "-"
        out.append(f"- Faithful: {faithful}")
        out.append(f"- Lesson: {lesson_of(reviews.get(row["id"]))}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"
