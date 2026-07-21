#!/usr/bin/env python3
"""Validate a candidate ITR JSON against the official ITD JSON schema.

Usage:
    python validate_itr_json.py <candidate.json> <schema.json>

Exits 0 if valid, 1 if not. Prints each validation error with its JSON path so
you can see exactly which field is wrong.

Dependency:  pip install jsonschema

The validator draft is auto-detected from the schema's "$schema" declaration, so
this works whether the ITD schema is Draft-07, 2020-12, etc.
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import validators
except ImportError:
    sys.exit("Install the dependency first:  pip install jsonschema")


def load(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f"File not found: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{path} is not valid JSON: {e}")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)

    candidate = load(sys.argv[1])
    schema = load(sys.argv[2])

    ValidatorClass = validators.validator_for(schema)
    try:
        ValidatorClass.check_schema(schema)
    except Exception as e:  # noqa: BLE001 - surface a bad schema clearly
        sys.exit(f"The schema itself is invalid: {e}")

    validator = ValidatorClass(schema)
    errors = sorted(validator.iter_errors(candidate), key=lambda e: list(e.path))

    if not errors:
        print("VALID - the JSON conforms to the schema.")
        print(
            "Note: schema-valid does NOT mean the numbers are correct. Review the "
            "reconciliation summary, and prove the first PAN through the official "
            "offline utility before uploading."
        )
        return 0

    print(f"INVALID - {len(errors)} error(s):\n")
    for err in errors:
        loc = " -> ".join(str(p) for p in err.path) or "(root)"
        print(f"  at {loc}: {err.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
