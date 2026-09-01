# RX50 G1 REQUIREMENTS ELICITATION PLAN

Status: PLAN FOR OWNER APPROVAL — G1 remains HOLD until requirements are captured
Date: 2026-08-15
Purpose: structured capture of G1 (firing-power domain) OWNER REQUIREMENTS. This plan does NOT create requirements; it only defines what must be captured and how. No firing number is invented. G1/G2 conclusions are NOT touched. No architecture is locked.

## 1. Why G1 is on HOLD

- Firing-power subsystem = FEASIBILITY HOLD (OPEN_ISSUES #1/#2). [STATUS]
- The actual simultaneous-load envelope and simultaneous-load requirements have not been locked. [FACT from PROJECT_CONTEXT]
- RX50 MUST NOT assume a firing-power design is validated. [FACT]
- Old RX24 `MAX_CONCURRENT_FIRE = 1` is obsolete for RX50 (DECISIONS.md). [FACT]
- Old firing current/pulse/power assumptions are NOT valid unless re-established from requirements/evidence. [FACT]

## 2. Scope of G1 (what the owner must define)

G1 closes when the owner provides explicit requirements (or approved measured/datasheet evidence) for the following. Each item is a REQUIREMENT CAPTURE FIELD — values come from the owner, not from engineering inference.

| # | REQUIREMENT FIELD | STATUS NOW | REQUIRED OWNER INPUT |
|---|---|---|---|
| R-01 | Maximum number of channels that may fire simultaneously | HOLD / TBD | explicit number or bound (owner requirement) |
| R-02 | Simultaneous load envelope (source capability, per-channel load, current paths) | HOLD / TBD | requirement or measured/datasheet evidence |
| R-03 | Pulse parameters (current, width, energy, voltage) | HOLD / TBD | requirement or validated load datasheet |
| R-04 | "Simultaneous" definition (event window, allowable skew budget) | HOLD / TBD | explicit timing semantics (G1 owns timing) |
| R-05 | Firing-power rail architecture constraints | HOLD / TBD | requirement/evidence |
| R-06 | Transient behavior and protection requirements | HOLD / TBD | requirement/evidence |
| R-07 | Thermal constraints for firing operation | HOLD / TBD | requirement/evidence |
| R-08 | PCB current-path / distribution / grounding constraints | HOLD / TBD | requirement/evidence |
| R-09 | Fault isolation behavior under multi-channel firing | HOLD / TBD | requirement/evidence |
| R-10 | Simultaneous activation authorization (interface to G6 interlock) | HOLD / TBD | owner evidence (G6-relevant) |

## 3. Requirements capture template

Each captured requirement uses this record (filled by owner/evidence, never by guess):

| FIELD | CONTENT |
|---|---|
| REQ_ID | e.g., G1-R-01 |
| STATEMENT | verbatim owner requirement or exact evidence quote |
| SOURCE | owner decision / datasheet / measurement / standard (with revision/table) |
| VALUE(S) | numeric content ONLY if provided by the source; otherwise "TBD" |
| UNIT | |
| CONDITION | applicability condition (e.g., temp, supply) |
| STATUS | PROPOSED / APPROVED / REJECTED / NEEDS RECHECK / TBD |
| SIGN-OFF | owner approval date + name |
| DEPENDENCY | e.g., feeds G2 feasibility; feeds G6 interlock |

## 4. Elicitation process (no design work)

1. Owner states R-01..R-10 (or delegates specific evidence search: validated load datasheets, standards, measurements). [OWNER]
2. Engineering classifies each answer as FACT (source-provided) vs ASSUMPTION (never a requirement). [CONSTRAINT]
3. Any number not traceable to a source is marked TBD / NEEDS RECHECK. No number is filled from intuition. [CONSTRAINT]
4. Captured requirements are consolidated in a G1 REQUIREMENTS REGISTER (once the owner approves the first capture). [RECOMMENDATION]
5. G1 leaves HOLD only when the owner signs off the requirement set (R-01..R-10). G2 (firing-power feasibility) may then open. [RECOMMENDATION]

## 5. Hard constraints

- No firing voltage/current/pulse/energy/skew invented. [CONSTRAINT]
- No MAX_CONCURRENT_FIRE=1 reintroduced. [CONSTRAINT]
- No G1/G2 conclusion drawn in this plan. [CONSTRAINT]
- No firing design / rail / component selection in this plan. [CONSTRAINT]
- G4 measurement continues independently (not blocked by G1). [STATUS]

## 6. Recommended next action

- Owner responds to the R-01..R-10 fields (partial answers allowed; rest stay TBD). [OWNER]
- On owner approval, this plan becomes the G1 REQUIREMENTS REGISTER and G2 opens as a feasibility batch using only signed requirements. [RECOMMENDATION]

---

G1 = HOLD (awaiting requirements capture)
G5 = NOT LOCKED
G4 = MEASUREMENT PENDING (independent track)