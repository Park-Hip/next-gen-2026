"""The session lister reads the main checkout, the Orca worktrees and the opencode database."""
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "ai_sessions.py"
spec = importlib.util.spec_from_file_location("ai_sessions_under_test", SCRIPT)
ai_sessions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai_sessions)

MAIN_TIME = "2026-10-20T15:48:00.000Z"
NEXT_TIME = "2026-10-20T15:49:00.000Z"


@pytest.fixture
def home(tmp_path):
    return tmp_path / "home"


@pytest.fixture
def project(tmp_path):
    return tmp_path / "orca" / "projects" / "next-gen"


@pytest.fixture
def worktree(home):
    # The checkout itself is never created: a removed worktree keeps its session folder.
    return home / "orca" / "workspaces" / "next-gen" / "issue-84"


def write_jsonl(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def write_pi(home: Path, checkout: Path, name: str, prompt: str, edit: Path,
             start: str = MAIN_TIME, end: str = NEXT_TIME) -> None:
    folder = home / ".pi" / "agent" / "sessions" / f"--{ai_sessions.encoded_path(checkout)}--"
    write_jsonl(folder / name, [
        {"timestamp": start, "message": {"role": "user", "content": prompt}},
        {"timestamp": end, "message": {"role": "assistant", "provider": "opencode", "model": "deepseek",
                                       "content": [{"type": "toolCall", "name": "edit",
                                                    "arguments": {"path": str(edit)}}]}},
    ])


def write_claude_code(home: Path, checkout: Path, name: str, rows: list) -> None:
    folder = home / ".claude" / "projects" / ai_sessions.encoded_path(checkout)
    write_jsonl(folder / name, rows)


def test_pi_sessions_in_main_and_removed_worktree(home, project, worktree):
    write_pi(home, project, "main.jsonl", "build issue 84", project / "README.md")
    write_pi(home, worktree, "worktree.jsonl", "build issue 84 in a worktree", worktree / "scripts/ai_sessions.py",
             start="2026-10-20T16:48:00.000Z", end="2026-10-20T16:49:00.000Z")

    sessions, mirrors = ai_sessions.load_sessions(home=home, project=project)

    assert mirrors == 0
    assert [(s["tool"], s["where"]) for s in sessions] == [("Pi", "main"), ("Pi", "issue-84")]
    assert list(sessions[0]["changed"]) == ["README.md"]
    assert list(sessions[1]["changed"]) == ["scripts/ai_sessions.py"]
    assert [p[1] for p in sessions[1]["prompts"]] == ["build issue 84 in a worktree"]


def test_claude_code_lists_cli_sessions_and_skips_bridge_mirrors(home, project, worktree):
    write_claude_code(home, worktree, "cli.jsonl", [
        {"type": "user", "entrypoint": "cli", "timestamp": MAIN_TIME,
         "message": {"role": "user", "content": "build issue 84"}},
        {"type": "assistant", "entrypoint": "cli", "timestamp": NEXT_TIME,
         "message": {"role": "assistant", "model": "claude-sonnet-5-5",
                     "content": [{"type": "tool_use", "name": "Edit",
                                  "input": {"file_path": str(worktree / "docs/how_this_was_built.md")}}]}},
    ])
    write_claude_code(home, worktree, "mirror.jsonl", [
        {"type": "user", "entrypoint": "sdk-ts", "timestamp": MAIN_TIME,
         "message": {"role": "user", "content": "a Pi session mirrored by claude-bridge"}},
    ])

    sessions, mirrors = ai_sessions.load_sessions(home=home, project=project)

    assert mirrors == 1
    assert [(s["tool"], s["where"]) for s in sessions] == [("Claude Code", "issue-84")]
    assert list(sessions[0]["changed"]) == ["docs/how_this_was_built.md"]


def create_opencode(home: Path) -> Path:
    database = home / ".local" / "share" / "opencode" / "opencode.db"
    database.parent.mkdir(parents=True)
    connection = sqlite3.connect(database)
    connection.execute("create table session_v2 "
                       "(id text, parent_id text, directory text, model text, time_created integer)")
    connection.execute("create table session_message "
                       "(session_id text, type text, seq integer, time_created integer, data text)")
    return database


def add_session(connection, session_id, parent, directory, created):
    connection.execute("insert into session_v2 values (?, ?, ?, ?, ?)",
                       (session_id, parent, str(directory), json.dumps({"id": "deepseek-v4.1-flash-free",
                                                                        "providerID": "opencode"}), created))


def add_message(connection, session_id, kind, seq, created, data):
    connection.execute("insert into session_message values (?, ?, ?, ?, ?)",
                       (session_id, kind, seq, created, json.dumps(data)))


def test_opencode_lists_top_level_sessions_once(home, project, worktree):
    database = create_opencode(home)
    connection = sqlite3.connect(database)
    add_session(connection, "ses_parent", None, worktree, 1792511289219)
    add_message(connection, "ses_parent", "user", 1, 1792511299000, {"text": "implement issue 84"})
    add_message(connection, "ses_parent", "assistant", 2, 1792511300000, {
        "model": {"id": "deepseek-v4.1-flash-free", "providerID": "opencode"},
        "content": [
            {"type": "tool", "name": "edit", "state": {"input": {"path": str(worktree / "scripts/ai_sessions.py")}}},
            {"type": "tool", "name": "shell", "state": {"input": {"command": "python -m pytest"}}},
            {"type": "tool", "name": "subagent", "state": {"input": {}}},
        ],
    })
    # Both a child session and a subagent tool call exist; that is one subagent call, not two.
    add_session(connection, "ses_child", "ses_parent", worktree, 1792511310000)
    add_message(connection, "ses_child", "user", 1, 1792511311000, {"text": "You are a subagent"})
    # A session of another project under the same home folder is ignored.
    add_session(connection, "ses_other", None, home / "orca" / "workspaces" / "other-project" / "issue-1",
                1792511320000)
    add_message(connection, "ses_other", "user", 1, 1792511321000, {"text": "other project"})
    connection.commit()
    connection.close()
    before = database.read_bytes()

    sessions, mirrors = ai_sessions.load_sessions(home=home, project=project)

    assert mirrors == 0
    assert len(sessions) == 1
    session = sessions[0]
    assert (session["tool"], session["where"]) == ("opencode", "issue-84")
    assert [p[1] for p in session["prompts"]] == ["implement issue 84"]
    assert session["models"] == {"opencode/deepseek-v4.1-flash-free": 1}
    assert list(session["changed"]) == ["scripts/ai_sessions.py"]
    assert session["bash"] == 1
    assert session["subagents"] == 1
    # The database is opened read-only: the script leaves every byte as it found it.
    assert database.read_bytes() == before


def test_missing_opencode_database_is_not_an_error(home, project):
    sessions, mirrors = ai_sessions.load_sessions(home=home, project=project)

    assert (sessions, mirrors) == ([], 0)
