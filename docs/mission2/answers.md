# Mission 2 - 3 câu hỏi bắt buộc

The answers to the 3 mandatory questions of the Mission 2 brief, submitted separately from the README.
Every unit, person, document and number is simulated ("giả lập").
Each answer is a draft by Claude from the sources it names; Hiep rewrites it in his own words before it is submitted.

## Câu 1: what we chose to prove

> Phần quan trọng nhất bạn chọn để hiện thực hóa trong MVP là gì? Vì sao nếu phần này hoạt động, bạn tin rằng hướng giải quyết của mình là khả thi?

[Draft from "The bet" in `docs/mission2/plan.md`; Hiep rewrites this answer in his own words.]

We chose to prove that deterministic rules can build the asker's scope before any AI runs, and that the AI then answers only from that scope, with a source, or says it found nothing.
The scope is the documents in force on the as-of date that the asker may read and that apply to their unit, minus the policies another kept policy is declared to replace.

If the scope is right, a wrong version, another unit's rule or a restricted document cannot reach an answer, because the AI never sees them.
The hard parts of the brief, which version, which unit and who may read it, then become lookups on document metadata that give the same result every time and are tested without any AI.
What remains is a language task: the AI citing a valid document in the scope that does not answer the question, or misstating it.
That is the riskiest assumption of our Mission 1 design, and it is what the test set measures on the real model.
So the approach is feasible if both hold: the rules are correct on every test case, and the AI, inside a correct scope, answers with a checkable source or refuses.

## Câu 2: what changed since Mission 1

> So với kế hoạch ở Mission 1, bạn đã thay đổi quyết định hoặc thiết kế nào? Điều gì trong quá trình làm khiến bạn thay đổi?

[Draft from the ADRs and the promise ledger; Hiep rewrites this answer in his own words.]

