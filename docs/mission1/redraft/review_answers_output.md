# Independent review of the 3 mandatory answers - output

Prompt: `docs/mission1/review_prompt_answers.md` (built from commit `95346e3`), run by Hiep on 08/10 in two web chats.
The answers and the document did not change between building the prompt and the runs.

| Run | Tool | Model | Share link |
|---|---|---|---|
| A | ChatGPT web | `gpt-5-6-t-mini` (read from the share page data; a small "thinking mini" model chosen by "auto", not the strongest available) | https://chatgpt.com/share/6ac79398-c4d0-83ec-92ad-fb66722c2cbf |
| B | Gemini web | Gemini 3 Pro (the only model name found on the rendered share page; uncertain) | https://share.gemini.google/82hJ0cK03txm |

Replies are copied verbatim from the share pages, with three mechanical changes: em dashes replaced by "-" (project rule), ChatGPT's file-citation markers removed, and headings demoted to fit this file.
Gemini's reply was extracted from the rendered page, so its tables and list formatting are approximate.

## Run A - ChatGPT

### Message 1 reply

##### Answer 1 - 114 words

###### 1. Decision first
**Yes.** The first sentence is a decision:
> “Tôi chọn: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình.”

A judge reading only that sentence knows the chosen problem.

###### 2. Reason
**Present, but not maximally sharp.** The answer gives:
> “Lý do: quy định của Tập đoàn, của công ty, bản cũ và bản nháp gần giống nhau.”

and then the consequence:
> “Câu trả lời theo nhầm văn bản trông giống hệt câu đúng, nên người hỏi làm theo mà không biết mình sai.”

That is a real justification: wrong-document selection is dangerous precisely because the error can look credible.

Weakness: it does not explicitly establish **why this is the single highest-priority problem**, rather than access control, retrieval failure, or outdated data. It shows why the problem matters, but not fully why it wins the forced choice.

###### 3. Coverage
| Sub-question | Coverage | Assessment |
|---|---|---|
| The problem | **Yes** | Clearly identifies uncertainty about which rule applies |
| The user | **Yes** | “nhân sự các công ty thành viên” |
| The outcome they need | **Yes** | Correct unit, allowed document, effective version, source, self-verification |

The main weakness is the user scope:
> “Người dùng là nhân sự các công ty thành viên…”

The brief describes knowledge across **Tập đoàn → Công ty → Phòng ban → Nhóm**, so this silently excludes some possible users/scopes without explaining why.

###### 4. Brevity
**Good.** At 114 words it is comfortably inside the 60–150 recommendation.

Potential cuts:
> “cho chính mình”

is slightly redundant after “nhân sự”.

> “như xin nghỉ phép”

is an example, not necessary.

> “mà không chờ HR”

is useful but somewhat secondary to the core outcome.

Nothing is seriously over-detailed.

###### 5. Clarity for a new reader
Mostly clear. Two phrases could be questioned:

> “từ văn bản họ được xem”

I interpret this as **the answer must be grounded only in documents the employee is authorized to access**, not merely any relevant document in the corpus.

> “theo bản đang có hiệu lực”

I interpret this as **version/status filtering**, not simply the newest file.

Both meanings are understandable, but the first especially could be stated more explicitly because “được xem” can mean technical visibility rather than authorization/applicability.

###### 6. Logic
No major logical error.

One real vulnerability: the answer effectively combines **applicability + authorization + validity**, but does not distinguish them. A document can be visible to someone without actually applying to their unit. The sentence:
> “đúng với đơn vị của họ, từ văn bản họ được xem”

handles both, but the distinction is implicit.

Another vulnerability is the unexplained restriction to:
> “nhân sự các công ty thành viên”

That is a scope choice, but the answer gives no reason for it.

###### 7. PITCH attack
**Strongest interviewer question:**

> “Why is ‘not knowing which regulation applies’ the single most important problem, rather than unauthorized access or inability to retrieve the right document?”

A weak reply would sound like:
> “Vì nếu trả lời sai thì nhân viên sẽ làm sai theo.”

That only repeats the consequence already stated. It does not defend the prioritization.

###### 8. Scores
| Dimension | Score | Reason |
|---|---:|---|
| Decision clarity | **5/5** | The chosen problem is explicit in sentence one |
| Quality of reason | **4/5** | Concrete and relevant, but does not fully defend why this is the #1 problem |
| Brevity | **5/5** | 114 words; little waste |
| Clarity for a new reader | **4/5** | Mostly plain language; authorization/applicability distinction is implicit |
| Fit with scoring criteria | **4/5** | Strong problem framing and sensible priority, but user scope is under-justified |

