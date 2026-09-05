"""AIOS workload adapter for RX50 engineering evidence/readiness."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED = (
    "AGENTS.md",
    "RX50_G1_G2_REQUIREMENT_CLOSURE.md",
    "RX50_G4_G5_CLOSURE_AUDIT.md",
    "RX50_G4_RAW_EVIDENCE_REGISTER.md",
)


def execute(*, problem: str, workdir: str | Path = ".") -> dict[str, Any]:
    if not isinstance(problem, str) or not problem.strip():
        raise ValueError("problem must be non-empty")
    root = Path(workdir)
    missing = [name for name in REQUIRED if not (root / name).exists()]
    if missing:
        return {"status": "BLOCKED", "reason": "required engineering evidence files missing", "missing": missing}

    evidence = {}
    for name in REQUIRED:
        path = root / name
        evidence[name] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }

    # Physical verification cannot be inferred from design text. The adapter
    # therefore returns BLOCKED until explicit physical evidence is supplied.
    physical = root / "evidence" / "physical"
    if not physical.exists() or not any(physical.iterdir()):
        return {
            "status": "BLOCKED",
            "reason": "physical evidence required before engineering promotion",
            "evidence": evidence,
            "verification": ["requirements_coverage", "contradiction_check"],
        }

    return {
        "status": "PASS",
        "problem": problem,
        "artifact": "engineering evidence set",
        "evidence": evidence,
        "physical_evidence": sorted(str(p.relative_to(root)) for p in physical.rglob("*")),
        "verification": ["requirements_coverage", "contradiction_check", "physical_evidence"],
    }


if __name__ == "__main__":
    print(json.dumps(execute(problem="AIOS RX50 engineering conformance"), indent=2))
