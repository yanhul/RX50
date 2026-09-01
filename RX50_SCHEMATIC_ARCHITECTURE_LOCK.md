# RX50 SCHEMATIC ARCHITECTURE LOCK

Status: **NOT LOCKED / BLOCKED** — prerequisites missing
Date: 2026-08-15
Batch: RX50 SCHEMATIC CLOSURE BATCH (Phase D input)
Rule: architecture is NOT locked on missing evidence. Nothing in this file is an architecture decision.

## Gate status

| PREREQUISITE | STATUS | WHY BLOCKING |
|---|---|---|
| G4 evidence (T-G4-01..06) | MEASUREMENT PENDING | no raw data received; RON@3.3V / settling / leakage / isolation unknown |
| Topology A/B decision | UNDECIDED | measurement-gated; owner decision required after data |
| G5 pin-map closure | PROVISIONAL / NOT LOCKED | downstream of G4 (owner direction: close G4 first) |
| G1 requirements (R-01..R-04) | OPEN / TBD | owner fill sheet not answered |
| G2 firing-power requirements | HOLD | depends on G1 |

## What would need to be locked before schematic architecture (deferred)

- Continuity MUX topology (A/B) and its ADC allocation. [DEFERRED]
- Firing-power rail architecture, protection, thermal, current-path constraints. [DEFERRED — G1/G2]
- Pin-map / GPIO / ADC / OE / INH allocation. [DEFERRED — G5 after G4]
- Sheet hierarchy and component/function allocation. [DEFERRED]

## Statement

The schematic architecture is NOT locked and will not be locked until: (1) G4 is evidence-backed, (2) topology A/B is owner-decided, (3) G5 pin map is closed, (4) G1/G2 requirements are owner-supplied and evidence-backed. No architecture conclusion is drawn in this batch. [STATUS]

---

G4 = MEASUREMENT PENDING | G1/G2 = HOLD | G5 = PROVISIONAL / NOT LOCKED