# Thinking phase - my answers (round 1)

Raw answers from the thinking-phase workbook (`thinking-workbook.html`, originally `.lavish/thinking-workbook.html`), copied verbatim except two typo fixes ("scopd" -> "scope", "Land" -> "Lan").
Empty fields are marked "(not answered yet)".

## Company 101

- Interviews possible: No, I will rely on public Q&A sources
- Surprised or unclear: (not answered yet)

## Exercise 1 - Question inventory

- Top 5 "would hate to get wrong":
  - Q01 Quy định nghỉ phép năm của tôi như thế nào?
  - Q09 Làm thêm giờ (OT) được tính lương thế nào?
  - Q10 Thưởng KPI và thưởng Tết được tính ra sao?
  - Q12 Lương của đồng nghiệp A là bao nhiêu?
  - Q18 Có được dùng ChatGPT hay công cụ AI với dữ liệu công ty không?
- Pattern: A - HR policy questions are both frequent and costly when wrong, so focus there first
- Tag disagreements: (not answered yet)
- My own questions: (not answered yet)

## Exercise 2 - Users and stakes

- Primary user: B - All employees in subsidiaries
- Combination: B and A, focus on B
- Outcome sentence: answer with cited sources
- Gatekeepers: HR
- Why this user: User B is the most suitable candidate for this project since it enables the same question, different answer. The response must rely on the roles and the different characteristics of all employees. This is a very good, practical, and very close-to-realistic system in production.

## Exercise 3 - Break naive RAG

- Failures that really happen: F1, F2, F3, F4, F5, F6, F7 (F8 left unticked)
- Would a bigger model fix F1, F3, F4: No, a smarter LLM cannot fix it because it relies on external data that the LLM cannot handle or see, like the metadata, the data about the user, and the data about the document itself. So a smarter LLM cannot handle this.
- Worst failure: F2 - Because it can retrieve outdated data, which is very harmful and causes misleading information
- Bonus (Lan asks about GameCo): I think we should not just lie about this. Normally the answer would contain gameco, which is sufficient to understand that it's not applied to Lan. If Lan is very careful, that is sufficient. But if Lan is not that careful and just scans the answer, we need to maybe add a caveat or a line that explains this.

## Exercise 4 - Pre-mortem

| ID | Likelihood | Impact |
|---|---|---|
| R01 | Cao | Cao |
| R02 | Cao | Cao |
| R03 | Cao | Cao |
| R04 | Cao | TB |
| R05 | Cao | Cao |
| R06 | TB | TB |
| R07 | Cao | TB |
| R08 | TB | Cao |
| R09 | TB | Cao |
| R10 | Cao | Cao |
| R11 | TB | TB |
| R12 | Cao | Cao |
| R13 | Cao | Cao |

- Top 3 fix type: technology
- My own failure stories: (not answered yet)

## Exercise 5 - Decision log

| Decision | Choice | Why | Would change my mind |
|---|---|---|---|
| D1 MVP knowledge domain | b: HR + onboarding/IT | (not answered yet) | (not answered yet) |
| D2 When unsure | a: Decline and say who to ask | Option A is the safest. We cannot give a best guess on what is uncertain, especially if it's related to important information about the company. | (not answered yet) |
| D3 Who decides which document wins | a: Rules over metadata | We cannot let the important parts of which documents win to a semantic random around and this should be governed in a deterministic way. | (not answered yet) |
| D4 Self-service or HR copilot | a: Self-service for everyone | I would choose this because it is a good scope for the MVP. | (not answered yet) |
| D5 Interface | a: A web chat page | It should be a web chat page first that mimics the ChatGPT interface. A chatbot inside a complete chat tool is not very suitable right now because we have no idea how the app is used or which tool they use. It gives me more scope and more control, which is not related to the building application itself. So option A is a fit. | (not answered yet) |
| D6 When to catch conflicts | c: Both | (not answered yet) | (not answered yet) |

## Exercise 6 - Define "good"

- Leak tolerance: 0, a release blocker
- System A or B: B
- Applicability accuracy target: 80%
- Max acceptable "please ask HR" rate: 10%
- Latency target: Under 15 s
- Pilot outcomes: % questions resolved without HR; Fewer repeat questions to HR
- Test set method: Generate with AI, then review every case
- Reasoning: I use the access for an internal knowledge base application. Reliability is very important. It can answer fewer questions and be less useful but each of its responses and answers must come with confidence and must be correct so that the people in the company would trust it and it is usable.

## Exercise 7 - Cut scope

