"""AIOS workload adapter for RX50 engineering evidence/readiness."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED = (
    "AGENTS.md", "RX50_G1_G2_REQUIREMENT_CLOSURE.md",
    "RX50_G4_G5_CLOSURE_AUDIT.md", "RX50_G4_RAW_EVIDENCE_REGISTER.md",
)
PROVENANCE = {"producer": "yanhul/RX50", "adapter": "rx50.engineering@1"}


def _artifact_manifest(root: Path, evidence: tuple[str, ...]) -> str:
    """Persist a generated, reproducible manifest and return its local ref."""
    artifact = root / "harness" / "state" / "rx50_engineering_evidence_set.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "rx50-engineering-evidence-set",
        "evidence_refs": list(evidence),
        "provenance": PROVENANCE,
    }
    artifact.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(artifact.relative_to(root))


def execute(*, problem: str, workdir: str | Path = ".") -> dict[str, Any]:
    if not isinstance(problem, str) or not problem.strip():
        raise ValueError("problem must be non-empty")
    root = Path(workdir)
    missing = [name for name in REQUIRED if not (root / name).exists()]
    if missing:
        return {"status": "BLOCKED", "reason": "required engineering evidence files missing", "missing": missing,
                "artifact_refs": (), "evidence_refs": (), "verification_refs": (), "provenance": PROVENANCE}
    evidence = tuple(f"sha256:{name}:{hashlib.sha256((root / name).read_bytes()).hexdigest()}" for name in REQUIRED)
    artifact_ref = _artifact_manifest(root, evidence)
    physical = root / "evidence" / "physical"
    if not physical.exists() or not any(physical.iterdir()):
        return {"status": "BLOCKED", "reason": "physical evidence required before engineering promotion",
                "artifact_refs": (artifact_ref,), "evidence_refs": evidence,
                "verification_refs": ("requirements_coverage", "contradiction_check"), "provenance": PROVENANCE}
    return {"status": "PASS", "problem": problem, "artifact_refs": (artifact_ref,),
            "evidence_refs": evidence,
            "verification_refs": ("requirements_coverage", "contradiction_check", "physical_evidence"),
            "provenance": PROVENANCE,
            "physical_evidence": sorted(str(p.relative_to(root)) for p in physical.rglob("*"))}


if __name__ == "__main__":
    print(json.dumps(execute(problem="AIOS RX50 engineering conformance"), indent=2))
