"""evaluation.committed: the run the committed report names, as the "Test cases" page reads it."""
import re

import pytest

from builders import committed_fixture

from appota_kb.core.paths import ROOT
from appota_kb.evaluation.committed import NO_RESULT, PENDING, committed_run, report_run_path
from appota_kb.evaluation.report import REPORT_REL
from appota_kb.integrations.data_files import cases_sha256


def test_report_run_path():
    text = (ROOT / REPORT_REL).read_text(encoding="utf-8")
    path = report_run_path(text)
    assert path is not None and re.fullmatch(r"results/\d{8}-\d{4}\.jsonl", path)
    assert report_run_path("no results file here") is None


def test_committed_run_none_without_report(cases, tmp_path):
    assert committed_run(cases, root=tmp_path) is None


def test_committed_run_matches_the_report(cases, documents, personas, tmp_path):
    run_id = committed_fixture(tmp_path, documents, personas, cases)
    view = committed_run(cases, root=tmp_path)
    assert view.run_id == run_id
    assert view.results_path == f"results/{run_id}.jsonl"
    assert view.commit == "c" * 7
    assert not view.dirty
    assert view.model == "gemini-3.5-flash-lite, medium"
    assert view.started != ""
    assert set(view.rows) == {row["id"] for row in cases}

    first = view.rows[1]
    assert first.verdict == "Đạt"
    assert first.lesson == "Bài học hàng 1."
    assert first.card["kind"] == "answer"
    assert first.card["lines"][1] == "Bạn được nghỉ phép năm 14 ngày mỗi năm."
    assert first.failures == ()

    # A refusal row that expects a refusal passes; a row that expects an answer fails.
    assert view.rows[6].verdict == "Đạt"
    assert view.rows[6].card["kind"] == "refusal"
    assert view.rows[2].verdict == "Chưa đạt"
    assert "card" in view.rows[2].failures
    assert view.rows[6].lesson == PENDING
    assert dict(view.counts)["Đạt"] + dict(view.counts)["Chưa đạt"] == len(cases)


def test_committed_run_stale_when_cases_change(cases, documents, personas, tmp_path):
    committed_fixture(tmp_path, documents, personas, cases, cases_sha256="abc")
    assert committed_run(cases, root=tmp_path).stale is True

    fresh = tmp_path / "fresh"
    committed_fixture(fresh, documents, personas, cases, cases_sha256=cases_sha256())
    assert committed_run(cases, root=fresh).stale is False


def test_committed_run_missing_results_file_raises(cases, documents, personas, tmp_path):
    run_id = committed_fixture(tmp_path, documents, personas, cases)
    (tmp_path / "results" / f"{run_id}.jsonl").unlink()
    with pytest.raises(ValueError, match=run_id):
        committed_run(cases, root=tmp_path)


def test_committed_run_on_the_real_files(cases):
    """The page and docs/mission2/test_report.md read the same run, so every verdict agrees."""
    text = (ROOT / REPORT_REL).read_text(encoding="utf-8")
    view = committed_run(cases)
    assert f"`{view.results_path}`" in text

    table = {}
    for line in text.splitlines():
        match = re.match(r"\| (\d+) \|", line)
        if match:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
            table[int(cells[0])] = (cells[4], cells[5])
    assert set(table) == {row["id"] for row in cases}
    for row_id, (verdict, lesson) in table.items():
        assert view.rows[row_id].verdict == verdict
        assert view.rows[row_id].lesson.replace("|", "\\|") == lesson
    assert NO_RESULT not in {r.verdict for r in view.rows.values()}
