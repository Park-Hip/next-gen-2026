# 0017. A refusal says why, and an answer says what it does not cover

- Status: Proposed
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: The refusal wording of Phần 2 of the Mission 1 document (promise C4) for the reasons `quote_mismatch`, `outside_retrieved` and `malformed`; promise R10 is kept; it adds a rule to the prompt of ADR 0011, which keeps its status
- Issue: #96
- Research: None

## Context

Mission 3 general requirement 4 asks the product to refuse or to show that the basis is not enough.
Hiep's principle for it: refuse only when nothing can be verified; when a verified answer covers part of the question, show it and say what it does not cover; the model may add a caveat, but it never gets past a check.
Step 7 refuses for four reasons, and the card keeps the reason: `no_points`, `malformed`, `quote_mismatch` and `outside_retrieved`.
All four gave one text, "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn." (gap G4.3).
On the simulated data ("giả lập"), signed in as Minh on 07/10/2026 with the leave question, no points, malformed output, a quote that is not in its chunk and a citation outside the retrieved chunks gave the same card, word for word (probe P6).
For the last three, the model did answer or the system failed, so "không tìm thấy quy định" can be read as "there is no rule".
Promise R10 wants one text for "not allowed" and "not found", so a restricted document is never revealed; both are `no_points`, and the other three reasons depend only on the model's reply to chunks from the asker's own scope.
Two things about the code would have broken a change of text alone.
The reply cache stored every reply, so a text that says "thử lại" or "hỏi lại" would have replayed the same cached failure.
The R10 gate compared all refusal cards of a run with each other, so one refusal with a different reason would have failed the gate.
A faithful answer can also leave out part of what was asked, and nothing tells the asker (gap G4.5): row 16 gives the 3-working-day rule and does not say that the system does not compute the date asked for.

## Options considered

1. **One text for every reason** - the v1 behaviour; it reveals nothing, but it says "no rule found" when a rule was found and not verified, or when the system failed.
2. **Three texts chosen from the reason by a fixed mapping** - text 1 for no points, unchanged; text 2 for `quote_mismatch` and `outside_retrieved`; text 3 for `malformed`; each has only the HR contact as a variable (chosen).
3. **A text that carries the model's own explanation** - more informative, but model text would reach a refusal card and could quote a chunk or name a document.
4. **For `malformed`, the page's existing error instead of a refusal card** - one message for every system failure, but the evaluation run stops at that row and the raw reply is lost from the results file.
5. **For the prompt, a check that the quotes cover every part of the question** - it would read meaning, which only the model does, so it was not built; the model's sentence stays unchecked (ADR 0011).

The strongest alternative is option 1, which keeps R10 trivially.

## Decision

`card_text.refusal_card` picks the text from `card.reason` by a fixed mapping:

- `quote_mismatch` and `outside_retrieved`: "Hệ thống không đối chiếu được câu trả lời với nguyên văn quy định nên không đưa ra câu trả lời." and "Bạn có thể hỏi lại hoặc liên hệ {hr}."
- `malformed`: "Hệ thống gặp lỗi khi tạo câu trả lời." and "Vui lòng thử lại; nếu vẫn lỗi, liên hệ {hr}."
- Any other reason, including `no_points` and no reason: the text of v1, unchanged.

A reason added later therefore falls back to the text that reveals nothing.
Each text has only `{hr}` as a variable: no refusal names a document or quotes a chunk, and no model text reaches a refusal card.
`malformed` shows the refusal card with text 3 under the same "Từ chối" heading, with status 200; the results file keeps the raw reply and `reason: "malformed"`.
What step 7 refuses and every check in `services/citations.py` do not change.
`ask()` stores a reply in the cache only after step 7, and never one that step 7 refused for `malformed`, `quote_mismatch` or `outside_retrieved`; a `no_points` refusal, an answer and a conflict stay cached.
The R10 gate compares refusal cards within each reason: all refusal cards with the same reason must be identical apart from the HR contact.
"Not allowed" and "not found" are both `no_points`, so R10 is checked exactly as before.
The prompt gets one rule after "Never compute a date, an amount or another value.":
"If the quotes do not answer every part of the question, say in the sentence which part they do not answer.
If the question asks for a value that no clause states, such as a date that would have to be computed, state what the clause says and say in the sentence that the system does not compute that value.
This does not apply to a value about the employee's own record: for that, return an empty list as above."
The third line keeps row 11 a refusal.
The strict-grounding clause of ADR 0003, the own-record rule and "Never compute" are unchanged, and no example sentence is added, so the model does not copy one caveat into every answer.

## Reasons

[chờ Hiệp]

## Consequences

- A refusal tells the asker whether nothing was found, the answer could not be verified, or the system failed, and what to do next.
- "Not allowed" and "not found" still read the same, so a restricted document is still never revealed (R10).
- Texts 2 and 3 depend only on the model's reply and on chunks from the asker's scope, so they reveal nothing outside it.
- Asking again after a model fault reaches the model, so a retry can succeed; a `no_points` refusal is still replayed from the cache.
- The R10 gate no longer compares texts across reasons, so a text that differs between two reasons is not caught by it; the mapping is pinned by pytest instead.
- The caveat is a sentence the model writes and no rule checks; a model that leaves out a part without saying so is caught only by Hiep's reading of the answers, and the rule may add a caveat that is wrong or missing.
- Texts 2 and 3 are shown only by pytest and the manual check; no row of the evaluation set produces them, because all 8 refusals of run `20261021-1032` are `no_points`.
- Built in #96: the mapping in `services/card_text.py`, the cache rule in `services/ask.py`, the per-reason gate in `evaluation/score.py` and its threshold text in `evaluation/report.py`, the prompt rule, and the tests listed in the issue.

## Would change if

- The shared run shows a caveat that is wrong or missing in more than a rare answer, so the sentence needs a check or the rule is withdrawn.
- A refusal text is shown to be read as "there is no rule", or a retry after a model fault keeps failing for the same reason.
- A new refusal reason appears that the fallback to text 1 does not suit.

## Evidence

- Probe P6 in `docs/mission3/gaps.md`, reproduced on the page at `892a5d7`; it becomes `test_p6_the_four_replies_give_three_texts` in `tests/api/test_page.py`.
- `tests/services/test_card_text.py`: the mapping for each reason, `None` and an unknown reason; no refusal text names a document or quotes a chunk, for every persona and reason.
- `tests/services/test_ask.py` and `tests/api/test_page.py`: a reply refused for a model fault is asked again; a `no_points` refusal and a conflict are cached.
- `tests/evaluation/test_score.py`: two `no_points` refusals that differ fail the gate; texts 2 and 3 pass it within their reason.
- `tests/services/answering/test_prompt.py`: the new rule is in the instruction, with the strict-grounding clause, the own-record rule and "Never compute" kept.
- Evidence log line for the session that built it.
