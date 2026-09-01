from pathlib import Path
import json

from autonomous.controller import sha256_file


def test_hash_is_stable(tmp_path: Path):
    p = tmp_path / 'evidence.txt'
    p.write_text('evidence')
    assert sha256_file(p) == sha256_file(p)


def test_state_schema_is_json_serializable():
    state = {'state': 'HOLD', 'iteration': 1, 'history': [], 'evidence_hashes': {}}
    assert json.loads(json.dumps(state))['state'] == 'HOLD'
