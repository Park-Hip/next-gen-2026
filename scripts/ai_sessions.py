"""List the AI sessions recorded for this project, to check the evidence log against them.

Usage:
  python scripts/ai_sessions.py                 # one block per session: tool, time, where, models, prompts, files changed
  python scripts/ai_sessions.py --since 09/10   # only sessions that started on or after that day (dd/mm, this year)
  python scripts/ai_sessions.py --prompts 19:24 # verbatim prompts of the session that started at 19:24 local time

Three sources, all read-only here:
- Pi: ~/.pi/agent/sessions/<encoded project path>/*.jsonl
- Claude Code: ~/.claude/projects/<encoded project path>/*.jsonl. Pi runs Claude models through claude-bridge,
  which also writes Claude Code session files (entrypoint "sdk-ts"); those mirror Pi sessions already listed,
  so only files written entirely by the Claude Code CLI (entrypoint "cli") are shown.
- opencode: ~/.local/share/opencode/opencode.db, a SQLite database opened read-only (tables session_v2 and
  session_message). A subagent session (parent_id set) counts as one subagent call of its parent, not a
  session of its own.
The main checkout and every Orca worktree of this project under ~/orca/workspaces/<project folder>/ are read,
including worktrees already removed: each keeps its own Pi and Claude Code folder, and opencode records the
directory its sessions ran in.
Times are shown in local time; session file names and timestamps use UTC.
"""

import collections
import datetime
import json
import os
import pathlib
import re
import sqlite3
import subprocess
import sys

PROJECT = pathlib.Path(__file__).resolve().parent.parent
LOG_NAME = "evidence_log.md"
COMPACTION = "The conversation history before this point was compacted"
WORKTREES = pathlib.Path("orca") / "workspaces"


def encoded_path(path: pathlib.Path) -> str:
    # Both tools store sessions under the project path with ":" and separators replaced by "-".
    return str(path).replace(":", "-").replace("\\", "-").replace("/", "-")


def main_checkout(project: pathlib.Path) -> pathlib.Path:
    """The main checkout, also when this script runs from a worktree."""
    try:
        common = subprocess.run(
            ["git", "-C", str(project), "rev-parse", "--path-format=absolute", "--git-common-dir"],
            check=True, capture_output=True, encoding="utf-8").stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return project
    return pathlib.Path(common).parent.resolve()


def checkout_for(encoded: str, main: pathlib.Path, worktrees: pathlib.Path):
    """Return (checkout, where) for a Pi or Claude Code session folder, or None for another project."""
    if encoded == encoded_path(main):
        return main, "main"
    prefix = encoded_path(worktrees) + "-"
    if encoded.startswith(prefix):
        slug = encoded[len(prefix):]
        return worktrees / slug, slug
    return None


def checkout_of(directory: pathlib.Path, main: pathlib.Path, worktrees: pathlib.Path):
    """The same as checkout_for(), for the real directory opencode records."""
    directory = pathlib.Path(os.path.normpath(directory))
    main = pathlib.Path(os.path.normpath(main))
    worktrees = pathlib.Path(os.path.normpath(worktrees))
    if os.path.normcase(str(directory)) == os.path.normcase(str(main)):
        return main, "main"
    try:
        slug = directory.relative_to(worktrees)
    except ValueError:
        return None
    return directory, slug.as_posix()


