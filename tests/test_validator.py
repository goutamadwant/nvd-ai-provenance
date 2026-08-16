from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_module() -> ModuleType:
    module_path = ROOT / "validator" / "vepp_validator.py"
    spec = importlib.util.spec_from_file_location("vepp_validator", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    assert isinstance(value, dict)
    return value


def test_manifest_vectors() -> None:
    validator = load_module()
    manifest_path = ROOT / "test-vectors" / "manifest.json"
    manifest = read_json(manifest_path)
    schema = read_json(ROOT / "schema" / "vepp.schema.json")

    for vector in manifest["vectors"]:
        assert isinstance(vector, dict)
        document = read_json((manifest_path.parent / vector["path"]).resolve())
        issues = validator.validate_document(document, schema)
        codes = {issue.code for issue in issues}
        if vector["expected"] == "valid":
            assert issues == [], (vector["path"], [str(issue) for issue in issues])
        else:
            assert issues, vector["path"]
            assert set(vector.get("expectedCodes", [])) <= codes


def test_duplicate_ids_are_rejected() -> None:
    validator = load_module()
    schema = read_json(ROOT / "schema" / "vepp.schema.json")
    document = read_json(ROOT / "examples" / "human-verified-remediation.json")
    document["assertions"].append(dict(document["assertions"][0]))

    issues = validator.validate_document(document, schema)

    assert "DUPLICATE_ASSERTION_ID" in {issue.code for issue in issues}


def test_dynamic_claim_requires_observation_time() -> None:
    validator = load_module()
    schema = read_json(ROOT / "schema" / "vepp.schema.json")
    document = read_json(ROOT / "examples" / "human-verified-remediation.json")
    document["assertions"][0]["claimType"] = "exploit_activity"

    issues = validator.validate_document(document, schema)

    assert "DYNAMIC_CLAIM_WITHOUT_TIME" in {issue.code for issue in issues}
