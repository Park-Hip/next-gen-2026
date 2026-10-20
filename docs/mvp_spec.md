# MVP spec - Tri thức nội bộ Appota

Status: draft by Claude (Opus 5.5), 20/10/2026, for Hiep to review; items marked **[to decide]** are open.
All Appota data in this project is simulated ("giả lập").

## Terms

| Term | Meaning |
|---|---|
| Unit | A part of the organisation: the Group, a member company, a department or a team |
| Internal document | A written rule issued by a unit, such as a leave policy or a procedure |
| Document owner | The person in a unit (usually HR) who issues and maintains that unit's documents |
| Version | One edition of a document; a document can have several over time |
| In force | The version that is valid on a given date: published, and its effective date has come |
| Applies to | The units whose employees must follow a document |
| May read | The employees allowed to see a document; a document can apply to someone they may not read, and the reverse |

## 1. Problem statement

Appota is a group of companies, each with its own departments and teams.
Its internal rules are issued at every level: the Group sets a policy, a member company may replace it for its own staff, and a department may add to it.
Each rule changes over time, so the same document exists in an old version, the version in force and sometimes a future version.
Some documents may be read only by some employees, such as HR or managers.

An employee who needs a rule, for example how many days of annual leave they have, faces three questions at once: which documents apply to their unit, which version is in force today, and which of them they are allowed to read.
These documents read almost the same, so an answer taken from the wrong one looks exactly like a right one, and the employee acts on it without knowing it is wrong.
Sometimes two applicable documents disagree and nobody has said which one wins, and sometimes no document answers the question at all.
Today the employee either asks HR and waits, or guesses.

Document owners face the other side of the same problem.
They must publish new documents and new versions, say from when they take effect and for whom, and keep them consistent with the documents of other units.

**The outcome the company wants:** an employee makes the right decision the first time, from the rule that applies to them, without waiting for HR; and when the right answer cannot be given, they are told so and sent to the right person instead of being given a wrong one.

## 2. Users

| User | What they need |
|---|---|
| Employee | The rule that applies to them on the date they ask, in words they understand, with a source they can check; a clear "not enough information, ask HR" when the answer cannot be given |
| Document owner | Publish a document or a new version, say when it takes effect, who it applies to, who may read it and how it relates to other units' documents, and see the state of their unit's documents |
| HR contact of a unit | Receive the questions of their unit's employees that the system cannot answer |

## 3. Requirements

The last column names the metric that tests each requirement; the metrics are defined in section 6.

### 3.1 Employee

| ID | Requirement | Reason | Tested by |
|---|---|---|---|
| E1 | An employee asks a question in everyday Vietnamese and gets an answer in plain Vietnamese that answers it directly | Employees should not have to read and interpret policy text to know what to do | Readability |
| E2 | The answer follows only the documents that apply to the employee's unit | The same question has different correct answers in different units | Right sources and right kind |
| E3 | The answer follows only the version in force | Old and future versions read almost the same as the current one, and an answer from them looks right | Right sources and right kind |
| E4 | The answer never uses, shows or hints at a document the employee may not read, including its title or existence | Some documents are confidential, such as salary scales | Leaks |
| E5 | When applicable documents disagree and no owner has said which one wins, the employee is told so and shown both, and nothing is chosen for them | A silent choice can be the wrong rule, presented as the right one | Right sources and right kind |
| E6 | When the documents the employee may use do not answer the question, the system says so and names who to ask | A guess that looks like an answer is worse than no answer | Right sources and right kind; Unsafe answers |
| E7 | Every answer shows what it is based on: the document, the part of it, the version and its effective date, and the employee can read that part | The employee must be able to check an answer before acting on it | Source shown |
| E8 | The employee's unit and roles come from their account, never from what they type in the question | Otherwise anyone could claim a role to read what they may not | Leaks |

### 3.2 Document owner

| ID | Requirement | Reason | Tested by |
|---|---|---|---|
| H1 | An owner publishes a new document or a new version, with when it takes effect, which units it applies to and who may read it | Rules change, and the people who own them must be able to change them | Owner scenarios |
| H2 | An owner states how their document relates to other units' documents on the same subject: it replaces them for their unit, or it adds to them | Only the owner knows which rule is meant to win; the system must not guess | Owner scenarios |
| H3 | A published change reaches employees from its effective date, with no technical help | Employees must get the new rule on the day it starts, not before and not later | Owner scenarios |
| H4 | An owner sees their unit's documents, their versions and which one is in force | Owners must be able to check what employees are being told | Owner scenarios |
| H5 | Only an owner of a unit can publish or change that unit's documents | A wrong publication changes what every employee of the unit is told | Owner scenarios |

