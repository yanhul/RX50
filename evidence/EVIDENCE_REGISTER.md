# RX50 EVIDENCE REGISTER

- Generated: 2026-08-15 by M001. Shared source of truth for evidence items.
- Hierarchy level (1..8): 1 locked decision -> 2 explicit requirement -> 3 manufacturer datasheet -> 4 verified measurement -> 5 derived calculation -> 6 assumption -> 7 proposal -> 8 previous AI conclusion.
- Verified-now = re-checked against source during M001/M004 session work.

## Level-3 datasheet facts (VERIFIED during audit)

| ID | Fact | Value | Source | Status |
|---|---|---|---|---|
| EV-01 | STM32F103 ADC RADC / CADC | 1 kΩ / 8 pF | ST DS5319 R20 §5.3.18 | VERIFIED |
| EV-02 | STM32F103 ADC sampling time tS | 1.5..239.5 cycles (0.107..17.1 µs @14 MHz) | DS5319 Tables 47/49 | VERIFIED |
| EV-03 | STM32F103 ADC conversion tCONV | tS + 12.5 = 14..252 cycles (1..18 µs @14 MHz) | DS5319 Table 48/Eq.1 | VERIFIED |
| EV-04 | STM32F103 RAIN max vs tS (Table 48) | 0.4 / 5.9 / 11.4 / 25.2 / 37.2 / 50 kΩ | DS5319 | VERIFIED |
| EV-05 | STM32F103 ADC accuracy | ±2 LSB max ET guaranteed ONLY when RAIN <10 kΩ | DS5319 | VERIFIED |
| EV-06 | STM32F103 VREF+ on LQFP48 | internally tied to VDDA | DS5319 | VERIFIED |
| EV-07 | STM32F103 ADC count / channels | 2x 12-bit ADC, 10 external (PA0-7, PB0, PB1) | DS5319 | VERIFIED |
| EV-08 | STM32F103 CMOS GPIO VOH source fields | Table 37 VOH(min) = VDD−0.4 V for an I/O pin when 8 pins are sourced at the same time; Table 37 states that, unless otherwise specified, output-voltage parameters use the ambient-temperature and VDD conditions summarized in Table 9. Table 9 gives standard VDD = 2.0–3.6 V. The VOH row itself has no separate IIO condition; footnote 3 requires sourced I/O current to remain within Table 7 absolute limits and total IVDD. | ST DS5319 Rev 20 Table 9, Table 37 §5.3.13 | VERIFIED; source fields captured; RX50 operating-point VDD remains a separate project-evidence requirement |
| EV-09 | STM32F103 USART1 | 4.5 Mbit/s @ VDD=3.3 V (NOT 10 Mbps) | DS5319 | VERIFIED (C-03 source) |
| EV-10 | CD4067 RON @5/10/15 V 25 °C | 1050 / 400 / 240 Ω max | TI SCHS052D Rev D | VERIFIED |
| EV-11 | CD4067 RON @3.3 V | NOT SPECIFIED by TI | SCHS052D | VERIFIED (absence) |
| EV-12 | CD4067 VIH @5 V | 3.5 V -> 3.3 V logic cannot guarantee VIH on 5 V rail | SCHS052D | VERIFIED |
| EV-13 | CD4067 OFF leakage | ±100 nA (25 °C) / ±1000 nA (85-125 °C) @18 V; ±10 pA typ @10 V | SCHS052D | VERIFIED |
| EV-14 | CD4067 capacitance / BW | CIS 5 pF, COS 55 pF, BW 14 MHz | SCHS052D | VERIFIED |
| EV-15 | CD4067 settling / charge injection | settling typical curves only, NO guaranteed; charge injection NOT specified | SCHS052D | VERIFIED (absence) |
| EV-16 | SN74HC595 basics | 8-bit SR + 3-state storage reg; shift clock 24 MHz typ; IOL/IOH ±7.8 mA max @6 V | TI SCLS041J | VERIFIED |
| EV-17 | SN74HC595 power-up / SRCLR | storage register NOT cleared by SRCLR; undefined at power-up | SCLS041J | VERIFIED |
| EV-18 | SN74HC595 timing @4.5 V | tsu 25 ns, tpd 40 ns, tsu RCLK 19 ns, tw 20 ns, fmax 25 MHz | SCLS041J | VERIFIED |
| EV-19 | SX1278 SPI | up to 10 MHz | Semtech datasheet note | VERIFIED (report cite) |
| EV-20 | MAX3485 | 3.3 V RS-485, up to 10 Mbps | ADI/TI | VERIFIED (report cite) |
| EV-21 | IRLML6344 | 30 V N-ch; RDS(on) ~22/29 mΩ typ @VGS=4.5 V — single-drain vs pulsed columns differ | Infineon StrongIRFET | NEEDS RECHECK before BOM |
| EV-22 | AO4407A | DigiKey listing 12 A @Ta, 3.1 W | DigiKey (NOT AOS PDF) | NEEDS RECHECK vs AOS datasheet |
| EV-23 | SMBJ15CA | 15 V standoff, 24.4 V max clamp | Littelfuse | VERIFIED (report cite) |
| EV-24 | TPS562201 | 4.5-17 V in, 2 A buck, D-CAP2 | TI | VERIFIED (report cite) |
| EV-45 | CD4067 absolute-max current IS/ID (CONT) | ±20 mA abs max / ±10 mA recommended op. (also control-input pin ISEL/IEN ±30 mA) | TI SCHS052D Rev D (Absolute Max / Rec. Op.) | VERIFIED (was NEEDS RECHECK; closed by M003B) |
| EV-47 | STM32F103 IINJ(PIN) on any other (non-FT) pin | ±5 mA | ST DS5319 Table 7 (Rev 19/20) | VERIFIED (M003B) |
| EV-47b | STM32F103 ΣIINJ(PIN) total injected current | ±25 mA | ST DS5319 Table 7 | VERIFIED (M003B) |
| EV-48 | STM32F103 VIN abs max on non-FT pin | VSS−0.3 to 4.0 V | ST DS5319 Table 6 (Rev 18/19 text; see C-22) | VERIFIED (M003B) |
| EV-49 | STM32F103 datasheet identity / revision | STM32F103C8 (STM32F103C8T6, LQFP48), STM32F103xx medium-density performance line; official datasheet DS5319 = document CD00161566, current revision Rev 20 (st.com); secondary sheetsdata render rejected as authority (older-revision wording; see C-22). Governing G4 constraint = IINJ ±5 mA (EV-47), unaffected | ST product page; st.com resource CD00161566 (Rev 20); C-22 | VERIFIED (M003C, authority level) |

