# Simulated data (giả lập)

The data the Mission 1 design was checked on, as files for Mission 2.
Every unit, person, document and number here is simulated.

| Path | What it is |
|---|---|
| `documents/<id>.md` | The 10 documents: YAML front matter with the metadata, then the text, one "Điều" per line (the procedure document has plain steps, on purpose) |
| `org.yaml` | The org tree; `hr` is the contact the cards name |
| `personas.yaml` | Minh, Lan and Hà: unit and roles, the two fields the HR system would give |
| `test_cases.yaml` | The test cases: rows 1-10 of the Mission 1 test matrix and rows 11-15 from issue #10; each has its wordings of the question, the card, the expected answer and the documents it must and must not cite (fields explained at the top of the file) |

Metadata fields, as read by the rules:

| Field | Meaning |
|---|---|
| `series` | One policy across its versions; the published version with the latest `effective_from` not after the as-of date is in force |
| `topic` | One per document; only used to find conflict pairs |
| `access` | Who may read it: `all_staff`, `unit:<unit>` or `roles:<role>,<role>` |
| `applies_to` | The unit it covers, with every unit below it |
| `status` | `published` or `draft` |
| `effective_from`, `effective_to` | `effective_to` only when the document really ends |
| `overrides` | "Dùng thay": one series this document is used instead of, for the units it applies to |
| `complements` | "Bổ sung": series this document adds to without contradicting them |

Source: `docs/mission1/redraft/artifacts.md` and `docs/mission1/redraft/checks/adopted_rules.py`.
The tests in `tests/` check the files and run the rules on them.
`data/` is now the source of truth; `artifacts.md` stays as the Mission 1 snapshot.
