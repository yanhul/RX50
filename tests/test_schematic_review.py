from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMATIC = ROOT / "schematic" / "RX50_FUNCTIONAL.sch"
INDEX = ROOT / "schematic" / "RX50_SHEET_INDEX.md"
REVIEW = ROOT / "schematic" / "RX50_ELECTRICAL_REVIEW.md"


def test_functional_schematic_is_structurally_closed():
    text = SCHEMATIC.read_text()
    assert text.count("$Comp") == text.count("$EndComp")
    assert text.rstrip().endswith("$EndSCHEMATC")
    assert "STM32F103C8T6" in text
    assert "SX1278 / RA-02" in text
    assert "MAX3485" in text
    assert "74HC595 #1" in text
    assert "74HC595 #7" in text
    assert "CD4067B #1" in text
    assert "CD4067B #4" in text


def test_schematic_review_preserves_hard_gates():
    index = INDEX.read_text()
    review = REVIEW.read_text()
    schematic = SCHEMATIC.read_text()
    for text in (index, review, schematic):
        assert "G1" in text and "G2" in text
        assert "HOLD" in text
        assert "NOT FOR MANUFACTURING" in text or "NOT RELEASED" in text
    assert "firing voltage" in schematic
    assert "firing current" in schematic
    assert "OE is NOT MCU-owned" in schematic
