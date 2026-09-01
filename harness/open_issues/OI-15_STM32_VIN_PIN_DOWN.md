# OI-15 — STM32F103 VIN Page-Level Pin-Down Verification

**Issue ID:** OI-15
**Status:** OPEN
**Origin:** C-22 (CONTRADICTION_REGISTER.md)
**Date opened:** 2026-08-15
**Opened by:** M006.2
**Safety relevance:** **ELEVATED** — incorrect assumption about VIN tolerance may cause pin damage

---

## 1. EXACT VERIFICATION QUESTION

For **every** non-5V-tolerant (non-FT) pin on the STM32F103C8/STM32F103C8T6, does the authoritative datasheet (ST DS5319 Rev 20, document ID CD00161566) confirm that:

> Maximum input voltage on a non-FT pin = VSS − 0.3 V to **4.0 V**

and that **no non-FT pin has a VIN limit lower than 4.0 V**?

This must be verified **page by page** against Table 6 (Pin definitions) in the current revision of DS5319.

---

## 2. ORIGIN — C-22 SUMMARY

C-22 documented a conflict between two sources:

| Source | VIN claim | Authority level |
|---|---|---|
| **DS5319 Rev 18/19** (STMicroelectronics, primary datasheet) | non-FT VIN = VSS−0.3..4.0 V | High — ST primary datasheet, but older revision |
| **sheetsdata** (third-party render) | non-FT VIN = VDD+0.3 V | Rejected — third-party, older-revision wording |

**Resolution (per M003C):** DS5319 Rev 20 is the current primary authority. The non-FT VIN limit is VSS−0.3..4.0 V per Rev 18/19 wording, carried forward to Rev 20.

**Residual:** The actual Rev 20 PDF has not been examined. Table 6 (Pin definitions) must be opened and **visually confirmed** that every non-FT pin entry lists 4.0 V as the absolute maximum VIN, and that no pin has a lower absolute maximum. This page-level verification is OI-15.

---

## 3. SAFETY RELEVANCE

**Classification:** ELEVATED RISK — potential pin damage.

If any non-FT pin is mistakenly assumed to tolerate ≥4.0 V (e.g., VDD+0.3 V = 3.6 V for a 3.3 V supply, or worse, 5.0 V tolerance), applying a voltage above the true absolute maximum rating may cause:

- Latch-up (destructive)
- Permanent damage to the GPIO cell
- Reliability degradation even if immediate failure does not occur

The RX50 continuity circuit routes muxed signals to the STM32 ADC. C-20b explicitly identifies a 5 V-referenced sense node that would exceed 4.0 V VIN if connected directly. C-22 (OI-15) and C-20b (5 V→ADC exposure) are **distinct but related** safety concerns:

- **OI-15 (this issue):** Verify the VIN limit for every non-FT pin from the authoritative PDF.
- **C-20b (separate):** Design mitigation for the 5 V sense node that exceeds whatever the verified VIN limit turns out to be.

---

## 4. REQUIRED PRIMARY EVIDENCE

To close OI-15, the following evidence must be obtained:

| Evidence | Purpose |
|---|---|
| **ST DS5319 Rev 20** (or latest revision as of verification date) | Current authoritative datasheet for STM32F103C8/STM32F103C8T6 |
| Document ID **CD00161566** | ST internal identifier for DS5319 — confirm the correct document is obtained |
| **Table 6** (Pin definitions) within that PDF | Pin-by-pin VIN limit listing |

---

## 5. REQUIRED DATASHEET SECTION/TABLE

When DS5319 Rev 20 (or current) is available:

| Section | Table | What to verify |
|---|---|---|
| Pinouts and pin description | **Table 6** (Pin definitions) | For each pin marked as non-FT (not 5 V tolerant), confirm the absolute maximum VIN is listed as 4.0 V (or VSS−0.3..4.0 V). Check that no non-FT pin has a limit lower than 4.0 V. |
| Electrical characteristics | Table with Absolute Maximum Ratings | Confirm the general VIN limit statement for non-FT pins matches 4.0 V. |
| Document revision history | Last page(s) | Confirm the document revision is Rev 20 or later, and check for any errata affecting pin VIN limits. |

---

## 6. ACCEPTANCE CONDITION FOR CLOSING

OI-15 may be closed **only** when ALL of the following are true:

1. DS5319 Rev 20 (or current) PDF has been obtained and is stored in `evidence/`.
2. Table 6 has been read page by page.
3. Every non-FT pin has been confirmed to have VIN absolute maximum = 4.0 V (or VSS−0.3..4.0 V).
4. No pin has been found with a lower VIN limit.
5. A verification statement has been recorded in this issue (or a linked verification artifact) confirming the above.
6. The verification statement is signed/dated.

**This issue cannot be closed by inference.** The PDF must be opened and read. Historical conclusions from M003C (that confirmed the authority level) do not substitute for visual verification of Table 6.

---

## 7. WHY THIS ISSUE REMAINS UNRESOLVED

The issue is OPEN because:

1. **DS5319 Rev 20 PDF is not present in this repository** — no file exists in `evidence/` or elsewhere.
2. **No page-level verification has been performed** — C-22 was resolved at the authority level (M003C determined which source wins), but the actual page-by-page pin-down was deferred to OI-15.
3. **Table 6 may contain per-pin exceptions** — the general VIN statement in the electrical characteristics table may differ from individual pin entries in Table 6. Only visual inspection can confirm.
4. **Document revision may have changed** — if a later revision (Rev 21+) exists, the verification should be performed against the latest available revision.

---

## 8. TRACEABILITY

| Reference | Relationship | Status in repository |
|---|---|---|
| **C-22** | Origin — this issue is the residual action from C-22 | Exists in CONTRADICTION_REGISTER.md |
| **DS5319** | Primary evidence required — STM32F103 datasheet | **ABSENT** from repository |
| **EV-47** | Referenced in C-22 as governing evidence for T-G4-06 (IINJ ±5 mA current limit) | Referenced only; content **ABSENT** from repository |
| **EV-48** | Referenced in C-20b as governing evidence for ADC pin VIN limit (≤4.0 V) | Referenced only; content **ABSENT** from repository |
| **T-G4-06** | Test gate governed by IINJ ±5 mA per EV-47; not directly related to OI-15 but referenced in same C-22 context | Template **ABSENT** from repository |

### Important distinction between EV-47, EV-48, and OI-15

| Reference | What it governs | Status |
|---|---|---|
| EV-47 | IINJ ±5 mA (current injection limit) — governs T-G4-06 | Not in repository; content unknown |
| EV-48 | ADC pin VIN ≤4.0 V — referenced in C-20b for 5V→ADC exposure | Not in repository; content unknown |
| OI-15 (this issue) | Page-level verification that STM32F103 non-FT VIN = 4.0 V per DS5319 Rev 20 Table 6 | OPEN |

OI-15 is a prerequisite for EV-48 verification: if the VIN limit is confirmed as 4.0 V, then EV-48's implication (ADC pin ≤4.0 V) is consistent. If the verified limit is different, EV-48 may need updating.

---

## 9. EXPLICIT VERIFICATION STATUS

**No verification has yet occurred.**

- No DS5319 PDF has been opened.
- No Table 6 has been read.
- No pin has been confirmed against the datasheet.
- The historical conclusion (non-FT VIN = 4.0 V) is a **HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT** (from M003C, Level 8 in the evidence hierarchy).
- The M003C conclusion that DS5319 Rev 20 is authoritative is also a **HISTORICAL CONCLUSION — UNDERLYING EVIDENCE ABSENT**.

The current working assumption (4.0 V limit) may be correct, but it has not been demonstrated from primary evidence stored in this repository.

---

## REFERENCES

| Reference | Type | Relationship to OI-15 |
|---|---|---|
| CONTRADICTION_REGISTER.md | Register | Contains C-22 which defines OI-15 as a residual |
| DS5319 Rev 20 (CD00161566) | Manufacturer datasheet | Required primary evidence — not in repository |
| T-G4-05_LEAKAGE_CHARACTERIZATION.md | Test gate template | Referenced 4.0 V VIN limit in Section 7.5 (HISTORICAL CONCLUSION) |
| EV-47 | Evidence item | Referenced in C-22 — not in repository |
| EV-48 | Evidence item | Referenced in C-20b — not in repository |
| T-G4-06 | Test gate template | Referenced in C-22 — not yet created |
| C-20b | Open contradiction | Related but separate safety issue (5 V→ADC exposure) |