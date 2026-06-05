"""Tests for Search-as-Code validator-query compilation (validator_query.py).

Pure tests (no live LLM): a stub llm_fn + synthetic brand profiles exercise the
grounding / scope / validation / determinism guarantees. The registry is
introspected from the real validator report dataclasses, and execution runs the
real ``validate_analysis`` engine — so these are genuine end-to-end checks with no
network and no model.
"""

from __future__ import annotations

import json

import pytest

from spectral_branding import validator_query as vq


def _registry() -> dict:
    return vq.build_validator_registry()


def _analysis() -> dict:
    return {
        "brand_profiles": {
            "BrandA": [0.3, 0.5, 0.2, 0.4, 0.6, 0.3, 0.5, 0.4],
            "BrandB": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            "BrandC": [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        }
    }


def _stub(program: dict):
    state = {"calls": 0}

    def fn(system: str, user: str) -> str:
        state["calls"] += 1
        return json.dumps(program)

    fn.state = state  # type: ignore[attr-defined]
    return fn


# --- registry grounding -------------------------------------------------------


def test_registry_introspected_from_reports():
    reg = _registry()
    assert set(reg["validators"]) == {
        "metric",
        "trajectory",
        "capacity",
        "allocation",
        "specification",
        "metamerism",
    }
    # per-brand vs aggregate scope is captured
    assert reg["validators"]["trajectory"]["scope"] == "per_brand"
    assert reg["validators"]["capacity"]["scope"] == "aggregate"
    # a documented categorical carries its vocab; a numeric is typed numeric
    overall = reg["validators"]["trajectory"]["parameters"]["overall_risk"]
    assert overall == {
        "kind": "categorical",
        "values": ["low", "moderate", "high", "critical"],
    }
    assert (
        reg["validators"]["capacity"]["parameters"]["utilization"]["kind"] == "numeric"
    )


# --- grounding: unknown terms rejected/flagged, never silently mapped ----------


def test_unknown_validator_raises():
    with pytest.raises(ValueError, match="not a known validator"):
        vq.validate_program(
            {
                "schema_version": "0.2",
                "predicates": [
                    {"validator": "ghost", "parameter": "x", "op": "eq", "value": 1}
                ],
                "gates": [],
            },
            _registry(),
        )


def test_unknown_parameter_raises():
    with pytest.raises(ValueError, match="not exposed by validator"):
        vq.validate_program(
            {
                "schema_version": "0.2",
                "predicates": [
                    {
                        "validator": "trajectory",
                        "parameter": "made_up",
                        "op": "eq",
                        "value": "x",
                    }
                ],
                "gates": [],
            },
            _registry(),
        )


def test_scope_enforced_aggregate_cannot_be_predicate():
    with pytest.raises(ValueError, match="is aggregate"):
        vq.validate_program(
            {
                "schema_version": "0.2",
                "predicates": [
                    {
                        "validator": "capacity",
                        "parameter": "utilization",
                        "op": "le",
                        "threshold": 0.9,
                    }
                ],
                "gates": [],
            },
            _registry(),
        )


def test_unknown_categorical_value_flagged():
    flags = vq.validate_program(
        {
            "schema_version": "0.2",
            "predicates": [
                {
                    "validator": "trajectory",
                    "parameter": "overall_risk",
                    "op": "eq",
                    "value": "extreme",
                }
            ],
            "gates": [],
        },
        _registry(),
    )
    assert any("extreme" in f and "overall_risk" in f for f in flags)


def test_numeric_op_requires_threshold():
    with pytest.raises(ValueError, match="threshold"):
        vq.validate_program(
            {
                "schema_version": "0.2",
                "gates": [
                    {"validator": "capacity", "parameter": "utilization", "op": "le"}
                ],
                "predicates": [],
            },
            _registry(),
        )


def test_compile_flags_hallucinated_parameter_via_stub():
    reg = _registry()
    # The LLM tries a real validator but a non-existent parameter -> structural raise
    # surfaces through compile (validate_program raises).
    bad = {
        "schema_version": "0.2",
        "predicates": [
            {"validator": "metric", "parameter": "accuracy", "op": "eq", "value": True}
        ],
        "gates": [],
        "flags": [],
    }
    with pytest.raises(ValueError, match="not exposed"):
        vq.compile_nl_to_program("accurate brands", reg, llm_fn=_stub(bad))


# --- deterministic execution --------------------------------------------------


def test_execute_per_brand_predicate_and_gate():
    reg = _registry()
    analysis = _analysis()
    program = {
        "schema_version": "0.2",
        "predicates": [
            {"validator": "metric", "parameter": "valid", "op": "eq", "value": True}
        ],
        "gates": [
            {
                "validator": "capacity",
                "parameter": "n_brands",
                "op": "ge",
                "threshold": 2,
            }
        ],
        "flags": [],
    }
    res = vq.execute_program(analysis, program, registry=reg)
    assert res["n_brands"] == 3
    assert res["gates"][0]["measured"] == 3 and res["gates"][0]["passed"] is True
    assert res["gates_passed"] is True
    # every selected brand carries the measured value it was filtered on
    for sel in res["selected"]:
        assert "metric.valid" in sel["values"]


def test_gate_on_missing_report_is_noted_not_crash():
    reg = _registry()
    # allocation needs founder_weights + observers; absent here -> report is None
    program = {
        "schema_version": "0.2",
        "predicates": [],
        "gates": [
            {
                "validator": "allocation",
                "parameter": "alignment_gap",
                "op": "le",
                "threshold": 0.2,
            }
        ],
        "flags": [],
    }
    res = vq.execute_program(_analysis(), program, registry=reg)
    assert res["gates"][0]["passed"] is None
    assert "not available" in res["gates"][0]["note"]


def test_reproducibility_zero_llm_on_reexecute():
    reg = _registry()
    analysis = _analysis()
    program = {
        "schema_version": "0.2",
        "predicates": [
            {
                "validator": "trajectory",
                "parameter": "overall_risk",
                "op": "in",
                "values": ["high", "critical"],
            }
        ],
        "gates": [],
        "flags": [],
    }
    stub = _stub(program)
    compiled = vq.compile_nl_to_program(
        "brands at high absorption risk", reg, llm_fn=stub
    )
    assert stub.state["calls"] == 1
    r1 = vq.execute_program(analysis, compiled)
    r2 = vq.execute_program(analysis, compiled)
    assert [s["brand"] for s in r1["selected"]] == [s["brand"] for s in r2["selected"]]
    assert stub.state["calls"] == 1  # re-execution touched no model