The design did not change: the 7 steps, the rules before any AI, and the three cards are built as Mission 1 described them.
The rules and their tests merged on 13/10/2026 (PR #25) before retrieval (PR #28), as Mission 1 promised.
What changed is around them:

| Mission 1 plan | v1 | What made us change | Decision |
|---|---|---|---|
| Steps 2 and 3: filter access and applicability, then apply "dùng thay" | Access is applied last: a replacing policy the asker may not read still replaces the old one, and the asker gets a refusal | Testing a restricted new version: it brought the old Group policy back for Minh, with a false conflict card | [ADR 0010](../decisions/0010-access-never-decides-precedence.md) |
| Step 7 refuses an answer whose citation was not retrieved | Also, each point quotes its clause word for word, and step 7 refuses the answer if the quote is not in the cited chunk | Research on grounded answers: a valid chunk id alone does not show that the point says what the chunk says | [ADR 0003](../decisions/0003-gemini-38-flash-enum-citations-quote-check.md) |
| The answer card shows an answer sentence the LLM writes | It shows the quotes step 7 checked, word for word | Reading the first real run: a sentence dropped a condition its quote had ("chính thức"), and no rule checked the sentence | [ADR 0009](../decisions/0009-answer-card-shows-the-verified-quote.md) |
| An off-the-shelf LLM | `gemini-3.5-flash-lite` at medium thinking | The first choice, `gemini-3.8-flash`, returned "high demand" errors and allows 20 requests a day on the free tier, too few for one evaluation run | [ADR 0008](../decisions/0008-gemini-35-flash-lite-at-medium.md) |
| A "Báo sai" button on the answer card, and an owners' page listing reports and conflicts | Not built | Hiep judged it adds little value to Mission 2, and the free host loses its files on every restart | [ADR 0004](../decisions/0004-render-free-singapore-no-bao-sai.md) |
| The conflict card says the conflict is recorded for HR | No conflict record, so the card does not say so | Cut for Mission 2 with the owners' page, for the same reason (Hiep, 14/10/2026) | [#15](https://github.com/Park-Hip/next-gen-2026/issues/15) |
| Each case asked in 3 wordings, and run several times, one failure failing the case | Each case asked once, in its main wording; the other wordings stay in the test file | The Gemini free-tier rate limit, shared with the demo | [ADR 0006](../decisions/0006-own-harness-one-run-main-wording.md) |
| Context recall tracked | Not measured | Too soon on 10 simulated documents; revisit with real documents | [ADR 0007](../decisions/0007-defer-context-recall.md) |
| 10 test cases | 18 | The brief asks for a case the product handles well, a hard one and a failing one; three more failures found by probing the live pipeline became limitation cases | [#10](https://github.com/Park-Hip/next-gen-2026/issues/10), [#51](https://github.com/Park-Hip/next-gen-2026/issues/51), [#52](https://github.com/Park-Hip/next-gen-2026/issues/52), [#53](https://github.com/Park-Hip/next-gen-2026/issues/53) |

Every promise of the Mission 1 document, with what shipped: [`docs/mission2/mission1_promises.md`](mission1_promises.md).
Each decision links the research it came from in [`docs/research/`](../research/); the index of decisions is [`docs/decisions/`](../decisions/README.md).

## Câu 3: where it is most likely to go wrong

> Trường hợp nào hiện khiến hệ thống dễ trả lời sai hoặc sử dụng sai tri thức nhất? Bạn phát hiện và kiểm soát rủi ro đó như thế nào?

[Draft from the test report and the issues; Hiep rewrites this answer in his own words.]

**Most likely to use the wrong knowledge: a mistake in the metadata an owner sets ([#50](https://github.com/Park-Hip/next-gen-2026/issues/50)).**
The rules guarantee the right version, unit and access only when the metadata is right, and nothing in v1 checks it.
If PayCo's leave policy is tagged with a different topic, Hà's conflict pair disappears and Hà can get an answer card "13 ngày" instead of the conflict card.
If an amendment that changes one clause is declared "bổ sung", the old clause stays in scope with no conflict, so an answer can cite the old "14 ngày".
"0 leaks" holds on the same condition: a wrong access field leaks every time.
How we found it: editing a copy of the simulated data and printing the scope the rules build, with no model.
How it is controlled today: owners declare every relation by hand, and when they have declared none the conflict card quotes both sides and sends the asker to HR instead of choosing.
What it needs: a check when an owner publishes, and a way for employees and owners to report a wrong answer; both are deferred in [`docs/scope.md`](../scope.md).

**Most likely to answer wrongly: a real clause in the asker's scope that does not answer the question.**
Step 7 proves that each quote is word for word in the chunk it cites, not that it answers the question; this was the riskiest assumption of our Mission 1 design.
Example ([#53](https://github.com/Park-Hip/next-gen-2026/issues/53)): asked on 15/12/2026 how many leave days Minh gets from next year, the model quoted this year's clause, 14 days, although version 3 gives 15 from 01/01/2027.
The quote is correct and the version is in force today, so no rule can see that it answers another question.
How it is controlled today: the answer card shows only the checked quote with its document, Điều and effective date, so the employee sees exactly what the answer rests on; and in the evaluation, every answer must contain its expected key facts and Hiep reads every answer against its question.

**How we find and control these risks: an example ([#47](https://github.com/Park-Hip/next-gen-2026/issues/47)).**
Reading the first real run, row 5 quoted "Nhân sự chính thức của Tập đoàn được nghỉ phép năm 12 ngày mỗi năm.", but the card showed the model's sentence "Bạn được nghỉ phép năm 12 ngày mỗi năm.", without the condition "chính thức".
No rule checked that sentence: offline, a point quoting the single word "ngày" with an invented sentence "30 ngày" got an answer card with a real source line.
The fix is deterministic: the card now shows the checked quote instead of any sentence the model writes ([ADR 0009](../decisions/0009-answer-card-shows-the-verified-quote.md)), and a test keeps it so.
