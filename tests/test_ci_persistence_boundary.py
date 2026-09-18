from pathlib import Path

WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "autonomous-evidence.yml"
).read_text(encoding="utf-8")

def test_autonomous_evidence_never_mutates_main_from_branch_validation():
    assert "branches: [main]" in WORKFLOW
    assert "git rebase origin/main" not in WORKFLOW
    assert "git push origin HEAD:main" not in WORKFLOW
    assert "RX50_STATE_BRANCH: automation/rx50-state" in WORKFLOW
    assert "git push --force-with-lease" in WORKFLOW
    assert "HEAD:${RX50_STATE_BRANCH}" in WORKFLOW

def test_persistence_write_is_gated_to_main():
    assert "if: ${{ github.ref == 'refs/heads/main' }}" in WORKFLOW
