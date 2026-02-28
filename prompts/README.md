# Spectral Brand Analysis: AI Prompt Kit

**Version**: 2.0 (Post-Track-0 Validation)
**Last Updated**: 2026-02-27

---

## What This Is

A set of 6 structured prompts for analyzing any brand through the Spectral Brand Theory (SBT) framework. Each module is a self-contained prompt that can be used with Claude, GPT, or any capable LLM.

**v2.0** incorporates 9 novel mechanisms discovered during Track 0 validation across 5 brands (Patagonia, Tesla, IKEA, Hermès, Erewhon). Key additions:
- **Dark signals / structural absence**: Value creation through designed signal restriction
- **Coherence type taxonomy**: 5 distinct types (ecosystem, signal, identity, experiential_asymmetry, incoherent)
- **Cloud formation modes**: standard, mediated, stalled
- **Cloud valence**: positive/negative/ambivalent with asymmetric resilience
- **Temporal compounding curve**: Heritage compounds non-linearly over decades
- **D/A Goldilocks zone**: Optimal designed/ambient ratio is 55-65%
- **Brand health vs power independence**: A brand can be maximally famous and structurally broken

Each module includes:
- **System prompt** with SBT methodology and instructions (including v2.0 Track 0 discoveries)
- **User prompt template** with fill-in-the-blank fields
- **Output template** (YAML) for structured, machine-readable results
- **Framework references** that can be swapped for alternatives

## How to Use

1. Start with **Module 1** (Brand Decomposition) -- it produces the signal inventory that all other modules need
2. Run **Module 2** (Observer Mapping) to define your target cohorts
3. Modules 3-6 build on 1 and 2 (see dependency table below)

### With Output Templates

For each module, include the corresponding YAML template from `templates/` in your prompt. Tell the AI: "Structure your output using the provided YAML template." This ensures:
- Consistent output across analysis sessions
- Machine-readable results that can feed into the next module
- Framework-aligned categorization (SWOT, PESTEL, etc.)

Templates are optional but recommended. Without them, the AI produces free-form analysis. With them, you get structured data.

### Swapping Frameworks

Each template uses specific external frameworks (SWOT, Maslow, PESTEL, etc.) but these are **not locked in**. See `templates/FRAMEWORKS.md` for the full reference of which frameworks each module uses and what alternatives are available. To swap: update the `frameworks_used` section in the template and adjust field names accordingly.

## Modules

| Module | Prompt | Template | Purpose | Depends On |
|--------|--------|----------|---------|------------|
| 1 | `01_BRAND_DECOMPOSITION.md` | `templates/01_brand_decomposition.yaml` | Decompose a brand into signals across 8 dimensions | None |
| 2 | `02_OBSERVER_MAPPING.md` | `templates/02_observer_mapping.yaml` | Map target observer cohorts with spectral profiles | None |
| 3 | `03_CLOUD_PREDICTION.md` | `templates/03_cloud_prediction.yaml` | Predict how each cohort assembles the brand | 1 + 2 |
| 4 | `04_COHERENCE_AUDIT.md` | `templates/04_coherence_audit.yaml` | Score brand coherence and identify gaps | 3 |
| 5 | `05_EMISSION_STRATEGY.md` | `templates/05_emission_strategy.yaml` | Design emission plan for target convictions | 1 + 2 + 4 |
| 6 | `06_RECOLLAPSE_SIMULATION.md` | `templates/06_recollapse_simulation.yaml` | Simulate conviction disruption and re-collapse | 3 + 4 |

## Frameworks Used Per Module

| Module | Primary Framework | Secondary | Alternatives |
|--------|------------------|-----------|-------------|
| 1 | ISO 20671 (brand evaluation) | Interbrand Brand Strength | Kapferer Prism, Keller CBBE |
| 2 | Maslow (needs hierarchy) | VALS, Schwartz Values | Jobs-to-be-Done, Personas, Sinus-Milieus |
| 3 | SWOT Analysis | Perceptual Mapping | Force Field, Stakeholder Mapping, Blue Ocean |
| 4 | ISO 10668 (brand valuation) | BAV, Balanced Scorecard | NPS, Keller CBBE, Aaker Equity |
| 5 | RACE (digital marketing) | Ansoff Matrix, AIDA | SOSTAC, Blue Ocean, Porter, McKinsey 3H |
| 6 | PESTEL Analysis | Risk Matrix, Scenario Planning | VUCA, Cynefin, Black Swan, Bowtie |

Full details: [templates/FRAMEWORKS.md](../templates/FRAMEWORKS.md)

## Quick Start

1. Copy the system prompt from Module 1 into a new conversation with your LLM
2. Optionally paste the YAML template and say "use this structure for output"
3. Provide your brand name and any supporting materials (website URL, social profiles, recent campaigns)
4. The LLM will produce a structured signal inventory
5. Feed that output into Module 2 and continue through the pipeline
