# RX50 BATCH ENGINEERING REPORT

Status: DRAFT (batch phase 7 output)
Date: 2026-08-15
Scope: RX24 -> RX50 delta engineering, evidence-first.

Label legend:
- [FACT]           Manufacturer / datasheet / explicit requirement evidence.
- [CALCULATION]    Arithmetic derived from inputs above; valid only if inputs are valid.
- [ASSUMPTION]     Engineering assumption. NOT a requirement.
- [RECOMMENDATION] Proposed direction; requires owner approval.
- LOCKED / EVIDENCE-BACKED / HOLD / TBD / NEEDS RECHECK per DECISIONS.md.

---

## 1. Executive summary

- RX50 target is 50 output channels with simultaneous multi-channel firing capability as a requirement to be evaluated. The old RX24 `MAX_CONCURRENT_FIRE = 1` constraint is obsolete and is NOT carried forward.
- No firing-power value (current, pulse width, energy, voltage, timing tolerance) is currently specified. Every item that depends on the simultaneous-load envelope (firing-power subsystem, MOSFET output stage, power distribution, PCB current paths, thermal, command semantics, safety authorization) is therefore **HOLD** until G1 closes.
- Evidence-first inventory of the baseline components is complete. Architecture-level scaling quantities (MUX count, shift-register count, GPIO budget) are **CALCULATION**s under an explicit **ASSUMPTION** of 1:1 fan-out; they are candidates, not decisions.
- The design is NOT validated for any firing-power scenario. Continuity measurement feasibility depends on CD4067 on-resistance vs the ADC drive requirement; the RX24 concerns (ADC source impedance, leakage, settling) remain and are now quantified against datasheet limits.
- Gate map: G1 (load envelope, master gate, HOLD), G2 (firing-power, HOLD), G3 (output expansion), G4 (continuity), G5 (MCU+pin map), G6 (safety/interlock), G7 (PCB/connectors), G8 (protocol/command semantics), G9 (firmware), G10 (test/validation).
- Master gates that must close before schematic/PCB: G1, G2, G3, G4, G5, G6, G8.

## 2. RX24 baseline (as documented, NEEDS RECHECK per item)

Source: PROJECT_CONTEXT.md lines 23-49. Baseline, NOT automatically valid for RX50.

- MCU: STM32F103C8T6, LQFP48.
- LoRa: SX1278 / Ra-02.
- RS485: MAX3485.
- Input: 3S Li-ion, nominal range "previously treated as" 9.0-12.6 V (PROVISIONAL).
- Reverse-polarity protection: AO4407A P-MOS.
- Input TVS: SMBJ15CA.
- Logic rail: TPS562201 -> 3.3 V.
- Output MOSFET baseline: IRLML6344.
- Output expansion baseline: 74HC595 shift registers.
- Continuity MUX baseline: CD4067.
- Safety/interlock: dedicated logic gates + MCU-controlled arm path; outputs default OFF on reset/power loss/firmware fault/RF loss.
- Continuity subsystem (RX24): per-channel divider + post-MUX ADC network; ADC source impedance flagged as a design concern; CD4067 leakage and settling flagged; scan timing revised conservatively during RX24 review.

RX24 decision status for RX50 (DECISIONS.md):
- KEEP as baseline concept (re-verify): STM32F103C8T6, SX1278/Ra-02, MAX3485, 74HC595 expansion concept, CD4067 continuity concept, dedicated HW safety/interlock, 3.3 V logic rail.
- NOT carried forward: MAX_CONCURRENT_FIRE=1; any old firing-current/pulse assumption; any old simultaneous-load power budget; any old 24-channel timing estimate.

## 3. RX50 proposed architecture (draft, gates G1/G2 pending)

- [RECOMMENDATION] Output expansion: chain of 74HC595 shift registers, one register drives one output channel (high-side or low-side stage). Simultaneous channel update via LATCH/STROBE and a hardware OE/blanking path consistent with default-OFF safety behavior.
- [RECOMMENDATION] Continuity: CD4067-based 16:1 multiplexing with 4 MUX devices + shared address/select lines, ADC on post-MUX sense node.
- [RECOMMENDATION] MCU: STM32F103C8T6 retained as baseline candidate (needs G5 pin/RAM/flash re-check for 50 channels).
- [RECOMMENDATION] Communications: SX1278 LoRa + MAX3485 RS485 retained; protocol needs G8 re-check for 50-channel addressing and simultaneous-command handling.
- [RECOMMENDATION] Power: input protection (AO4407A reverse polarity, SMBJ15CA TVS), TPS562201 -> 3.3 V logic rail. Firing-power rail architecture: HOLD until G1/G2.
- [HOLD] Output MOSFET stage, per-channel drive, firing current path, distribution, thermal, grounding: all pending G1/G2 numbers.

## 4. KEEP / MODIFY / REPLACE / TBD (per delta-review scope, PROJECT_CONTEXT.md lines 51-65)

