# Independent review of the Mission 1 draft

Reviewer: Claude Opus 5.5 (`claude-opus-5-5`), running as a coding agent in a fresh session with no conversation history.
Date: 2026-10-07.
Prompt: `docs/mission1/review_prompt.md`, executed in order (Part A written and saved before the draft was opened).

## Disclosure and assumptions

- Files read for Part A: `mission1_brief.md`, `rules.md`, and `ai_policies.md`.
  `ai_policies.md` was not on the attachment list, but it is an official competition document and is needed to judge the evidence log in Part E.
- Files read for Parts B-G: `build/mission1_draft.pdf` (rendered from `document.md`), `answers.md`, `evidence_log.md`.
- Files not read: `playbook.md`, `criteria.md`, `thinking/`.
- Anchoring caveat: the session auto-loads the project `AGENTS.md`, which states a "core thesis" (a relevant document is not necessarily allowed, in force, or applicable) and a working rule (deterministic rules decide access, validity and precedence; the LLM only interprets language).
  So this review is not fully independent of the candidate's framing on those two points.
  A reviewer from a different model family with no project files would be a stronger independence check.
- Added after reading the evidence log: the draft, the answers and the review prompt were all produced with Claude Opus 5.5, the same model that wrote this review.
  Same-model review shares blind spots with the drafter, so this does not satisfy the evidence log's "chạy prompt trên AI khác" item.
  Run the same prompt on a different model family (for example GPT or Gemini) as well, and compare.
- Legal facts in Part B5 were checked with web search during this review (sources named there).
- Vietnamese phrases in Part A are hypothetical examples of common mistakes, not quotes from the draft.
  From Part B on, quoted Vietnamese is taken from the draft, the answers or the evidence log; table cells are sometimes joined with their column label.
- Assumption: the 40/35/25 criteria apply to the whole submission (PDF + 3 answers + evidence log), with the PDF carrying most of the weight.

---

## Part A - The standard (written before reading the draft)

### A1. What a top score looks like per criterion

**Khung vấn đề (40%) - "bạn có hiểu đúng vấn đề không?"**

A top submission shows that the problem is not search, it is correctness relative to the asker.
It names the distinct ways a "relevant" answer can still be wrong for this person, and keeps them separate: the asker may not be allowed to see the source, the source may not apply to the asker's unit or employee type, or the source may not be the version in force on the relevant date.
It names who suffers from each failure and what each failure costs, and it notices that the costs are asymmetric (a leaked confidential document or a confident outdated answer is worse than "I don't know, ask HR").
It ranks the problems and commits to one, with a reason.
It separates facts from the brief, assumptions the candidate made, and things that would need real-user validation.

What a no-code submission can show here: concrete persona x question x date scenarios with the expected correct answer and the tempting wrong answer, a small taxonomy of failure types, and an explicit list of assumptions.

**Thực thi (35%) - "giải pháp có chạy thật không?"**

Without code, "chạy thật" can only be argued, so the evidence must be concrete enough that a judge can mentally execute it.
What convinces a judge, in order of strength:

1. A worked trace of one real question through the whole pipeline, with the actual intermediate data: the asker's profile, the candidate documents with their metadata, which ones each filter removed and why, how a conflict was resolved, and the final answer with its citation and "applies to you because".
2. A sample of the simulated data: the metadata schema with a few real rows, designed so it contains the hard cases (same question across units, superseded version, future-effective version, restricted document, cross-level conflict, no document).
3. A test matrix: specific questions x personas x dates with expected outcomes, including the cases where the correct output is a refusal or an escalation, and pass/fail gates.
4. A build plan that names concrete, known-to-work components (for example metadata-filtered retrieval in a vector store, a relational table for document metadata, a rules function for precedence) and a scope that fits Mission 2.
5. The non-happy paths: what the user actually sees when access is denied, when nothing applies, when two documents conflict, when the question is ambiguous.
6. Operational reality: where documents and their metadata come from, who keeps them current, and what happens on a new version or a reorganisation.

A submission that only shows a generic architecture diagram does not earn this criterion, because every RAG diagram looks the same and none of them shows that the hard part works.

**Chất lượng quyết định (25%) - "lý do chọn A thay vì B có thuyết phục không?"**

A top submission makes 2-4 consequential choices, each with a real alternative B, the criterion used to choose, what A costs, and the condition under which B would win.
The choices are traceable to the problem framing (for example, "because a wrong-but-confident answer costs more than an abstention, I choose ...").
It also shows deliberate non-choices: what is consciously not built, and why that is safe.
The rules call this criterion "lựa chọn bắt buộc", which links it directly to the 3 Forced Decision answers.

### A2. Phrases that signal what the judges value

| Quote | What it implies |
|---|---|
| "tìm đúng tri thức, trong đúng bối cảnh và đúng phạm vi được phép sử dụng" | Three separate kinds of "đúng": the content, the context of the asker, and the permitted scope. Correctness is multi-dimensional. |
| "Thách thức không chỉ là tìm được tài liệu liên quan" | Relevance-only RAG is explicitly named as the naive answer. A submission that stops at "good retrieval" has missed the brief. |
| "ai đang hỏi, họ thuộc đơn vị nào, được phép tiếp cận thông tin gì và tài liệu nào đang có hiệu lực" | Four inputs: identity, unit membership, authorization, validity. The asker's context is an input to retrieval, not an afterthought. |
| "cùng câu hỏi ... hai nhân sự thuộc hai đơn vị khác nhau có thể cần nhận câu trả lời khác nhau" | Personalization by unit. Note "có thể": sometimes the answer is the same (a group-wide rule), so the system must know when the difference matters. Note also "của tôi" in the example question: the system must resolve "me". |
| "Tập đoàn → Công ty → Phòng ban → Nhóm" | A hierarchy, which implies inheritance and override. The candidate must define precedence. |
| "nhiều loại tài liệu và phiên bản khác nhau" | Versioning and document types (policy, procedure, guideline, announcement, FAQ) are part of the problem. |
| "tự xây dựng dữ liệu giả lập phù hợp" | "phù hợp" means the dataset must be designed to exercise the hard cases. Data design is part of the work, not a chore. |
| "Hiểu đúng vấn đề, biết ưu tiên và thiết kế hướng giải quyết" | Prioritization is explicitly valued. |
| "vấn đề quan trọng nhất ... cách bạn sẽ kiểm chứng nó" | Commit to one problem and say how it will be validated. |
| "Không kỳ vọng một tài liệu hoàn hảo. Hãy ưu tiên chất lượng tư duy, khả năng lựa chọn và lý do đằng sau những quyết định của bạn" | Depth of reasoning beats coverage. Choosing means saying no. |
| "chủ động chưa làm những gì" | Deliberate cuts are scored, not just features. |
| "Trả lời ngắn gọn, rõ quyết định và lý do. Khuyến nghị 60–150 từ" | Decision first, reason second, nothing else. |
| "tiếp tục hoàn thiện khi thực tế thay đổi" | Mission 3 will change reality (new version, reorg, new unit, new permission rule). A design where change is data or configuration, not code, is favoured. |
| Rules: "một giải pháp chưa hoàn hảo nhưng bạn hiểu tường tận hơn là một giải pháp hoàn hảo mà bạn không thể giải thích. Vòng PITCH sẽ lộ ra" | Every claim must be defensible live. Breadth the candidate cannot defend is a liability. |
| Rules: "Không có tiêu chí ẩn" | Page budget should follow 40/35/25. |
| AI policy: "Ảo giác AI rõ ràng mà không xác minh = trượt tiêu chí đó" | Any unverified fact (law articles, numbers) can fail a whole criterion. Fewer, verified facts beat many unverified ones. |

### A3. What an excellent answer looks like per section

**1. Vấn đề & người dùng**

Excellent:

- A problem statement framed as the user's outcome, not as a solution: the employee needs an answer that applies to them, that they are allowed to rely on, and that is current, with a way to check it.
- Users segmented by job, not by job title, using jobs-to-be-done framing **[Practice]**: an employee asking about their own entitlement, a new hire who does not yet know which rules apply, a manager applying a rule to their team, and the document owner (HR, Legal, unit admin) who must publish and maintain knowledge and is hurt by repetitive questions and by leaks.
- The current workaround and its cost (ask HR on chat, search a shared drive, ask a colleague, read an old copy).
- A ranking of the problems and one chosen as most important, with the reason.
- Explicit assumptions, since there is no user research, plus how the riskiest one would be tested (assumption mapping, as in Bland and Osterwalder, *Testing Business Ideas*, 2019) **[Practice]**.

Common mistakes:

- Stating the solution as the problem ("cần một chatbot RAG").
- Generic personas whose needs do not differ.
- Invented statistics about time spent searching, or real statistics from other companies presented as if they applied to Appota.
- Forgetting the document owner as a user, even though the system fails without them.
- Ignoring "của tôi", that is, never saying how the system knows who "me" is.

**2. Giải pháp & luồng hoạt động**

Excellent:

- One main flow, end to end, in which the asker's context is resolved first from a trusted source, then permission and validity are applied before or during retrieval, then applicability and precedence are resolved, then the answer is written only from what survived, with a citation, the version, the effective date and why it applies to this person.
- The non-happy paths are drawn, not mentioned: no access, nothing applies, conflict that rules cannot resolve, ambiguous question that needs a clarifying question.
- A second, smaller flow for how documents enter the system with metadata and how a new version supersedes an old one.

Common mistakes:

- A generic "embed → vector DB → LLM" diagram with a "check permission" box that is never explained.
- Enforcing permission in the prompt ("do not reveal X") or filtering after top-k retrieval, which both leaks and loses recall.
  The security trimming and metadata-filtering practice in enterprise search, and the OWASP Top 10 for LLM Applications (2025) entries on Sensitive Information Disclosure and on Vector and Embedding Weaknesses, all point to enforcing access before content reaches the model **[Practice]**.
- No ingestion or maintenance flow, so the design silently assumes perfect metadata.
- Feature sprawl (Slack bot, dashboard, analytics, multi-agent) that does not serve the chosen problem.

**3. AI, dữ liệu & con người**

Excellent:

- A clear division of labour.
  AI interprets the question, asks a clarifying question, and writes a grounded answer from permitted, valid, applicable passages.
  AI does not decide who may see what, which version is in force, which level overrides which, or compute entitlements from a rule table.
  Those are deterministic, testable functions.
- AI does not answer from its own general knowledge (for example general labour law) when the question is about an internal rule, or it labels that clearly.
- Data: a trusted employee directory as the source of the asker's attributes, a document store with a defined metadata schema (scope, audience, classification, effective dates, version, supersedes, owner), and a simulated dataset deliberately seeded with hard cases.
- Access model chosen with a reason: unit + role + classification is closer to attribute-based access control (NIST SP 800-162, 2014) than to pure role-based access control **[Practice]**.
- People: document owners who set and approve metadata at publish time, HR or the owner as the escalation target, and a feedback loop where a reported wrong answer reaches the owner.
  Humans are placed at exceptions, not on every answer.

Common mistakes:

- "AI understands permissions" or "the LLM picks the latest version".
- Taking the asker's unit from what they type, which anyone can spoof.
- A data section that lists file formats instead of a schema.
- No named owner for metadata, so the system decays.
- Human review of every answer, which does not scale and defeats the product.

**4. Quyết định & rủi ro**

Excellent:

- 2-4 decisions in full A vs B form (see A4).
- Risks found with a pre-mortem (Klein, "Performing a Project Premortem", *Harvard Business Review*, 2007) **[Practice]**: "it is six months later and the assistant failed; why?"
- Risks specific to this problem, each with a mechanism, an impact, a mitigation and a detection signal: leakage of restricted content, a confident outdated answer, a correct rule applied to the wrong unit, the model blending two conflicting rules into one invented rule, missing or wrong metadata at ingest, identity edge cases (transfer, two units, probation, intern, contractor), instructions hidden inside documents (prompt injection), over-trust, and non-adoption.

Common mistakes:

- Generic risks ("AI có thể ảo giác", "bảo mật dữ liệu") with no mechanism.
- Fake decisions (see A4).
- Tool choices presented as decisions ("chọn Python").
- No cost stated for the chosen option.

**5. Kiểm chứng & MVP**

Excellent:

- Success defined by measurable checks tied to the failures in section 1, run on a golden test set of question x persona x date cases: zero access violations as a hard gate, correct version, correct applicability, correct abstention or escalation, correct citation, and only then answer quality.
- The test set is built from the simulated data and covers each hard case at least once, plus a few adversarial attempts to extract restricted content indirectly.
- A clear statement of which checks are deterministic and which need human or LLM-judged scoring (for example the faithfulness and context-precision ideas in RAGAS, Es et al., 2023) **[Practice]**.
- An MVP built around the riskiest assumption first **[Practice]**, with an explicit "not doing" list (real SSO, live connectors to Drive or SharePoint, admin UI, analytics, fine-tuning) and the reason each cut is safe.
- What would be measured with real users later (escalation rate, deflected HR questions, reported wrong answers), clearly marked as not measurable in the competition.

Common mistakes:

- "Độ chính xác > 90%" with no definition, no test set, and no way to measure it in Mission 2.
- User-satisfaction targets that cannot be measured.
- An MVP that is the full product.
- A test plan that uses one persona, which cannot detect the core failure (same question, different unit).

### A4. What makes "A instead of B" convincing, and what makes it fake

Convincing:

- B is what a competent person would actually choose, ideally the default or naive approach (for example "let the LLM read everything and decide").
- The choice criterion is stated and comes from the problem framing (for example the asymmetric cost of errors).
- A's cost is named honestly: lower recall, more "I don't know" answers, the burden of maintaining metadata, latency.
- A reversal condition says when B would win (for example "if documents arrive without metadata at scale, LLM-assisted tagging at ingest becomes necessary").
- Ideally the same scenario is run through A and B to show where they differ.

Fake:

- B is a strawman nobody would choose.
- A dominates B on every axis, so nothing was given up.
- The "decision" is a value statement ("ưu tiên an toàn thay vì rủi ro").
- The decision does not change what gets built.
- The choice was forced by the brief (for example "use simulated data") and presented as the candidate's own.
- Tool choices with no stakes.

### A5. Non-obvious parts of this problem

A strong candidate should notice most of these; a weak one will miss them.

1. **Access, applicability and validity are three different filters.**
   A PayCo employee may be allowed to read GameCo's leave policy, but it does not apply to them.
   A new policy may apply to them but not be in force yet.
   A policy may be in force and applicable but restricted (for example a salary band).
   Merging them into "permission" produces wrong answers that look correct.
2. **Precedence is not simply "most specific wins".**
   A lower level may legitimately add to a higher rule (more leave days), or may contradict it by mistake (a stale local copy), and some higher rules are floors that lower levels cannot go below (including the legal floor).
   The relationship needs to be declared in metadata (supersedes, overrides, supplements), not inferred by the model, and an unresolved conflict should be surfaced or escalated, never blended.
3. **"In force" depends on a date, and not always today.**
   A question about a past expense claim may fall under the old version, and a question about leave next quarter may fall under a version that has been approved but is not effective yet.
   Effective date, approval date and publication date are different fields.
4. **Leakage happens through the model and through existence.**
   If a restricted passage reaches the prompt, it can leak no matter what the prompt says.
   Even a refusal like "có tài liệu về việc này nhưng bạn không có quyền" reveals that the document exists.
   Answers built from several permitted documents can still reveal something sensitive by aggregation.
5. **Identity is the root of everything.**
   Unit membership must come from a trusted directory, not from the conversation.
   Edge cases: transfers between units, people in two units, managers who may see team-level documents, interns, probation staff, contractors, and cross-company project teams.
6. **Applicability depends on more than the unit.**
   Employee type, seniority, location and level change the answer.
   An entitlement that depends on seniority must be computed deterministically, not by LLM arithmetic.
