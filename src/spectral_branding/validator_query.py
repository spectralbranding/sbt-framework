"""Search-as-Code: compile NL -> validated validator-query -> deterministic run.

Implements the "Search / Query as a Generated, Grounded Artifact" pattern over the
R1-R7 validators. Instead of reading the free-text validation summary and eyeballing
which brands violate which bound, the LLM compiles a natural-language question into a
typed, validated, reproducible *validator query* grounded in a LIVE registry built by
INTROSPECTING the validator report dataclasses. The query then executes
DETERMINISTICALLY through the existing ``validate_analysis`` engine.

PIPELINE:
    NL question
      -> build_validator_registry()           # live registry from the report fields
      -> compile_nl_to_program(q, reg, llm_fn) # ONE LLM call (defaults to local Ollama)
      -> validate_program(program, reg)        # structural raise + unknown-term flags
      -> execute_program(analysis, program)    # validate_analysis + deterministic eval

The four disciplines: ground the LLM in a live registry (it cannot invent a validator
or a parameter that the reports don't expose); flag unknowns, never silently map; the
query is a typed, validated artifact; query -> execution is deterministic (the program
is the reproducibility / audit key, re-run with ZERO LLM calls).

SCOPES:
    - ``predicates`` select BRANDS by PER-BRAND validators (metric R1, trajectory R6).
    - ``gates`` are aggregate pass/fail checks on the brand SET (capacity R4, allocation
      R7, specification R5, metamerism R2).

LOCAL-FIRST: the compile step takes an injectable ``llm_fn`` defaulting to local Ollama
($0). Tests inject a stub so no live LLM runs in CI.
"""

from __future__ import annotations

import dataclasses
import json
import typing
from typing import Any, Callable

from spectral_branding.validators.capacity_analyzer import CapacityReport
from spectral_branding.validators.metamerism_detector import MetamerismReport
from spectral_branding.validators.metric_validator import (
    MetricReport,
    validate_signal_profile,
)
from spectral_branding.validators.resource_allocation_validator import AllocationReport
from spectral_branding.validators.specification_validator import SpecificationReport
from spectral_branding.validators.trajectory_risk import TrajectoryReport
from spectral_branding.validators.validate import validate_analysis

SCHEMA_VERSION = "0.2"

# An llm_fn takes (system_prompt, user_prompt) and returns raw text (a JSON program).
LLMFn = Callable[[str, str], str]

# validator -> (report dataclass, scope). Scope decides predicate vs gate.
_VALIDATORS: dict[str, tuple[type, str]] = {
    "metric": (MetricReport, "per_brand"),
    "trajectory": (TrajectoryReport, "per_brand"),
    "capacity": (CapacityReport, "aggregate"),
    "allocation": (AllocationReport, "aggregate"),
    "specification": (SpecificationReport, "aggregate"),
    "metamerism": (MetamerismReport, "aggregate"),
}

# Report fields that carry no queryable scalar (free-text diagnostics).
_SKIP_FIELDS = {"warnings", "errors"}

# Categorical vocab that is documented in the report (not introspectable from types).
_KNOWN_CATEGORICAL: dict[tuple[str, str], list[str]] = {
    ("trajectory", "overall_risk"): ["low", "moderate", "high", "critical"],
}

_NUMERIC_OPS = {"ge", "le", "gt", "lt", "eq", "ne"}
_CATEGORICAL_OPS = {"eq", "ne", "in"}
_OP_FN: dict[str, Callable[[Any, Any], bool]] = {
    "ge": lambda a, b: a >= b,
    "le": lambda a, b: a <= b,
    "gt": lambda a, b: a > b,
    "lt": lambda a, b: a < b,
    "eq": lambda a, b: a == b,
    "ne": lambda a, b: a != b,
}


# ---------------------------------------------------------------------------
# build_validator_registry — live registry introspected from the report fields
# ---------------------------------------------------------------------------


