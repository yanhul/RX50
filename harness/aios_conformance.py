#!/usr/bin/env python3
"""Fail-closed AIOS boundary conformance gate for RX50."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "AGENTS.md": (
        "Never invent numerical specifications.",
        "When evidence conflicts, report the conflict instead of choosing silently.",
        "Do not claim that a design is validated unless the required evidence/test exists.",
    ),
    "harness/controller.py": (
        'phase="OBSERVE"',
        'phase="DECIDE"',
        'phase="VERIFY"',
        'phase="PERSIST"',
        'phase="YIELD"',
    ),
}

def main() -> int:
    failures = []
    for rel, needles in REQUIRED.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                failures.append(f"{rel}: missing invariant: {needle}")
    if failures:
        print("AIOS_CONFORMANCE: BLOCKED")
        for failure in failures: print("- " + failure)
        return 1
    print("AIOS_CONFORMANCE: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
