# 0017. A refusal says why, and an answer says what it does not cover

- Status: Accepted
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: The refusal wording of Phần 2 of the Mission 1 document (promise C4) for three of the four refusal reasons (a quote that does not match, a citation outside what was retrieved, unreadable AI output); promise R10 is kept; it adds a rule to the prompt of ADR 0011, which keeps its status
- Issue: #96
- Research: None

## In short

- **The problem:** The product refuses for four different reasons, and every refusal said the same thing: "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn."
  When the AI did find a rule but its quote could not be verified, or when the system itself failed, Minh would read that as "there is no rule".
  A faithful answer can also leave out part of the question without saying so: Minh asks for the last day to file leave for Monday 19/10/2026, and gets the "3 working days" rule with no word that the system does not work out dates.
- **The decision:** The refusal text now depends on why the system refused, chosen by a fixed rule and never by the AI.
  Three texts exist: nothing found, answer could not be checked against the document, and a system error.
  The prompt also tells the AI to say, in its sentence, which part of the question the quotes do not answer.
- **What the employee sees:** A refusal that says whether nothing was found, the answer could not be verified, or the system failed, and what to do next.
  An answer that says what it does not cover.
  "Not allowed" and "not found" still read the same, so a restricted document is still never revealed.
- **What we give up:** The caveat is a sentence the AI writes and no rule checks, so it may be wrong or missing.
  No test case of the evaluation produces the two new refusal texts; only offline tests and a manual check show them.

## Context

Mission 3 general requirement 4 asks the product to refuse or to show that the basis is not enough.
Hiep's principle for it: refuse only when nothing can be verified; when a verified answer covers part of the question, show it and say what it does not cover; the AI may add a caveat, but it never gets past a check.

The quote check refuses for four reasons, and the card keeps the reason:

- the AI returned no points (nothing answers the question);
- the AI's output could not be read;
- a quote is not in the passage it cites;
- the AI cites a passage that was not retrieved.

All four gave one text, "Hệ thống không tìm thấy quy định phù hợp để trả lời câu hỏi này cho bạn."
On the simulated data ("giả lập"), signed in as Minh on 07/10/2026 with the leave question, the four cases gave the same card, word for word.
In the last three, the AI did answer or the system failed, so "không tìm thấy quy định" can be read as "there is no rule".
Promise R10 wants one text for "not allowed" and "not found", so a restricted document is never revealed; both are "no points", and the other three reasons depend only on the AI's reply to passages from the asker's own scope.

Two behaviours of the product would have undermined a change of wording alone:

- The reply cache stored every reply, so a text that says "thử lại" (try again) or "hỏi lại" (ask again) would have replayed the same cached failure.
- The R10 check of the evaluation compared all refusal cards of a run with each other, so one refusal with a different reason would have failed it.

A faithful answer can also leave out part of what was asked, and nothing tells the asker.
In test case 16, Minh asks for the last day to file leave for Monday 19/10/2026; the answer gives the 3-working-day rule and does not say that the system does not compute the date asked for.

## Options considered

1. **One text for every reason** - the Mission 2 behaviour; it reveals nothing, but it says "no rule found" when a rule was found and not verified, or when the system failed.
2. **Three texts chosen from the reason by a fixed mapping** - text 1 for no points, unchanged; text 2 for a quote that does not match and for a citation outside what was retrieved; text 3 for unreadable output; each has only the HR contact as a variable (chosen).
3. **A text that carries the AI's own explanation** - more informative, but AI text would reach a refusal card and could quote a passage or name a document.
4. **For unreadable output, the page's existing error instead of a refusal card** - one message for every system failure, but the evaluation run stops at that case and the raw reply is lost from the results file.
5. **For the prompt, a check that the quotes cover every part of the question** - it would read meaning, which only the AI does, so it was not built; the AI's sentence stays unchecked (ADR 0011).

The strongest alternative is option 1, which keeps R10 trivially.

## Decision

The refusal text is picked from the reason by a fixed mapping:

- **A quote that does not match, or a citation outside what was retrieved:**
  "Hệ thống không đối chiếu được câu trả lời với nguyên văn quy định nên không đưa ra câu trả lời."
  "Bạn có thể hỏi lại hoặc liên hệ {hr}."
- **Unreadable output:**
  "Hệ thống gặp lỗi khi tạo câu trả lời."
  "Vui lòng thử lại; nếu vẫn lỗi, liên hệ {hr}."
- **Any other reason, including no points and no reason:** the text of the Mission 2 version, unchanged.

A reason added later therefore falls back to the text that reveals nothing.
Each text has only the HR contact ({hr}) as a variable: no refusal names a document or quotes a passage, and no AI text reaches a refusal card.
Unreadable output shows the refusal card with text 3 under the same "Từ chối" heading, with status 200; the results file keeps the raw reply and the reason.