---

#### Answer 2 - 134 words

###### 1. Decision first
**Yes, but the decision is too abstract.**

> “Tôi làm trước phần quyết định câu trả lời đúng hay sai, vì đó là rủi ro lớn nhất.”

The judge knows the candidate is prioritizing correctness, but **“phần quyết định câu trả lời đúng hay sai” is not a concrete product component**. It sounds like internal shorthand rather than a defined thing.

###### 2. Reason
This is the weakest part of the three answers.

For what gets built first:
> “vì đó là rủi ro lớn nhất.”

That is a reason, but it is close to an assertion. **Why is it the largest risk?** The answer does not demonstrate it.

For what is deliberately not built, there is a reason:
> “chúng chỉ đổi nơi lấy dữ liệu hoặc nơi hiển thị, không đổi việc câu trả lời đúng hay sai.”

This is **too broad and partly wrong**.

Not every omitted component merely changes input/output location. In particular, authorization/integration can directly affect **which information the user is allowed to receive**, which is central to the brief.

###### 3. Coverage
| Sub-question | Coverage | Assessment |
|---|---|---|
| What to build first | **Yes** | Explicitly prioritizes deterministic document-selection logic |
| What deliberately not to build | **Yes** | Five things listed |
| Why build that first | **Weakly yes** | “rủi ro lớn nhất” is asserted rather than convincingly established |
| Why not build the others yet | **Yes, but flawed** | Reason is stated, but overstates the irrelevance of integrations |

The biggest problem is not missing coverage; it is **weak justification**.

###### 4. Brevity
**Reasonably concise, but several details can be compressed.**

The following is somewhat implementation-heavy for a 60–150-word forced decision:

> “Ngày 3: giao diện web để chọn người hỏi và xem kết quả.”

The important decision is prioritization, not UI detail.

This sentence is also too long conceptually:

> “Luật phải đúng mọi ca trước khi thêm AI, để lỗi sau đó chắc chắn do AI.”

It packs in an unrealistic testing guarantee and an attribution claim.

###### 5. Clarity for a new reader
The biggest internal-jargon phrase is:

> “phần quyết định câu trả lời đúng hay sai”

I understand it as **a deterministic policy/rules layer that resolves user + unit + document applicability before generation**.

But a new judge cannot know that from the phrase alone.

Another unclear phrase:

> “Luật phải đúng mọi ca”

I interpret it as **the rule engine should pass all predefined test cases before the LLM is introduced**. “Mọi ca” is ambiguous: every manually known case, every test case, or literally every possible case?

###### 6. Logic
There are **two serious logic issues**.

First:
> “Luật phải đúng mọi ca trước khi thêm AI, để lỗi sau đó chắc chắn do AI.”

“Chắc chắn” is too strong. Even with correct rules, errors can arise from data quality, integration, retrieval, source metadata, prompt construction, or other system components. You cannot isolate all later errors as “AI errors” simply by testing the rules first.

Second:
> “chúng chỉ đổi nơi lấy dữ liệu hoặc nơi hiển thị, không đổi việc câu trả lời đúng hay sai.”

This is the more dangerous claim. **Authentication/authorization integration can change what information the system is permitted to return**, which absolutely affects correctness in this problem.

Not integrating “DOCX/PDF” is defensible for a 3-day MVP, but the stated rationale is not.

###### 7. PITCH attack
**Strongest interviewer question:**

> “You say ‘đăng nhập thật’ and HR-system integration do not affect whether the answer is correct. How is an answer correct if the system gives an employee information they are not allowed to access?”

A weak reply:
> “Em chỉ chưa có thời gian làm phần đó.”

That admits the answer’s stated reasoning was wrong. The issue is not merely time; the candidate claimed those integrations do not affect correctness.

###### 8. Scores
| Dimension | Score | Reason |
|---|---:|---|
| Decision clarity | **4/5** | Priority is clear, but “phần quyết định…” is vague |
| Quality of reason | **2/5** | “Largest risk” is asserted; omission rationale contains a false overgeneralization |
| Brevity | **4/5** | 134 words, but some implementation detail and repetition can go |
| Clarity for a new reader | **3/5** | “phần quyết định” and “mọi ca” sound like internal language |
| Fit with scoring criteria | **3/5** | Strong prioritization instinct, but execution rationale has a meaningful conceptual flaw |

