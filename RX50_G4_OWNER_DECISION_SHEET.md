# RX50 G4 OWNER DECISION SHEET (CONSOLIDATED)

Status: COMPLETE (Part I of batch G4-MEAS-BATCH-01)
Date: 2026-08-15
Rule: consolidated single sheet; the same information is not asked twice. Minimum information needed to physically start = GROUP 1 only.

## GROUP 1 — REQUIRED BEFORE MEASUREMENT

| # | DECISION | DEFAULT IF NOT SUPPLIED | STATUS |
|---|---|---|---|
| 1.1 | Fixture approach (F1/F2/F3 topology-level build approval) | approved by default (topology level only) | OWNER DECISION REQUIRED |
| 1.2 | Test resistor values (calibrated, to be recorded; OWNER TEST VALUE - TBD) | must be supplied or operator-selected + recorded | OWNER DECISION REQUIRED |
| 1.3 | ITEST for T-G4-01 (bounded by DUT absolute max; value owner/operator, recorded) | operator-selected within datasheet bounds + recorded | OWNER DECISION REQUIRED |
| 1.4 | Temperature coverage (ambient only vs approved soak + duration) | ambient only, recorded | OWNER DECISION REQUIRED |
| 1.5 | DUT sample count (single = characterization; multiple = sample characterization) | single unit | OWNER DECISION REQUIRED |
| 1.6 | Available instruments (IDs + calibration status) | operator logs available set | OWNER DECISION REQUIRED |

## GROUP 2 — OPTIONAL / CHARACTERIZATION (execution allowed without these)

| # | DECISION | IF NOT SUPPLIED |
|---|---|---|
| 2.1 | Settling threshold (mV or bits band for T-G4-04) | characterization-only execution (explicitly allowed) |
| 2.2 | Isolation threshold (T-G4-06) | characterization-only execution (explicitly allowed) |
| 2.3 | Continuity threshold (T-G4-03 accuracy target) | results reported per point; PASS/FAIL = NOT AVAILABLE |
| 2.4 | Engineering margin on RTH + RON + RTRACE < 10 k (T-G4-01) | NO margin applied; datasheet 10 k used as-is |

## GROUP 3 — NOT REQUIRED NOW

- G5 pin-map locking and topology selection (downstream; blocked by G4).
- G1/G2 conclusions; firing power/current/pulse/energy/skew values.
- Schematic, PCB, BOM, final divider/resistor design values, connector selection.
- Any cross-gate decision not driven by G4 data.

## Start condition

Physical measurement may begin when GROUP 1 (1.1-1.6) is answered/recorded. GROUP 2 defaults permit characterization-only execution with zero added input. GROUP 3 is explicitly deferred. [RECOMMENDATION]