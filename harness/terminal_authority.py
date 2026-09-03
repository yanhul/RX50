"""External attestation for terminal controller state.

The controller must not treat a persisted ``terminal=true`` flag as authority.
A deployment-held secret attests the exact terminal decision and state digest.
The agent/controller never receives permission to mint or alter the attestation.
"""
from __future__ import annotations
import hashlib, hmac, json

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def state_digest(state):
    material = dict(state)
    material.pop("updated_at", None)
    material.pop("terminal_attestation", None)
    return hashlib.sha256(canonical(material).encode("utf-8")).hexdigest()

def verify_terminal_attestation(state, attestation, secret):
    if not isinstance(secret, str) or not secret: raise ValueError("missing terminal authority secret")
    if not isinstance(attestation, dict): raise ValueError("terminal attestation missing")
    required={"type","state_digest","terminal_reason","signature"}
    if set(attestation)!=required or attestation.get("type")!="RX50_TERMINAL_ATTESTATION": raise ValueError("terminal attestation schema/type mismatch")
    digest=state_digest(state)
    if attestation.get("state_digest")!=digest: raise ValueError("terminal state digest mismatch")
    reason=attestation.get("terminal_reason")
    if not isinstance(reason,str) or not reason.strip() or state.get("terminal_reason")!=reason: raise ValueError("terminal reason mismatch")
    msg=f"{digest}\n{reason}".encode("utf-8")
    expected=hmac.new(secret.encode("utf-8"),msg,hashlib.sha256).hexdigest()
    if not hmac.compare_digest(attestation.get("signature",""),expected): raise ValueError("terminal attestation signature mismatch")
    return True
