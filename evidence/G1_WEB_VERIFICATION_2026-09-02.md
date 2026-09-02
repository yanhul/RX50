# G1 Web Verification — 2026-09-02

## Scope
Verify the previously proposed G1 e-match candidates using live web sources. This file records evidence only; it does not lock the e-match or simultaneous-channel requirement.

## MJG Technologies — Firewire Initiator

**Manufacturer source:** https://electricmatch.com/

The current MJG Technologies site identifies MJG Technologies as the manufacturer and describes the Firewire Initiator product family. The site states that MJG developed the Firewire Initiator in 2014 and currently lists Firewire Initiator products. This verifies manufacturer/product traceability, but does **not** by itself establish the electrical firing envelope required for RX50 design.

**Manufacturer product page:** https://electricmatch.com/pyrotechnics

The current product page explicitly lists “MJG Firewire Initiator- Standard” and describes it as an ATF non-regulated igniter. Again, no RX50 firing-current/resistance/pulse envelope is locked from this page.

**Disposition:** Manufacturer/product identity VERIFIED. Electrical load-envelope evidence for G1 remains INCOMPLETE.

## Oxral

A current North-American product listing from Ultratec identifies “Oxral (BGZD) E-Matches” and gives a minimum firing information of 0.5 A for 0.05 s. This is distributor/manufacturer-adjacent product evidence, not an authoritative current manufacturer datasheet. It is therefore retained as supporting evidence only and not used to lock RX50 parameters.

Source: https://ultratecfx.com/pyrotechnics/products-catalog/oxral-e-matches/

**Disposition:** Candidate identified; authoritative manufacturer electrical datasheet NOT established.

## Daveyfire N28F / 28F

A historical RRC2 manual reproduces a table listing Daveyfire 28B/28BR/28F and electrical values. This is legacy secondary evidence, not a current manufacturer source. It confirms historical existence of the model family but is insufficient for current RX50 locking.

Source: https://manuals.plus/m/1b4658cb4caad290cf215aaf91e032ba1da30828ca4da11dcbd50f0b89174a1a

**Disposition:** LEGACY REFERENCE ONLY. Do not lock RX50 from these values.

## Result

- MJG Firewire Initiator: **manufacturer identity verified; exact electrical load envelope still pending authoritative source**.
- Oxral BGZD: **supporting product evidence; authoritative manufacturer electrical source pending**.
- Daveyfire 28F: **legacy reference only**.
- No e-match is promoted to LOCKED.
- Simultaneous-channel requirement remains an owner requirement and is not inferred from the number of physical outputs.

## Gate

`G1 = HOLD`

Blocking items remain:
- OI-G1-01: authoritative electrical load-envelope evidence for selected exact e-match.
- OI-G1-02: authoritative simultaneous/worst-case channel requirement.

No design parameter is changed by this evidence update.
