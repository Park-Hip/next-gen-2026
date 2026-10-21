# Simulated data (giả lập)

The data the Mission 1 design was checked on, as files for Mission 2.
Every unit, person, document and number here is simulated.

| Path | What it is |
|---|---|
| `documents/<id>.md` | The 10 documents: YAML front matter with the metadata, then the text, one "Điều" per line (the procedure document has plain steps, on purpose) |
| `org.yaml` | The org tree; `hr` is the contact the cards name |
| `personas.yaml` | Minh, Lan and Hà: unit and roles, the two fields the HR system would give |
| `test_cases.yaml` | The test cases: rows 1-10 of the Mission 1 test matrix and rows 11-15 from issue #10; each has its `purpose` (why it is tested, shown to the judges), its wordings of the question, the card, the expected answer, the documents it must and must not cite, and the `key_facts` an answer must state (fields explained at the top of the file) |

Metadata fields, as read by the rules:

| Field | Meaning |
|---|---|
| `series` | One policy across its versions; the published version with the latest `effective_from` not after the as-of date is in force; two published versions of one series with the same `effective_from` fail the load |
| `topic` | One per document; only used to find conflict pairs |
| `access` | Who may read it: `all_staff`, `unit:<unit>` or `roles:<role>,<role>`; never who it is for, and it never changes which document replaces which (ADR 0010) |
| `applies_to` | The unit it covers, with every unit below it |
| `status` | `published` or `draft` |
| `effective_from`, `effective_to` | `effective_to` only when the document really ends |
| `overrides` | "Dùng thay": one series this document is used instead of, for the units it applies to, whether or not the asker may read this document (ADR 0010); a series that overrides itself, or a cycle of overrides, fails the load |
| `complements` | "Bổ sung": series this document adds to without contradicting them |

Owners change a document only by publishing a full new version (ADR 0013).
To change one clause, the owner copies the version in force, changes the clause and publishes the copy as the next version of the same `series`.
A company that changes one clause of a Group policy publishes a complete policy of its own, with the Group clauses it keeps, and declares `overrides`.
A separate amendment that holds only the changed clauses is never published; the rules cannot detect one, so this is a rule for owners.

Source: `docs/mission1/redraft/artifacts.md` and `docs/mission1/redraft/checks/adopted_rules.py`.
The tests in `tests/` check the files and run the rules on them.
`data/` is now the source of truth; `artifacts.md` stays as the Mission 1 snapshot.