**One replacement sentence that would improve it most:**

> “Tôi làm trước lớp luật xác định tài liệu được phép áp dụng cho từng người hỏi, vì nếu chọn sai tài liệu thì phần AI trả lời tốt đến đâu cũng vẫn cho ra đáp án sai.”

That fixes both the vague “phần quyết định” wording and the weak prioritization rationale.

---

#### Answer 3 - 130 words

###### 1. Decision first
**Yes.**

> “Luật cố định chọn văn bản trước khi AI trả lời; AI không bao giờ tự quyết văn bản nào đúng.”

The decision is immediately understandable: **source selection must happen before generation, using deterministic rules rather than the LLM.**

###### 2. Reason
**Strong.**

The answer gives a particularly good explicit rationale:

> “Lý do: khi chưa ai xác nhận, chọn một văn bản là đoán, và đoán sai thì người hỏi vẫn tin là đúng.”

That is not merely a restatement. It identifies the specific failure mode: **false confidence**.

The only missing piece is a reason for why the proposed HR metadata mechanism is sufficiently trustworthy. The answer assumes the HR annotation is authoritative.

###### 3. Coverage
| Sub-question | Coverage | Assessment |
|---|---|---|
| What system does before answering | **Yes** | Deterministic source-selection layer |
| Different content | **Mostly yes** | Uses replacement / simultaneous-use metadata |
| Different version | **Yes** | Keeps only officially issued + currently effective version |
| What if still ambiguous | **Yes** | Does not choose; escalates to HR |

The main gap is an edge case:

> “hay hai văn bản dùng cùng nhau”

If both are currently valid **and conflict**, saying they “use together” does not actually resolve the contradiction. The answer needs a rule for that case.

###### 4. Brevity
**Good.** 130 words is appropriate.

One piece that may be unnecessarily expansive:

> “Khác đơn vị: chỉ giữ văn bản người hỏi được xem và áp dụng cho đơn vị của họ.”

It introduces a second axis that is relevant to the overall problem, but the actual forced question is specifically about differing content/version. It is defensible, not a major problem.

###### 5. Clarity for a new reader
Two terms sound like internal shorthand:

> “Luật cố định”

I understand this as **deterministic, auditable business rules rather than probabilistic LLM judgment**.

> “văn bản này thay văn bản kia”

I understand this as **explicit supersession metadata**.

Those meanings are inferable, but the first phrase could still be challenged as jargon.

Another potentially ambiguous phrase:

> “đang có hiệu lực hôm nay”

I interpret it as **effective-date/status filtering using the current date**, which is reasonable.

###### 6. Logic
The logic is mostly sound.

One important missing case: if HR marks two documents as:
> “hai văn bản dùng cùng nhau”

but their provisions genuinely conflict, the system still has no deterministic resolution. The response has solved **selection ambiguity**, but not necessarily **semantic contradiction**.

Also:

> “AI không bao giờ tự quyết văn bản nào đúng.”

This is a defensible architectural boundary, but it is an absolute statement. A judge could ask whether the AI may at least detect or flag a conflict. The answer should distinguish **AI cannot authorize the source** from **AI can identify a conflict**.

###### 7. PITCH attack
**Strongest interviewer question:**

> “Suppose HR says two documents are both applicable and should be ‘dùng cùng nhau’, but their rules conflict. Which rule does the user actually follow?”

A weak reply:
> “Khi đó đưa cả hai cho HR xử lý.”

That exposes a gap: the answer claims a design, but the hard conflict case still falls back to humans without saying so explicitly.

###### 8. Scores
| Dimension | Score | Reason |
|---|---:|---|
| Decision clarity | **5/5** | Architectural decision is explicit immediately |
| Quality of reason | **5/5** | Clear rationale based on avoiding false certainty |
| Brevity | **4/5** | 130 words and focused; a little extra scope |
| Clarity for a new reader | **4/5** | Understandable, though “luật cố định” is jargon-ish |
| Fit with scoring criteria | **5/5** | Strong trade-off, safety boundary, and failure handling |

---

#### Overall ranking

###### 3rd - Answer 2
Good prioritization instinct, but it contains the most attackable reasoning, especially:
> “không đổi việc câu trả lời đúng hay sai.”

That statement is too broad for a system whose central requirement includes authorization and context.

