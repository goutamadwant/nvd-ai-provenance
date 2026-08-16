#!/usr/bin/env python3
"""Validate VEPP documents against the schema and semantic profile rules."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

DYNAMIC_CLAIM_TYPES = {"exploit_activity", "exploit_probability", "priority"}


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        payload = json.load(stream)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _json_path(parts: list[Any]) -> str:
    if not parts:
        return "$"
    return "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in parts)


def schema_issues(document: dict[str, Any], schema: dict[str, Any]) -> list[ValidationIssue]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        ValidationIssue("SCHEMA", _json_path(list(error.absolute_path)), error.message)
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
    ]


def semantic_issues(document: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    assertions = document.get("assertions")
    if not isinstance(assertions, list):
        return issues

    assertion_by_id: dict[str, dict[str, Any]] = {}
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            continue
        assertion_id = assertion.get("id")
        if not isinstance(assertion_id, str):
            continue
        if assertion_id in assertion_by_id:
            issues.append(
                ValidationIssue(
                    "DUPLICATE_ASSERTION_ID",
                    f"$.assertions[{index}].id",
                    f"assertion id {assertion_id!r} is not unique",
                )
            )
        else:
            assertion_by_id[assertion_id] = assertion

    replacements: dict[str, str] = {}
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict):
            continue
        assertion_id = assertion.get("id")
        claim_type = assertion.get("claimType")
        if claim_type in DYNAMIC_CLAIM_TYPES and "validTime" not in assertion:
            issues.append(
                ValidationIssue(
                    "DYNAMIC_CLAIM_WITHOUT_TIME",
                    f"$.assertions[{index}]",
                    f"{claim_type} assertions require validTime",
                )
            )

        lifecycle = assertion.get("lifecycle")
        if not isinstance(lifecycle, dict) or lifecycle.get("state") != "superseded":
            continue
        replacement = lifecycle.get("replacedBy")
        if not isinstance(replacement, str) or not isinstance(assertion_id, str):
            continue
        replacements[assertion_id] = replacement
        if replacement == assertion_id:
            issues.append(
                ValidationIssue(
                    "SELF_SUPERSESSION",
                    f"$.assertions[{index}].lifecycle.replacedBy",
                    "an assertion cannot supersede itself",
                )
            )
        elif replacement not in assertion_by_id:
            issues.append(
                ValidationIssue(
                    "UNKNOWN_REPLACEMENT",
                    f"$.assertions[{index}].lifecycle.replacedBy",
                    f"replacement assertion {replacement!r} does not exist",
                )
            )

    for assertion_id in replacements:
        seen: set[str] = set()
        cursor = assertion_id
        while cursor in replacements:
            if cursor in seen:
                issues.append(
                    ValidationIssue(
                        "SUPERSESSION_CYCLE",
                        "$.assertions",
                        f"supersession chain containing {assertion_id!r} is cyclic",
                    )
                )
                break
            seen.add(cursor)
            cursor = replacements[cursor]

    return issues


def validate_document(
    document: dict[str, Any], schema: dict[str, Any]
) -> list[ValidationIssue]:
    return schema_issues(document, schema) + semantic_issues(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", type=Path, help="VEPP JSON Schema path")
    parser.add_argument("documents", nargs="+", type=Path, help="documents to validate")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        schema = load_json(args.schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR schema: {exc}", file=sys.stderr)
        return 2

    failed = False
    for path in args.documents:
        try:
            document = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"FAIL {path}: {exc}")
            failed = True
            continue
        issues = validate_document(document, schema)
        if issues:
            failed = True
            print(f"FAIL {path}")
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
