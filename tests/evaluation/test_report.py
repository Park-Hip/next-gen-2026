"""evaluation.report: the generated test report, on a full fake run and on the committed run."""
import pytest

from builders import chunk_text, fake_meta, row_by_id, scripted_answerer
from fakes import no_points, reply_citing

from appota_kb.core.paths import ROOT
from appota_kb.evaluation.committed import report_run_path
import appota_kb.evaluation.report as report_mod
from appota_kb.evaluation.report import REPORT_REL, _write_lf, build_report
from appota_kb.evaluation.report import main as report_main
from appota_kb.evaluation.review import load_reviews
from appota_kb.evaluation.run import run
from appota_kb.evaluation.score import load_run, score_all


def test_report_on_full_fake_run(cases, personas, documents, tmp_path, monkeypatch):
    monkeypatch.setattr(report_mod, "RESULTS", tmp_path)
    monkeypatch.setattr(report_mod, "REPORT_PATH", tmp_path / "test_report.md")

    replies = {row["questions"][0]: no_points() for row in cases}
    answerer = scripted_answerer(documents, replies)
    path = tmp_path / "run.jsonl"
    assert run(answerer, cases, documents, personas, path, fake_meta()) == 0

    assert report_main(["report", str(path)]) == 0
    review_md = tmp_path / "run.review.md"
    review_yaml = tmp_path / "run.review.yaml"
    assert review_md.exists()
    assert review_yaml.exists()

    # A second call keeps a filled YAML untouched.
    text = review_yaml.read_text(encoding="utf-8")
    filled = text.replace(
        "- row: 1\n  faithful:\n  lesson:\n  note:",
        "- row: 1\n  faithful: yes\n  lesson: Bài học hàng 1.\n  note:",
        1,
    )
    review_yaml.write_text(filled, encoding="utf-8")
    report_main(["report", str(path)])
    assert review_yaml.read_text(encoding="utf-8") == filled

    report_text = (tmp_path / "test_report.md").read_text(encoding="utf-8")
    assert "k of n" in report_text
    assert "95% upper bound" in report_text
    for row in cases:
        assert row["questions"][0] in report_text
    for column in ("Kỳ vọng", "Kết quả thực tế", "Đạt/Chưa đạt", "Điều học được"):
        assert column in report_text
    assert "[chờ Hiệp]" in report_text
    assert "Bài học hàng 1." in report_text
    # The report and the review sheet stay LF-only on every OS (issue #60).
    assert b"\r\n" not in review_md.read_bytes()
    assert b"\r\n" not in (tmp_path / "test_report.md").read_bytes()


def test_write_lf_uses_lf_line_endings(tmp_path):
    path = tmp_path / "r.review.md"
    _write_lf(path, "đạt\nlỗi\n")
    assert path.read_bytes() == "đạt\nlỗi\n".encode("utf-8")


def test_report_incomplete_writes_nothing(cases, personas, documents, tmp_path, monkeypatch):
    monkeypatch.setattr(report_mod, "RESULTS", tmp_path)
    monkeypatch.setattr(report_mod, "REPORT_PATH", tmp_path / "test_report.md")
    row = row_by_id(cases, 1)
    quote = chunk_text(documents, "LEAVE-GAMECO-v2#2")
    answerer = scripted_answerer(
        documents,
        {row["questions"][0]: reply_citing("LEAVE-GAMECO-v2#2", quote_from={"LEAVE-GAMECO-v2#2": quote})},
    )
    path = tmp_path / "partial.jsonl"
    run(answerer, [row], documents, personas, path, fake_meta())
    assert report_main(["report", str(path)]) == 0
    assert not (tmp_path / "test_report.md").exists()


def test_committed_report_matches_source():
    report_path = ROOT / REPORT_REL
    if not report_path.exists():
        pytest.skip("no committed report yet; generated after the final run")
    text = report_path.read_text(encoding="utf-8")
    rel = report_run_path(text)
    assert rel, "the report header must name its results file"
    results_path = ROOT / rel
    run_id = results_path.stem

    from appota_kb.core.config import load_config
    from appota_kb.integrations.data_files import (
        load_org,
        load_personas,
        load_test_cases,
    )

    rows = load_test_cases()
    personas = load_personas(load_org())

    records = load_run(results_path)
    scores = score_all(rows, records)
    reviews = load_reviews(ROOT / "results" / f"{run_id}.review.yaml")
    rebuilt = build_report(
        run_id, f"results/{run_id}.jsonl", records, rows, scores, reviews,
        load_config().eval, personas,
    )
    assert rebuilt == text
