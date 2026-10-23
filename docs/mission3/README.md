# Mission 3: an answer that answers the question, and stays checkable

This page explains the one improvement we chose for Mission 3, why we chose it, and the evidence that it made the product better.
The Mission 2 card quoted the right rule word for word, but often left the employee to work out the answer.
The Mission 3 card answers the question in one sentence, says until when that answer holds, and keeps the checked quote right under it.

For example, on 15/12/2026 Minh asks how many days of annual leave he gets from next year.
Mission 2 showed "14 ngày" with nothing saying that this rule ends on 31/12/2026.
Mission 3 answers that 14 days apply until 31/12/2026 and that a new version of the policy applies from 01/01/2027.

All companies, people, documents and numbers are simulated ("giả lập").
Hiep is the candidate; AI tools helped build the product, under Hiep's decisions and review ([how this was built](../how_this_was_built.md)).
The terms used here are explained in the [glossary](../../README.md#glossary).

![The same question on both versions. Mission 2 shows only the quote "14 ngày" and its start date. Mission 3 answers that version 2 of the policy, with 14 days, applies only until 31/12/2026 and that version 3 applies from 01/01/2027; it keeps the same quote, ends the source line with the end date and adds a "Sắp thay đổi" line](../images/before-after-row18.png)

*Screenshots of a local run of each version on 23/10/2026.
The AI's wording varies between runs: this answer also says that the quotes do not give next year's number.*

## The direction we chose

**From "quote the right rule" to "answer the question", without giving up the check.**

Whenever the system can answer, the answer card is what the employee reads, so it is where an improvement reaches the most people.
In Hiep's words:

> "nguyên văn trung thực nhưng không phải lúc nào cũng trả lời thẳng câu hỏi. Thiết kế trong Mission 2 quá cứng nhắc và bị hạn chế khi gặp các câu hỏi mà đoạn trích trong văn bản không thể là câu trả lời."
>
> (A word-for-word quote is faithful, but it does not always answer the question directly. The Mission 2 design was too rigid, and it fell short on questions where no passage of a document can itself be the answer.)

Letting the AI write the answer is a risk.
So the direction has one condition: the fixed rules keep every decision they made in Mission 2.
They still decide who may read what, which version is in force, which policy applies and which one wins.
The AI writes the answer, and may flag two clauses that disagree.
The rules check that flag and every quote under the answer, word for word, and then pick the card.

## What changed

Each change below has the same shape: what Mission 2 did, what Mission 3 does, and the test case that shows it.

### 1. One answer above the checked quotes

- **Mission 2:** the card showed only the quoted clauses.
  The employee had to read them and work out the answer.
- **Mission 3:** the AI writes one answer in plain Vietnamese, in bold, above the quotes that back it.
  A fixed line on the card says which text is the system's answer and which is the checked original.
- **Shown by:** every answer card of the Mission 3 run, for example Minh's question on how to request leave and who approves it (test case 3).
  The answer covers both parts in one sentence: create the request in the internal HR system, and the team lead approves it.
  It also leaves out a third point of the procedure, that the result is sent to the company email (see [What is still wrong](#what-is-still-wrong)).

[Decision records 0011 and 0018]

### 2. The answer says until when it holds, and what replaces it

- **Mission 2:** the card gave only the date a version started, and the AI was not told the date of the question.
  Asked about next year's leave, Minh got this year's "14 ngày" with no warning.
- **Mission 3:** the rules work out the last day a version applies and what replaces it.
  The card shows "đến hết 31/12/2026" and the line "Sắp thay đổi: Quy chế nghỉ phép GameCo (bản 3) áp dụng từ 01/01/2027."
  The AI is given the date of the question and the dates of each clause, so its answer can say the same.
- **Shown by:** Minh's next-year question (test case 18), one of the two unsafe answers of Mission 2.
  A rule that ends with no replacement now sends the asker to HR (test case 21).

[Decision record 0012]

### 3. The answer never hides a second source

- **Mission 2:** only the labels an owner put on documents could reveal a conflict.
  With a wrong topic label on the PayCo leave policy, Hà was told "13 ngày", and nothing mentioned the Group policy's 12 days, which also apply to her.
- **Mission 3:** the AI may also flag two quoted clauses that give different answers.
  The rules check the flag, then show the conflict card with both sides and send Hà to HR.
  The AI can add a conflict card, never remove one.
- **Shown by:** Hà's leave question with the wrong label (test case 19), the other unsafe answer of Mission 2.
  Two questions that look like conflicts but are not still get a plain answer (test cases 3 and 20).

[Decision record 0014]

### 4. The answer says what it does not cover, and a refusal says why

- **Mission 2:** Minh asked for the last day to request leave for Monday 19/10/2026.
  In 2 of 4 runs he was refused; in the other 2 he got the three-working-day clause alone, with no word that the date was not worked out.
  Every refusal also read the same, whatever its reason.
- **Mission 3:** Minh gets the three-working-day rule, and the answer adds that the system does not work out the date.
  A refusal now says whether nothing was found, the answer could not be checked, or the system failed.
- **Shown by:** Minh's deadline question (test case 16), answered in all 5 Mission 3 runs.
  It stays a known limitation, because 5 runs do not make a rate.
  The new refusal texts are shown by the automated tests, because every refusal in the runs had the same reason.

[Decision record 0017]

### 5. Each source opens the clause it quotes

- **Mission 2:** the employee saw only the quote, never the rest of the clause.
- **Mission 3:** each source line links to the cited version of the document, with the quoted clause highlighted.
  The page shows when that version applies and to whom.
  A document outside the asker's rights gives the same "not found" page as one that does not exist.
- **Shown by:** the automated tests, because the runs record only the card's text.

### Also changed, outside the direction

Mission 2 took the asker as a parameter in the page address, so anyone could ask as anyone.
Mission 3 adds a simulated sign-in: the server, not the visitor, decides who is asking.
A new account, Hoa from GameCo HR, shows a restricted document being granted, not only refused (test case 22).
[Decision record 0016]

## The evidence

Both versions were asked the test cases with the real AI model, and both runs were scored by the same checks.
The totals leave out case 16, a known limitation kept on purpose.
Mission 2 also leaves out case 22, because its account does not exist there.
Case 19 is new for Mission 3, so the Mission 2 submission reported 1 unsafe answer (case 18), not 2.

| | Mission 2 | Mission 3 |
|---|---|---|
| Test cases scored | 20 | 21 |
| Rules picked the wrong documents | 0 | 0 |
| Leaks of restricted text | 0 | 0 |
| Unsafe answers | 2 (cases 18 and 19) | 0 |
| Over-cautious cards | 0 | 0 |
| Answer cards Hiep reviewed: nothing false against the quotes | not reviewed | 10 of 10, the 9 counted plus case 16 (one leaves out a point, case 3) |

- The two unsafe answers of Mission 2 are gone: next year's leave (case 18) and the hidden conflict (case 19).
- No test case that passed on Mission 2 fails on Mission 3.
- The deadline question (case 16) was refused in the Mission 2 run and answered in the Mission 3 run; over all runs, Mission 2 answered it 2 times in 4 and Mission 3 5 times in 5.

Read the numbers with two cautions.
Each version is shown by one run, and one run is not a rate.
Mission 2 gave the unwarned "14 ngày" to the next-year question in all 4 of its runs.
Mission 3 refused that question once in its 4 earlier runs, so its fix is not guaranteed every time.

Every test case, side by side: [before and after, case by case](runs.md).
The full Mission 3 run in the brief's format: [test report](../test_report.md).

## What we chose not to do

Each of these was a real option that we weighed and left out.

| Not done | Why | What it costs |
|---|---|---|
| A page where owners publish documents, with a check for contradictions at publish time | Hiep: "hiện tại vẫn chưa cần trang quản lí cho chủ sở hữu văn bản, số lượng văn bản còn ít và có thể mô phỏng được" (there are still few documents, and they can be simulated) | Nothing checks an owner's labels before employees see them |
| Letting the AI remove a conflict card when both sides say the same on the point asked | Hiep: "hai văn bản có mâu thuẫn thì nên được báo cáo là mâu thuẫn, cho dù cả hai văn bản đều đồng ý về một câu trả lời" (two documents that conflict are reported as a conflict, even when they agree on the answer) [decision record 0019] | Hà is sent to HR for a question both her policies answer the same way |
| Answering a question about next year from next year's version | Choosing the version from the words of the question would let the AI decide which version is valid [decision record 0012] | The card names the change and its date, but not next year's number |
| A check of the AI's answer while the product runs | A rule on numbers would refuse correct answers that give dates, such as case 18, whose answer gives 31/12/2026 and 01/01/2027 although its quote does not; it would still miss a dropped condition, and a second AI model would be one more thing to trust [decision record 0018] | A wrong answer above a correct quote is caught only by a reader |

## What is still wrong

1. **The AI's answer is not checked while the product runs.**
   This is the cost of the direction.
   The quotes under it are checked, so the reader can compare, but a wrong number or a dropped condition reaches the employee.
   Hiep's review of the Mission 3 run found no answer that says something its quotes do not.
   One answer is incomplete: it leaves out that the approval result is sent to the company email (case 3).
2. **The rules are only as right as the labels owners put on documents.**
   A wrong access label still leaks a document, and nothing checks the labels when a document is published.
   This was shown only on edited copies of the simulated data, and a check at publish time is not built.
3. **A conflict the AI does not notice still gives a one-sided answer.**
   The AI can add a conflict only when it reads both sides and sees that they differ.
4. **A question about another period gets the rule in force on the chosen date.**
   About next year, the card says when that rule ends and what replaces it, but never gives the next version's numbers.
   About a past year, it is usually refused: Minh's question about his leave in 2025 was refused 8 times in 9.
   The ninth time, it answered with this year's "14 ngày", when the rule in 2025 gave 13. [An experiment on 23/10/2026, not a test case]
5. **A question that needs a clause applied to a case is sometimes refused,** although the right clause was found.
   Mission 2 refused it in 2 of 4 runs and Mission 3 answered it in 5 of 5, but its rate is not measured.

Items 2 to 5 are open issues labelled `limitation` on GitHub; item 1 is recorded as a decision with its cost. [Issues #50, #74, #53 and #51; decision records 0011 and 0018]

## Technical detail

| | Mission 2 version | Mission 3 version |
|---|---|---|
| Code | Tag `mission2` (`b6ca78d`), as submitted on 15/10/2026 | `main`; the run below is at `bb329b5`, the branch for cases 15 and 17 (main plus one commit, merged in PR #115) |
| Run | `20261021-2319`, plus `20261022-0630-m2-rows19-21` for cases 19-21 | `20261022-1602` |
| Model | `gemini-3.5-flash-lite` at medium thinking, `gemini-embedding-001`, top 5 | Same |

- Both runs are scored by `evaluation/score.py` with the Mission 3 test file `data/test_cases.yaml`, so both columns use one yardstick.
- Cases 19-21 edit a document label in memory, which the Mission 2 harness cannot do; [runs.md](runs.md#technical-detail) explains how they were asked on the Mission 2 code.
- Hiep's review of the Mission 3 answer cards is in `results/20261022-1602.review.yaml`.
- Case 16 on the Mission 2 code: answered in `20261014-2239` (the Mission 2 submission) and `20261021-2311`, refused in `20261021-2315` and `20261021-2319`; on the Mission 3 code it is answered in `20261021-2253`, `-2258`, `-2301`, `20261022-1432` and `-1602`, with the caveat from `1432` on, after issue #96.
- Case 18 on Mission 3: refused only in `20261021-2301`; `20261022-1432` ran on a worktree that was not clean.
- The screenshots were taken by hand on a local run of each version on 23/10/2026; on Mission 2, case 16 gave the quote-only answer card each time it was asked.
- The changes: answer above the quotes (issue #75, PR #90; issue #112, PR #113), validity and next version (issue #83, PR #93), conflicts flagged by the model (issue #87, PR #92), refusal reasons (issue #96, PR #102), source page (issue #77, PR #99), sign-in (issue #76, PR #94; issue #101, PR #103).
- Decided behaviour rather than defects: case 17, a conflict shown although both sides agree (decision record 0019), and case 15, a replacement that drops a Group clause (decision record 0013).