| ID | Feature | My call |
|---|---|---|
| X01 | Simulated org and documents with deliberate traps | 3 ngày đầu |
| X02 | Test set: persona x question with expected answers | 3 ngày đầu |
| X03 | Access filter before search | 3 ngày đầu |
| X04 | Validity filter and scope precedence rules | 3 ngày đầu |
| X05 | Answer with citations; decline with "who to ask" | 3 ngày đầu |
| X06 | Persona switcher (fake login) | 3 ngày đầu |
| X07 | Real SSO login | Sau này |
| X08 | Real HR system (HRIS) sync | Sau này |
| X09 | Document admin UI | Sau này |
| X10 | AI suggests metadata when a document is uploaded | Sau này |
| X11 | Conflict check when a document is published | Sau này |
| X12 | Reading scanned PDFs (OCR) | Sau này |
| X13 | Slack / Lark / Teams integration | Không làm |
| X14 | Personal data lookups (remaining leave days) | Không làm |
| X15 | Multi-turn chat with memory | 3 ngày đầu |
| X16 | Analytics dashboard | Không làm |
| X17 | Thumbs up / down feedback button | Sau này |
| X18 | Multiple languages | Không làm |
| X19 | Fine-tuning a model | Không làm |
| X20 | Polished mobile UI | Không làm |

- Why postponing is safe: (not answered yet)

## Exercise 8 - Change scenarios

| ID | Scenario | My call |
|---|---|---|
| S01 | An employee transfers from GameCo to PayCo | (not answered yet) |
| S02 | Two departments merge | (not answered yet) |
| S03 | The group acquires a new company | (not answered yet) |
| S04 | A new leave policy takes effect next month | Data |
| S05 | Someone holds roles in two companies at once (kiêm nhiệm) | Code |
| S06 | Documents move from Google Drive to Lark | Code |
| S07 | Leadership: interns may no longer see process X | Config |
| S08 | The number of documents grows 10x | (not answered yet) |
| S09 | The legal minimum for annual leave changes (hypothetical) | (not answered yet) |
| S10 | User feedback: answers are too long | (not answered yet) |

- Biggest worry: (not answered yet)

---

# Round 2 - decisions after discussion

## My decisions (from chat)

| Tension | My decision |
|---|---|
| Decline rate vs System B | Accept a higher decline rate. Safety over coverage. |
| Who stops the launch after a salary leak | HR. |
| R13 group chat vs web chat | My design has no group chat; I rate risks for my own design. |
| Conflicts at publish time vs MVP | Ask-time only in the 3-day version; publish-time check later. |
| Applicability 80% | I meant 80% of all questions. |
| Outcome sentence | Employees need to get answers based on published policies, without wrong answers or data leaks. |
| Primary user | Narrow "all employees" to: an employee at the moment they must make a decision that a policy governs. |
| Self-service wrong answers | Open, to discuss. |
| Hotel-limit contradiction (same scope, same validity) | Open, to discuss. |
| Include IT in scope | Not sure. |

## Claude drafts for the missing parts

Everything below was drafted by Claude (Claude Code, Opus 5.5) at my request.
I must review each line, rewrite it in my own words, or reject it, and log it in the evidence log.

### Open questions resolved as suggestions

**Self-service: how do we find out when the bot is wrong?**
Suggestion: move X17 into the 3-day MVP as a "Báo sai" (report wrong) button that sends the question, answer and cited sources to the document owner.
Every answer also shows its source and effective date, so the employee can check it in seconds.
Reason: self-service with no feedback loop makes mistakes invisible, and the button costs very little to build.

**Hotel-limit contradiction: who notices it?**
Suggestion: two steps.
1. Metadata alone can flag a *possible* conflict: two active documents, same topic, same scope, overlapping validity dates. This is a deterministic rule.
2. Only then does the LLM compare the two passages on the point being asked and confirm whether they really disagree.
If they disagree, the system does not pick and does not blend: it shows both sources, says they conflict, and notifies the owner.
This means D3 becomes option c ("rules decide; the LLM only detects contradictions and explains").
Reason: rules stay in charge of the decision, and the LLM is used only for reading text, which rules cannot do.

**Include IT?**
Suggestion: D1 = HR policies, plus one exception: the group-wide AI tool usage policy (Q18).
Reason: IT questions rarely depend on who is asking, so they do not show off the core, and they double the documents to simulate in 3 days.
The AI usage policy is the exception because it is group-wide, changes often (a good version test) and matters for data security.

**The 80% target - a conflict to fix.**
If the system declines about 25% of questions (System B), at most 75% of *all* questions can be answered, so 80% of all questions is impossible.
Suggestion: split it into two numbers.
- Applicability accuracy: 95% or more of *answered* questions use the right document and version.
- Decline rate: at most 25% in the MVP, then lower over time with clarifying questions.

**Gatekeepers.**
Your answer: HR.
Suggested addition: IT/security and legal, because a salary leak is a personal-data incident under Luật 91/2025/QH15 (in force since 01/01/2026), and leadership would likely take the stop decision.
Keep HR as the data owner who raises the alarm.

**Outcome sentence (Vietnamese draft from your words).**
"Khi cần ra một quyết định chịu sự điều chỉnh của quy định (xin nghỉ, đăng ký OT, thanh toán công tác phí), nhân sự cần biết chắc quy định nào đang áp dụng cho chính mình để hành động ngay, không phải chờ HR, không dùng nhầm bản cũ và không bao giờ thấy thông tin ngoài quyền của mình."

### Exercise 1 - three extra questions (drafts)