###### 2nd - Answer 3
The strongest technical decision and strongest explicit reason. Its weakness is the unresolved case where two simultaneously valid documents conflict.

###### 1st - Answer 1
Best standalone problem framing. It directly answers problem/user/outcome with little wasted text. Its main weakness is that the choice of “nhân sự các công ty thành viên” is not justified and the #1 prioritization argument could be sharper.

##### One change that would improve each answer most

**Answer 1:** Defend the forced prioritization more explicitly, rather than only describing the harm.

**Answer 2:** Replace the vague/overstated reasoning around the rule layer and omitted integrations. This is the answer most worth fixing before submission.

**Answer 3:** Explicitly define what happens when **two currently valid, applicable documents conflict even though HR says both are used**.

Ready for message 2.

### Message 2 reply

##### 1. Contradictions

###### Answer 1
The earlier concern that the answer did not really defend why this is the **single most important problem** is largely resolved by the document.

Answer 1 says:
> “Lý do: quy định của Tập đoàn, của công ty, bản cũ và bản nháp gần giống nhau.”

The document expands this into an explicit prioritization:
> “Loại thứ nhất, để lộ văn bản cho người không được xem, nghiêm trọng nhưng có cách chặn rõ ràng…”  
> “Loại thứ hai là trả lời theo nhầm quy định. Lỗi này khó nhận ra…”

So there is **no contradiction**. The document supplies the missing argument rather than contradicting the answer.

One scope mismatch remains:

Answer 1:
> “Người dùng là nhân sự các công ty thành viên…”

Document:
> “Người dùng chính là nhân sự các công ty thành viên…”

So this is actually consistent.

###### Answer 2
The **decision and build order are consistent** with the document:

Answer 2:
> “Ngày 1: dữ liệu giả lập, luật chọn văn bản cho người hỏi và bộ câu hỏi kiểm thử.”  
> “Ngày 2: AI tìm và trả lời kèm nguồn…”  
> “Ngày 3: giao diện web…”

Document:
> “1. Phần luật và bộ test…”  
> “2. Thêm truy xuất và sinh câu trả lời…”  
> “3. Giao diện tối thiểu…”

However, this statement in Answer 2 is **not consistent with the document's treatment of HR-system integration**:

> “Lý do: chúng chỉ đổi nơi lấy dữ liệu hoặc nơi hiển thị, không đổi việc câu trả lời đúng hay sai.”

The document explicitly says the MVP uses a mock user selector **instead of** the HR system, but the real system must derive the user's unit from HR rather than let the user declare it:
> “Bộ chọn người hỏi giả lập thay cho hệ thống nhân sự; bản thật lấy đơn vị từ hệ thống nhân sự, không để người dùng tự khai.”

That means the HR integration is not merely cosmetic. It determines the identity/unit that feeds the authorization/applicability rules. The **decision not to integrate it in three days is defensible; the stated reason is not**.

There is a second wording problem, not a contradiction:
> “để lỗi sau đó chắc chắn do AI.”

The document itself repeats the same assumption:
> “phải đúng mọi ca trước khi thêm LLM, để lỗi sau đó chỉ có thể là lỗi của AI.”

So this is **supported by the document**, although it is still stronger than I would want in an interview.

###### Answer 3
The answer is strongly consistent with the document.

Answer 3:
> “Luật cố định chọn văn bản trước khi AI trả lời; AI không bao giờ tự quyết văn bản nào đúng.”

Document:
> “luật dựa trên metadata chọn ra những văn bản đúng với người hỏi, rồi AI mới tìm và trả lời…”

And:

Answer 3:
> “Nếu HR chưa ghi, hệ thống không chọn mà trích nguyên văn cả hai và chuyển người hỏi tới HR.”

Document:
> “Khi HR chưa khai báo quan hệ… hệ thống không chọn” and the conflict card shows the two source excerpts and sends the user to HR.

No substantive contradiction.

---

#### 2. Missing essentials

###### Answer 1
The document treats **the distinction between “được xem” and “áp dụng cho mình”** as central:

> “Được xem ≠ áp dụng cho mình…”

Answer 1 does mention both:
> “đúng với đơn vị của họ, từ văn bản họ được xem…”

So I would **not require an addition**. Given the 150-word limit, the omission is acceptable.

What the answer does omit is the **second user**, HR:
> “Người dùng thứ hai là chủ sở hữu văn bản…”

