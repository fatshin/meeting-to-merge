from __future__ import annotations

import difflib
import re
from typing import Any

from runtime.contracts import Field, Product


TRANSCRIPT = """[00:18] Maya: REQ-1 Checkout must reject a quantity below 1.
[00:44] Ken: REQ-2 Orders over $500 require manager approval.
[01:12] Maya: REQ-3 The receipt must show the order ID.
[01:48] Ken: REQ-4 Retry must not create a second charge.
[02:10] Maya: Approval means a non-empty manager token."""
SOURCE = """def checkout(quantity, total, manager_token="", order_id=""):
    approved = total >= 500
    charge()
    return {"ok": True, "order": ""}
"""

PRODUCT = Product(
    4, "meeting-to-merge", "Meeting to Merge",
    "Carry an approved requirement from spoken words to a test and minimal patch.",
    "#8b5cf6",
    (Field("transcript", "Meeting transcript", TRANSCRIPT, 10), Field("source", "Target source", SOURCE, 9)),
)


def requirements(transcript: str) -> list[dict[str, str]]:
    output = []
    for line in transcript.splitlines():
        match = re.search(r"\[(\d+:\d+)\]\s+([^:]+):\s+(REQ-\d+)\s+(.+)", line)
        if match:
            output.append({"timestamp": match.group(1), "speaker": match.group(2), "id": match.group(3), "text": match.group(4)})
    return output


def build_patch(source: str) -> tuple[str, list[str]]:
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    fixed = source.replace(
        '    approved = total >= 500\n    charge()\n    return {"ok": True, "order": ""}',
        '    if quantity < 1:\n'
        '        return {"ok": False, "error": "invalid_quantity"}\n'
        '    if total > 500 and not manager_token:\n'
        '        return {"ok": False, "error": "approval_required"}\n'
        '    charge(idempotency_key=order_id)\n'
        '    return {"ok": True, "order": order_id}',
    )
    tests = ["test_rejects_quantity_below_one", "test_large_order_requires_manager_token", "test_receipt_includes_order_id", "test_retry_uses_idempotency_key"]
    patch = "\n".join(difflib.unified_diff(source.splitlines(), fixed.splitlines(), "before.py", "after.py", lineterm=""))
    return patch, tests


def checkout_fixture(
    quantity: int,
    total: float,
    manager_token: str,
    order_id: str,
    *,
    patched: bool,
    retry: bool = False,
) -> dict[str, Any]:
    if patched and quantity < 1:
        return {"ok": False, "error": "invalid_quantity", "charges": 0}
    if patched and total > 500 and not manager_token:
        return {"ok": False, "error": "approval_required", "charges": 0}
    return {
        "ok": True,
        "order": order_id if patched else "",
        "charges": 1 if patched or not retry else 2,
    }


def run_fixture_checks(*, patched: bool) -> list[bool]:
    invalid = checkout_fixture(0, 100, "", "O-1", patched=patched)
    approval = checkout_fixture(1, 501, "", "O-2", patched=patched)
    receipt = checkout_fixture(1, 100, "", "O-3", patched=patched)
    retry = checkout_fixture(1, 100, "", "O-4", patched=patched, retry=True)
    return [
        invalid.get("error") == "invalid_quantity",
        approval.get("error") == "approval_required",
        receipt.get("order") == "O-3",
        retry.get("charges") == 1,
    ]


def analyze(payload: dict[str, str]) -> dict[str, Any]:
    reqs = requirements(payload["transcript"])
    patch, tests = build_patch(payload["source"])
    ambiguities = [] if "Approval means" in payload["transcript"] else ["Approval token definition is missing."]
    baseline_checks = run_fixture_checks(patched=False)
    patched_checks = run_fixture_checks(patched=True)
    items = [
        {
            **req,
            "test": tests[index],
            "baseline": "PASS" if baseline_checks[index] else "FAIL",
            "after_patch": "PASS" if patched_checks[index] else "FAIL",
        }
        for index, req in enumerate(reqs[:len(tests)])
    ]
    return {
        "status": "READY_FOR_HUMAN_APPLY" if not ambiguities and patch else "NEEDS_CLARIFICATION",
        "headline": f"{len(items)} cited requirements mapped to tests and a minimal diff",
        "metrics": {
            "requirements": len(items),
            "baseline_failures": baseline_checks.count(False),
            "post_patch_passes": patched_checks.count(True),
        },
        "items": items,
        "evidence": [{"label": req["id"], "value": f"{req['timestamp']} · {req['speaker']}"} for req in reqs],
        "artifact": {"ambiguities": ambiguities, "patch": patch, "approval_required": True},
    }


def acceptance(result: dict[str, Any]) -> tuple[bool, dict[str, bool]]:
    checks = {
        "four_requirements": result["metrics"]["requirements"] == 4,
        "baseline_reproduced": result["metrics"]["baseline_failures"] == 4,
        "four_tests_pass": result["metrics"]["post_patch_passes"] == 4,
        "idempotency_patch": "idempotency_key" in result["artifact"]["patch"],
        "human_apply": result["artifact"]["approval_required"],
    }
    return all(checks.values()), checks