7. **Metadata quality is the real bottleneck, not the model.**
   Real documents rarely carry clean scope and effective-date fields.
   Simulated data hides this, so a strong candidate says so and designs the publish step to require those fields with owner approval.
8. **"I don't know, ask X" is a correct answer.**
   Abstention and routing to the right owner are features, and the evaluation must reward them.
   So is a clarifying question when "nghỉ phép" could mean annual leave, sick leave or unpaid leave.
9. **Trust needs a visible reason.**
   "Áp dụng cho bạn vì bạn thuộc ..., nguồn ..., phiên bản ..., hiệu lực từ ..." lets the user and the owner check the answer, and makes errors reportable.
10. **Change over time is coming (Mission 3).**
    Reorganisations, new versions and new units should be data changes.
    Cached answers and stale indexes become wrong when a version changes.
11. **Classification and scope are different fields.**
    Scope says who a document applies to; classification says who may read it.
    They often get conflated.
12. **The evaluation needs the persona and date dimensions.**
    A test set where every question is asked by one user cannot detect the core failure.

---

## Part B - Verdict on the current draft

### Testing the candidate's diagnosis

The diagnosis: "the draft dumps a lot of information but does not deep dive into anything and lacks good reasoning."
It is half right.

- **Right about depth.**
  Nothing in the draft is shown step by step, not even the central mechanism.
  Sections 3 and 4 are lists (9 decisions with a one-line reason each, 6 risks, 4 human roles) where every item is asserted and none is worked through.
- **Wrong about "dumps information".**
  Section 1 is tight, and most individual ideas in the draft are correct, some of them sharp.
  The problem is not too much content.
  It is that conclusions are stated without showing the work.
- **What the diagnosis misses.**
  The rule that decides which document applies breaks as soon as it is run on the draft's own examples (B3).
  That is more serious than "lacks good reasoning": it is a correctness bug in the core design, and a judge who traces one example will find it.

So the redraft should not be "cut everything and go deeper everywhere".
It should keep the thesis, demonstrate the mechanism on one example, fix the mechanism where the demonstration breaks, and argue three decisions properly.

### B1. Section by section

| Section | Score | Justification |
|---|---|---|
| 1. Vấn đề & người dùng | 7/10 | The sharpest part of the draft, with a correct and non-obvious thesis, but it asserts the cost and the users instead of showing them, and two of five persona rows have no actual answer. |
| 2. Giải pháp & luồng | 5/10 | The shape is right, but the resolution rule at the heart of the product fails on the draft's own examples, and no question is traced through it. |
| 3. AI, dữ liệu & con người | 6/10 | A clear AI/no-AI split and good human roles, but the "AI only handles language" boundary is overstated, the access rule is missing, and the data has no example row. |
| 4. Quyết định & rủi ro | 4/10 | Nine one-line decisions, about half of them fake or low-stakes, none saying when B would win, and the best decision idea is hidden in the last risk row. |
| 5. Kiểm chứng & MVP | 6/10 | The right evaluation idea with two excellent mechanisms, but there is no test set to look at, no date dimension, and the thresholds have no reasons. |

#### 1. Vấn đề & người dùng - 7/10

**Keep:**

- "Nhân sự không thiếu tài liệu. Họ thiếu một câu trả lời đáng tin, đúng với chính họ, tại thời điểm hiện tại." **[Opinion]**
  An outcome-first framing, not a solution-first one.
- "Câu hỏi 'Quy định nghỉ phép của tôi như thế nào?' thực chất chứa bốn câu hỏi" and the four checks. **[Brief]**
  It maps one-to-one onto "ai đang hỏi, họ thuộc đơn vị nào, được phép tiếp cận thông tin gì và tài liệu nào đang có hiệu lực".
- "Vì sao khó: văn bản nguy hiểm nhất là văn bản giống nhất." **[Opinion]**
  The best single insight in the draft: non-obvious, specific to this problem, and testable.
- "Được xem ≠ được áp dụng" and "Mới nhất ≠ đang hiệu lực". **[Opinion]**
  These are exactly the distinctions a weak candidate merges.
- The persona table idea, including the "Điều được kiểm tra" column. **[Brief]**
  It turns the brief's own example into a test.
- "Sản phẩm chỉ sống được nếu HR tin câu trả lời và bảo mật đồng ý cho chạy." **[Opinion]**
  It names the gatekeepers, which students usually miss.
- "Người dùng chính: nhân sự công ty thành viên, vào lúc cần ra một quyết định do quy định điều chỉnh." **[Practice]**
  A user defined by situation, in the jobs-to-be-done style, not by job title.

**Deepen:**

- "Chatbot RAG thông thường sẽ gộp chúng thành một câu trả lời tự tin nhưng sai." **[Opinion]**
  Asserted, never shown.
  Show what a naive system retrieves for Minh's question and what it would say.
  This is the claim the whole document rests on, so it deserves the evidence.
- "Một mô hình lớn hơn cũng không sửa được, vì thông tin còn thiếu nằm ngoài câu chữ" and "Chỉ metadata phân biệt được các văn bản này." **[Opinion]**
  Half true.
  Who is asking is outside the text, but scope and effective date are often written in the document header.
  The stronger argument is that in-text signals are inconsistent and not enforceable (an old version never says it was superseded), so they must be lifted into structured fields once and confirmed by an owner.
  A judge can break the current wording with one counterexample.
- "Kết quả họ cần" mixes the outcome with product features. **[Practice]**
  The outcome is the decision done correctly the first time, without waiting for HR; the citation and version are how the product earns that.
- The cost asymmetry (a confident wrong answer costs more than a referral to HR) only appears in Section 4 as "Trả lời sai quy định đắt hơn chờ HR". **[Opinion]**
  It is a premise of the problem, so it belongs here, with who pays for each kind of error.
- The Hà and An rows: "Theo quy định thử việc của PayCo" and "Theo quy chế chương trình thực tập, không phải quy chế nhân viên". **[Opinion]**
  These point at a document instead of giving the answer, so they don't test anything.
  Give concrete simulated answers, or drop the rows.

**Cut:**

- The Law 91/2025 parenthetical as written, "một lần lộ dữ liệu lương là sự cố dữ liệu cá nhân theo Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15". **[Opinion]**
  The restricted example in the table is "Khung lương GameCo", a salary band, which identifies no one and is not personal data (see B5).
  Either change the example to individual salary data or drop the legal reference.
- Keep the legal-floor sentence only if the precedence model handles floors correctly (B3); otherwise it invites the hardest PITCH question.

**Missing:**

- The knowledge owner as a user with their own job: publish once, stop answering the same question, never be blamed for a leak. **[Practice]**
  The draft lists HR as "Bên kiểm soát" but not as someone the product must serve.
- The current workaround and its cost (ask HR in chat, search a shared drive, ask a colleague, use an old copy). **[Brief]**
  "Vấn đề thực sự là gì?" needs a baseline.
- A ranking: why "not knowing which rule applies" beats the obvious alternatives (leakage, missing documents, knowledge that only lives in chat). **[Brief]**
  The brief asks for "vấn đề quan trọng nhất", which implies a comparison.
- An assumptions list beyond SSO/HRIS, with the riskiest one marked, for example that documents can be given reliable scope and effective-date metadata, or that most high-stakes questions are about formal policies. **[Practice]**
- A scope note. **[Brief]**
  "Tri thức" and "nhiều loại tài liệu" in the brief are broader than HR policy.
  Say what kinds of knowledge are excluded, and whether the effective-date model even applies to procedures and technical guides.
- The as-of date in the persona table. **[Opinion]**
  The correct answer depends on the date, and no date is stated.

#### 2. Giải pháp & luồng hoạt động - 5/10

**Keep:**