### 3.3 The whole system

| ID | Requirement | Reason | Tested by |
|---|---|---|---|
| S1 | Every fact in an answer is supported by the document it cites | An answer the source does not support misleads even when the source is right | Faithfulness |
| S2 | When in doubt, the system refuses or flags rather than answers | A refusal costs a question to HR; a wrong answer costs a wrong decision | Unsafe answers; Over-caution |
| S3 | Every answer can be traced afterwards to the documents and passages it used | A wrong answer must be explainable to be fixed | Traceable answers |
| S4 | Published documents and their history are kept | Owners and employees must be able to rely on what was published | Owner scenarios |
| S5 | The system is used from a web browser, in Vietnamese | Employees and owners should need nothing installed | Owner scenarios and test questions are run through the web page |

## 4. Constraints

What the system receives as input, and the form it comes in.

| Input | Constraint |
|---|---|
| Documents | Markdown files in Vietnamese; each clause starts on its own line with "Điều 1", "Điều 2" and so on |
| Information about each document | Set by its owner when publishing: issuing unit, version, effective date, units it applies to, who may read it, subject, and its relations to other units' documents [to decide: the exact list] |
| Organisation | A fixed tree of units: the Group, member companies, departments and teams |
| Employees | Simulated accounts, each with one unit and a set of roles; a user signs in as one of them |
| Document owners | Simulated accounts, each owning the documents of one unit |
| Questions | Vietnamese text, asked on a given date; one question, one answer, with no conversation: each question is answered on its own, without earlier questions |
| Data | All simulated; no real Appota data |

## 5. Assumptions

Things taken as true without proof.

| ID | Assumption |
|---|---|
| A1 | Owners set the information of their documents correctly in most cases |
| A2 | Only three things decide which rule applies to an employee: their unit, what they may read, and the date; not employment type or seniority |
| A3 | Every rule an employee asks about is written in some document; practice that is not written down is out of scope |
| A4 | Employees can read and understand the source of an answer when they need to check it |

## 6. Evaluation

The system is evaluated on a set of test questions, each asked by a given simulated employee on a given date, with the expected result written before the run.
Every requirement in section 3 is covered by at least one test question or owner scenario, and the set includes hard and ambiguous questions, not only easy ones.

### 6.1 The three kinds of response

Every response is one of three kinds, and each test question says which kind it expects:

- **Answer:** the system answers the question and shows its source.
- **Conflict notice:** two applicable documents disagree and no owner has said which wins, so both are shown and the employee is sent to HR.
- **Refusal:** the system does not answer, says it found nothing it may use, and names who to ask.

### 6.2 Metrics

| Metric | What it measures | How it is counted | Target |
|---|---|---|---|
| Right sources and right kind | Whether the system used the documents that apply to the asker on that date, and gave the expected kind of response | Per question, compared with the expected documents and kind; automatic | Every question |
| Leaks | Whether anything from a document the asker may not read was used, cited or shown, including when the question claims another role or unit | Per question, any such document in the sources or in the text; automatic | 0 |
| Unsafe answers | Answers that should not have been given: an answer where a refusal or a conflict notice was expected, an answer missing the fact that answers the question, or one citing a document it must not use | Per question; automatic, then confirmed by hand | 0 |
| Faithfulness | Whether every statement of an answer is supported by the passage it cites | Each answer read by a person, statement by statement | Every answer |
| Over-caution | Refusals or conflict notices where an answer was expected | Share of the questions that expect an answer | At most 10% |
| Readability | Whether an answer answers the question directly, in plain Vietnamese | Each answer read by a person [to decide: the criterion] | Every answer |
| Source shown | Whether an answer names its document, the part used, the version and its effective date, and lets the employee read that part | Per answer; automatic | Every answer |
| Traceable answers | Whether the documents and passages behind each answer are recorded | Per question, the record of the run; automatic | Every question |
| Owner scenarios | Whether owners can publish and relate documents, see their state, and are stopped outside their unit, and whether a change reaches employees from its effective date and survives a restart | Scenario tests: publish, then ask before and on the effective date; publish for another unit; restart; automatic | Every scenario |

### 6.3 Acceptance

The MVP is accepted when every metric meets its target on the test set.
Reaching the targets on a small simulated set is the bar for letting real employees try it, not proof that it is safe.

## 7. Open questions

- The exact information an owner sets for each document (section 4).
- The criterion for Readability (section 6.2).
