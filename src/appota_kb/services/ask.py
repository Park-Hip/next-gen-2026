"""One question in its scope, end to end: the reply (cached or asked), step 7 and the card's lines.

The page and the evaluation harness both call ask(), so the card in the test report is the
card the page shows for the same reply.
"""
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable

from appota_kb.models.answer import Reply
from appota_kb.models.card import Card, CardLine
from appota_kb.models.scope import Scope
from appota_kb.services.card_text import render
from appota_kb.services.citations import card_for_answer


# Step 7 refusals that come from the model's reply, not from the question: asking again may give another reply.
MODEL_FAULTS = ("malformed", "quote_mismatch", "outside_retrieved")


@dataclass(frozen=True)
class Asked:
    reply: Reply
    card: Card
    lines: tuple[CardLine, ...]
    cache_hit: bool


class ReplyCache:
    """Demo LRU of finished replies (decision 5 of the #13 plan).

    Keyed by persona id, the as-of date, the scope's chunk ids and the question, so a changed scope misses.
    The date is in the key because the prompt carries it: the same chunks on two dates need two replies (ADR 0012).
    Step 7 still runs on every hit.
    A failed call is never stored, and neither is a reply that step 7 refused for a model fault (ADR 0017),
    so asking again reaches the model.
    """

    def __init__(self, size: int):
        self.size = size
        self._replies: OrderedDict[tuple, Reply] = OrderedDict()

    @staticmethod
    def _key(scope: Scope, question: str) -> tuple:
        return (scope.persona.id, scope.as_of, tuple(sorted(scope.chunk_ids)), question)

    def get(self, scope: Scope, question: str) -> Reply | None:
        key = self._key(scope, question)
        if key not in self._replies:
            return None
        self._replies.move_to_end(key)  # mark as most recently used
        return self._replies[key]

    def put(self, scope: Scope, question: str, reply: Reply) -> None:
        key = self._key(scope, question)
        self._replies[key] = reply
        self._replies.move_to_end(key)
        while len(self._replies) > self.size:
            self._replies.popitem(last=False)


def ask(
    scope: Scope,
    question: str,
    answerer: Callable[[Scope, str], Reply],
    cache: ReplyCache | None = None,
) -> Asked:
    """Steps 5-7 for one question: AnswerUnavailable and ScopeLeakError from the answerer propagate."""
    reply = cache.get(scope, question) if cache is not None else None
    cache_hit = reply is not None
    if reply is None:
        reply = answerer(scope, question)
    card = card_for_answer(scope, reply.retrieved, reply.points, reply.disagreement)
    if cache is not None and not cache_hit and card.reason not in MODEL_FAULTS:
        cache.put(scope, question, reply)
    by_id = {c.id: c for c in scope.chunks}
    lines = render(card, scope, reply.points, tuple(by_id[cid] for cid in reply.retrieved), answer=reply.answer)
    return Asked(reply=reply, card=card, lines=lines, cache_hit=cache_hit)