## Level-4 measurements (none exist yet)

| ID | Measurement | Status | Owner of evidence |
|---|---|---|---|
| EV-30 | CD4067 RON @3.3 V / 5 V vs temperature | MEASUREMENT PENDING | G4 fixture T-G4-01..06 |
| EV-31 | CD4067 settling time (real hardware) | MEASUREMENT PENDING | G4 |
| EV-32 | STM32F103 ADC RAIN <10 kΩ validation with MUX | MEASUREMENT PENDING | G4 |
| EV-33 | Continuity scan timing / isolation / leakage | MEASUREMENT PENDING | G4 |
| EV-34 | Firing simultaneity skew / rail sag (hot-fire) | PENDING G1 | G2/G10 |

## Missing evidence (gaps)

| ID | Gap | Impact |
|---|---|---|
| EV-40 | G1 load envelope (R-01..R-10) — fill sheet exists, empty | Blocks G1/G2/G6/G10 |
| EV-41 | Datasheet PDFs not in workspace | References not pinned to section/page |
| EV-42 | "G1 Evidence Register" / "G4 Evidence Retrieval" files referenced but absent | Missing artifacts |
| EV-43 | GLVN subject not analyzed | Needs owner clarification |
| EV-44 | STM32F103 VOL exact row (GPIO output drive condition; NOT the ADC-pin abs-max — see EV-47/EV-48) | NEEDS RECHECK |
| EV-46 | RX24 sequence/ACK + RF-loss timeout history | Historical record absent |


## Phase 2 closure entries

| ID | Fact / closure finding | Source | Status |
|---|---|---|---|
| EV-50 | SN74HC595 MCU control requires 3 mandatory signals (SER/SRCLK/RCLK) plus optional SRCLR; OE is hardware-interlock-owned, not an MCU GPIO | `RX50_G4_G5_CLOSURE_AUDIT.md` §13; `schematic/RX50_S03_OUTPUT_LOGIC.sch` | VERIFIED; final MCU pin allocation remains OPEN because G5 is not locked |
| EV-51 | USART RX is handled by NVIC USART RXNE; USART RX is not an EXTI source in the RX50 architectural model | `RX50_G4_G5_CLOSURE_AUDIT.md` §16/E-06; `RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md` §5.2 and §7 | VERIFIED; C-06 resolved |
| EV-52 | C-20b source relation is conditional: DS5319 supports VOH(min)=VDD−0.4 V for 8 sourced pins and CD4067 VIH@5 V is 3.5 V, but RX50 project_state.md leaves the 3.3 V logic rail BASELINE ONLY / NEEDS RECHECK — NOT locked; EV-09's 3.3 V USART condition does not prove the RX50 GPIO operating point | `evidence/EVIDENCE_REGISTER.md` EV-08/EV-09/EV-12; `harness/state/project_state.md`; `RX50_G4_G5_CLOSURE_AUDIT.md` S-14/S-15 | EVIDENCE GAP; lock project VDD before promoting C-20b |
| EV-53 | No authoritative SN74HC595 timing guarantee at the RX50 3.3 V operating point is present; interpolation is not a guaranteed specification | `RX50_G4_G5_CLOSURE_AUDIT.md` §13; `harness/state/CONTRADICTION_REGISTER.md` C-21 | EVIDENCE GAP |
| EV-54 | No physical CD4067 leakage results at 3.3 V or 5 V exist; 18 V datasheet bounds cannot be transferred to RX50 operating conditions | `harness/templates/T-G4-05_LEAKAGE_CHARACTERIZATION.md` §§1, 9–12; contradiction register C-20c | MEASUREMENT REQUIRED |
| EV-55 | G5 final MCU pin allocation and schematic net register are not authoritative/locked | `RX50_G5_PIN_MAP_FINAL.md`; `RX50_SCHEMATIC_NET_REGISTER.md` | VERIFIED; C-05 remains OPEN |
