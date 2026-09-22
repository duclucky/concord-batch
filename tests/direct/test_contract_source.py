from __future__ import annotations

import ast
from pathlib import Path


CONTRACT = Path("contracts/concord_batch.py")


def test_contract_is_ascii_and_header_is_coherent_v03():
    raw = CONTRACT.read_bytes()
    raw.decode("ascii")
    lines = raw.decode("ascii").splitlines()
    assert lines[0] == "# v0.3.0"
    assert lines[1] == '# { "Depends": "py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng" }'
    assert lines[2] == "import genlayer as gl"


def test_one_contract_class_and_sandboxed_meaning_validator():
    source = CONTRACT.read_text(encoding="ascii")
    tree = ast.parse(source)
    contract_classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Attribute) and base.attr == "Contract":
                    contract_classes.append(node.name)
    assert contract_classes == ["ConcordBatch"]
    assert "gl.vm.run_nondet_default(" in source
    assert "gl.vm.run_nondet(" not in source
    assert "_meaning_key" in source


def test_value_entrypoint_is_payable_and_withdraw_debits_before_transfer():
    source = CONTRACT.read_text(encoding="ascii")
    tree = ast.parse(source)
    methods = {
        node.name: ast.get_source_segment(source, node) or ""
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert "@gl.public.write.payable\n    def create_batch" in source
    withdraw = methods["withdraw_credit"]
    assert withdraw.find("credit.amount = bigint(0)") < withdraw.find("emit_transfer")