def _classify(type_hint: Any) -> str:
    """Map a resolved type hint to a query kind: bool | numeric | categorical | other."""
    origin = typing.get_origin(type_hint)
    if origin is not None:
        # Optional[X] / Union -> classify the first non-None arg
        args = [a for a in typing.get_args(type_hint) if a is not type(None)]
        if origin in (dict, list, tuple, set):
            return "other"
        if args:
            return _classify(args[0])
        return "other"
    if type_hint is bool:
        return "bool"
    if type_hint in (int, float):
        return "numeric"
    if type_hint is str:
        return "categorical"
    return "other"


def build_validator_registry() -> dict[str, Any]:
    """Build the live registry by introspecting the validator report dataclasses.

    The LLM is grounded in this surface only — real validator names and the real
    scalar parameters their reports expose (with kind + scope). It cannot invent a
    validator or a parameter.

    Returns {schema_version, ops, validators: {<name>: {scope, parameters: {<param>:
    {kind, values?}}}}}.
    """
    registry: dict[str, Any] = {}
    for name, (report_cls, scope) in _VALIDATORS.items():
        try:
            hints = typing.get_type_hints(report_cls)
        except Exception:  # pragma: no cover - defensive
            hints = {}
        params: dict[str, Any] = {}
        for f in dataclasses.fields(report_cls):
            if f.name in _SKIP_FIELDS:
                continue
            kind = _classify(hints.get(f.name, f.type))
            if kind == "other":
                continue  # mappings/collections are not directly filterable in v0.2
            entry: dict[str, Any] = {"kind": kind}
            vocab = _KNOWN_CATEGORICAL.get((name, f.name))
            if vocab:
                entry["values"] = vocab
            params[f.name] = entry
        registry[name] = {"scope": scope, "parameters": params}

    return {
        "schema_version": SCHEMA_VERSION,
        "ops": sorted(_NUMERIC_OPS | _CATEGORICAL_OPS),
        "validators": registry,
    }


# ---------------------------------------------------------------------------
# Validation — structural raise + unknown-term flags (never silent)
# ---------------------------------------------------------------------------


def _validate_predicate(
    pred: dict, registry: dict, where: str, expected_scope: str, flags: list[str]
) -> None:
    if not isinstance(pred, dict):
        raise ValueError(f"{where} must be an object")
    validator = pred.get("validator")
    validators = registry["validators"]
    if validator not in validators:
        raise ValueError(
            f"{where}.validator={validator!r} is not a known validator. "
            f"Known: {sorted(validators)}"
        )
    meta = validators[validator]
    if meta["scope"] != expected_scope:
        raise ValueError(
            f"{where}.validator={validator!r} is {meta['scope']}, but a "
            f"{expected_scope} {where.split('[')[0]} is required "
            f"(use {'gates' if expected_scope == 'aggregate' else 'predicates'})"
        )
    parameter = pred.get("parameter")
    if parameter not in meta["parameters"]:
        raise ValueError(
            f"{where}.parameter={parameter!r} is not exposed by validator "
            f"{validator!r}. Known: {sorted(meta['parameters'])}"
        )
    pmeta = meta["parameters"][parameter]
    op = pred.get("op")
    if pmeta["kind"] == "numeric":
        if op not in _NUMERIC_OPS:
            raise ValueError(f"{where}.op={op!r} invalid for numeric parameter")
        try:
            float(pred.get("threshold"))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            raise ValueError(f"{where} numeric op requires a float 'threshold'")
    else:  # bool / categorical
        if op not in _CATEGORICAL_OPS:
            raise ValueError(f"{where}.op={op!r} invalid for {pmeta['kind']} parameter")
        if op == "in":
            vals = pred.get("values")
            if not isinstance(vals, list) or not vals:
                raise ValueError(f"{where} op=in requires a non-empty 'values' list")
            candidates = vals
        else:
            if "value" not in pred:
                raise ValueError(f"{where} op={op!r} requires 'value'")
            candidates = [pred.get("value")]
        # Flag categorical values outside the documented vocab (never silently map).
        vocab = pmeta.get("values")
        if vocab:
            for v in candidates:
                if str(v) not in vocab:
                    flags.append(
                        f"{where}: value {v!r} not in known vocab for "
                        f"{validator}.{parameter} (known: {vocab})"
                    )


