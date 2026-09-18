# RX50 Phase 2 Evidence Closure

**Baseline:** `977b35014d7b7e01c56627894103bc95216befde`

**Worker status:** Evidence/engineering substrate only. No topology, schematic, PCB, or BOM decision is locked by this document.

## Scope and authority

This closure uses the canonical repository sources listed in the Phase 2 task. The repository remains fail-closed: candidate maps are not final maps, measurements are not inferred, and owner decisions remain outside worker authority.

## C-05 — SR control GPIO count

**Old state → new state:** `OPEN — 4–5 vs 3–4` → `OPEN — signal count corrected; pin allocation unresolved`.

**Verified evidence:** `RX50_G4_G5_CLOSURE_AUDIT.md` §9.1 and §13 state that a SN74HC595 requires **three mandatory MCU-controlled signals** (`SER`, `SRCLK`, `RCLK`) plus **optional `SRCLR`**, hence 3–4 MCU GPIOs. `OE` is hardware-interlock-owned and is not an MCU GPIO. `RX50_S03_OUTPUT_LOGIC.sch` repeats `SR_SER`, `SR_SRCLK`, `SR_RCLK`, `SRCLR`, and states that OE is hardware-interlock-owned.

The repository does **not** contain a locked RX50 pin allocation: `RX50_G5_PIN_MAP_FINAL.md` explicitly says G5 is provisional, and `RX50_SCHEMATIC_NET_REGISTER.md` is empty. The audit's PB3–PB5 and candidate allocations are conditional/provisional, not authoritative locked assignments.

**Verification:** regression coverage asserts the 3–4 signal rule, hardware-owned OE, and non-locked G5/net-register state. C-05 remains open pending owner-approved G5 pin-map evidence and G6 OE wiring evidence.

## C-06 — USART RX interrupt

**Old state → new state:** `OPEN — EXTI vs NVIC` → `RESOLVED — USART RX uses NVIC USART RXNE; EXTI is reserved for external interrupt sources`.

**Evidence:** `RX50_G4_G5_CLOSURE_AUDIT.md` §16 and error register E-06 explicitly correct the stale statement. `RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md` §5.2 states that RS485 RX is interrupt-driven through `USART RXNE`; §7 identifies EXTI for DIO0 and NVIC for USART RX. The same audit identifies DIO0 and fault/arm as EXTI candidates. This is an architectural interrupt classification, not a claim that firmware implementation exists.

**Verification:** regression coverage checks the authoritative NVIC/RXNE wording and prevents the stale `USART RX`-as-EXTI wording from being treated as current. The historical contradiction is retained as provenance in the contradiction register.

## C-21 — SN74HC595 timing at 3.3 V

**Old state → new state:** `NOT A CONTRADICTION / evidence gap` → `EVIDENCE GAP — 3.3 V timing guarantee absent`.

The repository records timing values at 4.5 V (and the task notes tabulated 2 V/4.5 V/6 V conditions), but no authoritative guaranteed timing row at the RX50 3.3 V operating point is present. Interpolation is not a guaranteed specification. The smallest reproducible closure path is either: (1) obtain an authoritative manufacturer guarantee explicitly covering 3.3 V and the required timing rows, or (2) measure the actual RX50 operating configuration at 3.3 V, recording supply, temperature, load, edge thresholds, `SER`, `SRCLK`, `RCLK`, `SRCLR`, and observed setup/hold, pulse-width, propagation, and maximum reliable clock results. Until then C-21 is not VERIFIED.

## C-20c — CD4067 leakage

**Old state → new state:** `UNRESOLVED — 3.3/5 V measurement missing` → `MEASUREMENT REQUIRED — no physical result exists`.

The datasheet values recorded in the repository are conditions/bounds, not RX50 operating-point measurements. The 18 V maximum/bound must not be transferred to 3.3 V or 5 V. T-G4-05 requires, separately at 3.3 V and 5 V, per-channel OFF leakage for every channel, aggregate all-OFF leakage, common-node voltage shift with the actual sense impedance, supply current, temperature, instrument/range, uncertainty, and fixture-only leakage baseline. A 5 V test must isolate/protect the STM32 ADC path so the ADC VIN limit is not exceeded. No pass/fail conclusion is permitted until an owner leakage requirement and the physical data exist.

