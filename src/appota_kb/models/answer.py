"""What step 6 returns: the model's answer, the quotes it cites and the retrieved ids."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """One quote from the model that step 7 checks, and the chunks it cites.

    The quote is the only text step 7 reads; the answer sits once above all quotes (ADR 0018).
    """
    quote: str
    chunks: tuple[str, ...]


@dataclass(frozen=True)
class Reply:
    retrieved: tuple[str, ...]          # chunk ids, best first
    answer: str                         # one claim that answers the whole question (ADR 0018)
    points: tuple[Point, ...] | None    # None: the output was not valid JSON of the contract
    raw: str                            # the model's text, for the log
    # The two chunk ids the model says disagree (ADR 0014); step 7 checks it, so it may be wrong or longer.
    disagreement: tuple[str, ...] = ()