For Question 1, I would still treat this as acceptable because the question asks for **“Người dùng là ai”**, and the main user is answered directly. Adding HR would cost words better spent on the core decision.

###### Answer 2
The document's central design is not merely “rules first”; it is specifically:

> “luật xác định phạm vi tìm kiếm của người hỏi trước, rồi AI mới tìm và trả lời trong phạm vi đó.”

Answer 2's:
> “phần quyết định câu trả lời đúng hay sai”

is therefore too vague. It misses the concrete concept **search-scope construction from metadata**.

**Cut:**  
> “Ngày 3: giao diện web để chọn người hỏi và xem kết quả.”

**Replacement:**  
> “Tôi làm trước lớp luật dựng phạm vi tìm kiếm đúng cho từng người hỏi, vì mọi bước AI sau đó chỉ được hoạt động trong phạm vi này.”

That keeps the answer under 150 words.

###### Answer 3
The document adds an important distinction for conflicting documents: **“dùng thay” vs “bổ sung”**.

Answer 3 covers this in compressed form:
> “văn bản này thay văn bản kia, hay hai văn bản dùng cùng nhau.”

So this is **not missing**.

One genuine missing edge case remains: what if both documents are declared to be used together but **their contents actually conflict**? The document's design calls such a pair a contradiction unless there is a declared “dùng thay” or “bổ sung” relationship.

Given 150 words, I would call this omission **acceptable**, but it is the strongest technical hole left in Q3.

---

#### 3. Overclaims

###### Answer 1
No meaningful overclaim.

###### Answer 2
The risky phrase is:

> “Luật phải đúng mọi ca trước khi thêm AI…”

and especially:

> “để lỗi sau đó chắc chắn do AI.”

The document gives this as its testing philosophy, but it does **not** demonstrate that “mọi ca” literally means every possible real-world case. It says the test set is simulated and explicitly warns:

> “Đạt các mục tiêu này trên một bộ test nhỏ, giả lập chỉ là điều kiện để mở, không phải bằng chứng hệ thống luôn đúng khi dùng thật.”

So in an interview, “mọi ca” could be attacked as meaning **all conceivable cases**, when the document really means all cases in the test suite.

Also:

> “chúng chỉ đổi nơi lấy dữ liệu…”

is an overclaim because the identity source affects the input to the authorization logic.

###### Answer 3
No serious overclaim.

> “AI không bao giờ tự quyết văn bản nào đúng.”

This is an architectural boundary explicitly supported by the document:
> “AI không làm… quyết định… văn bản nào áp dụng cho ai, văn bản nào thắng khi mâu thuẫn…”

So I would keep it.

---

#### 4. Wording mismatches

###### Answer 1
The answer says:

> “theo bản đang có hiệu lực”

The document more precisely distinguishes:
> “Mới nhất ≠ đang có hiệu lực.”

No problem; same concept.

The only slight mismatch is:

> “văn bản họ được xem”

versus the document's more precise pair:
> “được xem” and “áp dụng cho người hỏi.”

The answer contains both ideas, just less explicitly.

###### Answer 2
The largest mismatch is:

> “phần quyết định câu trả lời đúng hay sai”

versus the document's actual architectural term:

> “luật xác định phạm vi tìm kiếm của người hỏi trước”

These are related but **not identical**. The former sounds like a final answer-verdict engine; the latter is a metadata-based filtering layer.

Also:

> “AI tìm và trả lời”

is less precise than the document's:
> “Truy xuất” + “Sinh câu trả lời”

Not fatal, but the document makes a deliberate separation between retrieval and generation.

###### Answer 3
> “Khác đơn vị: chỉ giữ văn bản người hỏi được xem và áp dụng cho đơn vị của họ.”

The document's exact conceptual ordering is:
> “được xem và áp dụng cho người hỏi” followed by “dùng thay.”

The answer compresses this correctly.

> “hai văn bản dùng cùng nhau”

is less precise than the document's explicit metadata relation:
> “Bổ sung (complements).”

A judge will understand it, but “bổ sung” is the cleaner term.

---

#### 5. Changed views from message 1

###### Answer 1 - **Changed: positive**
I previously said the answer did not sufficiently explain why this was the **#1 problem**. After reading the document, that criticism should be reduced.

The document explicitly makes the prioritization argument: leakage is a mandatory safety condition, while answering from the wrong regulation is the selected core problem because the error is harder to detect and can look correct.

