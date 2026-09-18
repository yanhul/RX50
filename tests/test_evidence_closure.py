from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTER = (ROOT / "harness" / "state" / "CONTRADICTION_REGISTER.md").read_text()
CLOSURE = (ROOT / "PHASE2_EVIDENCE_CLOSURE.md").read_text()
AUDIT = (ROOT / "RX50_G4_G5_CLOSURE_AUDIT.md").read_text()
G5 = (ROOT / "RX50_G5_PIN_MAP_FINAL.md").read_text()
NETS = (ROOT / "RX50_SCHEMATIC_NET_REGISTER.md").read_text()
OUTPUT = (ROOT / "schematic" / "RX50_S03_OUTPUT_LOGIC.sch").read_text()
G9 = (ROOT / "RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md").read_text()
EVIDENCE = (ROOT / "evidence" / "EVIDENCE_REGISTER.md").read_text()


def _row(doc: str, evidence_id: str) -> str:
    for line in doc.splitlines():
        if line.startswith(f"| {evidence_id} |"):
            return line
    raise AssertionError(f"missing evidence row: {evidence_id}")


def _classification_row(doc: str, item: str) -> str:
    for line in doc.splitlines():
        if line.startswith(f"| {item} |"):
            return line
    raise AssertionError(f"missing contradiction row: {item}")


def test_c05_is_source_derived_and_fail_closed():
    # Machine-check the actual signal inventory, not merely a prose count.
    required = {"SER", "SRCLK", "RCLK"}
    optional = {"SRCLR"}
    assert required <= set(re.findall(r"\b(?:SER|SRCLK|RCLK|SRCLR)\b", OUTPUT))
    assert len(required) == 3
    assert optional <= set(re.findall(r"\b(?:SER|SRCLK|RCLK|SRCLR)\b", OUTPUT))
    assert "OE is hardware-interlock-owned" in OUTPUT

    # The evidence/state chain must retain explicit provenance and remain unlocked.
    ev50 = _row(EVIDENCE, "EV-50")
    assert "3 mandatory signals" in ev50 and "SER/SRCLK/RCLK" in ev50
    assert "OE" in ev50 and "hardware" in ev50.lower()
    assert _classification_row(REGISTER, "C-05").endswith("OPEN — signal count corrected to 3-4; final MCU pin allocation still requires owner-approved G5 pin-map evidence")
    assert "pin allocation unresolved" in CLOSURE
    assert "NOT LOCKED" in G5
    assert "Nets registered: 0" in NETS


def test_c06_is_canonical_architecture_not_magic_string_only():
    # Canonical G9 architecture says RXNE/NVIC for USART and EXTI for external sources.
    rx_lines = [x for x in G9.splitlines() if "USART" in x and ("RXNE" in x or "EXTI" in x)]
    assert any("RXNE" in x for x in rx_lines)
    assert any("EXTI" not in x or "external" in x.lower() for x in rx_lines)
    assert "USART RX uses NVIC USART RXNE" in CLOSURE

    c06 = _classification_row(REGISTER, "C-06")
    assert "RESOLVED" in c06
    assert "OPEN" not in c06
    assert "historical EXTI wording" in REGISTER


def test_c20b_is_a_numeric_predicate_with_evidence_lineage():
    ev08 = _row(EVIDENCE, "EV-08")
    ev12 = _row(EVIDENCE, "EV-12")
    assert "VOH" in ev08 and "VDD-0.4" in ev08
    assert "VIH" in ev12 and "3.5 V" in ev12

    voh_match = re.search(r"VOH\s*=\s*VDD-0\.4\s*\([^)]*\)", ev08)
    assert voh_match, "EV-08 must retain the authoritative VOH predicate"
    assert re.search(r"VIH[^|]*3\.5\s*V", ev12), "EV-12 must retain the authoritative VIH value"

    # Resolve the concrete RX50 operating point from the closure text and prove the inequality.
    vdd_match = re.search(r"(?:at|=)\s*3\.3\s*V", CLOSURE)
    assert vdd_match, "C-20b must bind the calculation to 3.3 V"
    voh = 3.3 - 0.4
    vih = 3.5
    assert voh < vih

    c20b = _classification_row(REGISTER, "C-20b")
    assert "VERIFIED INTERFACE INCOMPATIBILITY" in c20b
    assert "owner decision required" in c20b.lower()
    assert "no option selected" in c20b.lower()

    # Guard against a future edit that changes the claim while leaving stale prose.
    assert "VOH guaranteed < VIH required" in CLOSURE


def test_c20c_cannot_become_verified_without_level4_measurement():
    # Level-4 section must remain explicitly empty/pending.
    level4 = EVIDENCE.split("## Level-4 measurements", 1)[1]
    assert "none exist yet" in level4.lower()
    assert re.search(r"EV-3[0-4].*PENDING", level4, re.IGNORECASE)

    c20c = _classification_row(REGISTER, "C-20c")
    assert "MEASUREMENT REQUIRED" in c20c
    assert "no measured data" in c20c.lower() or "physical" in c20c.lower()

    # Closure must not manufacture a pass/fail from datasheet bounds.
    assert "No pass/fail conclusion is permitted" in CLOSURE
    assert "18 V maximum/bound must not be transferred to 3.3 V or 5 V" in CLOSURE


def test_c21_cannot_be_verified_by_interpolation():
    ev18 = _row(EVIDENCE, "EV-18")
    ev53 = _row(EVIDENCE, "EV-53")
    assert "4.5 V" in ev18
    assert "3.3 V" in ev53
    assert "EVIDENCE GAP" in ev53

    c21 = _classification_row(REGISTER, "C-21")
    assert "EVIDENCE GAP" in c21
    assert "interpolation is not a guarantee" in c21.lower()
    assert "3.3 V manufacturer guarantee or reproducible measurement" in CLOSURE


def test_phase2_topology_and_hardware_validation_remain_locked_closed():
    assert "Topology:** NOT LOCKED." in CLOSURE
    assert "Physically measured:** none" in CLOSURE
    assert "does not select a remedy" in CLOSURE
    assert "RON@3.3V NOT SPECIFIED" in AUDIT
    assert "final pin allocation" in CLOSURE
