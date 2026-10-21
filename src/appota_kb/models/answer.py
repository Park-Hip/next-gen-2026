"""What step 6 returns: the model's points, with the retrieved ids and the raw text."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """One grounded fact from the model: a plain sentence, a verbatim quote that step 7 checks,
    and the chunks it cites.

    The sentence is shown above the quote (ADR 0011); step 7 never reads it.
    """
    claim: str
    quote: str
    chunks: tuple[str, ...]


@dataclass(frozen=True)
class Reply:
    retrieved: tuple[str, ...]          # chunk ids, best first
    points: tuple[Point, ...] | None    # None: the output was not valid JSON of the contract
    raw: str                            # the model's text, for the log