- "lọc quyền trước, xác định văn bản đang hiệu lực và áp dụng đúng người, rồi mới để AI diễn giải kèm trích dẫn" **[Practice]**
- "Bước 1, 3, 4 là luật xác định, không dùng AI." as a principle, but see Deepen. **[Opinion]**
- The answer card, especially "Bạn đang hỏi với tư cách: ..." and "Sắp thay đổi: v3 có hiệu lực từ 01/01/2027." **[Opinion]**
  Showing the asker's context makes a wrong identity visible to the user.
- "Khi Lan (HR Tập đoàn) hỏi về phép năm của GameCo, hệ thống trả lời theo quy chế GameCo vì Lan được xem, nhưng ghi rõ 'quy định này không áp dụng cho bạn'." **[Opinion]**
  A concrete demonstration that access and applicability differ.
- "Quyết định của chủ sở hữu ... được lưu thành dữ liệu, nên cùng một cảnh báo không lặp lại." **[Opinion]**
- "Kiểm tra lúc đăng sửa tận gốc một lần; kiểm tra lúc hỏi bảo vệ người dùng khỏi các mâu thuẫn còn sót." **[Opinion]**
- "Thiết kế cho thay đổi": reorganisations and new versions are data changes. **[Brief]**
  It answers "tiếp tục hoàn thiện khi thực tế thay đổi" directly.

**Deepen:**

- The precedence list. **[Opinion]**
  Rule (1), "quy định cấp trên được đánh dấu bắt buộc, ví dụ mức sàn pháp lý", is evaluated first, so the 12-day floor would beat GameCo's 14 days.
  A floor does not win; it constrains.
  The model needs explicit relations between documents (for example: replaces, overrides, adds to, sets a minimum) and an evaluation order for each, not one ranking.
- Composition. **[Opinion]**
  Lan's answer, "13 ngày: 12 theo quy chế Tập đoàn + 1 ngày thâm niên", combines two rules and a calculation.
  The flow picks one winning document and hands it to AI, so who computes 12 + 1?
  If the LLM does, the "luật xác định" claim fails; if code does, the flow is missing a step.
- "Còn hòa ... cùng chủ đề". **[Opinion]**
  What decides that two passages share a topic?
  If it is embeddings or the LLM, step 4 is not purely deterministic.
  If it is a topic key assigned at publish time, say so and show the taxonomy.
  This is the hidden AI judgment in the design.
- Granularity. **[Opinion]**
  A GameCo policy may override only the annual-leave clause and inherit sick leave from the group.
  Precedence has to work per topic or clause, not per document.
- Step order. **[Opinion]**
  "3. Lọc hiệu lực" comes after "2. Tìm kiếm", which contradicts the Section 1 insight.
  If superseded and draft versions are near-identical, they can fill the top-k, the valid version is never retrieved, and the system refuses although the answer exists.
  Validity (and company-level applicability) should be a pre-filter, or retrieval should only identify the topic and selection should be deterministic.
- "Mỗi nhân sự có danh sách đơn vị trực thuộc ngay từ đầu, nên trường hợp kiêm nhiệm hai công ty là thay đổi dữ liệu, không phải viết lại hệ thống." **[Opinion]**
  Storing two units is data.
  Deciding which company's leave rule applies to someone employed by both is logic, and the precedence list has no rule for two applicable documents at the same level from different companies.

**Cut:**

- "Luồng đăng tài liệu (giai đoạn sau MVP)" can shrink to one line. **[Opinion]**
  It is post-MVP, and the space is needed for the trace.

**Missing:**

- A worked trace of one question with the candidate documents and what each step removes (C3, artifact 1). **[Practice]**
- What the user sees on the other paths: refusal, unresolved conflict, and "nothing specific applies to you". **[Opinion]**
  The diagram draws the branches but only one card is shown.
- A branch for "documents found, but none survives steps 3-4", for example only a draft exists or only another company's rule. **[Opinion]**
  The diagram has "Không có văn bản" only after step 2.
- Ambiguous questions: "nghỉ phép" can mean annual, sick or unpaid leave. **[Opinion]**
  Multi-turn is cut, so say what v1 does instead.
- The access rule itself. **[Opinion]**
  Metadata has a "quyền truy cập" field, but the policy is never stated (for example: everyone reads group and own-company documents, HR roles read all HR policies, restricted documents list roles).
- The retrieval mechanism (semantic, keyword, hybrid, or topic routing), in one line with a reason. **[Opinion]**

One layout point, because it is the main figure: the flow diagram renders at roughly 6-pt text in the PDF and is hard to read on paper.

#### 3. AI, dữ liệu & con người - 6/10

**Keep:**

- The "AI làm / AI không làm" table. **[Practice]**
- "Nếu AI hiểu sai câu hỏi, bộ lọc quyền vẫn nằm ngoài AI nên không thể gây rò rỉ." **[Practice]**
  The containment argument: correct and important.
- "Mọi câu AI viết đều kèm trích nguyên văn điều khoản để người dùng tự đối chiếu." **[Opinion]**
- The metadata field list, "phạm vi, đối tượng áp dụng, quyền truy cập, loại văn bản, phiên bản, trạng thái, ngày hiệu lực, văn bản thay thế, có được ghi đè không, chủ sở hữu". **[Opinion]**
  It keeps applicability and access as separate fields, which most designs conflate.
- "IT/bảo mật: quản lý quyền từ HRIS, không cấp quyền thủ công trong bot." **[Practice]**
  One source of truth for permissions.
- "Gợi ý metadata khi đăng tài liệu, để chủ sở hữu xác nhận". **[Opinion]**
  The right place for AI: a suggestion behind a human gate.

**Deepen:**

- "Lý do chia như vậy: AI có thể ảo giác" is the generic reason. **[Opinion]**
  The specific one: access, validity and precedence must be reproducible, auditable, and testable to 100% on known cases, and their errors are the expensive ones.
- "Nhận biết câu hỏi về bản thân hay về đơn vị khác" sits under "AI làm", but it decides whose rule is applied, so it affects correctness. **[Opinion]**
  The honest boundary is stronger: AI errors can cause a wrong-applicability answer (made visible by "Bạn đang hỏi với tư cách" and the citation), but never a leak.
- "Nhân sự: bấm 'Báo sai'". **[Opinion]**
  Where does the report go, who must respond, and how fast?
  Without an owner and a response time, the button changes nothing.

**Cut:**

- "Cây tổ chức: Tập đoàn → Công ty → Phòng ban → Nhóm." restates the brief. **[Opinion]**

**Missing:**

- A sample of the simulated data: 4-6 metadata rows covering a superseded version, a future version, a restricted document, and a cross-level pair. **[Brief]**
  "tự xây dựng dữ liệu giả lập phù hợp" is part of the task, and a field list does not show it.
- The dataset size, and how it was designed to cover each hard case. **[Opinion]**
- Fields the logic needs but the list lacks: a topic key, the relation to other documents (replaces, overrides, adds to, sets a minimum), an end date, and whether a future version may be shown. **[Opinion]**
- The metadata backfill problem: real documents arrive without tags, so who tags them, how long it takes, and what the system refuses meanwhile. **[Opinion]**
- The model and stack, even if tentative, with one reason each. **[Opinion]**
  "Chạy thật" is hard to believe when no component is named.

#### 4. Quyết định & rủi ro - 4/10

**Keep:**

- "LLM không thể lộ thứ nó không thấy." **[Practice]**
- "Trả lời sai quy định đắt hơn chờ HR. Đổi lại: tỷ lệ từ chối cao hơn". **[Opinion]**
  The right structure (reason plus cost); it needs the argument (B2).
- "Nếu vẫn quá nhiều, cân nhắc cho AI **thêm** cảnh báo, không bao giờ **gỡ** cảnh báo". **[Opinion]**
  The strongest decision idea in the draft: AI gets one-sided authority, it may raise a flag but never clear one.
  It belongs in the main conflict decision, not in the last risk row.
- Risk 2 with existence leakage, "qua tên văn bản khi từ chối", and "test rò rỉ tự động là điều kiện phát hành". **[Practice]**
- Risk 3, "Trả lời sai dù hệ thống đúng ... Đây là việc của con người, công nghệ chỉ nhắc". **[Opinion]**
  Honest about what technology cannot fix.

