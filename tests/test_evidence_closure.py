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


def test_c20b_is_source_derived_and_fails_closed_without_project_vdd():
    ev08 = _row(EVIDENCE, "EV-08")
    ev12 = _row(EVIDENCE, "EV-12")
    project_state = (ROOT / "harness" / "state" / "project_state.md").read_text()

    # Parse semantic source fields, not presentation wording.
    voh_match = re.search(r"VOH\(min\)\s*=\s*VDD\s*[−-]\s*([0-9]+(?:\.[0-9]+)?)\s*V", ev08)
    source_vdd_match = re.search(
        r"standard VDD\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*[–-]\s*([0-9]+(?:\.[0-9]+)?)\s*V",
        ev08,
    )
    pins_match = re.search(r"when\s+(\d+)\s+pins\s+are\s+sourced", ev08)
    voh_condition_match = re.search(r"VOH row condition is\s+([0-9.]+) V < VDD < ([0-9.]+) V", ev08)
    vih_match = re.search(r"VIH @5 V\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*V", ev12)

    assert voh_match, "EV-08 must expose a parseable VOH(min) source relation"
    assert source_vdd_match, "EV-08 must expose the Table 9 VDD source envelope"
    assert pins_match and int(pins_match.group(1)) == 8
    assert voh_condition_match
    assert vih_match and float(vih_match.group(1)) == 3.5

    delta = float(voh_match.group(1))
    source_vdd_min = float(source_vdd_match.group(1))
    source_vdd_max = float(source_vdd_match.group(2))
    voh_vdd_min = float(voh_condition_match.group(1))
    voh_vdd_max = float(voh_condition_match.group(2))
    vih = float(vih_match.group(1))
    assert delta == 0.4
    assert source_vdd_min == 2.0
    assert source_vdd_max == 3.6
    assert voh_vdd_min == 2.7
    assert voh_vdd_max == 3.6

    # Critical fail-closed boundary: EV-09's 3.3 V USART condition must not
    # be treated as proof that the RX50 GPIO supply is 3.3 V.
    assert "3.3 V logic rail" in project_state
    assert "BASELINE ONLY / NEEDS RECHECK" in project_state
    assert "NOT locked" in project_state

    ev52 = _row(EVIDENCE, "EV-52")
    assert "EVIDENCE GAP" in ev52
    assert "operating point" in ev52.lower()
    assert ("EV-09" not in ev52) or ("does not prove" in ev52.lower())

    c20b = _classification_row(REGISTER, "C-20b")
    assert "EVIDENCE GAP" in c20b
    assert "3.3 V" in c20b
    assert "not locked" in c20b.lower()
    assert "VERIFIED INTERFACE INCOMPATIBILITY" not in c20b

    assert "conditional incompatibility" in CLOSURE.lower()
    assert "cannot be promoted" in CLOSURE.lower()
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
    assert "No remedy is selected." in CLOSURE
    assert "RON@3.3V NOT SPECIFIED" in AUDIT
    assert "pin allocation" in CLOSURE and "unresolved" in CLOSURE.lower()
