from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = (ROOT / "harness" / "state" / "CONTRADICTION_REGISTER.md").read_text()
CLOSURE = (ROOT / "PHASE2_EVIDENCE_CLOSURE.md").read_text()
AUDIT = (ROOT / "RX50_G4_G5_CLOSURE_AUDIT.md").read_text()
G5 = (ROOT / "RX50_G5_PIN_MAP_FINAL.md").read_text()
NETS = (ROOT / "RX50_SCHEMATIC_NET_REGISTER.md").read_text()
OUTPUT = (ROOT / "schematic" / "RX50_S03_OUTPUT_LOGIC.sch").read_text()
G9 = (ROOT / "RX50_G9_FIRMWARE_AND_CROSS_GATE_REPORT.md").read_text()


def test_sr_control_count_and_oe_authority_are_fail_closed():
    assert "three mandatory MCU-controlled signals" in CLOSURE
    assert "`SER`, `SRCLK`, `RCLK`" in CLOSURE
    assert "OE is hardware-interlock-owned" in OUTPUT
    assert "C-05" in REGISTER and "OPEN" in REGISTER
    assert "pin allocation unresolved" in CLOSURE
    assert "NOT LOCKED" in G5
    assert "Nets registered: 0" in NETS


def test_usart_rx_is_nvic_not_exti_and_c06_is_unambiguous():
    assert "USART RXNE" in G9
    assert "USART RX uses NVIC USART RXNE" in CLOSURE
    c06 = next(line for line in REGISTER.splitlines() if line.startswith("| C-06 |"))
    assert "RESOLVED" in c06
    assert "OPEN" not in c06


def test_phase2_preserves_unknown_measurement_and_topology_gates():
    assert "C-21" in REGISTER and "EVIDENCE GAP" in REGISTER
    assert "C-20c" in REGISTER and "MEASUREMENT REQUIRED" in REGISTER
    assert "C-20b" in REGISTER and "VERIFIED INTERFACE INCOMPATIBILITY" in REGISTER
    assert "does not select a remedy" in CLOSURE
    assert "Topology:** NOT LOCKED" in CLOSURE
    assert "physically measured:** none" in CLOSURE.lower()
    assert "interpolation is not a guaranteed" in CLOSURE.lower()
    assert "RON@3.3V NOT SPECIFIED" in AUDIT