**Deepen:**

- Every real decision needs B's actual strengths, A's specific cost, and the condition under which B would win (A4). **[Practice]**
- The risk table has mitigations only. **[Practice]**
  Add likelihood, a ranking, and a detection signal for each risk (how would you know it is happening?).
  A pre-mortem framing makes this natural.
- "Văn bản chứa lệnh chèn vào ... Hậu quả: Rò rỉ". **[Practice]**
  With pre-filtering, an injected instruction cannot reveal text that is not in the context, so the realistic consequence is a manipulated answer.
  "văn bản chỉ được coi là dữ liệu" is an intention, not a mechanism.

**Cut:**

- "Danh tính: Từ SSO/HRIS" vs "Người dùng tự khai đơn vị". **[Opinion]**
  Not a real choice; it is an assumption.
- "Đưa tri thức vào: RAG" vs "Fine-tune". **[Opinion]**
  A textbook choice; replace it with a real retrieval decision (C2).
- "Giao diện: Trang web chat ... Chưa biết công ty dùng công cụ chat nào". **[Opinion]**
  Low stakes, and the reason is a knowledge gap, not a trade-off; one line in the MVP scope is enough.

**Missing:**

- Risks specific to this design: retrieval crowding that causes a false refusal, identity edge cases (transfer, two units, probation), a wrong topic tag that silently changes precedence, over-trust, non-adoption (people keep messaging HR), and showing a future version that is not announced yet. **[Opinion]**
- A ranking that says which risk kills the product first. **[Practice]**

#### 5. Kiểm chứng & MVP - 6/10

**Keep:**

- "Cách đánh giá: cùng một câu hỏi, persona khác nhau phải nhận câu trả lời khác nhau. Đây chính là ví dụ trong đề bài, biến thành bộ test." **[Brief]**
- "các ca bẫy tôi tự viết, vì AI viết test sẽ có cùng điểm mù với AI trả lời." **[Opinion]**
  Mature reasoning; keep it and be ready to defend it.
- "Test rò rỉ không cần LLM chấm: kiểm tra rằng không đoạn văn bản nào ngoài quyền của persona lọt vào ngữ cảnh." **[Practice]**
  Deterministic, cheap, and the best metric in the draft.
- "Tỷ lệ rò rỉ: 0, điều kiện bắt buộc để phát hành". **[Practice]**
- "Chủ động chưa làm: ...". **[Brief]**
- "Các phần giả lập (persona thay SSO/HRIS) dùng cùng giao diện dữ liệu với hệ thống thật". **[Practice]**
  A clean seam for replacing simulations later.

**Deepen:**

- The test unit is "(persona, câu hỏi)". **[Opinion]**
  Validity needs a third dimension, the as-of date.
  Without a date override, the v2-to-v3 switch on 01/01/2027 cannot be tested, and Mission 3 changes probably cannot either.
- "≥ 95%" for "Đúng văn bản, đúng phiên bản". **[Opinion]**
  The selection is deterministic, so on your own test set anything below 100% is a bug, not a quality level.
  Thresholds below 100% belong to the probabilistic stages: question interpretation, retrieval recall, answer faithfulness.
  Split the metrics by stage.
- "Tỷ lệ từ chối ≤ 25%". **[Practice]**
  On a test set you design, the refusal rate is set by how many refusal cases you wrote.
  Measure whether refusals are correct (refused when it should, answered when it should) instead.
- "< 15 giây", "20-30 người", "2 tuần" have no reasons. **[Opinion]**
  Derive them or drop them.
- "chỉ xây phần kiểm chứng giả định rủi ro nhất" never states the assumption. **[Practice]**
  Write it as a sentence that can be proven false.

**Cut:**

- "Thí điểm: 20-30 người trong một công ty, 2 tuần." **[Opinion]**
  It cannot happen during the program; keep one line marked as after the program, or cut it.
- "Cách tôi dùng AI khi làm bài" in the PDF. **[Opinion]**
  It duplicates the evidence log and, as written, overclaims (Part E).

**Missing:**

- The test set itself, as an excerpt of 8-10 rows (C3, artifact 6). **[Opinion]**
- The test set size and coverage per hard case. **[Opinion]**
- A baseline: the same test set run through naive RAG. **[Opinion]**
  It is the cheapest proof of the thesis in Mission 2, and committing to it now is strong.
- What "pass" means for the Mission 2 demo. **[Opinion]**

### B2. Decision check

| # | Decision (draft wording) | Real or fake | Names B? | Why A wins? | A's cost? | When B wins? |
|---|---|---|---|---|---|---|
| 1 | "Kiểm soát quyền: Lọc trước khi tìm kiếm, bằng luật" vs "Dặn LLM giấu, hoặc lọc sau" | Real, but half of B is a strawman | Yes | Partly: "LLM không thể lộ thứ nó không thấy" defeats "dặn LLM giấu" but not "lọc sau", which also keeps restricted text away from the model; the real case against post-filtering is lost recall | Named, but "cần metadata quyền chính xác" is a cost of both options | No |
| 2 | "Văn bản nào thắng: Luật trên metadata; hòa thì chuyển người" vs "Để LLM phán xét" | Real, and the most important one | Yes | Yes: testable, traceable, the LLM can miss a conflict | Yes: "nhiều cảnh báo hơn cho chủ sở hữu" | Only hinted, in the risk table |
| 3 | "Khi không chắc: Từ chối và chỉ rõ cần hỏi ai" vs "Đoán câu trả lời tốt nhất" | Real, but B is framed as a strawman; the real B is answering with an explicit caveat | Yes | Asserted, not argued | Yes, with an unexplained number ("tối đa 25%") | No, and "không chắc" is never defined |
| 4 | "Phạm vi MVP: Quy định HR + chính sách dùng công cụ AI" vs "Toàn bộ tri thức công ty" | Fake as framed: no one would build all knowledge in 3 days; the real alternatives (one topic only, another domain such as IT procedures) are not named | Strawman | Partly for HR; thin for adding the AI-tool policy | No | No |
| 5 | "Mô hình phục vụ: Nhân sự tự tra cứu" vs "Chỉ là công cụ hỗ trợ HR" | Real, and B is stronger than the draft admits | Yes | Weak: "Trả lời ngay" | No (employees act on errors no human checked) | No, though the draft's own "HR tin câu trả lời" premise argues for B |
| 6 | "Giao diện: Trang web chat" vs "Bot trong công cụ chat công ty" | Real but low stakes | Yes | The reason is a knowledge gap | No | No |
| 7 | "Lúc kiểm tra mâu thuẫn: Cả lúc đăng và lúc hỏi" vs "Chỉ lúc hỏi" | Fake as framed: A contains B, so nothing is given up | Yes | "Sửa tận gốc một lần" | No (owner workflow, an admin UI that is cut) | No |
| 8 | "Danh tính: Từ SSO/HRIS" vs "Người dùng tự khai đơn vị" | Fake: an assumption, not a choice | Strawman | Yes | No | No |
| 9 | "Đưa tri thức vào: RAG" vs "Fine-tune" | Fake: textbook | Strawman | Yes | No | No |
| 10 | Precedence order (1)-(4) | Real and central, but not presented as a choice | No (alternatives: issuer authority, latest effective date, a relation declared per pair) | No | No | No, and the order is wrong (B3) |
| 11 | Refusals hide existence: "không nêu tên văn bản mật" | Real (B: say the document exists and how to request access) | No | No | No | No |
| 12 | Show the next version: "Sắp thay đổi: v3 có hiệu lực từ 01/01/2027" | Real (B: show nothing until in force, since a future version may itself be confidential) | No | No | No | No |
| 13 | AI suggests metadata, owner confirms (post-MVP) | Real (B: owner fills fields manually, or AI tags automatically) | No | No | No | No |
| 14 | Trap cases written by hand, "vì AI viết test sẽ có cùng điểm mù với AI trả lời" | Real | Implicitly | Yes, well argued | Implicit (time) | No |
| 15 | AI may add a conflict warning, never remove one | Real, and the best idea in the draft | Implicitly | Implicitly (errors cost different amounts in each direction) | No | No |

