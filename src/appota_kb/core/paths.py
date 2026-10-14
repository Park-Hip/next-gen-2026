"""Where the repository's files are, found once from this file's location.

This relies on the editable install that `uv sync` makes: the config file, data/ and
results/ stay in the repository and are not packaged, so the package must run from the checkout.
The config file's path lives in core/config.py, the only module that names it (AGENTS.md "Config").
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # src/appota_kb/core/paths.py -> the repository
DATA = ROOT / "data"
RESULTS = ROOT / "results"
