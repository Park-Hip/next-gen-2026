"""List the AI sessions recorded for this project, to check the evidence log against them.

Usage:
  python scripts/ai_sessions.py                 # one block per session: tool, time, models, prompts, files changed
  python scripts/ai_sessions.py --since 09/10   # only sessions that started on or after that day (dd/mm, this year)
  python scripts/ai_sessions.py --prompts 19:24 # verbatim prompts of the session that started at 19:24 local time

Two sources, both read-only here:
- Pi: ~/.pi/agent/sessions/<encoded project path>/*.jsonl
- Claude Code: ~/.claude/projects/<encoded project path>/*.jsonl. Pi runs Claude models through claude-bridge,
  which also writes Claude Code session files (entrypoint "sdk-ts"); those mirror Pi sessions already listed,
  so only files written entirely by the Claude Code CLI (entrypoint "cli") are shown.
Times are shown in local time; session file names and timestamps use UTC.
"""

import collections
import datetime
import json
import pathlib
import re
import sys

PROJECT = pathlib.Path(__file__).resolve().parent.parent
LOG_NAME = "evidence_log.md"
COMPACTION = "The conversation history before this point was compacted"


def encoded_project() -> str:
    # Both tools store sessions under the project path with ":" and separators replaced by "-".
    return str(PROJECT).replace(":", "-").replace("\\", "-").replace("/", "-")


def local_time(stamp: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone()


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


def short_path(raw: str) -> str:
    path = pathlib.Path(raw)
    try:
        return path.resolve().relative_to(PROJECT).as_posix()
    except ValueError:
        return f"(outside project) {raw}"


def new_session(file: pathlib.Path, tool: str) -> dict:
    return {"file": file, "tool": tool, "start": None, "end": None, "models": collections.Counter(),
            "prompts": [], "changed": collections.Counter(), "bash": 0, "subagents": 0}


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
        info["changed"][short_path(path)] += 1
    elif name in ("bash", "powershell"):
        info["bash"] += 1
    elif name in ("subagent", "task", "agent"):
        info["subagents"] += 1


def read_pi(file: pathlib.Path) -> dict:
    info = new_session(file, "Pi")
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


def read_claude_code(file: pathlib.Path):
    """Return the session, or None if any entry came through claude-bridge (a mirror of a Pi session)."""
    info = new_session(file, "Claude Code")
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


def load_sessions():
    pi_files = sorted((pathlib.Path.home() / ".pi" / "agent" / "sessions" / f"--{encoded_project()}--").glob("*.jsonl"))
    cc_files = sorted((pathlib.Path.home() / ".claude" / "projects" / encoded_project()).glob("*.jsonl"))
    sessions = [read_pi(f) for f in pi_files]
    direct = [s for s in (read_claude_code(f) for f in cc_files) if s]
    mirrors = len(cc_files) - len(direct)
    sessions = [s for s in sessions + direct if s["start"]]
    return sorted(sessions, key=lambda s: s["start"]), mirrors


def print_summary(sessions: list, mirrors: int) -> None:
    for s in sessions:
        start, end = local_time(s["start"]), local_time(s["end"])
        end_text = f"{end:%H:%M}" if end.date() == start.date() else f"{end:%d/%m %H:%M}"
        print(f"== {start:%d/%m %H:%M}-{end_text}  {s['tool']}  ({s['file'].name[:24]})")
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