def local_time(stamp: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone()


def iso_time(milliseconds: int) -> str:
    return datetime.datetime.fromtimestamp(milliseconds / 1000, datetime.timezone.utc).isoformat()


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(p.get("text", "") for p in content or [] if isinstance(p, dict) and p.get("type") == "text")


def typed_prompt(text: str) -> str:
    """Return what the user typed, or "" for injected context."""
    # Claude Code wraps pasted text in <pasted_content> tags; the pasted text is what the user sent.
    text = re.sub(r"</?pasted_content[^>]*>", "", text).strip()
    # A skill invocation puts the skill file first and the user's own text after </skill>.
    skill = re.match(r'<skill name="([^"]+)"', text)
    if skill and "</skill>" in text:
        return f"[skill: {skill.group(1)}] {text.rsplit('</skill>', 1)[1].strip()}"
    # Text starting with a tag (system reminders, commands) or a compaction summary is not typed by the user.
    return "" if text.startswith("<") or text.startswith(COMPACTION) else text


def short_path(raw: str, roots: tuple, default_root: pathlib.Path) -> str:
    """The path relative to the checkout the session ran in, else to the project or its worktree root."""
    path = pathlib.Path(raw)
    if not path.is_absolute():
        path = default_root / path
    path = path.resolve()
    for root in roots:
        try:
            return path.relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
    return f"(outside) {raw}"


def new_session(file: pathlib.Path, tool: str, roots: tuple, where: str) -> dict:
    return {"file": file, "tool": tool, "where": where, "roots": roots, "start": None, "end": None,
            "models": collections.Counter(), "prompts": [], "changed": collections.Counter(), "bash": 0,
            "subagents": 0}


def entries(file: pathlib.Path):
    for line in file.open(encoding="utf-8"):
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def note_time(info: dict, entry: dict) -> None:
    if entry.get("timestamp"):
        info["start"] = info["start"] or entry["timestamp"]
        info["end"] = entry["timestamp"]


def note_tool(info: dict, name: str, args: dict) -> None:
    """Count one tool call; names differ between Pi ("edit"), Claude Code ("Edit") and MCP ("mcp__x__edit")."""
    name = (name or "").rsplit("__", 1)[-1].lower()
    path = args.get("path") or args.get("file_path")
    if name in ("edit", "write", "multiedit", "notebookedit") and path:
        info["changed"][short_path(path, info["roots"], info["roots"][0])] += 1
    elif name in ("bash", "powershell", "shell"):
        info["bash"] += 1
    elif name in ("subagent", "task", "agent"):
        info["subagents"] += 1


def read_pi(file: pathlib.Path, roots: tuple, where: str) -> dict:
    info = new_session(file, "Pi", roots, where)
    for entry in entries(file):
        note_time(info, entry)
        message = entry.get("message") or {}
        if message.get("role") == "user":
            prompt = typed_prompt(text_of(message.get("content")))
            if prompt:
                info["prompts"].append((entry["timestamp"], prompt))
        elif message.get("role") == "assistant":
            if message.get("model"):
                info["models"][f"{message.get('provider')}/{message['model']}"] += 1
            for part in message.get("content") or []:
                if isinstance(part, dict) and part.get("type") == "toolCall":
                    note_tool(info, part.get("name"), part.get("arguments") or {})
    return info


def read_claude_code(file: pathlib.Path, roots: tuple, where: str):
    """Return the session, or None if any entry came through claude-bridge (a mirror of a Pi session)."""
    info = new_session(file, "Claude Code", roots, where)
    for entry in entries(file):
        if entry.get("entrypoint") and entry["entrypoint"] != "cli":
            return None
        if entry.get("type") not in ("user", "assistant") or entry.get("isSidechain") or entry.get("isMeta"):
            continue
        note_time(info, entry)
        message = entry.get("message") or {}
        if entry["type"] == "user":
            prompt = typed_prompt(text_of(message.get("content")))
            if prompt:
                info["prompts"].append((entry["timestamp"], prompt))
        else:
            if message.get("model"):
                info["models"][message["model"]] += 1
            for part in message.get("content") or []:
                if isinstance(part, dict) and part.get("type") == "tool_use":
                    note_tool(info, part.get("name"), part.get("input") or {})
    return info if info["start"] else None


def read_opencode(connection: sqlite3.Connection, session_id: str, roots: tuple, where: str) -> dict:
    info = new_session(pathlib.Path(session_id), "opencode", roots, where)
    query = "select type, time_created, data from session_message where session_id = ? order by seq"
    for kind, created, raw in connection.execute(query, (session_id,)):
        try:
            data = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            continue
        stamp = iso_time(created)
        info["start"] = info["start"] or stamp
        info["end"] = stamp
        if kind == "user":
            prompt = (data.get("text") or "").strip()
            if prompt:
                info["prompts"].append((stamp, prompt))
        elif kind == "assistant":
            model = data.get("model") or {}
            if model.get("id"):
                info["models"][f"{model.get('providerID')}/{model['id']}"] += 1
            for part in data.get("content") or []:
                if isinstance(part, dict) and part.get("type") == "tool":
                    note_tool(info, part.get("name"), (part.get("state") or {}).get("input") or {})
    return info


def load_opencode(home: pathlib.Path, main: pathlib.Path, worktrees: pathlib.Path) -> list:
    database = home / ".local" / "share" / "opencode" / "opencode.db"
    if not database.is_file():
        return []
    # mode=ro makes SQLite refuse every write; the script only reads the session tables.
    connection = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
    try:
        rows = connection.execute(
            "select id, parent_id, directory, model, time_created from session_v2").fetchall()
        children = collections.Counter(parent for _, parent, *_ in rows if parent)
        sessions = []
        for session_id, parent, directory, model, created in rows:
            if parent:
                continue
            found = checkout_of(pathlib.Path(directory), main, worktrees)
            if not found:
                continue
            checkout, where = found
            info = read_opencode(connection, session_id, (checkout, main, worktrees), where)
            if not info["start"]:
                info["start"] = info["end"] = iso_time(created)
            if not info["models"]:
                current = json.loads(model or "{}")
                if current.get("id"):
                    info["models"][f"{current.get('providerID')}/{current['id']}"] += 1
            # A subagent shows both as a child session and as a tool call on some versions; count it once.
            info["subagents"] = max(info["subagents"], children[session_id])
            sessions.append(info)
        return sessions
    finally:
        connection.close()


def load_sessions(home: pathlib.Path | None = None, project: pathlib.Path | None = None):
    home = home or pathlib.Path.home()
    main = main_checkout(project or PROJECT)
    worktrees = home / WORKTREES / main.name
    sessions, mirrors = [], 0

    pi_root = home / ".pi" / "agent" / "sessions"
    for folder in sorted(pi_root.glob("--*--")):
        found = checkout_for(folder.name[2:-2], main, worktrees)
        if not found:
            continue
        checkout, where = found
        for file in sorted(folder.glob("*.jsonl")):
            sessions.append(read_pi(file, (checkout, main, worktrees), where))

    cc_root = home / ".claude" / "projects"
    for folder in sorted(cc_root.glob("*")) if cc_root.is_dir() else []:
        found = checkout_for(folder.name, main, worktrees)
        if not found or not folder.is_dir():
            continue
        checkout, where = found
        for file in sorted(folder.glob("*.jsonl")):
            session = read_claude_code(file, (checkout, main, worktrees), where)
            if session:
                sessions.append(session)
            else:
                mirrors += 1

    sessions += load_opencode(home, main, worktrees)
    sessions = [s for s in sessions if s["start"]]
    return sorted(sessions, key=lambda s: s["start"]), mirrors


def print_summary(sessions: list, mirrors: int) -> None:
    for s in sessions:
        start, end = local_time(s["start"]), local_time(s["end"])
        end_text = f"{end:%H:%M}" if end.date() == start.date() else f"{end:%d/%m %H:%M}"
        print(f"== {start:%d/%m %H:%M}-{end_text}  {s['tool']}  ({s['file'].name[:24]})")
        print(f"   where:    {s['where']}")
        print(f"   models:   {', '.join(f'{m} x{n}' for m, n in s['models'].items()) or '-'}")
        first = s["prompts"][0][1].replace("\n", " ")[:110] if s["prompts"] else "-"
        print(f"   prompts:  {len(s['prompts'])}  first: {first}")
        print(f"   changed:  {', '.join(sorted(s['changed'])) or '-'}")
        print(f"   bash calls: {s['bash']}, subagent calls: {s['subagents']}")
        # bash can also edit the log, so this flag only means "no edit/write tool call touched it".
        if s["changed"] and LOG_NAME not in s["changed"]:
            print(f"   ! changed files but made no edit/write call on {LOG_NAME}")
    print(f"\n{len(sessions)} sessions; {mirrors} Claude Code files skipped as claude-bridge mirrors of Pi sessions")


def print_prompts(session: dict) -> None:
    for stamp, prompt in session["prompts"]:
        print(f"--- {local_time(stamp):%d/%m %H:%M}")
        print(prompt)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sessions, mirrors = load_sessions()
    if not sessions:
        sys.exit("No sessions found for this project")
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == "--prompts":
        key = args[1]
        matches = [s for s in sessions if key in f"{local_time(s['start']):%d/%m %H:%M}" or key in s["file"].name]
        if len(matches) != 1:
            sys.exit(f"'{key}' matches {len(matches)} sessions; use a longer key")
        print_prompts(matches[0])
    elif len(args) == 2 and args[0] == "--since":
        day, month = (int(x) for x in args[1].split("/"))
        since = datetime.datetime.now().astimezone().replace(month=month, day=day, hour=0, minute=0, second=0, microsecond=0)
        print_summary([s for s in sessions if local_time(s["start"]) >= since], mirrors)
    elif not args:
        print_summary(sessions, mirrors)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
