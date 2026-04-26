# Roadmap

This is a research framework, not a commercial product. The roadmap reflects research priorities
and framework maturation milestones, not product release schedules. Items are added when the
theoretical or empirical foundation is established — not speculatively.

---

## Current State: v2.3 (March 2026)

- 7 prompt modules covering the full brand analysis pipeline
- 7 math-hardened validators (numpy + scipy), 102 unit tests
- 5 canonical brand demonstrations (Hermès, IKEA, Patagonia, Erewhon, Tesla)
- Mathematical foundations integrated from R0-R7 companion papers
- Velocity tracking + conformal prediction bands on trajectory estimates
- Fleet CI: black, flake8, mypy, pytest, Trivy

---

## Near-Term (v2.4 — v2.5)

### Empirical Validation Instruments [IN PROGRESS]

The 5-brand demonstration used LLM-generated signal inventories cross-validated against the
R1-R7 mathematical bounds. The next step is survey instruments that collect observer spectral
profiles from real respondents.

- [ ] Survey instrument design: 8-dimension perception battery (observer side)
- [ ] Scoring protocol: raw responses → spectral profile → cloud prediction input
- [ ] Inter-rater reliability checks: multi-observer convergence on same brand
- [ ] Pilot data collection protocol (research collaboration framework)

*Theoretical basis: R1 metric axioms define what a valid observer spectral profile looks like;
R3 cohort boundary concentration bounds define minimum sample sizes per cohort.*

### Velocity Tracking — Longitudinal Protocol [PLANNED]

The velocity validator currently operates on two snapshots. A longitudinal protocol specifies
how to collect and compare sequential snapshots in practice.

- [ ] Snapshot collection guide: what to capture, at what intervals, how to store
- [ ] Sequential input format: multi-snapshot YAML schema
- [ ] Acceleration detection: flag when velocity is itself changing (second derivative)
- [ ] Time-to-absorption warning threshold calibration

*Theoretical basis: R6 diffusion dynamics — absorption is irreversible; early warning is the
only intervention point.*

### Additional Brand Profiles [PLANNED]

Expand the canonical demonstration set to cover more coherence-type edge cases and
cross-cultural examples.

- [ ] At least 2 additional brands representing underrepresented coherence types
- [ ] At least 1 non-Western brand to begin cross-cultural coverage
- [ ] Each profile retroactively validated against R1-R7 bounds (same protocol as v2.3)

### Module 7 Financial Mapping Expansion [PLANNED]

The DIMENSION_GLOSSARY.yaml currently maps common marketing/operations line items. Expand
coverage to more industry-specific budget structures.

- [ ] Agency/consulting P&L patterns
- [ ] DTC brand budget structures (performance marketing split)
- [ ] Luxury/heritage brand budget patterns (high Temporal and Semiotic allocation norms)

---

## Medium-Term (v3.0)

### Cross-Cultural Validation Framework [PLANNED]

SBT posits that observer spectral profiles vary across cultural contexts. The 8 dimensions
are proposed as culturally invariant — but their relative weights are not. This needs
empirical testing.

- [ ] Cross-cultural dimension weight comparison (minimum 3 markets)
- [ ] Cultural modifier documentation: known weight shifts per dimension per context
- [ ] Cohort boundary sensitivity to cultural context

*Theoretical basis: R3 cohort boundaries — concentration of measure arguments hold
dimensionality-independent but observer weight priors are culturally conditioned.*

### Web Interface / Structured Output API [PLANNED]

The current framework is prompt-first: users copy prompts into an LLM. A thin structured
interface would make pipeline outputs machine-readable and composable.

- [ ] FastAPI wrapper around the Python validator module (local use only, no cloud dependency)
- [ ] Pipeline orchestration: chain Module 1-7 outputs programmatically
- [ ] Structured output validation endpoint: POST brand YAML → validation report JSON
- [ ] No SaaS ambition; designed for local research use and API experimentation

### Metamerism Detection Tooling [PLANNED]

R2 proves that brands with similar aggregate scores can have structurally different 8D profiles
(spectral metamerism). Tooling to detect and visualize this is under-developed.

- [ ] Automated metamerism scan: given N brand profiles, flag all metameric pairs
- [ ] Visual output: 8D radar comparison for flagged pairs
- [ ] Minimum separation report: cheapest signal change to break metamerism

### Specification Validator Integration (R5) [PLANNED]

The R5 (Impossibility) paper establishes bounds on organizational spec coverage and cascade
consistency. Module integration is partial — the specification validator exists but is not
wired into Module 5 (Emission Strategy) output.