So **Answer 1 is stronger than it looked standalone**.

###### Answer 2 - **Changed: no**
The main criticism survives and becomes **more concrete**.

The document confirms that the 3-day order is deliberate, but it also confirms that the eventual real system gets identity/unit information from the HR system.

Therefore the decision is good; the sentence explaining *why* the integration can be skipped is the real flaw.

###### Answer 3 - **Changed: slightly positive**
I previously identified the unresolved “both valid and conflicting” case. The document shows that the candidate has actually designed this general mechanism in detail through the “mâu thuẫn” state, “dùng thay,” and “bổ sung.”

Therefore the concern is now narrower: **Answer 3 itself is adequate, but its 130-word formulation does not expose the full conflict model.**

---

#### 6. Verdict per answer

###### Answer 1 - **Keep as is**
The document validates its problem framing and priority. Its standalone wording is already compact and accurate. There is no document-based reason to force an edit.

###### Answer 2 - **Small edit**
The three-day priority is correct and matches the document exactly. The problem is the sentence claiming omitted integrations merely affect data/display location. That is the one part I would fix before submission.

###### Answer 3 - **Keep as is**
It accurately captures the document's core safety decision: deterministic source selection before AI, explicit handling of supersession/current validity, and no guessing when metadata cannot resolve the conflict.

---

#### 7. Top 3 actions

**1. Fix Answer 2's rationale for not integrating the HR system.**  
Do not say it “does not change correctness.” The document itself says the real system must obtain the employee's unit from HR rather than let the user supply it.

**2. Make Answer 2 name the actual component being built.**  
Replace the vague:
> “phần quyết định câu trả lời đúng hay sai”

with the concrete concept of a **metadata-based rule layer that constructs the search scope**. This aligns the forced answer with the architecture judges will see in the PDF.

**3. Preserve Answer 1 and Answer 3 rather than over-editing them.**  
The PDF materially strengthens both. The biggest remaining risk is not lack of detail; it is introducing extra wording that creates new claims a judge can attack.



---

If you want, I can:

- Summarize this conversation
- Generate a critical review of the candidate's answers
- Create a checklist of criteria for evaluating candidate answers

## Run B - Gemini

### Message 1 reply

###### Answer 1 Review
- Decision first: Yes. The first sentence, "Tôi chọn: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình.", is a definitive decision. A judge knows immediately what problem is prioritized.

- Reason: The reason is present ("Lý do: quy định của Tập đoàn, của công ty, bản cũ và bản nháp gần giống nhau. Câu trả lời theo nhầm văn bản trông giống hệt câu đúng..."). It justifies the decision well by highlighting the specific danger of the AI sounding confident while being contextually wrong. No requested reason is missing.

- Coverage:
- Problem: Covered ("nhân sự không biết chắc quy định nào đang áp dụng...").

- User: Covered ("nhân sự các công ty thành viên").

- Outcome: Covered ("câu trả lời đúng với đơn vị của họ... kèm nguồn").

- Brevity: "khi cần làm một việc theo quy định, như xin nghỉ phép" is conversational filler. "Câu trả lời theo nhầm văn bản trông giống hệt câu đúng, nên người hỏi làm theo mà không biết mình sai" is slightly wordy.

- Clarity for a new reader: "từ văn bản họ được xem" is ambiguous. It could mean "the document they are currently looking at on their screen" or "the document their account has permission to access". I understood it as access permissions, but it lacks precision.

- Logic: The logic holds for corporate structures, but assumes the root cause is user confusion rather than scattered data.

- PITCH attack: "Why is 'the user not knowing which rule applies' the core problem, rather than 'the system lacking structured metadata to map users to rules'? Aren't you blaming the user for a systemic data issue?" A weak reply: "Because users are always confused by HR documents."

- Scores:
- Decision clarity: 5/5. Direct and unmistakable.

- Quality of the reason: 4/5. Strong consequence-based logic, slightly wordy.

- Brevity: 4/5. Minor filler.

- Clarity for a new reader: 4/5. Relies on the ambiguous "được xem".

- Fit with criteria: 5/5. Directly answers the Problem Framing requirement.

###### Answer 2 Review
- Decision first: Yes. "Tôi làm trước phần quyết định câu trả lời đúng hay sai, vì đó là rủi ro lớn nhất." The judge knows the priority is core validation logic over UI or integration.

