"""Ask every row of data/test_cases.yaml once and record one JSON line per row.

Run by hand (needs GEMINI_API_KEY):
  python -m appota_kb.evaluation.run [--rows 1,7,8] [--resume results/<run_id>.jsonl]
It goes through services.ask like the page, with no cache.

Scoring is a separate step (`python -m appota_kb.evaluation.report results/<run_id>.jsonl`) so a
check or a report fix re-scores saved replies with no API call (ADR 0006).
"""
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

from appota_kb.core.config import Config, load_config
from appota_kb.core.paths import RESULTS, ROOT
from appota_kb.evaluation.data_edit import with_edit
from appota_kb.evaluation.score import load_run
from appota_kb.integrations.data_files import cases_sha256, load_documents, load_org, load_personas, load_test_cases
from appota_kb.integrations.gemini import gemini_chat, gemini_embeddings
from appota_kb.services.answering.answerer import AnswerUnavailable, Answerer
from appota_kb.services.ask import ask
from appota_kb.services.retrieval.index import build_index
from appota_kb.services.retrieval.search import ScopeLeakError
from appota_kb.services.scope import scope as build_scope

# settings that a resumed run must keep, so the file stays one coherent run
RESUME_KEYS = ("run_id", "commit", "dirty", "cases_sha256", "model", "thinking_level",
               "embedding_model", "top_k")


def _git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def run_meta(config: Config, run_id: str) -> dict:
    """commit, dirty, cases_sha256 and the model settings, copied into every record."""
    commit = _git(["rev-parse", "HEAD"]).strip()
    dirty = bool(_git(["status", "--porcelain", "--", ".", ":(exclude)results"]).strip())
    return {
        "run_id": run_id,
        "commit": commit,
        "dirty": dirty,
        "cases_sha256": cases_sha256(),
        "model": config.llm.model,
        "thinking_level": config.llm.thinking_level,
        "embedding_model": config.retrieval.embedding_model,
        "top_k": config.retrieval.top_k,
        "utc_offset_hours": config.page.utc_offset_hours,
    }


def ask_row(answerer, row: dict, documents, personas, meta: dict) -> dict:
    """One record: apply data_edit, build the scope, ask questions[0] once, steps 5-7 via services.ask.

    AnswerUnavailable -> status error; ScopeLeakError -> status leak; anything else propagates.
    """
    started_at = datetime.now(timezone(timedelta(hours=meta["utc_offset_hours"]))).isoformat()
    record = {
        "run_id": meta["run_id"],
        "row": row["id"],
        "kind": row["kind"],
        "persona": row["persona"],
        "as_of": row["as_of"].isoformat(),
        "question": row["questions"][0],
        "status": None,
        "error": None,
        "started_at": started_at,
        "commit": meta["commit"],
        "dirty": meta["dirty"],
        "cases_sha256": meta["cases_sha256"],
        "model": meta["model"],
        "thinking_level": meta["thinking_level"],
        "embedding_model": meta["embedding_model"],
        "top_k": meta["top_k"],
        "scope_documents": None,
        "scope_conflicts": None,
        "scope_chunks": None,
        "retrieved": None,
        "retrieved_text": None,
        "raw": None,
        "points": None,
        "card": None,
        "latency_ms": None,
    }
    docs = with_edit(documents, row["data_edit"]) if "data_edit" in row else documents
    persona = personas[row["persona"]]
    as_of = row["as_of"]
    question = row["questions"][0]
    scoped = build_scope(persona, as_of, docs)
    record["scope_documents"] = [d.id for d in scoped.documents]
    record["scope_conflicts"] = [sorted([a.id, b.id]) for a, b in scoped.conflicts]
    record["scope_chunks"] = [c.id for c in scoped.chunks]

    started = time.perf_counter()
    try:
        asked = ask(scoped, question, answerer)
    except AnswerUnavailable as exc:
        record["status"] = "error"
        record["error"] = {"type": type(exc).__name__, "message": str(exc)}
        return record
    except ScopeLeakError as exc:
        record["status"] = "leak"
        record["error"] = {"type": type(exc).__name__, "message": str(exc)}
        return record
    record["latency_ms"] = round((time.perf_counter() - started) * 1000)

    reply, card, lines = asked.reply, asked.card, asked.lines
    by_text = {c.id: c.text for c in scoped.chunks}
    record["status"] = "ok"
    record["retrieved"] = list(reply.retrieved)
    record["retrieved_text"] = {cid: by_text[cid] for cid in reply.retrieved}
    record["raw"] = reply.raw
    record["points"] = None if reply.points is None else [
        {"chunks": list(p.chunks), "quote": p.quote, "text": p.text} for p in reply.points
    ]
    record["card"] = {
        "kind": card.kind,
        "reason": card.reason,
        "cited": [c.id for c in card.cited],
        "conflicts": [sorted([a.id, b.id]) for a, b in card.conflicts],
        "answer_text": (
            " ".join(p.text.strip() for p in (reply.points or ())) if card.kind == "answer" else None
        ),
        "lines": list(lines),
    }
    return record