def validate_program(program: dict, registry: dict) -> list[str]:
    """Validate a validator-query program. Raise on structural errors; return flags."""
    flags: list[str] = []
    if program.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be {SCHEMA_VERSION!r}, "
            f"got {program.get('schema_version')!r}"
        )
    predicates = program.get("predicates", [])
    gates = program.get("gates", [])
    if not isinstance(predicates, list) or not isinstance(gates, list):
        raise ValueError("'predicates' and 'gates' must be lists")
    for i, pred in enumerate(predicates):
        _validate_predicate(pred, registry, f"predicates[{i}]", "per_brand", flags)
    for i, gate in enumerate(gates):
        _validate_predicate(gate, registry, f"gates[{i}]", "aggregate", flags)
    return flags


# ---------------------------------------------------------------------------
# compile_nl_to_program — NL -> program (one LLM call; defaults to local Ollama)
# ---------------------------------------------------------------------------


def _build_system_prompt(registry: dict) -> str:
    lines: list[str] = []
    for name, meta in registry["validators"].items():
        plist = []
        for p, pm in meta["parameters"].items():
            tag = pm["kind"]
            if "values" in pm:
                tag += f" {pm['values']}"
            plist.append(f"{p}:{tag}")
        lines.append(f"  {name} ({meta['scope']}): {', '.join(plist)}")
    catalog = "\n".join(lines)
    return (
        "You compile a brand-validation question into a JSON query program over the\n"
        "SBT R1-R7 validators.\n\n"
        "OUTPUT: ONLY a JSON object. No prose, no markdown fences.\n\n"
        "PROGRAM SHAPE:\n"
        "{\n"
        f'  "schema_version": "{SCHEMA_VERSION}",\n'
        '  "predicates": [ {"validator": "<per_brand validator>", "parameter": "<p>",'
        ' "op": "ge|le|gt|lt|eq|ne", "threshold": <float>}'
        ' | {"validator":"...","parameter":"...","op":"eq|ne|in",'
        '"value": <v> | "values":[...]} ],\n'
        '  "gates": [ <same predicate shape, but aggregate validators> ],\n'
        '  "flags": ["<note for any term you could NOT ground in the catalog>"]\n'
        "}\n\n"
        "HARD RULES:\n"
        "- Use ONLY validators and parameters from the catalog below. Do NOT invent\n"
        "  one; if the question implies a metric not listed, add a note to 'flags'.\n"
        "- PER-BRAND validators go in 'predicates' (they select brands); AGGREGATE\n"
        "  validators go in 'gates' (pass/fail on the whole set).\n"
        "- numeric parameters use a 'threshold'; bool/categorical use 'value'/'values'.\n\n"
        "VALIDATOR CATALOG (the only validators/parameters that exist):\n"
        f"{catalog}\n"
    )


def _parse_program_json(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = "\n".join(
            ln for ln in text.split("\n") if not ln.strip().startswith("```")
        ).strip()
    if not text.startswith("{"):
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            text = text[start : end + 1]
    try:
        program = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM output is not valid JSON: {exc}\n---\n{raw}") from exc
    if not isinstance(program, dict):
        raise ValueError(
            f"LLM output parsed as {type(program).__name__}, expected object"
        )
    return program


def _default_llm_fn(system_prompt: str, user_prompt: str) -> str:
    """Local Ollama JSON-mode chat (prefer_local => $0)."""
    import os

    import httpx  # type: ignore[import-untyped]

    url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.environ.get("SBT_QUERY_MODEL", "qwen3:30b")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.0},
    }
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(f"{url}/api/chat", json=payload)
        resp.raise_for_status()
        content: str = resp.json()["message"]["content"]
        return content


def compile_nl_to_program(
    nl_text: str,
    registry: dict,
    llm_fn: LLMFn | None = None,
) -> dict:
    """Compile a natural-language question into a validated validator query.

    Exactly one LLM call. ``llm_fn`` defaults to local Ollama ($0); tests inject a
    stub (no live LLM in CI).
    """
    system = _build_system_prompt(registry)
    fn = llm_fn or _default_llm_fn
    raw = fn(system, nl_text)
    program = _parse_program_json(raw)

    program.setdefault("schema_version", SCHEMA_VERSION)
    program.setdefault("predicates", [])
    program.setdefault("gates", [])
    program.setdefault("flags", [])

    new_flags = validate_program(program, registry)
    program["flags"] = list(program.get("flags") or []) + new_flags
    return program


