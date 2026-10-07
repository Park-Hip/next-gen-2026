# Artifacts - Mission 1 redraft

All data is simulated ("giả lập").

## Data model sketch (Claude draft, not yet decided)

Purpose: make the Phase 1 decisions concrete.
Fields marked with a decision ID depend on that decision and may change.

### Employee profile

Source: HR records (MVP: persona switcher).

| Field | Example (Minh) | Used for |
|---|---|---|
| `units` | GameCo → Studio | Applicability; access to unit-only documents (two units: M5) |
| `roles` | `employee` (Lan: `hr_group`) | Access to restricted documents |

Employment type and start date are out of the MVP (M0); they can be added later as applicability fields.

### Document metadata

| Check | Fields | Example (GameCo v2) |
|---|---|---|
| Identity | `id`, `title`, `doc_type`, `owner` | POL-LEAVE-GAMECO-v2, quy chế, HR GameCo |
| Topic | `topic`, one value from a fixed list (M4) | `nghi_phep` |
| Allowed (who may read) | `access` | Group-wide / unit only / listed roles |
| Applicable (who it covers) | `applies_to.unit` | GameCo |
| In force (when) | `status`, `effective_from`, `effective_to` | published, from 01/01/2026 |
| Relations (M1a) | `replaces`, `overrides` | replaces GameCo-v1; overrides GROUP-v1 |

### Minh's trace (as of 07/10/2026)

Minh: GameCo, Studio. Question: "Phép năm của tôi?"

| Doc | Key metadata | Result | Deciding field |
|---|---|---|---|
| SAL-BAND-GAMECO | access: role `hr_gameco` | Removed: not allowed | `access` |
| LEAVE-PAYCO-v1 | applies to: PayCo | Removed: does not cover Minh | `applies_to` |
| LEAVE-GAMECO-v1 | in force 2024-2025 | Removed: replaced by v2 | `replaces`, dates |
| LEAVE-GAMECO-v3 | in force from 01/01/2027 | Removed: not in force yet (newest file, but not the answer) | `effective_from` |
| LEAVE-GROUP-v1 | Group-wide, 12 days | Applies to Minh | |
| LEAVE-GAMECO-v2 | GameCo, 14 days, overrides GROUP-v1 | Wins over GROUP-v1: 14 days | `overrides` |

Without the `overrides` field, the last two rows are a conflict (M1b) and Minh is routed to HR.
