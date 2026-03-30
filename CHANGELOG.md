# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.3.0] — 2026-03-20

### Added
- **Mathematical Foundations** integrated into core framework (Section 3.6): formal metric axioms,
  simplex constraints, and geometric bounds previously documented only in companion papers (R0-R7)
  are now part of the framework itself
- **Module 7 — Resource Allocation**: complete prompt, YAML output template, and validator hardening.
  Three practitioner features: financial report input (P&L / 10-K → dimension mapping via
  DIMENSION_GLOSSARY), Code Execution Mode (deterministic Python math, zero hallucination on hard
  numbers), and a clarification protocol for ambiguous budget line items
- **R7 Resource Allocation validator** (`src/spectral_branding/validators/`): checks optimal
  dimensional investment, alignment gap, and multi-cohort allocation efficiency against bounds
  proved in R7 (Spectral Resource Allocation)
- **Velocity tracking**: per-dimension velocity computation (signed rate of change, direction,
  acceleration, time-to-absorption estimates from sequential snapshots). Operationalizes the R6
  drift vector formalism
- **Conformal prediction bands** on velocity estimates (Proposition 6 implementation): uncertainty
  envelopes with coverage guarantees, not point estimates
- **Data quality gates** in Module 7: every output tagged with data source (`survey`,
  `financial_report`, `llm_estimate`); estimated inputs trigger mandatory warnings; if >30% of
  budget cannot be mapped to dimensions the tool refuses output rather than guessing
- **Demand-side analysis** note in README: observer cohort weights decompose market demand into
  eight dimensions; metamerism detection, capacity analysis, and trajectory risk reframed as
  investment guides
- **Retroactive mathematical validation** for all 5 canonical brand profiles (Hermès, IKEA,
  Patagonia, Erewhon, Tesla): every profile passes metric axioms (R1), no metameric pairs exist
  (R2), positioning capacity is unconstrained (R4), and trajectory risk is low (R6)
- **102 unit tests** across 7 validators (up from 86 in v2.2)
- **Microscope allegory** added to README: "Aaker drew the anatomy chart. SBT built the microscope."
- **CITATION.cff** updated: canonical preferred-citation title, ORCID added
- R7 paper reference and Zenodo DOI added to Research section

### Changed
- Framework document (`docs/FRAMEWORK.md`) updated to v2.3: version references, Hermès accent
  corrected, private repo path references removed, book draft sections removed
- SSRN links replaced with Zenodo concept DOIs across all documentation
- Test count updated from 86 to 102 in README and framework docs
- "validated" language softened to "demonstrated" in public-facing README to reflect exploratory
  status of the analysis

### Fixed
- Hermès accent (`Hermes` → `Hermès`) in FRAMEWORK.md
- Black pinned to 26.3.1 (CVE-2026-32274)
- `.flake8` config added to exclude `.venv` from linting
- `uv.lock` committed for reproducible CI builds
- `dev` optional dependencies added to `pyproject.toml` so CI installs test tools correctly
- Private repo references removed from FRAMEWORK.md header

---

## [2.2.0] — 2026-03-08

### Added
- **Signal Dissemination Layer**: pre-encounter mechanics added to framework (Hypotheses H6-H10).
  Models how signals propagate before any observer encounter occurs
- **Fleet CI workflow**: GitHub Actions quality + security checks (black, flake8, mypy, pytest,
  Trivy vulnerability scan). Trivy updated to official Action to fix DB download 404
- **orgschema-toolkit cross-reference** added to Related Projects in README
- **alibi repo link** added to README Research section
- **Trademark notice** added to README

### Changed
- Framework version references updated to v2.1 in all docs
- Stale Mermaid diagram label fixed (version label in pipeline diagram)

### Fixed
- Ontological self-contradiction in core brand claim (C4): resolved inconsistency in the
  "brand in itself" assertion
- Validation hedging and exploratory analysis framing (C1, C3, M17): language tightened to
  distinguish empirical claims from theoretical propositions
- D/A ratio arithmetic (M2, M5): corrected to three-part D/A/S notation (Designed / Ambient /
  Structural absence)
- Re-collapse definition inconsistency: clarified that surviving evidence and priors persist
  through re-collapse (not a full wipe)
- Re-collapse alibi analogy: priors are an SBT extension, not an alibi feature
- Terminology reconciliation: literature gaps, sensitivity summary, L1/L2 example added following
  adversarial review