- "Tôi đang thử việc thì đã được nghỉ phép năm chưa?" - applicability by contract type.
- "Tôi chuyển từ GameCo sang PayCo giữa năm thì phép năm tính theo quy định nào?" - transfer, two scopes at once.
- "Quy định WFH mới áp dụng từ ngày nào?" - validity, future effective date.

### Exercise 4 - forced top 3 and fix types (drafts)

| Rank | Risk | Fix type | Why |
|---|---|---|---|
| 1 | R02 wrong answer someone acts on | Technology | Validity and scope rules, citations, decline when unsure |
| 2 | R01 + R08 leak (merged: both end in restricted text reaching the user) | Technology | Access filter before search; deterministic leak tests on every case |
| 3 | R03 stale documents | Both | Technology: review dates and staleness alerts. People: one owner per document who must confirm it is still valid |

Two failure stories of my own (drafts):
- "Dự án thất bại vì tài liệu giả lập quá dễ: demo chạy đúng, nhưng dữ liệu thật có nhiều văn bản trùng chủ đề hơn nên hệ thống trả lời sai ngay tuần đầu."
- "Dự án thất bại vì không ai gắn metadata cho tài liệu cũ: hàng trăm văn bản bị cách ly vì thiếu ngày hiệu lực, nên bot gần như không trả lời được gì."

### Exercise 5 - missing reasons (drafts)

| Decision | Why (draft) | What would change my mind (draft) |
|---|---|---|
| D1 HR policies + AI usage policy | HR questions are frequent, costly when wrong and differ by unit, so they test the core best | If interviews showed most real questions are IT or process questions |
| D2 Decline and say who to ask | A wrong policy answer costs more than a short wait for HR | If the decline rate stays far above 25% in testing; then add clarifying questions |
| D3 Rules decide, LLM only confirms contradictions (option c) | Decisions stay testable; the LLM does only what rules cannot (read text) | If metadata turns out to be too unreliable to drive the rules |
| D4 Self-service, with a "Báo sai" button | Employees get answers immediately; the button makes mistakes visible to owners | If testing shows too many wrong answers on a topic; then route that topic to HR review |
| D5 Web chat page with an answer card | Fastest to build and demo; the company chat tool is unknown | If Appota confirms one chat tool everyone uses; then build the bot there |
| D6 Both, ask-time only in the MVP | Publish-time checks fix the source once; ask-time checks protect against old conflicts | If owners refuse extra steps at publish time; then rely on ask-time checks plus reports |

### Exercise 6 - employee-side measure (draft)

Add: time from question to a usable answer, and the share of answers marked "Báo sai".

### Exercise 7 - changes and reasons (drafts)

- X17 "Báo sai" button: move to the first 3 days (see above).
- X15 multi-turn memory: suggest moving to "later". It does not test the core, and memory that survives a persona switch can leak one persona's documents into another's answer. If you keep it, memory must reset whenever the persona changes.
- X13 chat-tool integration and X14 leave-balance lookups: suggest "later" instead of "won't do". Both are real needs (Q02 is very frequent); they are just not part of the core.
- Why postponing is safe:
  - X07/X08 SSO and HRIS: the persona switcher uses the same interface (who is asking, which unit, contract type), so real systems can replace it without changing the core.
  - X11 publish-time check: the ask-time guard already protects users in the MVP.
  - X14 leave balance: it needs HR system access and a privacy review; the MVP answers the policy and links to the HR system.

### Exercise 8 - remaining scenarios (drafts)

| ID | Call | Reason |
|---|---|---|
| S01 transfer | Data | Identity is read at question time, so access and applicability follow the new unit |
| S02 departments merge | Data + process | Update the org tree; decide who owns the old departments' documents |
| S03 new company | Data | Add an org node, its documents and its access rules |
| S08 10x documents | Infrastructure | Indexing and cost grow; the rules do not change |
| S09 legal minimum changes | Data | The floor lives in a document, not in code |
| S10 answers too long | Config | Change the answer template |

Biggest worry (draft): S05 concurrent roles.
Design decision now: a person has a *list* of unit memberships from day 1, so S05 becomes a data change instead of a code change.

---

# Round 3 - decisions

- I approve all Claude drafts in Round 2, including: gatekeepers HR + IT/security + legal; X15 multi-turn memory moved to "later"; X13 and X14 moved from "won't do" to "later"; the 95% (answered) / 25% (decline) split; D1 HR policies + AI usage policy; "Báo sai" button in the MVP.
- Changed my mind on D3 (hotel-limit contradiction): **back to option a, rules only. No AI in the conflict decision.**
  - Reason: the dangerous error is the AI saying "no conflict" when two documents disagree, and AI can hallucinate.
  - Rule: two active documents with the same topic, same scope and overlapping validity are always treated as a conflict. The system quotes both clauses word for word (no paraphrase), warns the user, and routes to the document owner.
  - False alarms are reduced deterministically: document-type authority (quy chế > quy trình > hướng dẫn) breaks ties, and an owner's decision ("complements" or "replaces") is saved as data so the same flag never returns.
  - Principle for the pitch: AI only where its mistakes are harmless.
  - Would change my mind if: false alarms overwhelm owners in testing; then consider an AI that may only add warnings, never remove them.
