"""Tests for the validator_query command-line interface (Search-as-Code CLI).

These exercise the CLI surface with NO live LLM and NO live Ollama: the --ask
path is tested by monkeypatching ``_default_llm_fn`` with a deterministic stub,
and the --program path needs no model at all. The program is the reproducibility
unit, so most checks load a saved program and re-run it deterministically.
"""

from __future__ import annotations

import json

import pytest

from spectral_branding import validator_query as vq

# A valid program over the live registry: select metric-valid brands and assert a
# capacity gate that holds for the sample analysis below.
_GOOD_PROGRAM = {
    "schema_version": "0.2",
    "predicates": [
        {"validator": "metric", "parameter": "valid", "op": "eq", "value": True}
    ],
    "gates": [
        {"validator": "capacity", "parameter": "n_brands", "op": "ge", "threshold": 2}
    ],
    "flags": [],
}

# Same selection but a gate that FAILS for the sample (n_brands >= 99) -> exit 2.
_FAILING_GATE_PROGRAM = {
    "schema_version": "0.2",
    "predicates": [],
    "gates": [
        {"validator": "capacity", "parameter": "n_brands", "op": "ge", "threshold": 99}
    ],
    "flags": [],
}

_ANALYSIS = {
    "brand_profiles": {
        "BrandA": [0.3, 0.5, 0.2, 0.4, 0.6, 0.3, 0.5, 0.4],
        "BrandB": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        "BrandC": [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    }
}


def _write(path, obj) -> str:
    path.write_text(json.dumps(obj))
    return str(path)


# --- --program path (no LLM) -------------------------------------------------


def test_program_only_no_report_skips_execution(tmp_path, capsys):
    prog = _write(tmp_path / "p.yaml", _GOOD_PROGRAM)
    code = vq.main(["--program", prog])
    out = capsys.readouterr().out
    assert code == 0
    assert "COMPILED VALIDATOR-QUERY PROGRAM" in out
    assert "no report provided" in out


def test_program_with_report_executes_exit_0(tmp_path, capsys):
    prog = _write(tmp_path / "p.yaml", _GOOD_PROGRAM)
    report = _write(tmp_path / "r.json", _ANALYSIS)
    code = vq.main(["--program", prog, "--report", report])
    out = capsys.readouterr().out
    assert code == 0
    assert "Selected:" in out
    assert "[PASS]" in out


def test_failing_gate_yields_exit_2(tmp_path):
    prog = _write(tmp_path / "p.yaml", _FAILING_GATE_PROGRAM)
    report = _write(tmp_path / "r.json", _ANALYSIS)
    code = vq.main(["--program", prog, "--report", report])
    assert code == 2


# --- error handling (exit 1) -------------------------------------------------


def test_missing_program_file_exit_1(tmp_path, capsys):
    code = vq.main(["--program", str(tmp_path / "nope.yaml")])
    err = capsys.readouterr().err
    assert code == 1
    assert "not found" in err


def test_bad_program_unknown_validator_exit_1(tmp_path, capsys):
    bad = {
        "schema_version": "0.2",
        "predicates": [
            {"validator": "ghost", "parameter": "x", "op": "eq", "value": 1}
        ],
        "gates": [],
    }
    prog = _write(tmp_path / "bad.yaml", bad)
    code = vq.main(["--program", prog])
    err = capsys.readouterr().err
    assert code == 1
    assert "validation failed" in err and "not a known validator" in err


def test_missing_report_file_exit_1(tmp_path, capsys):
    prog = _write(tmp_path / "p.yaml", _GOOD_PROGRAM)
    code = vq.main(["--program", prog, "--report", str(tmp_path / "nope.json")])
    err = capsys.readouterr().err
    assert code == 1
    assert "report file not found" in err


def test_non_mapping_program_exit_1(tmp_path, capsys):
    p = tmp_path / "list.json"
    p.write_text(json.dumps([1, 2, 3]))
    code = vq.main(["--program", str(p)])
    err = capsys.readouterr().err
    assert code == 1
    assert "mapping" in err


# --- mutually-exclusive / required mode --------------------------------------


def test_ask_and_program_mutually_exclusive(tmp_path):
    prog = _write(tmp_path / "p.yaml", _GOOD_PROGRAM)
    with pytest.raises(SystemExit):
        vq.main(["--ask", "x", "--program", prog])


def test_one_mode_required():
    with pytest.raises(SystemExit):
        vq.main([])


# --- --ask path (stubbed local llm_fn; NO live Ollama) -----------------------


def _patch_llm(monkeypatch, program: dict) -> dict:
    state = {"calls": 0}

    def fake(system: str, user: str) -> str:
        state["calls"] += 1
        return json.dumps(program)

    monkeypatch.setattr(vq, "_default_llm_fn", fake)
    return state


def test_ask_compiles_and_prints(monkeypatch, capsys):
    _patch_llm(monkeypatch, _GOOD_PROGRAM)
    code = vq.main(["--ask", "metric-valid brands with capacity headroom"])
    out = capsys.readouterr().out
    assert code == 0
    assert "Compiling NL request" in out
    assert "COMPILED VALIDATOR-QUERY PROGRAM" in out
    assert "no report provided" in out


def test_ask_save_program_round_trip(monkeypatch, tmp_path, capsys):
    state = _patch_llm(monkeypatch, _GOOD_PROGRAM)
    saved = tmp_path / "saved.yaml"
    report = _write(tmp_path / "r.json", _ANALYSIS)

    # 1) Compile via (stubbed) LLM and persist the program.
    code = vq.main(
        ["--ask", "valid brands", "--save-program", str(saved), "--report", report]
    )
    assert code == 0
    assert saved.exists()
    assert state["calls"] == 1

    # 2) Re-run deterministically from the saved program: NO further LLM calls.
    code2 = vq.main(["--program", str(saved), "--report", report])
    assert code2 == 0
    assert state["calls"] == 1  # the saved-program re-run touched no model

    out = capsys.readouterr().out
    assert "Program saved" in out


def test_ask_model_flag_sets_env(monkeypatch):
    _patch_llm(monkeypatch, _GOOD_PROGRAM)
    import os

    monkeypatch.delenv("SBT_QUERY_MODEL", raising=False)
    vq.main(["--ask", "x", "--model", "test-model:7b"])
    assert os.environ["SBT_QUERY_MODEL"] == "test-model:7b"


def test_ask_llm_failure_exit_1(monkeypatch, capsys):
    def boom(system: str, user: str) -> str:
        raise RuntimeError("ollama down")

    monkeypatch.setattr(vq, "_default_llm_fn", boom)
    code = vq.main(["--ask", "x"])
    err = capsys.readouterr().err
    assert code == 1
    assert "failed" in err