- [ ] Wire specification validator into Module 5 output
- [ ] Cross-check organizational capacity claims against R5 impossibility bounds
- [ ] Flag when emission strategy implies spec changes beyond capacity

---

## Long-Term (v4.0+)

### Real-Time Brand Monitoring Integration [FUTURE]

Brand perception shifts continuously. The current framework operates on static or periodic
snapshots. Real-time integration would require external data feeds.

- [ ] Define minimum signal feed specification: what inputs are needed at what frequency
- [ ] Velocity tracker adaptation for streaming input
- [ ] Alert system: notify when absorption risk threshold is crossed
- [ ] Privacy and data quality requirements for live signal ingestion

*Note: this is a research architecture goal, not a commercial monitoring product.*

### Integration with Brand Tracking Platforms [FUTURE]

Major brand tracking platforms (Kantar, Nielsen, YouGov BrandIndex) produce data that maps
partially onto SBT dimensions. Formal integration requires:

- [ ] Dimension mapping table: brand tracker metrics → SBT 8 dimensions
- [ ] Conversion protocol: tracker score ranges → spectral profile format
- [ ] Validation: does tracker-derived profile pass R1 metric axioms?
- [ ] Pilot with at least one platform's public data

### Formal Peer-Reviewed Validation Study [FUTURE]

The framework currently rests on mathematical proof (R0-R7) and LLM-assisted demonstration.
A peer-reviewed empirical validation study — survey data, real observers, real brands — would
move SBT from "mathematical framework with demonstration" to "empirically validated framework."

- [ ] Collaboration with at least one academic research group
- [ ] Pre-registered study protocol
- [ ] Minimum N per cohort: per R3 concentration of measure bounds
- [ ] Journal target: Journal of Consumer Research or similar

### Multi-Brand Portfolio Analysis (R21) [THEORY + EMPIRICAL COMPLETE]

R21 (Spectral Immunity, 2026ac) merges the R8 theory and R20 empirical work into a single
analytical–empirical paper: 9,925 observations across 40 brands, 13 models, and 7 training
traditions confirm spectral immunity for AI observers. Awareness gate is necessary but not
sufficient — bandwidth as generalization of rational inattention dominates. DOI:
[10.5281/zenodo.19765401](https://doi.org/10.5281/zenodo.19765401). Framework tooling for
portfolio analysis can now proceed against a published empirical baseline.

- [ ] Portfolio Module 8: cross-brand interference detection (with awareness-gate + bandwidth gating)
- [ ] Portfolio Module 9: coherence scoring across brand families
- [ ] Capacity analysis: E8 lattice bounds applied to portfolio positioning
- [ ] LVMH-type vs. Unilever-type portfolio archetypes as canonical demonstrations

### Coherence Shock Recovery and Threshold Inequality (R22) [THEORY + SIMULATION COMPLETE]

R22 (Spectral Gap Restoration, 2026ad) formalizes the sufficient condition for cohort
separability to survive disruption: corrective coherence emission rate μ must exceed spectral
leakage rate λ at the observer cohort's detection scale. Grounded in Kato-Rellich perturbation
theory and Diaconis–Stroock spectral-gap-mixing-time bounds. Monte Carlo demonstration with
Dove 2003–2023 design parameters: terminal gap 1.10 vs .02 (52x ratio), IRF half-life 1.4 vs
13.1 months. H22: gap collapse precedes conviction reorientation by 6–18 months. DOI:
[10.5281/zenodo.19778549](https://doi.org/10.5281/zenodo.19778549). Target: Marketing Science.

- [ ] Module 6 (Re-collapse Simulation) extension: compute μ/λ ratio from snapshot inputs
- [ ] Resilience scoring: flag when brand is in λ > μ regime (absorption risk)
- [ ] Companion paper using R10 Dove longitudinal data for empirical regime-map estimation

---

## Out of Scope

These items are explicitly not on the roadmap:

- **SaaS or cloud product**: the framework will remain open-source and local-first
- **Proprietary brand data collection**: the framework provides instruments, not data
- **Consulting engagements**: this is a research toolkit; commercial use is at the user's discretion
- **Social media sentiment integration**: sentiment is a proxy for signals, not signals themselves;
  this conflation is a documented limitation of existing brand tracking approaches

---

## Legend

| Status | Meaning |
|--------|---------|
| [DONE] | Shipped in a released version |
| [IN PROGRESS] | Active work, expected in next version |
| [PLANNED] | Committed to, not yet started |
| [FUTURE] | On the horizon, no committed timeline |

---

*This roadmap reflects the state of the research program as of March 2026. Items are updated
when theoretical foundations shift or empirical evidence changes priorities.*
