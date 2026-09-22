from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone


GEN = 10**18
BUDGET = 2 * GEN
BASE_TIME = 1893456000
SUBMIT_DEADLINE = BASE_TIME + 3600
REVIEW_DEADLINE = BASE_TIME + 7200
CONTRACT_PATH = "contracts/concord_batch.py"
LLM_PATTERN = r"(?s).*ConcordBatch semantic conflict judge.*"


def view(value) -> dict:
    return json.loads(value if isinstance(value, str) else str(value))


def address_text(value) -> str:
    if hasattr(value, "as_hex"):
        return value.as_hex
    return "0x" + bytes(value).hex()


def set_time(vm, timestamp: int) -> None:
    text = datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace("+00:00", "Z")
    vm.warp(text)
    message_module = sys.modules.get("genlayer.message")
    if message_module is not None:
        message_module.raw["datetime"] = text
        message_module.datetime = text
    gl_module = sys.modules.get("genlayer.gl")
    if gl_module is not None and getattr(gl_module, "message_raw", None) is not None:
        gl_module.message_raw["datetime"] = text


def create_batch(contract, vm, sponsor, a, b, c, batch_id="batch-1") -> None:
    set_time(vm, BASE_TIME)
    vm.sender = sponsor
    vm.value = BUDGET
    contract.create_batch(
        batch_id,
        a,
        b,
        c,
        "A,B,C",
        "Clear two intents only when their stated side effects can coexist under the shared service policy.",
        SUBMIT_DEADLINE,
        REVIEW_DEADLINE,
    )
    vm.value = 0


def submit_three(contract, vm, a, b, c, batch_id="batch-1") -> None:
    set_time(vm, BASE_TIME + 60)
    vm.sender = a
    contract.submit_intent(batch_id, "Rotate the service signing key.", "Maintenance window is open.", "Old key is revoked immediately.")
    vm.sender = b
    contract.submit_intent(batch_id, "Deploy a client configuration.", "Current signing key is accepted.", "Client pins the old key for 24 hours.")
    vm.sender = c
    contract.submit_intent(batch_id, "Update public documentation copy.", "Documentation repository is writable.", "No runtime resource changes.")


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def graph_payload(contract, lookup_batch_id="batch-1", relations=None, **overrides) -> dict:
    batch_id = lookup_batch_id
    batch = view(contract.get_batch(batch_id))
    if relations is None:
        relations = [
            ("A", "B", "INCOMPATIBLE", "POLICY_CONTRADICTION"),
            ("A", "C", "INDEPENDENT", "NO_RESOURCE_OVERLAP"),
            ("B", "C", "INDEPENDENT", "NO_RESOURCE_OVERLAP"),
        ]
    pairs = []
    for left, right, relation, _basis in relations:
        left_id = batch_id + "-" + left
        right_id = batch_id + "-" + right
        pairs.append({
            "pair_id": left_id + "|" + right_id,
            "left_id": left_id,
            "right_id": right_id,
            "relation": relation,
            "rationale": "bounded test rationale",
        })
    payload = {
        "batch_id": batch_id,
        "attempt_id": batch_id + "-attempt-" + str(batch["attempt_count"] + 1),
        "policy_digest": batch["policy_digest"],
        "intent_set_digest": batch["intent_set_digest"],
        "coverage": "COMPLETE",
        "pairs": pairs,
    }
    payload.update(overrides)
    return payload


def mock_graph(vm, contract, relations=None, **overrides) -> None:
    payload = graph_payload(contract, relations=relations, **overrides)
    vm.mock_llm(LLM_PATTERN, json.dumps(json.dumps(payload)))


def accounting_ok(data: dict) -> bool:
    return int(data["total_received"]) == int(data["total_locked"]) + int(data["total_credits"]) + int(data["total_withdrawn"])
