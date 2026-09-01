# RX50 FIRING DESIGN PROPOSAL — SINGLE REVIEW PACKAGE

Status: FOR OWNER REVIEW / NOT APPROVED
Date: 2026-08-15
Contains: A) firing control architecture, B) G2 firing-power feasibility outline, C) simultaneity + dry-fire test approach, D) proposed DECISIONS.md entries, E) proposed OPEN_ISSUES.md entries.

This file is the single consolidation point for owner approval. No schematic/PCB/BOM. No firing numbers invented. Nothing here is a decision until approved.

Label legend: [FACT] [CALCULATION] [ASSUMPTION] [RECOMMENDATION]
Status: LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK / OPEN / PROVISIONAL / CLOSEABLE

---

## 0. Baseline delta (RX24 -> RX50) relevant to firing

| RX24 baseline | RX50 delta | Implication | Status |
|---|---|---|---|
| MAX_CONCURRENT_FIRE = 1 | simultaneous multi-channel firing required/evaluated | concurrency model must be re-derived, not reused | MODIFY |
| old firing current/pulse/energy assumptions | NOT valid unless re-established from requirements/evidence | no numbers carried forward | REPLACE/TBD |
| 24-channel firing timing estimate | 50 channels | needs recalculation from evidence | NEEDS RECHECK |
| firing-power subsystem "FEASIBILITY HOLD" | unchanged | load envelope + simultaneity still unlocked | HOLD |
| IRLML6344 output MOSFET baseline | re-verify for simultaneous multi-channel current | thermal + parallel-current evidence required | NEEDS RECHECK |
| safety/interlock via logic gates + MCU arm path | keep concept; re-verify multi-channel authorization | no single-point failure; firmware not sole gate | MODIFY |

Rule 6 respected: RX24 single-channel concurrency is NOT reintroduced. [FACT]

---

## A. Firing control architecture (structural, G1-number-independent)

### A.1 Command chain (separation of control plane / power plane)
- Chain: G1 requirement -> G8 authorization -> G6 interlock -> G3 SR + OE blanking -> power switch. [RECOMMENDATION]
- Firmware is never the sole gate for output enable. [RECOMMENDATION]
- Each stage is independently verifiable in dry-fire test (Section C). [RECOMMENDATION]

### A.2 Hardware blanking & interlock
- OE = hardware blanking, gated by interlock (NOT MCU-direct). [RECOMMENDATION, consistent with G3/G6]
- Goal: a single firmware fault cannot cause unintended firing; no single-point failure can block a commanded fire. [ASSUMPTION, to be validated]
- Storage register of SN74HC595 is undefined at power-up -> OE-high (outputs disabled) is mandatory on reset. [FACT -> design constraint]

### A.3 Simultaneity principle
- Single RCLK edge updates all 56 latch bits simultaneously -> command simultaneity at register level. [FACT/CALCULATION, G3]
- Physical simultaneity at the load depends on 4 contributors that must be MEASURED, not assumed: (a) RCLK alignment, (b) gate-driver propagation delta, (c) switch rise-time delta, (d) rail sag. [ASSUMPTION -> measurement]
- No per-channel timed stagger (that would recreate RX24 serialization). [RECOMMENDATION, rule 6]

### A.4 Power delivery shape
- Common rail + per-channel switch -> simultaneity does not depend on per-channel supply. [RECOMMENDATION]
- Separate return paths: measurement/continuity return vs firing return. [RECOMMENDATION]
- Kelvin sensing proposed for threshold feedback (continuity). [ASSUMPTION]

### A.5 Sequenced control (firmware, G9 state machine)
- Mandatory sequence: BOOT -> SAFE -> ARM_REQUEST -> ARMED -> FIRE_AUTHORIZED -> FIRE_EXECUTION -> POST_FIRE -> FAULT sink. [RECOMMENDATION, consistent with G9]
- Authorization window, stale/duplicate window, RF-loss handling: values owned by G1. [OPEN]

---

## B. G2 firing-power feasibility outline (symbolic only; numbers HOLD)

All expressions are symbolic; inputs must come from G1 requirement / datasheet / measurement. No value is asserted here.

### B.1 Source capability
- P_fire_total = N_fire_max x I_fire x V_fire   [CALCULATION]
- Inputs required from G1: N_fire_max, I_fire per channel, V_fire, pulse duration/shape, duty/recovery time. [OPEN]

### B.2 Rail architecture
- Common rail + per-channel switch (Section A.4). [RECOMMENDATION]
- Rail transient: dV_rail = I_total x (R_source + R_trace); source impedance from power-path datasheet/measurement. [CALCULATION]

### B.3 Protection & fault isolation
- Per-channel protection (e.g., switch fault lockout) and overcurrent mechanism to be defined once G1 values exist. [OPEN]
- Fault taxonomy from G6 applies; no values invented. [FACT -> OPEN]

### B.4 Distribution / PCB current paths
- Copper cross-section requirement: A >= (I_total x L) / (sigma x dV_max)   [CALCULATION]
- Separate power/return routing; kelvin sensing. [RECOMMENDATION]

