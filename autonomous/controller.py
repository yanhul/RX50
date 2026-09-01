from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'autonomous' / 'state.json'
MAX_ITERATIONS = int(os.getenv('RX50_MAX_ITERATIONS', '8'))

TERMINAL = {'TERMINAL', 'EXHAUSTED'}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {'state': 'INIT', 'iteration': 0, 'history': [], 'evidence_hashes': {}}


def save_state(s: dict) -> None:
    s['updated_at'] = datetime.now(timezone.utc).isoformat()
    STATE.write_text(json.dumps(s, indent=2, sort_keys=True) + '\n')


def inventory_evidence() -> dict:
    result = {}
    for base in ('evidence', 'decisions', 'measurements', 'calculations', 'reports', 'harness/state', 'harness/open_issues'):
        d = ROOT / base
        if not d.exists():
            continue
        for p in d.rglob('*'):
            if p.is_file() and '.git' not in p.parts:
                result[str(p.relative_to(ROOT))] = sha256_file(p)
    return result


def run() -> int:
    s = load_state()
    if s.get('state') in TERMINAL:
        print(f"RX50_AUTONOMOUS TERMINAL state={s['state']}")
        return 0

    s['iteration'] = int(s.get('iteration', 0)) + 1
    if s['iteration'] > MAX_ITERATIONS:
        s['state'] = 'EXHAUSTED'
        s['terminal_reason'] = 'max_iterations'
        save_state(s)
        print(f'RX50_AUTONOMOUS EXHAUSTED max_iterations={MAX_ITERATIONS}')
        return 0

    current = inventory_evidence()
    previous = s.get('evidence_hashes', {})
    changed = sorted(k for k, v in current.items() if previous.get(k) != v)
    removed = sorted(k for k in previous if k not in current)
    s['evidence_hashes'] = current
    s['history'].append({'iteration': s['iteration'], 'changed': changed, 'removed': removed})

    # This controller is intentionally non-design-generative. It can identify
    # evidence changes and blockers, but cannot invent engineering values,
    # authorize hardware changes, or bypass owner/safety gates.
    blockers = []
    state_text = ROOT / 'harness/state/project_state.md'
    if state_text.exists():
        text = state_text.read_text(errors='replace').upper()
        for marker in ('HOLD', 'BLOCKED', 'NOT LOCKED', 'NOT AUTHORIZED'):
            if marker in text:
                blockers.append(marker)
    s['state'] = 'HOLD' if blockers else 'READY_FOR_REVIEW'
    s['blockers'] = sorted(set(blockers))
    save_state(s)
    print(f"RX50_AUTONOMOUS state={s['state']} iteration={s['iteration']} changed={len(changed)} blockers={','.join(s['blockers']) or 'none'}")
    return 0

if __name__ == '__main__':
    raise SystemExit(run())