| # | Area | Class | Notes |
|---|------|-------|-------|
| 1 | Output expansion 24 -> 50 | MODIFY | G3; count must scale, see section 6. |
| 2 | Shift-register count, cascade, OE, reset, simultaneous update | MODIFY/NEEDS RECHECK | G3; scan ratio ~2.08x vs 24ch; simultaneous update via latch/OE to be designed (G3). |
| 3 | MCU resource allocation & firmware channel map | NEEDS RECHECK | G5; see section 6 GPIO budget; RAM/flash for 50-ch state map TBD. |
| 4 | Continuity MUX for 50 channels | MODIFY | G4; see sections 5-6; CD4067 RON vs ADC drive is the key feasibility item. |
| 5 | Firing-power subsystem & simultaneous capability | TBD/HOLD | G1/G2 master gates. No numbers exist. |
| 6 | Protection, distribution, grounding, PCB current paths | TBD/HOLD | G2/G7; depends on G1. |
| 7 | Connectors & mechanical channel grouping | TBD | G7; 50-ch grouping undecided. |
| 8 | RF/RS485 protocol capacity & channel addressing | NEEDS RECHECK | G8. |
| 9 | Firmware state machine, faults, simultaneous command handling | NEEDS RECHECK | G9. |
| 10 | Safety/interlock under multi-channel | NEEDS RECHECK | G6; requires explicit simultaneous-activation authorization rule. |
| 11 | Test & validation | TBD | G10; must be derived from G1 once closed. |

## 5. Evidence table (component-level)

All entries below are [FACT] from official manufacturer documentation unless noted. Provenance recorded; PDF fetch returned binary, so section/page quotes are from extracted search hits — verify against downloaded PDF before pinning a reference.

| Component | Manufacturer doc | Key evidence [FACT] |
|-----------|------------------|---------------------|
| CD4067B (16:1 MUX) | TI SCHS052D Rev D (Jun 2003 - Aug 2024) | RON typ 125 ohm @ VDD-VSS=15V; RON max 1050 ohm @5V / 400 ohm @10V / 240 ohm @15V (25 C); RON rises with temperature; **RON @ 3.3V NOT SPECIFIED**; OFF-state leakage +-100 nA (25 C) / +-1000 nA (85-125 C) @18V, +-10 pA typ @10V; CIS 5 pF; COS 55 pF; BW 14 MHz; **VIH @5V = 3.5V -> 3.3V logic cannot drive a 5V-powered CD4067 to guaranteed VIH**; settling time only typical curves, NO guaranteed value; charge injection NOT SPECIFIED. |
| STM32F103C8 | ST DS5319 Rev 20, Sec 5.3.18 (Tables 47/48/49, Eq.1) | ADC: RADC 1 kohm; CADC 8 pF; sampling time tS 1.5-239.5 cycles (0.107-17.1 us @14 MHz); conversion tCONV 14-252 cycles (1-18 us); max source impedance RAIN 50 kohm @ tS=55.5 cyc/fADC=14 MHz; **accuracy +-2 LSB max ET guaranteed only when RAIN < 10 kohm**; VREF+ internally tied to VDDA on LQFP48; 2x 12-bit ADC, 10 external channels (PA0-PA7, PB0, PB1). |
| SN74HC595 | TI Rev J | 8-bit shift register + 3-state output register; shift clock 24 MHz (typical family limit); IOL/IOH +-7.8 mA max (HC @VCC=6V); latch/STROBE + OE for simultaneous output update. |
| IRLML6344 | Infineon StrongIRFET (SOT-23) | 30 V N-ch; VGS(th) 0.5-1.1 V; RDS(on) ~22/29 mOhm typ @VGS=4.5V (single-drain vs pulsed references differ — verify exact table before BOM). |
| SX1278 | Semtech | LoRa transceiver 137-525 MHz. |
| MAX3485 | Analog Devices (TI/ADI) | 3.3 V RS-485 transceiver, up to 10 Mbps. |
| TPS562201 | TI Rev D | 4.5-17 V input, 2 A synchronous buck, D-CAP2, SOT-23. |
| AO4407A | Alpha & Omega Semi | 30 V P-ch MOSFET; DigiKey listing: 12 A @ Ta, 3.1 W — verify against AOS datasheet before BOM. |
| SMBJ15CA | Littelfuse | Bidirectional TVS, 15 V standoff, 24.4 V max clamp, SMB package. |

Evidence conflicts / gaps to report (not silently resolved):
- CD4067 RON @3.3V: NOT SPECIFIED by manufacturer. If CD4067 is powered at 3.3V, RON is unknown; if powered at 5V, 3.3V logic VIH is not met. Either path needs a level-shifter or a different MUX (e.g., a 74HC-style analog switch or powered-at-3.3V device with specified RON). Recommendation to evaluate on hardware.
- STM32 ADC accuracy vs RAIN: full +-2 LSB ET requires RAIN < 10 kohm; the CD4067 RON (minimum 125 ohm typ at 15V, likely higher at 3.3V) plus divider source resistance must satisfy this, or accuracy degrades (TBD by measurement).

## 6. Calculations

[ASSUMPTION] All quantities here assume 1:1 fan-out of RX24 baseline concepts (one MUX/register stage per channel; no channel sharing within one MUX path). Not a decision.