Summary: 15 decisions, 4 fake as framed (4, 7, 8, 9), 1 low-stakes (6).
Of the real ones, two name a cost specific to A (2 and 3), and none states when B would win.
The most interesting real decisions (10, 11, 12, 15) are not presented as decisions at all.

### B3. Reasoning check

**Asserted but not shown:**

- "Chatbot RAG thông thường sẽ gộp chúng thành một câu trả lời tự tin nhưng sai."
- "tìm kiếm ngữ nghĩa xếp chúng ngang nhau" (an empirical claim that depends on chunking and the embedding model).
- "Trả lời sai quy định đắt hơn chờ HR."
- "Câu hỏi HR thường gặp, sai thì đắt, khác nhau theo đơn vị." (plausible; label it as an assumption).
- "Sửa tận gốc một lần thay vì xử lý ở mọi câu trả lời" (assumes owners act on warnings).

**Numbers with no stated reason:**

- "≥ 95%" (twice), "≤ 25%" and "tối đa 25%", "< 15 giây", "20-30 người", "2 tuần".
- The test set size is never given.

**Conclusions that do not follow:**

1. **Precedence rule (1) vs the persona table.**
   Rule (1) puts "quy định cấp trên được đánh dấu bắt buộc, ví dụ mức sàn pháp lý" first, so the 12-day floor would beat GameCo's 14 days for Minh.
   The table says 14.
   A floor constrains lower rules; it does not compete with them.
2. **"One winner" vs Lan's answer.**
   "13 ngày: 12 theo quy chế Tập đoàn + 1 ngày thâm niên" combines two sources and a calculation.
   The flow picks one document and lets AI explain it, so either the LLM does the arithmetic, contradicting "luật xác định quyết định mọi thứ liên quan đến đúng sai", or a step is missing.
3. **Rule (2) before rule (3).**
   Because scope is checked before document type, a team-level FAQ or announcement would beat a company-level quy chế on the same topic.
   That is unlikely to be intended.
4. **Step order vs the core insight.**
   Section 1 says near-identical versions rank equally, yet the flow retrieves first and filters validity afterwards.
   Superseded and draft versions can fill the top-k, and the system then refuses although the answer exists.
5. **"Bước 1, 3, 4 là luật xác định, không dùng AI" vs "Còn hòa ... cùng chủ đề".**
   Deciding that two passages share a topic is a semantic judgment.
   Unless topics are assigned at publish time, this is AI inside step 4.
6. **"AI chỉ xử lý ngôn ngữ" vs "Nhận biết câu hỏi về bản thân hay về đơn vị khác".**
   That classification decides whose rule applies, which is correctness, not language.
7. **"trường hợp kiêm nhiệm hai công ty là thay đổi dữ liệu, không phải viết lại hệ thống".**
   Storing two units is data; choosing between two companies' rules at the same level is logic the precedence list does not have.
8. **"Sản phẩm chỉ sống được nếu HR tin câu trả lời" vs choosing self-service over an HR-facing tool.**
   Nothing connects the premise to the choice.
9. **"Văn bản chứa lệnh chèn vào ... Hậu quả: Rò rỉ".**
   With pre-filtering, an injected instruction cannot reveal text that is not in the context.
10. **"một lần lộ dữ liệu lương là sự cố dữ liệu cá nhân" used for the "Khung lương GameCo" example.**
    A salary band identifies no one.
11. **"Không ai tự nhận được quyền mình không có" vs the MVP persona switcher.**
    The switcher is self-declared identity.
    That is fine for a demo, but say so, because a judge will.

### B4. Feasibility check

The 3-day MVP is the right size for one student if the corpus stays small (20-30 documents) and only one topic family is modelled in depth.
Nothing is grossly over-promised.
The risk is not scope; it is that the core rule is harder than the document admits.

- **Day 2 is overloaded.**
  Permission filter, validity, applicability, precedence with floors and composition, seniority calculation, and an LLM answer with clause-level citation.
  Once B3 items 1-3 are fixed, the precedence logic alone is the hardest part of the build.
  Consider supporting only two or three relation types in v1.
- **Day 1 underestimates dataset design.**
  Writing 20-30 consistent simulated documents with traps, plus a test set with expected outputs, can take a full day on its own.
- **"Trích nguyên văn điều khoản"** needs clause-level chunks with stable IDs.
  Easy with Markdown headings, but it must be designed in on Day 1.
- **"Quyết định của chủ sở hữu ... được lưu thành dữ liệu"** needs an owner-side action, and there is no admin UI in v1.
  Say it is a config edit for now.
- **"Thí điểm: 20-30 người ..., 2 tuần"** and its metrics cannot happen inside the program.
- **The publish flow, AI-suggested metadata and review-date alerts** are correctly labelled post-MVP, but they use space.

### B5. Fact check

| Claim | Where | Verdict | Note |
|---|---|---|---|
| "Mức sàn pháp lý: 12 ngày phép năm, cộng 1 ngày cho mỗi 5 năm làm việc (Bộ luật Lao động 2019, Điều 113-114)" | PDF p.1 | Confident correct, with nuances | Art. 113.1(a): 12 working days for 12 full months with one employer, normal conditions. Art. 113.2: pro rata under 12 months, which matters for Hà on probation. Art. 114: +1 day per full 5 years "cho một người sử dụng lao động", which matters for transfers between group companies. Checked on hethongphapluat.com (Art. 113, 114). |
| "Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15" | PDF p.1 | Confident correct | Issued 26/06/2025, effective 01/01/2026, per chinhphu.vn. |
| "một lần lộ dữ liệu lương là sự cố dữ liệu cá nhân theo Luật ..." | PDF p.1 | Unsure as a legal statement; likely wrong as applied to the example | The law defines personal data as data that identifies or helps identify a specific person (Art. 2.1). An identified employee's salary fits; a salary band does not. Whether salary is *sensitive* personal data: unsure (Decree 356/2025/NĐ-CP lists customers' financial data at financial institutions; the full list was not read). "Sự cố" was not confirmed as the law's term. |
| "tìm kiếm ngữ nghĩa xếp chúng ngang nhau" | PDF p.1 | Unsure | Plausible, but it is an empirical claim that depends on chunking and the model; show it rather than assert it. |
| Điều 118-119 Bộ luật Lao động 2019: written internal labour rules from 10 employees, registered with the provincial labour authority | Evidence log | Confident correct | Checked on pbgdpl.hanoi.gov.vn and hethongphapluat.com. |
| Law 91/2025/QH15 effective 01/01/2026 | Evidence log | Confident correct | As above. |
| Gary Klein, pre-mortem, *Harvard Business Review*, September 2007 | Evidence log | Confident correct | |
| Appota's subsidiaries: Gamota, AppotaPay, Adsota, ACheckin, Kdata | Evidence log | Unsure | Not checked; not used in the PDF, so mark it as such in the log. |
| NextGen roadmap "Explore → Build → Become" | Evidence log | Unsure | Not checked; not used in the PDF. |

The candidate should still check the two legal citations in the PDF on an official source (vbpl.vn, congbao.chinhphu.vn) and record that in the evidence log.
An AI checking an AI's facts is not the verification the policy asks for.

---

## Part C - Blueprint for the redraft

### C1. Sections, central claims, page budget, evidence

The central claims below are in English on purpose; the candidate should write their own Vietnamese version.

