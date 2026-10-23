# 0012. The card tells the asker when a version ends and what replaces it

- Status: Accepted
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: The Mission 1 rule that a future version is not shown before it takes effect (M8), for published versions
- Issue: #83
- Research: None

## In short

- **The problem:** Minh asks on 15/12/2026 what annual leave he gets next year.
  The system answered "14 ngày", this year's figure, although from 01/01/2027 a new version of the GameCo leave policy gives 15.
  The card said when a version started, never when it stops, and the AI was never told the date of the question.
  It was the only unsafe answer of the Mission 2 run.
- **The decision:** The fixed rules work out, for each document the asker can see, the last day it applies to that asker and what replaces it.
  The card shows that, and the AI is given the date of the question and the dates of each clause, with one rule for a question about another period.
- **What the employee sees:** The source line ends with "đến hết <ngày>", and a "Sắp thay đổi" notice under it says when the rule stops and what applies afterwards.
  Minh is told that 14 days applies until 31/12/2026 and that version 3 applies from 01/01/2027.
  If nothing the asker may read replaces the rule, the notice sends them to HR.
- **What we give up:** The system still does not answer a question about another period with that period's content.
  A notice appears however far away the change is, the saved-replies cache helps less across dates, and the asker cannot be told about a replacement they may not read.

All data is simulated ("giả lập").

## Context

The rules pick the version in force on the as-of date, and the card says when it started but never when it stops.
The AI is given no date, so a question about another period is answered with today's version.
The test case shows it: Minh on 15/12/2026 asks what he gets next year, and an answer card says "14 ngày" although version 3 applies from 01/01/2027.
It was the only unsafe answer of the Mission 2 run, and a limitation issue keeps it open.

## Options considered

Where the next change is computed:

1. **The rules that build the asker's scope compute it for the asker and store it with the scope** - the rules run on each future date where a published document starts or stops, and the first date a document leaves the scope is its change (chosen).
2. **A separate function that the page and the evaluation both call and pass to the answering step** - two call sites that must stay the same.

What "đến hết <ngày>" means:

1. **The last day the document is in this asker's scope** - one date for the source line, the notice and the prompt (chosen).
2. **The document's own validity, the same for everyone** - gives no end date when another policy replaces it for the asker's unit only.

The notice when no successor can be named (none exists, it is hidden, or another policy comes back):

1. **"Sắp thay đổi: quy định này hết hiệu lực với bạn sau <ngày>. Vui lòng hỏi <HR> về quy định áp dụng từ <ngày + 1>."** - true in all three cases, and a hidden successor gives exactly the text of no successor (chosen).
2. **"Hết hiệu lực sau <ngày>; chưa có văn bản thay thế áp dụng cho bạn."** - false when the successor is hidden and when the Group policy comes back.
3. **As option 2, naming the policy that comes back** - needs a rule for which documents entering the scope count as a successor.

How the AI learns the dates:

1. **The as-of date and each clause's window and change in the prompt, with one rule for a question about another period** (chosen).
2. **Only the as-of date and the windows, no notices** - the AI could say the clause ends, but not what replaces it.
3. **Refuse a question about another period** - the refusal card of today, with no information for the asker.

## Decision

The rules that build the asker's scope also return, for each document in it, the first later date it leaves the scope, and the documents in the asker's scope on the next day that replace it.
A replacement is the next version of the same policy, or a policy that declares "dùng thay" (replaces) it.
Only published documents count: a draft never enters a scope, so it is never named.
A successor the asker may not read is never named.

The source line ends with "đến hết <ngày>" when there is a change.
A "Sắp thay đổi" notice follows the source line of each cited document that has one, and follows each side's quotes on the conflict card.
Both come from the rules alone, with no AI text, whatever the distance to the change.

The prompt gives the AI the as-of date and, for each clause, the first day it applies and, when there is a change, the last day and what happens next.
One new rule tells the AI, when the question asks about another time, to say in the sentence until when a clause applies, and never to present it as the rule for that time.
The AI never sees a successor's content, so the system tells the asker that version 3 applies from 01/01/2027 and does not answer "15 ngày".
The saved-replies cache key gains the as-of date.

The Mission 2 test case on this question becomes a hard case that expects an answer card, and one new test case covers a document that ends with no successor.

## Reasons

The date the asker names must not decide which rule applies; that stays with the rules.
The card, not the model, tells the asker that a version ends and what replaces it, so the asker is warned without the model ever seeing the future version's content.
Letting the model answer from next year's version would make validity depend on how the question is read.

Drafted by AI; approved by Hiep on 23/10/2026.

## Consequences

- The question above is no longer a limitation: the card says until when 14 days applies and what replaces it.
- The sentence is checked by Hiep's reading, not at run time (ADR 0011); a sentence that gives 14 days as next year's number fails that test case.
- The system still does not answer a question about another period with that period's content; the limitation issue stays open for that. [#53]
- A notice shows however far away the change is, and no config key is added.
- Every saved reply is tied to one date, so the demo cache hits less across dates.
- A change in the policy series of a restricted successor is invisible to the asker, who sees the generic notice.
- The simulated data is unchanged; the data-edit tool can set an end date.

## Would change if

- Notices for changes far in the future confuse askers: add a time window and a config key.
- Owners want to announce a version before it is published: add a status between draft and published, which is a new ADR.

## Evidence

- Offline tests with fake models and in-memory edits (files in Technical detail).
- The shared full run on `gemini-3.5-flash-lite` after the three related changes are merged, with Hiep's reading of the two cases concerned.
- Evidence log line of 21/10/2026.

## Technical detail

- Issue #83; limitation #53; related changes #76, #83 and #87; gaps G1.1 (no date given to the AI) and G1.2 (no end date on the card); Mission 1 decision M8.
- `scope()` returns `Scope.changes`, a tuple of `Change(document_id, last_day, successors)`.
  The rules run on the dates where a published document starts (`effective_from`) or the day after one ends (`effective_to`).
- The prompt carries `valid_from` for each chunk, and `valid_to` and `change` when there is a change; the as-of date is in `<as_of>`.
- The reply cache key is persona id, as-of date, the scope's chunk ids and the question.
- Cases: 18 (Minh, 15/12/2026) becomes a hard case with an answer card; 21 covers a document that ends with no successor.
- `data_edit` can set `effective_to`.
- Tests: `tests/services/test_scope.py`, `tests/services/test_card_text.py`, `tests/services/answering/test_prompt.py`, `tests/services/test_ask.py`, `tests/api/test_page.py`.