### B.5 Thermal
- Per-channel MOSFET dissipation: Pd = I_fire^2 x RDS(on)   [CALCULATION]
- Thermal budget requires G1 firing pattern (simultaneous group + recovery). [OPEN]
- IRLML6344 baseline re-verification needed for simultaneous group current. [NEEDS RECHECK]

### B.6 Status
- Feasibility cannot be concluded without G1 load envelope. Firing-power remains FEASIBILITY HOLD. [HOLD]
- The symbolic framework above is CLOSEABLE NOW as structure. [RECOMMENDATION]

---

## C. Simultaneity + dry-fire test approach

### C.1 Definition gap (owner decision)
- "Simultaneous" must be defined by G1: (i) simultaneous command edge, or (ii) load reaching threshold within skew X. Two different physical meanings. [OPEN]

### C.2 Dry-fire harness (no load)
- Objective: verify command chain, interlock, blanking, and timing without firing current. [RECOMMENDATION]
- Measures: RCLK edge alignment across shift registers, OE blanking propagation, state-machine sequencing, fail-safe on fault injection. [ASSUMPTION]

### C.3 Hot-fire qualification (with load, after G1 numbers)
- Objective: record per-channel timing simultaneously to prove skew meets spec. [RECOMMENDATION]
- Test IDs, pass/fail criteria: TBD until G1 supplies skew budget. [OPEN]

### C.4 Proposed test list

| TEST ID | OBJECTIVE | SETUP | MEASUREMENT | PASS/FAIL CRITERION | DEPENDENCY |
|---|---|---|---|---|---|
| T-F-01 dry-fire | command chain + interlock | command via G8, observe OE/state | sequence + OE timing | TBD (owner) | firmware skeleton |
| T-F-02 dry-fire | RCLK alignment across 7x HC595 | scope on all RCLK | edge-to-edge skew | TBD (owner) | hardware prototype |
| T-F-03 dry-fire | blanking fail-safe on fault injection | inject fault, observe OE | OE asserted | TBD (owner) | interlock wiring |
| T-F-04 hot-fire | per-channel simultaneity | simultaneous command, record all channels | skew vs spec | TBD (G1 skew) | G1 numbers |
| T-F-05 hot-fire | rail sag under simultaneous group | fire N channels, scope rail | dV_rail | TBD (G1) | G1 numbers |

- No firing threshold invented; criteria TBD where no requirement exists. [CONSTRAINT respected]

---

## D. Proposed DECISIONS.md additions (for owner approval)

Proposed new entries to add to DECISIONS.md if approved:

1. Firing control uses a segmented command chain: requirement -> authorization -> interlock -> SR+OE blanking -> power switch; firmware is never the sole gate. [RECOMMENDATION]
2. OE/blanking is hardware-gated by interlock, not MCU-direct; outputs default OFF on reset (storage register undefined at power-up). [RECOMMENDATION]
3. Simultaneity is native via single RCLK edge; no per-channel timed stagger; RX24 single-channel concurrency stays obsolete. [RECOMMENDATION]
4. Power delivery: common rail + per-channel switch; separate measurement/firing return paths. [RECOMMENDATION]
5. "Simultaneous" definition (command-edge vs threshold-within-skew) must be locked by G1 before G2 closure. [OPEN]
6. G2 feasibility framework (Section B) approved as symbolic structure; numeric closure deferred to G1 load envelope. [HOLD]

## E. Proposed OPEN_ISSUES.md additions (for owner approval)

Proposed new/updated entries:

1. (NEW) Simultaneity definition + skew budget: OWNER/G1. Blocking hot-fire qualification. [HOLD]
2. (NEW) Dry-fire harness + T-F-01..03 can proceed independent of G1. [CLOSEABLE]
3. (UPDATE Issue 2 firing-power) add symbolic framework reference; keep FEASIBILITY HOLD. [HOLD]
4. (UPDATE Issue 8 safety) add: single firmware fault must not enable outputs; no single-point failure blocks a commanded fire. [OPEN]

## F. Items requiring owner/G1 decision (explicit, no numbers invented)

1. Define "simultaneous": command-edge vs threshold-within-skew. [OPEN]
2. G1 load envelope: N_fire_max, I_fire, pulse shape/energy, V_fire, recovery time. [HOLD]
3. Skew budget for hot-fire qualification. [HOLD]
4. Authorization window / stale / duplicate / RF-loss timeout values. [OPEN]
5. Continuity threshold + isolation spec (G4, separate from firing). [OPEN]

## G. Status summary

- CLOSEABLE NOW (structure only): control chain, blanking/interlock principle, native simultaneity principle, symbolic G2 framework, dry-fire harness.
- HOLD: any firing number, skew budget, simultaneity definition, rail sag target.
- NOT decided: topology finalization (G4), pin map (G5), OE wiring (G6) — those remain with their own gates.
- Nothing in this package requires modification of source context files until owner approves Sections D/E.

---

END OF REVIEW PACKAGE