## C-20b — logic-level contradiction and owner packet

**Old state → new state:** `CONTRADICTION — resolution required; underlying source was described as absent` → `VERIFIED INTERFACE INCOMPATIBILITY — owner decision required; topology not selected`.

Repository evidence records STM32 VOH minimum as `VDD - 0.4 V` under the cited condition, giving 2.9 V at 3.3 V, and CD4067 VIH at 5 V as 3.5 V. Therefore `VOH guaranteed < VIH required`; direct 3.3 V MCU drive cannot be guaranteed to meet a 5 V CD4067 input. This establishes an interface incompatibility, not merely an open research question. It does not select a remedy. The separate 5 V-referenced sense-node-to-ADC exposure remains an independent owner mitigation decision and must be closed before any 5 V fixture run.

### Decision matrix — no winner selected

| Option | Required evidence | Affected circuitry | Verification required | Unresolved risks | Downstream gates |
|---|---|---|---|---|---|
| A — level shift STM32 → CD4067 | Translator datasheet; VOH/VIH source conditions; delay at 3.3/5 V | Address/control lines; PCB area and power | Logic-high/low margins, timing at 3.3 V, scan timing, reset/fault behavior | Added part, propagation delay, availability; ADC exposure remains | G4, G5, G6, G9, G10 |
| B — CD4067 at 3.3 V | Guaranteed VIH/VIL and leakage/RON at 3.3 V; actual continuity requirements | MUX supply, analog path, address lines | VIH/VIL, RON, leakage, settling, ADC accuracy | 3.3 V RON/settling and signal range not guaranteed | G4, G5, G6, G10 |
| C — replace with 3.3 V-compatible mux | Candidate datasheet, availability, pin/channel and electrical comparison | BOM, schematic, layout, firmware assumptions | Full replacement characterization: logic, RON, leakage, settling, ADC path | New component risk and topology re-review | G3, G4, G5, G6, G7, G10 |
| D — level shift + ADC/sense mitigation | All A evidence plus divider/clamp/buffer evidence and ADC limits | Control path and common-I/O sense path | Logic margins, ADC VIN protection, ratio/accuracy, fault injection, leakage/settling | Highest complexity; added error and failure modes | G4, G5, G6, G7, G9, G10 |

**Separate 5 V → STM32 ADC exposure:** owner must choose and evidence either a sense-node divider/clamp that keeps ADC VIN within the verified limit, or a topology that prevents the 5 V node from reaching the ADC common-I/O path. This document does not choose either mitigation.

## Classification summary

| Item | Classification | Closure condition |
|---|---|---|
| C-05 | OPEN | Owner-approved G5 pin map plus G6 OE wiring evidence |
| C-06 | VERIFIED / RESOLVED | Regression invariant and canonical audit/G9 provenance |
| C-21 | EVIDENCE GAP | 3.3 V manufacturer guarantee or reproducible measurement |
| C-20c | MEASUREMENT REQUIRED | Physical T-G4-05 results at intended conditions plus owner limit |
| C-20b | VERIFIED INTERFACE INCOMPATIBILITY / DECISION REQUIRED | Owner selects and authorizes an option and separately closes ADC exposure |

## Topology and hardware validation

**Topology:** NOT LOCKED.

**Datasheet verified:** repository-registered manufacturer facts cited above, subject to the source/revision references in `evidence/EVIDENCE_REGISTER.md`.

**Analytically verified:** signal count (3–4), `VOH < VIH` comparison, and decision dependencies.

**Simulated:** none claimed.

**Physically measured:** none for C-20c, C-21, or the RX50 circuit. No physical validation claim is made.

**Still unknown:** C-05 final pins, C-21 3.3 V guarantee, C-20c operating-point leakage, C-20b owner option, ADC exposure mitigation, G1/G2 load envelope, and all owner acceptance thresholds.
