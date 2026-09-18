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
    return next((x for x in doc.splitlines() if x.startswith(f"| {evidence_id} |")), "")


def _classification_row(doc: str, item: str) -> str:
    return next((x for x in doc.splitlines() if x.startswith(f"| {item} |")), "")


def test_c05_is_source_derived_and_fail_closed():
    required = {"SER", "SRCLK", "RCLK"}
    optional = {"SRCLR"}
    actual = {m.group(1) for m in re.finditer(r"\bSR_(SER|SRCLK|RCLK|SRCLR)\b", OUTPUT)}
    assert required <= actual
    # SRCLR is optional: absence is valid. If present, the canonical source name must be used.
    if optional & actual:
        assert "SR_SRCLR" in OUTPUT
    assert "OE is hardware-interlock-owned" in OUTPUT

    ev50 = _row(EVIDENCE, "EV-50")
    assert "3 mandatory signals" in ev50 and "SER/SRCLK/RCLK" in ev50
    assert "OE" in ev50 and "hardware" in ev50.lower()
    assert "C-05" in REGISTER
    assert "OPEN — signal count corrected to 3-4" in _classification_row(REGISTER, "C-05")
    assert "final MCU pin allocation" in _classification_row(REGISTER, "C-05")
    assert "pin allocation unresolved" in CLOSURE
    assert "NOT LOCKED" in G5
    assert "Nets registered: 0" in NETS


def test_c06_is_canonical_architecture_not_magic_string_only():
    rx_lines = [x for x in G9.splitlines() if "USART" in x and ("RXNE" in x or "EXTI" in x)]
    assert any("RXNE" in x for x in rx_lines)
    assert "USART RX uses NVIC USART RXNE" in CLOSURE

    c06 = _classification_row(REGISTER, "C-06")
    assert "RESOLVED" in c06
    assert "OPEN" not in c06
    assert "USART" in c06 and "RXNE" in c06


def test_c20b_is_a_numeric_predicate_with_evidence_lineage():
    ev08 = _row(EVIDENCE, "EV-08")
    ev12 = _row(EVIDENCE, "EV-12")
    assert "VOH = VDD-0.4" in ev08
    assert "VIH @5 V" in ev12 and "3.5 V" in ev12

    # Derive the predicate from the authoritative evidence rows; do not
    # duplicate the source values as independent test constants.
    vdd_match = re.search(r"at\\s+([0-9]+(?:\\.[0-9]+)?)\\s*V", CLOSURE)
    assert vdd_match, "closure must identify the operating point"
    vdd = float(vdd_match.group(1))
    assert vdd == 3.3
    voh_delta_match = re.search(r"VOH\\s*=\\s*VDD\\s*-\\s*([0-9]+(?:\\.[0-9]+)?)", ev08)
    vih_match = re.search(r"VIH @5 V\\s*\\|\\s*([0-9]+(?:\\.[0-9]+)?)\\s*V", ev12)
    assert voh_delta_match, "EV-08 must expose the authoritative VOH delta"
    assert vih_match, "EV-12 must expose the authoritative VIH value"
    voh = vdd - float(voh_delta_match.group(1))
    vih = float(vih_match.group(1))
    assert voh < vih

    ev52 = _row(EVIDENCE, "EV-52")
    ev52_voh = re.search(r"VOH guarantee\\s*([0-9]+(?:\\.[0-9]+)?)\\s*V", ev52)
    ev52_vih = re.search(r"VIH requirement\\s*([0-9]+(?:\\.[0-9]+)?)\\s*V", ev52)
    assert ev52_voh and ev52_vih
    assert float(ev52_voh.group(1)) == voh
    assert float(ev52_vih.group(1)) == vih
    assert "VERIFIED" in ev52

    c20b = _classification_row(REGISTER, "C-20b")
    assert "VERIFIED INTERFACE INCOMPATIBILITY" in c20b
    assert "owner decision required" in c20b.lower()
    assert "no option selected" in c20b.lower()
    assert "VOH guaranteed < VIH required" in CLOSURE


def test_c20c_cannot_be_verified_without_level4_measurement():
    level4 = EVIDENCE.split("## Level-4 measurements", 1)[1]
    assert "none exist yet" in level4.lower()
    for evidence_id in ("EV-30", "EV-31", "EV-32", "EV-33"):
        assert "MEASUREMENT PENDING" in _row(EVIDENCE, evidence_id)

    c20c = _classification_row(REGISTER, "C-20c")
    assert "MEASUREMENT REQUIRED" in c20c
    assert "no measured data" in c20c.lower() or "physical" in c20c.lower()
    assert "No pass/fail conclusion is permitted" in CLOSURE
    assert "18 V maximum/bound must not be transferred to 3.3 V or 5 V" in CLOSURE


def test_c21_cannot_be_verified_by_interpolation():
    ev18 = _row(EVIDENCE, "EV-18")
    ev53 = _row(EVIDENCE, "EV-53")
    assert "4.5 V" in ev18
    assert "3.3 V" in ev53 and "EVIDENCE GAP" in ev53

    c21 = _classification_row(REGISTER, "C-21")
    assert "EVIDENCE GAP" in c21
    assert "interpolation is not a guarantee" in c21.lower()
    assert "3.3 V manufacturer guarantee or reproducible measurement" in CLOSURE


def test_phase2_topology_and_hardware_validation_remain_fail_closed():
    assert "Topology:** NOT LOCKED." in CLOSURE
    assert "Physically measured:** none" in CLOSURE
    assert "does not select a remedy" in CLOSURE
    assert "RON@3.3V NOT SPECIFIED" in AUDIT
    assert "pin allocation" in CLOSURE and "unresolved" in CLOSURE.lower()