def run(answerer, rows: list[dict], documents, personas, path: Path, meta: dict) -> int:
    """Append one record per row to `path`, flushing after each line; stop at the first error.

    Returns the exit code: 0 complete, 2 a leak was recorded, 3 stopped on an error.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    leak_seen = False
    for row in rows:
        record = ask_row(answerer, row, documents, personas, meta)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()
        if record["status"] == "leak":
            leak_seen = True
        if record["status"] == "error":
            return 3
    return 2 if leak_seen else 0


def _select_rows(rows: list[dict], spec: str) -> list[dict]:
    """The rows named by a comma list, in file order (kept by --rows)."""
    selected = {int(token) for token in spec.split(",") if token.strip()}
    return [r for r in rows if r["id"] in selected]


def _check_resume(meta: dict, existing: list[dict]) -> None:
    if not existing:
        return
    first = existing[0]
    changed = [key for key in RESUME_KEYS if first.get(key) != meta[key]]
    if changed:
        raise ValueError(f"resume refused: {', '.join(changed)} changed since the first record")


def main(argv: list[str]) -> int:
    logging.basicConfig(level=logging.INFO)
    rows_spec = None
    resume_arg = None
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--rows":
            if i + 1 >= len(args):
                raise SystemExit("usage: python -m appota_kb.evaluation.run [--rows 1,7,8] [--resume results/<run_id>.jsonl]")
            rows_spec = args[i + 1]
            i += 2
        elif args[i] == "--resume":
            if i + 1 >= len(args):
                raise SystemExit("usage: python -m appota_kb.evaluation.run [--rows 1,7,8] [--resume results/<run_id>.jsonl]")
            resume_arg = args[i + 1]
            i += 2
        else:
            raise SystemExit("usage: python -m appota_kb.evaluation.run [--rows 1,7,8] [--resume results/<run_id>.jsonl]")

    load_dotenv(ROOT / ".env")
    if not os.environ.get("GEMINI_API_KEY"):
        sys.stderr.write("GEMINI_API_KEY is not set; set it to a Gemini API key to run the evaluation\n")
        return 1

    config = load_config()
    documents = load_documents()
    personas = load_personas(load_org())
    rows = load_test_cases()
    if rows_spec is not None:
        try:
            rows = _select_rows(rows, rows_spec)
        except ValueError as exc:
            sys.stderr.write(f"--rows: {exc}\n")
            return 2

    now = datetime.now(timezone(timedelta(hours=config.page.utc_offset_hours)))
    run_id = now.strftime("%Y%m%d-%H%M")
    target = RESULTS / f"{run_id}.jsonl"
    if resume_arg is not None:
        target = Path(resume_arg)
        run_id = target.stem

    meta = run_meta(config, run_id)

    if resume_arg is not None:
        if not target.exists():
            sys.stderr.write(f"{target}: not found\n")
            return 2
        existing = load_run(target)
        try:
            _check_resume(meta, existing)
        except ValueError as exc:
            sys.stderr.write(f"{exc}\n")
            return 2
        done = {r["row"] for r in existing if r["status"] in ("ok", "leak")}
        rows = [r for r in rows if r["id"] not in done]
    elif target.exists():
        sys.stderr.write(f"{target}: already exists; resume it with --resume {target}\n")
        return 2

    index = build_index(documents, gemini_embeddings(config.retrieval.embedding_model))
    answerer = Answerer(index, gemini_chat(config.llm), config.retrieval)
    return run(answerer, rows, documents, personas, target, meta)


if __name__ == "__main__":
    sys.exit(main(sys.argv))