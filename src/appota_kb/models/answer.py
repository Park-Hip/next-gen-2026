"""What step 6 returns: the model's points, with the retrieved ids and the raw text."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """One grounded fact from the model: the chunks it cites and a verbatim quote that step 7 checks."""
    chunks: tuple[str, ...]
    quote: str


@dataclass(frozen=True)
class Reply:
    retrieved: tuple[str, ...]          # chunk ids, best first
    points: tuple[Point, ...] | None    # None: the output was not valid JSON of the contract
    raw: str                            # the model's text, for the log