| Section | Central claim to argue | Pages | Evidence it needs | Main criterion |
|---|---|---|---|---|
| Page-1 opener + 1. Vấn đề & người dùng | A relevant answer can be wrong for this person in three distinct ways, and the expensive failure is a confident wrong answer the employee acts on, not a failed search. | 1.25 | Persona x question x as-of-date table with the correct answer and the naive answer; failure types with who pays; current workaround; users including the owner; assumptions with the riskiest marked; why this problem beats leakage and missing documents. | Khung vấn đề |
| 2. Giải pháp & luồng | Who is asking and which rule applies are decided by explicit rules before the model sees anything; the model only reads and explains. | 1.25 | Readable flow; the resolution model as a small decision table (relation types, order, composition); one worked trace; three output cards (answer, refusal, conflict). | Thực thi (and Khung) |
| 3. AI, dữ liệu & con người | Correctness lives in metadata and ownership; the model's errors are contained to wording and applicability, never access. | 0.75 | AI/no-AI table with an honest boundary; metadata sample rows; the access rule; owners and the feedback loop with a response time. | Thực thi and Khung |
| 4. Quyết định & rủi ro | Three choices define this design, and each has a cost the candidate accepts on purpose. | 1.0 | Three full A-vs-B arguments (C2); a pre-mortem top 5 risks with likelihood, detection signal and mitigation. | Chất lượng quyết định |
| 5. Kiểm chứng & MVP | v1 works if a persona x question x date test set passes with zero leakage and beats naive RAG on it; the 3 days build exactly what that test needs. | 0.75 | Test matrix excerpt; metrics split by stage with reasoned gates; baseline plan; day plan; cut list with why each cut is safe. | Thực thi |

### C2. The decisions that deserve a full A-vs-B argument

1. **Who decides precedence and conflicts.**
   A: explicit relation rules on metadata, where AI may raise a conflict flag but never clear one.
   B: the LLM reads every permitted, valid candidate and reconciles them.
   Why this one: it is the thesis of the design, it is what mandatory question 3 asks, and B is what most other candidates will build.
   Convincing reasoning would run one conflict case through both, name what B does better (catching conflicts nobody encoded, handling partial overrides), estimate A's cost in owner workload, and say when B should take over as a detector feeding A.
2. **What happens when the rules cannot produce one applicable answer.**
   A: refuse and route to the right owner.
   B: answer with an explicit caveat (the honest version of B, not "đoán").
   Why this one: it sets the user experience and the refusal trade-off, and it tests the cost-asymmetry claim from Section 1.
   Convincing reasoning would define the triggers precisely, compare the cost of a false refusal with a false answer for two or three question types, and say for which questions B wins.
3. **Launch model.**
   A: employees ask directly.
   B: an HR-facing assistant first, with HR checking answers before employees see them.
   Why this one: the draft's own premise that HR trust keeps the product alive makes B a serious option, and it is a product judgment, not a technical one.
   Convincing reasoning would compare who catches errors in each model, how trust gets built, what each costs HR, and what evidence would move from B to A.
   Either answer, or a staged path, is fine if argued.
4. **Optional: how retrieval and selection split.**
   A: semantic chunk retrieval with metadata pre-filters.
   B: classify the question into a topic key, look up the applicable rule deterministically, and fall back to free retrieval.
   Why this one: the draft's own insight (near-identical versions rank equally) undermines letting ranking decide anything, and this choice sets the Mission 2 architecture.
   Convincing reasoning would compare coverage of unexpected questions with precision of selection, at 30 and at 3,000 documents, on the worked trace.

Why not the others: pre-filtering permissions is close to consensus practice, so one line with a reason is enough; identity from HRIS and RAG vs fine-tune are not real choices; the UI is low stakes.

### C3. Artifacts that earn "Thực thi" without code

| # | Artifact | Contents | Where |
|---|---|---|---|
| 1 | Worked trace of one question | Persona and as-of date; 6-8 simulated candidate documents with key metadata; for each step, what is removed and why; the relation used; any calculation; the final card. Pick a question that exercises at least three filters. | Section 2 |
| 2 | Naive vs correct contrast | What plain RAG would retrieve and answer for the same question, next to the correct answer. | Page-1 opener or Section 1 |
| 3 | Metadata sample | 4-6 rows covering a superseded version, a future version, a restricted document, a cross-level pair, and a two-unit person. | Section 3 |
| 4 | Resolution spec | Relation types and evaluation order as a small decision table. | Section 2 |
| 5 | Output cards | Answer, refusal, conflict; say whether the refusal for "not found" and "not allowed" is identical. | Section 2 |
| 6 | Test matrix excerpt | 8-10 rows: persona, question, as-of date, expected behaviour, must cite, must not cite; including adversarial rows. | Section 5 |
| 7 | Optional small experiment **[Opinion]** | Embed the simulated near-identical documents with a real embedding model and report the top-k for one question. One line and one number in the PDF, logged in the evidence log, re-runnable at the PITCH. It would turn the core claim from asserted to measured. | Section 1 or 5 |

Label every artifact "giả lập".

### C4. What should open page 1

A judge who reads only the first half page should get four things:

1. The diagnosis in one sentence: finding relevant text is the easy part; the right answer depends on who asks and when, and must not leak.
2. One concrete contrast: Minh's question, what a naive system would say, what the right answer is, and why.
3. The cost asymmetry and the principle it leads to: explicit rules decide, AI explains, and the system refers the user elsewhere when the rules cannot decide.
4. The one problem and the one user chosen.

The current box, "Một câu hỏi, bốn phép kiểm tra ...", is a good start; it lacks the contrast and the choice.

### C5. Criterion map

The sections overlap, so read this as primary and secondary weight.

- **Khung vấn đề (40%)**: Section 1 (primary), plus the parts of Sections 2 and 3 that show subtle understanding (relation types, identity edge cases, honest AI boundary).
  About 2 pages of the 5 should be doing this work.
- **Thực thi (35%)**: Sections 2, 3 and 5 through the artifacts in C3.
  About 1.75 pages.
- **Chất lượng quyết định (25%)**: Section 4, plus the decisions argued inside Section 2.
  About 1.25 pages.

The current draft spends roughly 1.2 pages on a 9-row decision table and risk table, and leaves 0.7 of page 5 empty.

---

## Part D - The 3 mandatory answers

Word counts (whitespace split): Q1 = 125, Q2 = 130, Q3 = 133, all inside the recommended 60-150.

### Q1 - Vấn đề quan trọng nhất

- **Opens with the decision:** yes, "Tôi chọn vấn đề: nhân sự không biết chắc quy định nào đang áp dụng cho chính mình."
- **Gives the reason:** yes, near-identical group, company and old versions.
- **Focused:** yes.
- **Gap:** it never says why this problem beats the obvious alternative, leakage, which it then lists as a constraint. **[Brief]**
  "Quan trọng nhất" invites that comparison.
- **Consistency with C:** consistent; add the cost asymmetry once Section 1 frames it.
- **Weakest sentence:** "Kết quả họ cần: một câu trả lời đúng với đơn vị, loại hợp đồng và thời điểm hiện tại, kèm nguồn, phiên bản và ngày hiệu lực để tự hành động ngay."
  It describes the answer card, not the outcome. **[Practice]**
  State what the user achieves, then at most one property that makes it trustworthy.

### Q2 - Ba ngày đầu

- **Opens with the decision:** yes.
- **Gives the reason:** weakly.
- **Focused:** overloaded; seven build items and seven cuts in 130 words leave no room for the why.
- **Consistency with C:** will need to change.
  Add the as-of date to the build and to the test unit.
  "tích hợp Lark/Slack" contradicts the PDF's "Chưa biết công ty dùng công cụ chat nào".
  "tra cứu dữ liệu cá nhân" is cut here but not listed in the PDF.
  If the redraft changes the retrieval split or the launch model (C2), this answer changes too.
- **Weakest sentence:** "Lý do: đó là bài toán tích hợp và mở rộng; nếu phần lõi sai, mọi thứ khác vô nghĩa."
  Not all cuts are integration (multi-turn, personal-data lookup), "mọi thứ khác vô nghĩa" is a slogan, and the riskiest assumption is never stated. **[Practice]**
  Name the assumption the 3 days test, and give one reason the cuts do not affect testing it.

### Q3 - Hai tài liệu liên quan nhưng khác nhau

