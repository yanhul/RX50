from pathlib import Path

from aios.adapter import _closure_blockers

ROOT = Path(__file__).resolve().parents[1]


def test_authoritative_closure_blockers_are_exposed():
    blockers = _closure_blockers(ROOT)
    assert blockers == (
        "G1:HOLD",
        "G2:HOLD",
        "G4:MEASUREMENT_PENDING",
        "G5:NOT_LOCKED",
    )
