import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_controller_blocks_missing_evidence():
    result = subprocess.run(
        [sys.executable, str(ROOT / "harness" / "controller.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "BLOCKED: NO EVIDENCE" in result.stdout


def test_queue_has_no_unregistered_authority():
    queue = json.loads((ROOT / "state" / "bc_queue.json").read_text())
    item = queue["queue"][0]
    assert item["owner_authorized"] is False
    assert item["safety_authorized"] is False
    assert item["frozen"] is False
