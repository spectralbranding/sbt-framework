# Validator Query — grounded NL questions over the R1–R7 validators

`validator_query.py` lets you ask a natural-language question about how a set of
brands behaves under the SBT validators and get a typed, reproducible answer —
instead of reading the free-text `ValidationResult.summary()` and eyeballing which
brands violate which bound. It applies the "Search / Query as a Generated, Grounded
Artifact" pattern: the LLM compiles the question into a validated query program; the
program executes deterministically through the existing `validate_analysis` engine.

DSL: `docs/validator_query_schema_v0.2.yaml`

## Pipeline

```
NL question
  -> build_validator_registry()            # live registry introspected from report fields
  -> compile_nl_to_program(q, reg, llm_fn) # ONE LLM call; defaults to local Ollama ($0)
  -> validate_program(program, reg)        # structural raise + unknown-term flags
  -> execute_program(analysis, program)    # validate_analysis + deterministic eval
```

## Why it passes the efficiency gate

- **Structured store with stable vocab** — the six validator report dataclasses
  (`MetricReport`, `TrajectoryReport`, `CapacityReport`, `AllocationReport`,
  `SpecificationReport`, `MetamerismReport`) expose ~30 measurable scalar parameters.
- **Rich query space** — per-brand selection × aggregate gates × 6 validators × many
  parameters × numeric/categorical/bool ops.
- **Auditability / re-run** — validation is deterministic and the program is the audit
  key; a saved program re-runs with **zero LLM calls**.

## The four disciplines

1. **Grounded in a live registry.** `build_validator_registry()` *introspects the
   report dataclasses* (`dataclasses.fields` + resolved type hints), so the model can
   only reference validators/parameters that actually exist — it cannot invent one. If
   a report gains a field, the registry gains it automatically.
2. **Flag unknowns, never silently map.** An unknown validator/parameter raises; a
   categorical value outside the documented vocab (e.g. `overall_risk: extreme`) lands
   in `flags`.
3. **Typed artifact, validated before execution.** `validate_program()` enforces
   schema version, validator existence, **scope** (per-brand validators only in
   `predicates`, aggregate only in `gates`), parameter existence, and op/value typing.
4. **Deterministic translation + reproducibility.** `execute_program()` has no LLM in
   the hot path.

## Scopes

- `predicates` select **brands** by **per-brand** validators (`metric` R1,
  `trajectory` R6).
- `gates` are aggregate pass/fail checks on the **whole set** (`capacity` R4,
  `allocation` R7, `specification` R5, `metamerism` R2). A gate whose report isn't
  computable for the given analysis (e.g. `allocation` without founder weights) is
  noted, not crashed.

## Local-first ($0)

`compile_nl_to_program` takes an injectable `llm_fn`; the default does a local Ollama
JSON-mode call (`OLLAMA_URL`, `SBT_QUERY_MODEL`, default `qwen3:30b`). No paid API.
Tests inject a stub — no live LLM in CI.

## Usage

```python
from spectral_branding import validator_query as vq

analysis = {"brand_profiles": {"Acme": [...8 dims...], "Globex": [...]}}
reg = vq.build_validator_registry()
program = vq.compile_nl_to_program(
    "which brands are at high or critical absorption risk, "
    "given the set isn't overcrowded (capacity utilization <= 0.9)?",
    reg,
)
result = vq.execute_program(analysis, program)          # deterministic; re-run = 0 LLM
# result -> {program, flags, selected: [{brand, values}], gates: [...], gates_passed}
```

## Tests

`tests/test_validator_query.py` — registry-from-introspection, unknown
validator/parameter raises, scope enforcement, flagged unknown vocab, deterministic
per-brand selection + aggregate gates, missing-report handling, and zero-LLM
reproducibility. All run against the real `validate_analysis` with synthetic profiles;
no network, no model.