What the quote check refuses, and every check it makes, do not change.
The reply cache stores a reply only after the quote check, and never one that the quote check refused for unreadable output, a non-matching quote or a citation outside what was retrieved; a "no points" refusal, an answer and a conflict stay cached.
The R10 check compares refusal cards within each reason: all refusal cards with the same reason must be identical apart from the HR contact.
"Not allowed" and "not found" are both "no points", so R10 is checked exactly as before.

The prompt gets one rule after "Never compute a date, an amount or another value.":
"If the quotes do not answer every part of the question, say in the sentence which part they do not answer.
If the question asks for a value that no clause states, such as a date that would have to be computed, state what the clause says and say in the sentence that the system does not compute that value.
This does not apply to a value about the employee's own record: for that, return an empty list as above."
The third line keeps the question about the employee's own leave balance (case 11) a refusal.
The strict-grounding clause of ADR 0003, the own-record rule and "Never compute" are unchanged, and no example sentence is added, so the AI does not copy one caveat into every answer.

## Reasons

A refusal must not say "không tìm thấy quy định" when a rule was found but could not be verified, or when the system itself failed; that makes the asker read it as "there is no rule".
Each reason gets its own text, picked by a fixed rule and never by the model, and "not allowed" and "not found" keep the same wording so a restricted document is still never revealed.

Drafted by AI; approved by Hiep on 23/10/2026.

## Consequences

- A refusal tells the asker whether nothing was found, the answer could not be verified, or the system failed, and what to do next.
- "Not allowed" and "not found" still read the same, so a restricted document is still never revealed.
- Texts 2 and 3 depend only on the AI's reply and on passages from the asker's scope, so they reveal nothing outside it.
- Asking again after an AI fault reaches the AI, so a retry can succeed; a "no points" refusal is still replayed from the cache.
- The R10 check no longer compares texts across reasons, so a text that differs between two reasons is not caught by it; the mapping is pinned by offline tests instead.
- The caveat is a sentence the AI writes and no rule checks; an AI that leaves out a part without saying so is caught only by Hiep's reading of the answers, and the rule may add a caveat that is wrong or missing.
- Texts 2 and 3 are shown only by offline tests and the manual check; no test case of the evaluation produces them, because all 8 refusals of the full evaluation run of 21/10/2026 are "no points".

## Would change if

- The shared run shows a caveat that is wrong or missing in more than a rare answer, so the sentence needs a check or the rule is withdrawn.
- A refusal text is shown to be read as "there is no rule", or a retry after an AI fault keeps failing for the same reason.
- A new refusal reason appears that the fallback to text 1 does not suit.

## Evidence

- A probe reproduces the four cases on the page and shows the four replies giving the same text; it becomes a test that the four replies give three texts.
- Offline tests cover: the mapping for each reason, no reason and an unknown reason; that no refusal text names a document or quotes a passage, for every account and reason; that a reply refused for an AI fault is asked again while a "no points" refusal and a conflict are cached; that two "no points" refusals that differ fail the R10 check while texts 2 and 3 pass it within their reason; and that the new prompt rule is present with the strict-grounding clause, the own-record rule and "Never compute" kept.
- Evidence log line for the session that built it.

## Technical detail

- Issue #96; Mission 3 requirement 4; gaps G4.3 (one text for every reason) and G4.5 (no word on what an answer leaves out); probe P6 in `docs/mission3/gaps.md`, reproduced on the page at commit `892a5d7`; promises C4 and R10; case 16 (the date that would have to be computed), case 11 (the own-record question).
- The step 7 refusal reasons (kept on the card as `reason`): `no_points`, `malformed`, `quote_mismatch`, `outside_retrieved`.
- `card_text.refusal_card` picks the text from `card.reason`: `quote_mismatch` and `outside_retrieved` give text 2, `malformed` gives text 3, anything else (including `no_points` and `None`) gives the Mission 2 text.
  `REFUSAL_TEXT_BY_REASON` in `services/card_text.py` holds the mapping.
- `ask()` in `services/ask.py` stores a reply in the cache only after step 7 and not when the reason is in `MODEL_FAULTS` (`malformed`, `quote_mismatch`, `outside_retrieved`).
- The per-reason check is `refusals_identical` in `evaluation/score.py`; its threshold text is in `evaluation/report.py`.
- The prompt rule is in `services/answering/prompt.py`; `services/citations.py` checks are unchanged.
- In the full evaluation run `20261021-1032`, all 8 refusals have reason `no_points`.
- Tests: `test_p6_the_four_replies_give_three_texts` in `tests/api/test_page.py`; `tests/services/test_card_text.py`; `tests/services/test_ask.py`; `tests/api/test_page.py`; `tests/evaluation/test_score.py`; `tests/services/answering/test_prompt.py`.
