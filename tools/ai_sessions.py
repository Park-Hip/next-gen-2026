"""List the Pi agent sessions recorded for this project, to check the evidence log against them.

Usage:
  python tools/ai_sessions.py                 # one block per session: time, models, prompts, files changed
  python tools/ai_sessions.py --prompts 19:24 # verbatim prompts of the session that started at 19:24 local time

Session files live in ~/.pi/agent/sessions/<encoded project path>/ and are read-only here.
Times are shown in local time; session file names use UTC.
"""

import collections
import datetime
import json
import pathlib
import re
import sys

PROJECT = pathlib.Path(__file__).resolve().parent.parent
LOG_NAME = "evidence_log.md"


def sessions_dir() -> pathlib.Path:
    # Pi stores sessions under the project path with ":" and separators replaced by "-".
    encoded = str(PROJECT).replace(":", "-").replace("\\", "-").replace("/", "-")
    return pathlib.Path.home() / ".pi" / "agent" / "sessions" / f"--{encoded}--"


def local_time(stamp: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone()


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text")


def typed_prompt(text: str) -> str:
    """Return what the user typed, or "" for injected context."""
    text = text.strip()
    # A skill invocation puts the skill file first and the user's own text after </skill>.
    skill = re.match(r'<skill name="([^"]+)"', text)
    if skill and "</skill>" in text:
        return f"[skill: {skill.group(1)}] {text.rsplit('</skill>', 1)[1].strip()}"
    # Other text starting with a tag (system reminders) is not something the user typed.
    return "" if text.startswith("<") else text


def short_path(raw: str) -> str:
    path = pathlib.Path(raw)
    try:
        return path.resolve().relative_to(PROJECT).as_posix()
    except ValueError:
        return f"(outside project) {raw}"


def read_session(file: pathlib.Path) -> dict:
    info = {"file": file, "start": None, "end": None, "models": collections.Counter(),
            "prompts": [], "changed": collections.Counter(), "bash": 0, "subagents": 0}
    for line in file.open(encoding="utf-8"):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("timestamp"):
            info["start"] = info["start"] or entry["timestamp"]
            info["end"] = entry["timestamp"]
        message = entry.get("message") or {}
        role = message.get("role")
        if role == "user":
            prompt = typed_prompt(text_of(message.get("content")))
            if prompt:
                info["prompts"].append((entry["timestamp"], prompt))
        elif role == "assistant":
            if message.get("model"):
                info["models"][f"{message.get('provider')}/{message['model']}"] += 1
            for part in message.get("content") or []:
                if not isinstance(part, dict) or part.get("type") != "toolCall":
                    continue
                name, args = part.get("name"), part.get("arguments") or {}
                if name in ("edit", "write") and args.get("path"):
                    info["changed"][short_path(args["path"])] += 1
                elif name == "bash":
                    info["bash"] += 1
                elif name == "subagent":
                    info["subagents"] += 1
    return info


def print_summary(sessions: list) -> None:
    for s in sessions:
        start, end = local_time(s["start"]), local_time(s["end"])
        print(f"== {start:%d/%m %H:%M}-{end:%H:%M}  ({s['file'].name[:24]})")
        print(f"   models:   {', '.join(f'{m} x{n}' for m, n in s['models'].items()) or '-'}")
        first = s["prompts"][0][1].replace("\n", " ")[:110] if s["prompts"] else "-"
        print(f"   prompts:  {len(s['prompts'])}  first: {first}")
        print(f"   changed:  {', '.join(sorted(s['changed'])) or '-'}")
        print(f"   bash calls: {s['bash']}, subagent calls: {s['subagents']}")
        # bash can also edit the log, so this flag only means "no edit/write tool call touched it".
        if s["changed"] and LOG_NAME not in s["changed"]:
            print(f"   ! changed files but made no edit/write call on {LOG_NAME}")


def print_prompts(session: dict) -> None:
    for stamp, prompt in session["prompts"]:
        print(f"--- {local_time(stamp):%d/%m %H:%M}")
        print(prompt)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    folder = sessions_dir()
    files = sorted(folder.glob("*.jsonl"))
    if not files:
        sys.exit(f"No sessions found in {folder}")
    sessions = [read_session(f) for f in files]
    if len(sys.argv) == 3 and sys.argv[1] == "--prompts":
        key = sys.argv[2]
        matches = [s for s in sessions if key in f"{local_time(s['start']):%d/%m %H:%M}" or key in s["file"].name]
        if len(matches) != 1:
            sys.exit(f"'{key}' matches {len(matches)} sessions; use a longer key")
        print_prompts(matches[0])
    elif len(sys.argv) == 1:
        print_summary(sessions)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