- Reason: The reason justifies the priority ("vì đó là rủi ro lớn nhất") and also explicitly justifies the exclusions ("chúng chỉ đổi nơi lấy dữ liệu hoặc nơi hiển thị, không đổi việc câu trả lời đúng hay sai").

- Coverage:
- What first: Covered (dummy data, routing rules, AI generation, testing).

- What deliberately not yet: Covered (real logins, HR system sync, chat integration, document parsing).

- Why: Covered for both choices.

- Brevity: The chronological formatting ("Ngày 1", "Ngày 2", "Ngày 3") eats up word count and forces artificial pacing that isn't strictly necessary for a "what and why" question.

- Clarity for a new reader: "phần quyết định câu trả lời đúng hay sai" is imprecise jargon. I understood this to mean the document retrieval and filtering logic (RAG pipeline) that precedes the LLM prompt, but phrasing it as "quyết định đúng hay sai" sounds like an answer key grading system.

- Logic: The claim "Luật phải đúng mọi ca trước khi thêm AI" is naive. Achieving 100% edge-case perfection ("mọi ca") on rule-based logic in one day on mock data is practically impossible and a setup for failure in execution.

- PITCH attack: "You claim you will make the rules 'đúng mọi ca' (correct in all cases) on Day 1. How is that realistically possible in a complex corporate hierarchy within 24 hours?" A weak reply: "I will just write if/else statements for the 5 examples I make up."

- Scores:
- Decision clarity: 4/5. Clear intent, but imprecise phrasing.

- Quality of the reason: 4/5. Execution-focused, but hindered by the naive "mọi ca" claim.

- Brevity: 3/5. Day-by-day diary format adds unnecessary bulk.

- Clarity for a new reader: 4/5. Internal jargon requires translation by the reader.

- Fit with criteria: 4/5. Strong alignment with Execution, but docked for naive timeframe claims.

###### Answer 3 Review
- Decision first: Yes. "Luật cố định chọn văn bản trước khi AI trả lời; AI không bao giờ tự quyết văn bản nào đúng." Immediate architectural decision to use deterministic filtering before generative output.

- Reason: "Lý do: khi chưa ai xác nhận, chọn một văn bản là đoán, và đoán sai thì người hỏi vẫn tin là đúng." This justifies the fallback mechanism (sending to HR) strongly, highlighting the danger of LLM hallucinations in compliance scenarios.

- Coverage:
- System design before answering: Covered (rigid pre-filtering cascade).

- Khác nội dung (different content): Covered (checking HR metadata for "thay văn bản kia" or falling back to citing both).

- Khác phiên bản (different version): Covered ("chỉ giữ bản đã ban hành và đang có hiệu lực hôm nay").

- Brevity: Very tight. No conversational filler, uses a direct conditional structure (Khác phiên bản -> Khác đơn vị -> Nếu vẫn còn -> Nếu HR chưa ghi).

- Clarity for a new reader: "hệ thống làm theo điều HR đã ghi khi đăng văn bản" assumes the existence of specific metadata tags (supersedes/complements). I understood this as looking for dependency metadata, but it assumes HR actually inputs this data.

- Logic: "chỉ giữ bản đã ban hành và đang có hiệu lực hôm nay" completely blocks users from querying historical policies or upcoming drafts. If an employee asks "What was the maternity leave policy last year when I took it?", the system fails.

- PITCH attack: "Your system defaults to sending the user to HR if document metadata is incomplete. Given most companies have messy, legacy data, won't this system just flood HR with support tickets on day one?" A weak reply: "HR just needs to clean all their data before using my product."

- Scores:
- Decision clarity: 5/5. Extremely definitive.

- Quality of the reason: 4/5. Excellent justification for the fallback, but ignores the assumption of perfect metadata.

- Brevity: 5/5. Structurally excellent.

- Clarity for a new reader: 5/5. The step-by-step logic cascade is easy to read.

- Fit with criteria: 5/5. Perfectly answers the trade-off and risk prompt.

###### Overall Synthesis
Ranking from weakest to strongest:
- 3rd (Weakest): Answer 2. The day-by-day structure is filler, and claiming the logic will be "đúng mọi ca" in one day reveals a lack of real-world execution experience.

- 2nd: Answer 1. Solid problem framing, but relies on slightly ambiguous phrasing ("được xem") and is a bit wordy in its justification.

- 1st (Strongest): Answer 3. Excellent structural logic cascade. It directly tackles the AI hallucination risk by enforcing rigid pre-filtering, even if it assumes slightly too much about HR metadata quality.