# ---------------------------------------------------------------------------
# execute_program — deterministic evaluation over validate_analysis output
# ---------------------------------------------------------------------------


def _report_value(report: Any, parameter: str) -> Any:
    return getattr(report, parameter, None)


def _eval(pred: dict, value: Any) -> bool:
    if value is None:
        return False
    op = pred["op"]
    if op == "in":
        return str(value) in {str(v) for v in pred["values"]}
    target = pred.get("threshold", pred.get("value"))
    if op in ("ge", "le", "gt", "lt"):
        try:
            return _OP_FN[op](float(value), float(target))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return False
    return _OP_FN[op](value, target)


def execute_program(
    analysis: dict, program: dict, registry: dict | None = None
) -> dict:
    """Execute a validated program over an analysis dict. ZERO LLM calls.

    Per-brand ``predicates`` select brands; aggregate ``gates`` are pass/fail checks.
    Returns {program, flags, selected, n_brands, gates, gates_passed}.
    """
    if registry is not None:
        extra = validate_program(program, registry)
        program = {**program, "flags": list(program.get("flags") or []) + extra}

    result = validate_analysis(analysis)
    brand_profiles: dict[str, list[float]] = analysis.get("brand_profiles", {})

    # Per-brand reports we can compute/lookup deterministically.
    per_brand_reports: dict[str, dict[str, Any]] = {}
    for name, profile in brand_profiles.items():
        per_brand_reports[name] = {
            "metric": validate_signal_profile(profile),
            "trajectory": result.trajectories.get(name),
        }

    predicates = program.get("predicates", [])
    selected: list[dict] = []
    for name in brand_profiles:
        reports = per_brand_reports[name]
        values: dict[str, Any] = {}
        ok = True
        for pred in predicates:
            report = reports.get(pred["validator"])
            val = _report_value(report, pred["parameter"]) if report else None
            values[f"{pred['validator']}.{pred['parameter']}"] = val
            if not _eval(pred, val):
                ok = False
        if ok:
            selected.append({"brand": name, "values": values})

    # Aggregate gates.
    aggregate_reports = {
        "capacity": result.capacity,
        "allocation": result.allocation,
        "specification": result.specification,
        "metamerism": result.metamerism,
    }
    gate_results: list[dict] = []
    gates_passed = True
    for gate in program.get("gates", []):
        report = aggregate_reports.get(gate["validator"])
        if report is None:
            gate_results.append(
                {
                    **_gate_echo(gate),
                    "measured": None,
                    "passed": None,
                    "note": f"{gate['validator']} report not available for this analysis",
                }
            )
            continue
        measured = _report_value(report, gate["parameter"])
        passed = _eval(gate, measured)
        gates_passed = gates_passed and passed
        gate_results.append(
            {**_gate_echo(gate), "measured": measured, "passed": passed}
        )

    return {
        "program": program,
        "flags": program.get("flags", []),
        "selected": selected,
        "n_brands": len(brand_profiles),
        "gates": gate_results,
        "gates_passed": gates_passed,
    }


def _gate_echo(gate: dict) -> dict:
    out = {
        "validator": gate["validator"],
        "parameter": gate["parameter"],
        "op": gate["op"],
    }
    if "threshold" in gate:
        out["threshold"] = gate["threshold"]
    if "value" in gate:
        out["value"] = gate["value"]
    if "values" in gate:
        out["values"] = gate["values"]
    return out


def compile_and_query(
    nl_text: str,
    analysis: dict,
    llm_fn: LLMFn | None = None,
    registry: dict | None = None,
) -> dict:
    """Full pipeline: build registry -> compile (1 LLM call) -> execute."""
    registry = registry or build_validator_registry()
    program = compile_nl_to_program(nl_text, registry, llm_fn)
    return execute_program(analysis, program, registry=None)
