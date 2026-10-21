# 0012. The card tells the asker when a version ends and what replaces it

- Status: Proposed
- Date: 2026-10-21
- Origin: Hiep + AI
- Supersedes: Mission 1 M8 ("a future version is not shown before it takes effect") for published versions
- Issue: #83
- Research: None

## Context

The rules pick the version in force on the as-of date and the card says when it started, never when it stops (gap G1.2).
The model is given no date, so a question about another period is answered with today's version (gap G1.1).
Row 18 shows it: Minh on 15/12/2026 asks what he gets next year, and an answer card says "14 ngày" although version 3 applies from 01/01/2027.
It was the only unsafe answer of the Mission 2 run, and limitation #53 keeps it open.
All data is simulated ("giả lập").

## Options considered

Where the next change is computed:

1. **`scope()` computes it for the asker and stores it on `Scope`** - the rules run on each future date where a published document starts or ends, and the first date a document leaves the scope is its change (chosen).
2. **A separate function that the page and the harness call and pass to `ask()`** - two call sites that must stay the same.

What "đến hết <ngày>" means:

1. **The last day the document is in this asker's scope** - one date for the source line, the notice and the prompt (chosen).
2. **The document's own validity, the same for everyone** - gives no end date when another policy replaces it for the asker's unit only.

The notice when no successor can be named (none exists, it is hidden, or another policy comes back):

1. **"Sắp thay đổi: quy định này hết hiệu lực với bạn sau <ngày>. Vui lòng hỏi <HR> về quy định áp dụng từ <ngày + 1>."** - true in all three cases, and a hidden successor gives exactly the text of no successor (chosen).
2. **"Hết hiệu lực sau <ngày>; chưa có văn bản thay thế áp dụng cho bạn."** - false when the successor is hidden and when the Group policy comes back.
3. **As option 2, naming the policy that comes back** - needs a rule for which documents entering the scope count as a successor.

How the model learns the dates:

1. **The as-of date and each chunk's window and change in the prompt, with one rule for a question about another period** (chosen).
2. **Only the as-of date and the windows, no notices** - the model could say the clause ends, but not what replaces it.
3. **Refuse a question about another period** - the refusal card of today, with no information for the asker.

## Decision

`scope()` also returns, for each document in the asker's scope, the first later date it leaves the scope (`Change`) and the documents in the asker's scope on the next day that replace it: the next version of its series or a policy that declares "dùng thay" over it.
Published documents only: a draft never enters a scope, so it is never named.
A successor the asker may not read is never named.

The source line ends with "đến hết <ngày>" when there is a change.
A "Sắp thay đổi" notice follows the source line of each cited document that has one, and each side's quotes on the conflict card.
Both come from the rules alone, with no model text, whatever the distance to the change.

The prompt gives the as-of date and, for each chunk, `valid_from`, and when there is a change `valid_to` and `change`.
One new rule tells the model to say in the sentence until when a clause applies when the question asks about another time, and never to present it as the rule for that time.
The model never sees a successor's content, so the system tells the asker that version 3 applies from 01/01/2027 and does not answer "15 ngày".
The reply cache key gains the as-of date.

Row 18 becomes a hard case with an answer card, and one new row covers a document that ends with no successor.

## Reasons

[chờ Hiệp]

## Consequences

- Row 18 is no longer a limitation: the card says until when 14 days applies and what replaces it.
- The sentence is checked by Hiep's reading, not at run time (ADR 0011); a sentence that gives 14 days as next year's number fails row 18.
- The system still does not answer a question about another period with that period's content; #53 stays open for that.
- A notice shows however far away the change is, and no config key is added.
- Every cached reply is tied to one date, so the demo cache hits less across dates.
- A change in the series of a restricted successor is invisible to the asker, who sees the generic notice.
- `data/` is unchanged; `data_edit` can set `effective_to`.

## Would change if

- Notices for changes far in the future confuse askers: add a time window and a config key.
- Owners want to announce a version before it is published: a status between draft and published, which is a new ADR.

## Evidence

pytest with fake models and in-memory edits: `tests/services/test_scope.py`, `test_card_text.py`, `test_prompt.py`, `test_ask.py`, `tests/api/test_page.py`.
The shared full run on `gemini-3.5-flash-lite` after #76, #83 and #87 are merged, with Hiep's reading of row 18 and row 21.
Evidence log line of 21/10/2026.