Highest impact improvements:
- Answer 1: Replace the ambiguous access phrase. Proposed sentence: "Kết quả họ cần là câu trả lời đúng dựa trên quyền truy cập dữ liệu của đơn vị họ, theo bản đang có hiệu lực, kèm trích dẫn nguồn."

- Answer 2: Drop the chronological diary and naive claims to focus purely on the architectural priority. Proposed sentence: "Luật lọc và phân quyền văn bản phải chuẩn xác trước khi đưa vào AI, để đảm bảo sai sót (nếu có) đến từ AI chứ không phải do sai luồng dữ liệu."

- Answer 3: Acknowledge that users might explicitly want historical documents rather than hard-blocking them. Proposed sentence: "Khác phiên bản: mặc định ưu tiên bản đang có hiệu lực, trừ khi người dùng chủ động yêu cầu tra cứu bản cũ hoặc bản nháp."

Ready for message 2.

### Message 2 reply

- Contradictions
There are no structural contradictions. The three short answers are exceptionally faithful summaries of the candidate's document, matching the step order, the metadata logic, and the MVP priorities exactly.

- Missing essentials
In Answer 3, the document treats the "Thẻ mâu thuẫn" (Conflict card) as a central UI mechanism for handling ambiguity (Section 2). Answer 3 describes its function perfectly ("trích nguyên văn cả hai và chuyển người hỏi tới HR") but omits the actual name of the state/card.
Fix: Acceptable omission for brevity, but easily fixed by swapping out "không chọn mà" to make room for the exact term.
Proposed sentence: "Nếu HR chưa ghi, hệ thống hiện thẻ mâu thuẫn, trích nguyên văn cả hai và chuyển tới HR."

- Overclaims
None. In message 1, I flagged Answer 2's claim that rules must be "đúng mọi ca" (correct in all cases) as a naive overclaim. However, the document (Section 5) clearly defines this as a deterministic metadata filter tested against mock data using code scripts, not an AI prediction. For a rule-based unit test, 100% accuracy is standard engineering practice. The answer accurately reflects the document's rigorous test design.

- Wording mismatches
Answer 2 uses "phần quyết định câu trả lời đúng hay sai" to describe what is built first. This sounds like an AI evaluation step. The document uses the much clearer term "luật xác định phạm vi tìm kiếm" (rules to determine search scope). A judge reading Answer 2 alone will misunderstand the architecture; reading both creates a jarring disconnect.
Proposed sentence: "Tôi làm trước phần luật xác định phạm vi tìm kiếm, vì phạm vi sai là rủi ro lớn nhất."

- Changed views

- Answer 2's "đúng mọi ca": I completely retract my criticism from message 1. The document proves the candidate understands the difference between deterministic code (which can and should pass 100% of unit tests) and generative AI (which cannot). The answer is actually very strong.

- Answer 3 blocking historical policies: In message 1, I noted this breaks historical queries (e.g., "What was the policy last year?"). The document (Section 2) explicitly acknowledges this limit: "Vì vậy phiên bản đầu chỉ trả lời về quy định áp dụng cho chính người hỏi". This is a deliberate, highly rational MVP scoping choice to guarantee safety first. My critique of the product's ultimate limit stands, but as an MVP decision, it is flawless.

- Verdict per answer

- Answer 1: Small edit. Update the ambiguous "được xem" to match the document's precise dual-requirement: "từ văn bản họ được xem và áp dụng cho đơn vị của họ".

- Answer 2: Small edit. Replace the vague "quyết định đúng hay sai" with the document's precise architectural term "luật xác định phạm vi tìm kiếm".

- Answer 3: Keep as is (or apply the small edit to include "thẻ mâu thuẫn"). The logic is bulletproof and perfectly distills a complex flowchart into 130 words.

- Top 3 actions

- Fix the terminology mismatch in Answer 2. Change "quyết định câu trả lời đúng hay sai" to "luật xác định phạm vi tìm kiếm" so the judge understands you are building a deterministic metadata filter, not an AI evaluator.

- Clarify the access rule in Answer 1. Change "từ văn bản họ được xem" to "từ văn bản họ được xem và áp dụng cho đơn vị của họ", bridging the critical distinction you made in Section 1 of the document.

- Name the UI state in Answer 3. Introduce the term "thẻ mâu thuẫn" into the text so the judge explicitly sees the connection to your product's UI design.