- **Opens with the decision:** yes, "Thứ tự ưu tiên do luật trên metadata quyết định, không để LLM tự chọn."
- **Gives the reason:** yes, but generic ("vì AI có thể ảo giác").
- **Focused:** the best of the three; it walks through the cases in order.
- **Consistency with C:** must be updated once the resolution model is fixed (relation types, composition, topic granularity).
- **Weakest sentence:** "Khác phạm vi: quy định của đơn vị cụ thể nhất được áp dụng, trừ khi quy định cấp trên được đánh dấu bắt buộc, ví dụ mức tối thiểu theo luật."
  Read literally, a legal minimum of 12 days replaces a company rule of 14, the opposite of the persona table. **[Opinion]**
  A judge who knows labour law will catch it in seconds.
  Distinguish a rule that replaces from a rule that sets a minimum, and say which one the example is.
- Second weakest: "Cùng phạm vi, cùng chủ đề, cùng hiệu lực: coi là mâu thuẫn".
  Two same-scope documents on one topic can be complementary (entitlement vs request procedure), so how "chủ đề" is defined decides whether owners drown in false alerts.

---

## Part E - The evidence log

**What works:**

- Every entry has a tool, a summarised prompt, the output, and a verification status, and the ⏳/✅ split is honest.
- Entry 4 records a rejected AI suggestion with the candidate's own reason ("LLM có thể ảo giác và nói 'không mâu thuẫn' khi thực ra có").
  This is exactly the kind of evidence of ownership judges look for. **[Opinion]**
- Entry 1 labels the Mission 2-3 prediction as speculation, and entry 2 says illustrative numbers were not used as data.

**What a judge would find missing or unconvincing:**

1. **The PDF's ownership claim contradicts the log.** **[Brief]**
   The PDF says "mọi quyết định cuối cùng và lý do là của tôi".
   Entry 4 says Claude drafted "lý do và điều kiện đổi ý cho D1-D6, top 3 rủi ro, kịch bản S01-S10, đề xuất nút 'Báo sai', phạm vi HR cộng chính sách dùng AI, tách chỉ tiêu thành 95% ... và tối đa 25% ...", and that the candidate "duyệt chung toàn bộ bản nháp (Round 3), chưa thảo luận từng mục".
   A judge will read both, and the policy forbids "Nộp đầu ra của AI mà bạn không hiểu".
   The redraft has to make the claim true, or the claim has to change.
2. **Approval is marked as verification.**
   "Tôi duyệt cả 7, chưa thảo luận chi tiết" carries a ✅ under "Xác minh".
   Approving is not verifying.
   Either verify and record what changed, or use a different status.
3. **Facts used in the PDF are still ⏳.** **[Brief]**
   Art. 113-114 and Law 91/2025 appear in the PDF, and the log says they are unverified.
   The policy says "Ảo giác AI rõ ràng mà không xác minh = trượt tiêu chí đó".
4. **Prompts are summaries.** **[Brief]**
   The policy asks for "mọi công cụ AI + prompt đã định hình kết quả cuối cùng".
   Summaries are acceptable for long chats, but the prompts that shaped the submission most (drafting the document and the answers) should be quoted verbatim or attached.
5. **Verification is about format, not content.**
   Word counts, page counts and screenshots check presentation.
   A judge wants content checks, for example "I traced Minh's case by hand and found ...".
6. **No origin map.** **[Opinion]**
   Nothing shows, per decision and per answer, who proposed it and what the candidate changed.
   That one table would answer the judge's main question about the log.
7. **Entry 7 expects a review by "AI khác".**
   This review ran on the same model that drafted the work; log it that way, and don't present it as independent.
8. **Internal noise.**
   "Mục 1-7 dùng tên file trước khi thư mục được sắp xếp lại vào `docs/`" and paths like `.lavish/thinking-workbook.html` mean nothing to a judge without the repository.
   Describe the artifacts, or say they are available on request.
9. **Unused unverified facts** (subsidiaries, roadmap) should be marked "không dùng trong bài nộp" so they do not read as unchecked claims.

---

## Part F - PITCH preparation

Ordered from most to least likely.

1. **"Walk me through what happens when Minh asks 'Phép năm của tôi?'. Which documents does the system consider, which does it drop at each step, and why does it end at 14 days?"**
   A strong answer contains the actual candidate set from the simulated data, each step's rule in one sentence, the relation that makes GameCo v2 beat the group rule, exactly where AI is and is not involved, and what changes on 01/01/2027.
2. **"Which parts did you write, and which did AI write? Where do 25% and 95% come from?"**
   A strong answer contains an origin account consistent with the evidence log, and for each number its source and what would change it, or why it was replaced.
3. **"The legal minimum is a mandatory rule, and your order puts mandatory rules first. Why doesn't Minh get 12 days? And how does Lan get 13?"**
   A strong answer contains the difference between replacing and setting a minimum, how a base entitlement and a seniority bonus are combined and by which component, and who declares the relation between two documents.
4. **"With 20-30 documents, why use an LLM at all? Why not a search page filtered by the user's unit?"**
   A strong answer contains what the LLM adds that filters cannot (natural phrasing, abbreviations, missing diacritics, explaining why a rule applies), what it costs, and what would make the candidate drop it.
   A candidate in an AI program who cannot answer this is in trouble.
5. **"Real documents don't come with clean metadata. Who tags the existing ones, how long does it take, and what does the system answer before they are tagged?"**
   A strong answer contains a backfill plan, what is refused meanwhile, the cost to owners, and why partial coverage is still useful.
6. **"How does the system know two documents are about the same topic? Isn't that an AI judgment?"**
   A strong answer contains where topics come from (assigned at publish time, or an honest admission that AI decides), how a wrong topic shows up, and what it breaks.
7. **"An employee moved from PayCo to GameCo after four years, or works for both. What does the system answer?"**
   A strong answer contains where the data comes from, which rule applies, how seniority counts across group companies (Art. 114 counts years with one employer), and when the system escalates instead.
8. **"You say HR trust keeps the product alive. Why launch to employees directly instead of giving HR the tool first?"**
   A strong answer contains who catches errors in each model, how trust is built, and what evidence would move from one to the other.

Also prepare for: whether "không có thông tin trong quyền của bạn" itself reveals that something exists; who decides whether a future version may be shown before it is announced; and what an injected instruction inside a permitted document can actually do.

---

## Part G - Priorities

1. **Show the mechanism on one question.**
   Add the worked trace with a simulated candidate set, and the naive-vs-correct contrast.
   Criterion: Thực thi (primary), Khung vấn đề.
   Why first: it is the only way a no-code document shows "chạy thật", and doing it will expose the bugs that change 2 fixes.
2. **Fix and specify the resolution model.**
   Relation types (replaces, overrides, adds to, sets a minimum), composition, validity as a pre-filter, topic keys, and the rule for a person in two units.
   Criterion: Thực thi, Khung vấn đề.
   Why: the current rule fails on the draft's own examples, and the same rule appears in mandatory answer 3.
3. **Replace the 9-row decision table with three full A-vs-B arguments (C2).**
   Move the fake choices into one line of assumptions.
   Criterion: Chất lượng quyết định.
   Why: 25% of the score rests on the quality of a few arguments, not on the number of rows.
4. **Rebuild Section 5 around a persona x question x date test matrix.**
   Include an excerpt, metrics split by stage, thresholds with reasons, and a naive-RAG baseline.
   Criterion: Thực thi.
   Why: it turns "giải pháp có chạy thật không?" into something Mission 2 can check.
5. **Make Section 1 earn its 40%.**
   Failure types with who pays, the cost asymmetry, the current workaround, the knowledge owner as a user, assumptions with the riskiest marked, and why this problem beats the alternatives.
   Criterion: Khung vấn đề.
   Why: the thesis is already good; this adds the evidence that it is the right problem.

**Before submitting, regardless of rank:** reconcile the PDF's ownership claim with the evidence log, verify the two legal citations yourself on an official source, fix the salary-band example, and bring the three answers in line with the redraft (Lark/Slack, the date dimension, the precedence wording).
