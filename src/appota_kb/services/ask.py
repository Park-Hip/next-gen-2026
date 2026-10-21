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


@dataclass(frozen=True)
class Asked:
    reply: Reply
    card: Card
    lines: tuple[CardLine, ...]
    cache_hit: bool


class ReplyCache:
    """Demo LRU of finished replies (decision 5 of the #13 plan).

    Keyed by persona id, the scope's chunk ids and the question, so a changed scope misses.
    Step 7 still runs on every hit, and a failed call is never stored.
    """

    def __init__(self, size: int):
        self.size = size
        self._replies: OrderedDict[tuple, Reply] = OrderedDict()

    @staticmethod
    def _key(scope: Scope, question: str) -> tuple:
        return (scope.persona.id, tuple(sorted(scope.chunk_ids)), question)

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
        if cache is not None:
            cache.put(scope, question, reply)
    card = card_for_answer(scope, reply.retrieved, reply.points)
    by_id = {c.id: c for c in scope.chunks}
    lines = render(card, scope, reply.points, tuple(by_id[cid] for cid in reply.retrieved))
    return Asked(reply=reply, card=card, lines=lines, cache_hit=cache_hit)