- CD4067 MUX count: ceil(50 / 16) = 4 [CALCULATION].
- 74HC595 register count: ceil(50 / 8) = 7 [CALCULATION].
- Continuity scan ratio vs RX24 24-ch: 50 / 24 ~= 2.08x [CALCULATION]. Per-ch scan time must be re-derived, NOT scaled from RX24 (PROJECT_CONTEXT.md line 44).
- GPIO budget for 4 MUX (continuity): shared address bus = 4 address + 4 enable = 8 GPIO; independent addressing = 16 GPIO [CALCULATION, ASSUMPTION]. Plus 7 SR: 3-5 GPIO (SER/SRCLK/RCLK/OE/optional latch) [CALCULATION, ASSUMPTION]. Feasible within STM32F103C8 GPIO budget but final allocation is G5.
- ADC channels needed: 1 (post-MUX sense) plus optional per-rail monitor; the 10 external channels on LQFP48 are ample [CALCULATION].
- ADC source impedance feasibility: requirement RAIN < 10 kohm for +-2 LSB ET [FACT]. CD4067 RON @3.3V unknown [FACT]; divider + RON total must be measured/verified <= 10 kohm, or accuracy claim dropped [ASSUMPTION -> TBD].

## 7. Assumptions (explicit, non-authoritative)

- A1: 1:1 fan-out scaling of 74HC595 and CD4067 concepts is structurally acceptable (no architecture change forced by 50 vs 24 count). Must be confirmed in G3/G4.
- A2: 3S Li-ion 9.0-12.6 V input range carried as PROVISIONAL only; re-verified at power design.
- A3: Continuity sense network can be designed to RAIN < 10 kohm at the ADC. Unverified; requires hardware measurement (CD4067 RON @3.3V).
- A4: Default-OFF and OE/blanking safety behavior remains valid for 50 channels. Pending G6 review of simultaneous authorization.
- A5: No assumption is made about any firing current, pulse, energy, voltage, or timing value. G1 is open by definition.

## 8. Risks

- R1 (HIGH): G1 open -> firing-power design unconstrained. Any schematic work now could be invalidated. Gate before schematic.
- R2 (HIGH): CD4067 RON @3.3V unspecified + VIH mismatch at 5V. Level-shift or MUX change may be required; affects G4 topology.
- R3 (MEDIUM): ADC accuracy not guaranteed unless RAIN < 10 kohm; continuity threshold validity depends on measurement. Verify on hardware.
- R4 (MEDIUM): simultaneous-update behavior of SR chain (glitch on partial shift) interacts with safety interlock; must be reviewed in G6/G9.
- R5 (MEDIUM): protocol/address space and RF packet timing for 50 channels unverified (G8).
- R6 (LOW-MED): thermal/PCB current paths unresolved until G1/G2; connector grouping (G7) may change with channel layout.
- R7 (LOW): datasheet PDF references to be re-pinned to exact section/page after downloading official PDFs into workspace.

## 9. Open issues (carried from OPEN_ISSUES.md)

1. Simultaneous-channel load envelope — HOLD/TBD (G1, master).
2. Firing-power subsystem — FEASIBILITY HOLD (G2).
3. Output expansion — NEEDS RECHECK (G3).
4. Continuity subsystem — NEEDS RECHECK (G4).
5. MCU resources — NEEDS RECHECK (G5).
6. Communications — NEEDS RECHECK (G8).
7. PCB and connectors — TBD (G7).
8. Safety — NEEDS RECHECK (G6).

No issue is silently resolved in this report.

## 10. Items requiring owner approval

- A) Provide/release the G1 simultaneous-load envelope (channels that may fire at once + validated load per channel: current, pulse, energy, voltage, timing tolerance). This is the single highest-value input; it unblocks G2, firing-power, PCB, thermal, and safety authorization.
- B) Approve re-downloading the official PDFs (TI SCHS052D, ST DS5319, SN74HC595, Infineon IRLML6344, AOS AO4407A) into the workspace to pin exact section/page references.
- C) Approve a hardware continuity-measurement fixture (CD4067 + STM32F103 ADC) to close the RON@3.3V and RAIN<10k feasibility gap.
- D) Confirm the safety concept for simultaneous firing: what authorization is required before a multi-channel command is accepted (G6).

## 11. Recommended next implementation steps

1. Close G1 (item A above). Everything else that is safety- or architecture-affecting stalls until then.
2. In parallel (non-blocking): pin evidence PDFs into workspace (B) and file the 8 open issues with exact references.
3. When G1 has numbers: run G2 feasibility (source capability, rail architecture, transient, protection, distribution, thermal, fault isolation) using only those numbers.
4. Then: G3 (SR chain + simultaneous update), G4 (MUX topology + ADC measurement), G5 (pin/RAM/flash map), G8 (protocol), G6 (safety), G7 (PCB/connectors), G10 (test plan).
5. Produce schematic sheets only after G1, G2, G3, G4, G5, G6, G8 are closed; keep each sheet change as a reviewed delta (AGENTS.md workflow).
6. Update OPEN_ISSUES.md and DECISIONS.md at each gate close so the project record stays evidence-first.