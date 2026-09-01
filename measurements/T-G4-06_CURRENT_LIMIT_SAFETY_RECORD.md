# RX50 G4 T-G4-06 CURRENT-LIMIT SAFETY RECORD

- File: measurements/T-G4-06_CURRENT_LIMIT_SAFETY_RECORD.md (NEW, M003D)
- Created: 2026-08-15 by M003D
- Status: **NOT VERIFIED / INCOMPLETE**
- Rule: this record MUST NOT contain invented physical verification. Fields below are the required fields from the M003D mission brief (section 6). Every field is preserved; values are recorded only when real evidence exists.

## Safety record status

**NOT VERIFIED** — the F3 fault-injection fixture has NOT actually been checked. No element installed, no measurement made, no record supplied by the owner/operator.

| FIELD | VALUE | STATUS |
|---|---|---|
| Current-limit element identity | NOT SUPPLIED | INCOMPLETE |
| Intended nominal value | NOT SUPPLIED | INCOMPLETE |
| Measured value (if required by protocol) | NOT SUPPLIED | INCOMPLETE |
| Verification method | NOT SUPPLIED | INCOMPLETE |
| Instrument | NOT SUPPLIED | INCOMPLETE |
| Fixture identity | F3 (combined node; conceptual only — no build recorded) | INCOMPLETE |
| Verification date | NOT SUPPLIED | INCOMPLETE |
| Operator | NOT SUPPLIED | INCOMPLETE |
| Calculated/verified maximum current | NOT ESTABLISHED (no value selected) | INCOMPLETE |
| Applicable absolute limits (datasheet reference, NOT verification) | IINJ(PIN) ±5 mA (EV-47, DS5319 Table 7); ΣIINJ(PIN) ±25 mA (EV-47b); CD4067 IS/ID ±20 mA abs / ±10 mA rec (EV-45, SCHS052D Rev D); governing bound ≤ ±5 mA | REFERENCE ONLY |
| Pass/fail result | NOT AVAILABLE (nothing tested) | INCOMPLETE |

## Traceability

- E6 `CURRENT_LIMIT` field (RX50_G4_RAW_DATA_TEMPLATES.md): MANDATORY for all fault injection — EMPTY (0 rows ingested).
- Closure engine item 6 (RX50_G4_CLOSURE_ENGINE.md): MEASUREMENT PENDING.
- Owner/operator action required before T-G4-06 execution: select element value within ≤ ±5 mA, physically verify in F3, record this file completely (start pack 1.2/1.3/1.6 + owner record 2026-08-15: "MUST be verified BEFORE T-G4-06 execution").

## Rules

- This record may be updated to VERIFIED only when actual physical verification evidence exists in the repository.
- A resistor value in a decision document, a calculated current, or a datasheet value is NOT physical verification.
- T-G4-06 execution is NOT authorized by this record.
