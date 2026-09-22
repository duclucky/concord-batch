from __future__ import annotations

from typing import Any


def _first(mapping: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = mapping.get(name)
        if value not in (None, ""):
            return value
    return None


def normalize_receipt(payload: dict[str, Any]) -> dict[str, str]:
    """Project only non-sensitive deployment proof fields from raw or SDK receipts."""
    if not isinstance(payload, dict):
        raise ValueError("receipt must be an object")
    nested = payload.get("result") if isinstance(payload.get("result"), dict) else {}
    deployment = payload.get("deployment") if isinstance(payload.get("deployment"), dict) else {}
    address = _first(payload, "contractAddress", "recipient", "to")
    if address is None:
        address = _first(nested, "contractAddress", "recipient")
    if address is None:
        address = _first(deployment, "contractAddress")
    tx_hash = _first(payload, "transactionHash", "hash", "txHash")
    if tx_hash is None:
        tx_hash = _first(nested, "transactionHash", "hash")
    status = _first(payload, "statusName", "status", "finalityStatus")
    execution = _first(payload, "txExecutionResultName", "txExecutionResult", "executionResult")
    normalized = {
        "transactionHash": str(tx_hash or ""),
        "contractAddress": str(address or ""),
        "status": str(status or ""),
        "executionResult": str(execution or ""),
    }
    if normalized["transactionHash"] and not _is_hex(normalized["transactionHash"], 64):
        raise ValueError("invalid transaction hash")
    if normalized["contractAddress"] and not _is_hex(normalized["contractAddress"], 40):
        raise ValueError("invalid contract address")
    return normalized


def _is_hex(value: str, digits: int) -> bool:
    if not value.startswith("0x") or len(value) != digits + 2:
        return False
    return all(char in "0123456789abcdefABCDEF" for char in value[2:])