- SSRN URL placeholder replaced with live preprint link
- "novel" → "candidate" mechanisms: hedging language in README to reflect pre-peer-review status

---

## [2.1.0] — 2026-03-03

### Added
- **Non-ergodic perception** added to framework and glossary (v2.1): signals compound
  multiplicatively; sequence matters; perception path-dependent
- **AI Agent Observer** entry in GLOSSARY: LLM as a third observer type alongside human and
  search-engine observers
- **Search Engine Observer** entry in GLOSSARY: connected to the three-observer model (human /
  AI agent / search engine)
- **Coherence taxonomy derivation** added to Module 5 / FRAMEWORK.md: 5 coherence types with
  derivation logic (Ecosystem, Signal, Identity, Experiential asymmetry, Incoherent)
- **Dual-layer output architecture**: structured YAML + human-readable narrative output for all
  modules
- **Observer Cohort** glossary entry expanded: dynamic membership definition, perceptual (not
  demographic) grounding
- **Priors** glossary entry: cognitive science basis, objective vs. belief-weighted distinction
- **Discovery 7.11 — Cross-model pipeline robustness**: full 5-brand replication data across
  Claude, GPT-4, and Gemini models
- **Brand** foundational definition added to glossary
- **Brand Code** term added to glossary; `brand-code` repo linked in Research section

### Changed
- Observer model sharpened (M3, M11, M16, M2): precision improvements on cohort formation
  mechanics and signal filtering
- Theory status upgraded to hypothesis-stage with explicit H6-H10 (Session 06 update)
- Related frameworks section expanded (M7, M8, M11): Aaker, Kapferer, Keller positioning clarified

### Fixed
- Collapse threshold specified (C5, M12, M13): re-collapse mechanics clarified
- Scarcity formula corrected
- Brand conviction terminology: "brand belief" → "brand conviction" throughout all documents

---

## [2.0.0] — 2026-02-26

### Added
- Initial public release of the Spectral Brand Theory framework
- **7 prompt modules** (copy-paste into any LLM):
  - Module 1: Brand Decomposition — 8-dimension signal inventory, D/A ratio
  - Module 2: Observer Mapping — 3-5 observer cohort profiles
  - Module 3: Cloud Prediction — per-cohort perception cloud map
  - Module 4: Coherence Audit — 7-metric coherence scoring (A+ to F)
  - Module 5: Emission Strategy — dimensionally specific action plan per cohort
  - Module 6: Re-collapse Simulation — disruption resilience testing
  - Module 7: Resource Allocation — optimal investment, alignment gaps, blind spots
- **7 YAML output templates** for structured results (one per module)
- **DIMENSION_GLOSSARY.yaml**: dual-purpose dimension reference (human-readable + LLM-parseable).
  Maps financial report line items to the 8 dimensions for Module 7 financial input mode
- **ATOM_TAXONOMY.yaml** (`data/`): signal classification reference
- **FRAMEWORK.md** (`docs/`): full theoretical framework document
- **GLOSSARY.md** (`docs/`): term definitions and relationships
- **Architecture diagrams** (`docs/architecture/`):
  - `BRAND_PIPELINE.mmd`: full signal pipeline (emission → cloud → collapse)
  - `OBSERVER_MODEL.mmd`: observer cohort spectral profiles
  - `ALIBI_ANALOGY.mmd`: structural analogy between alibi finance and SBT
- **Python validation module** (`src/spectral_branding/validators/`): 6 math-hardened validators
  (numpy + scipy) covering metric, metamerism, cohort, capacity, trajectory, and specification
  checks
- **86 unit tests** for validators (`tests/`)
- **5 canonical brand demonstrations**: Hermès, IKEA, Patagonia, Erewhon, Tesla — covering all
  5 coherence types with 25+ non-obvious findings and 9 candidate mechanisms
- **`pyproject.toml`** with hatchling build system, Python 3.12+, numpy + scipy dependencies
- **`CITATION.cff`** for machine-readable citation
- **Framework reference** (`docs/FRAMEWORKS.md`): mapping to Aaker, Kapferer, Keller frameworks
- **Mermaid landing-page diagram** in README: 8-dimension brand signal → perception pipeline

---

[2.3.0]: https://github.com/spectralbranding/sbt-framework/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/spectralbranding/sbt-framework/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/spectralbranding/sbt-framework/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/spectralbranding/sbt-framework/releases/tag/v2.0.0
