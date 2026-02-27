# Spectral Brand Theory — Framework & Toolkit

An AI-native brand analysis framework. Six structured prompt modules that turn any capable LLM into a brand perception X-ray machine.

## What Is Spectral Brand Theory?

Brands are not objects with fixed properties. They are multi-dimensional signal sources perceived differently by every observer. Spectral Brand Theory (SBT) models this formally:

- **8 dimensions** of brand signal: semiotic, narrative, ideological, experiential, social, economic, cultural, temporal
- **Observer spectral profiles**: each audience cohort has different sensitivity, weights, and tolerances
- **Perception clouds**: probabilistic clusters that form in observers' minds from perceived signals
- **Conviction collapse**: when enough evidence accumulates, clouds crystallize into stable brand beliefs
- **Re-collapse**: new evidence (scandal, campaign, product failure) forces conviction to rebuild from scratch

The result: structural diagnosis of brand architecture that traditional audits cannot produce.

## Quick Start

**Run Module 1 on your brand in 10 minutes:**

1. Open a conversation with Claude, GPT-4, or equivalent LLM
2. Paste the system prompt from [`prompts/01_BRAND_DECOMPOSITION.md`](prompts/01_BRAND_DECOMPOSITION.md)
3. Provide your brand name, category, and any available materials
4. Optionally paste the YAML template from [`templates/01_brand_decomposition.yaml`](templates/01_brand_decomposition.yaml) for structured output

**Full 6-module pipeline:**

```
Module 1: Brand Decomposition    → Signal inventory across 8 dimensions
    ↓
Module 2: Observer Mapping       → 3-5 audience spectral profiles
    ↓
Module 3: Cloud Prediction       → Per-cohort perception clouds
    ↓
Module 4: Coherence Audit        → 7-metric scorecard + grade (A+ to F)
    ↓
Module 5: Emission Strategy      → Dimensionally specific action plan
    ↓
Module 6: Re-collapse Simulation → Disruption resilience testing
```

Each module feeds into the next. Total time: 2-4 hours for a complete brand audit.

## What You Get

After running the full pipeline on a brand, you get:

- **Signal inventory**: every signal the brand emits, classified by dimension, source type, and emission type
- **Observer profiles**: formal spectral profiles for 3-5 audience cohorts
- **Perception map**: what each cohort actually perceives (different cohorts = different brands)
- **Coherence grade**: A+ through F, with coherence *type* (ecosystem, signal, identity, experiential asymmetry, or incoherent)
- **Designed/ambient ratio**: how much of the brand's story is written by the brand vs. the environment
- **Emission strategy**: dimensionally specific recommendations for each cohort
- **Resilience profile**: how the brand responds to disruption, per cohort

## Validated Across 5 Brands

| Brand | Grade | Coherence Type | Key Finding |
|-------|-------|---------------|-------------|
| Hermes | A+ | Ecosystem | Structural absence (dark signals) creates more value than emission |
| IKEA | A- | Signal | Consistent designed signals produce uniform resilience |
| Patagonia | B+ | Identity | Ideological core creates depth at the cost of breadth |
| Erewhon | B- | Experiential asymmetry | Local and mediated audiences perceive different brands |
| Tesla | C- | Incoherent | Maximum emission power, minimum architectural health |

25+ validated non-obvious insights across the five studies.

## Repository Structure

```
sbt-framework/
├── README.md              ← You are here
├── prompts/               ← 6 prompt modules (copy-paste into any LLM)
│   ├── 01_BRAND_DECOMPOSITION.md
│   ├── 02_OBSERVER_MAPPING.md
│   ├── 03_CLOUD_PREDICTION.md
│   ├── 04_COHERENCE_AUDIT.md
│   ├── 05_EMISSION_STRATEGY.md
│   ├── 06_RECOLLAPSE_SIMULATION.md
│   └── README.md
├── templates/             ← YAML output schemas for structured results
│   ├── 01_brand_decomposition.yaml
│   ├── 02_observer_mapping.yaml
│   ├── 03_cloud_prediction.yaml
│   ├── 04_coherence_audit.yaml
│   ├── 05_emission_strategy.yaml
│   └── 06_recollapse_simulation.yaml
└── docs/                  ← Framework documentation
    ├── FRAMEWORK.md       ← Full theoretical framework (v2.0)
    └── GLOSSARY.md        ← Term definitions and relationships
```

## Key Concepts

| Concept | Definition |
|---------|-----------|
| **Signal** | A brand emission classified by dimension and source type |
| **Spectral profile** | An observer's sensitivity, weights, and tolerances across 8 dimensions |
| **Perception cloud** | Probabilistic cluster of signals in an observer's mind |
| **Conviction** | Stable brand belief formed when a cloud passes the collapse threshold |
| **Dark signal** | Structural absence — designed restriction that functions as a signal |
| **D/A ratio** | Designed vs. ambient signal balance (optimal zone: 55-65% designed) |
| **Coherence type** | Structural category of brand architecture (5 types, each with different resilience) |

## Related

| Resource | Description |
|----------|-------------|
| [Research Papers](https://github.com/spectralbranding/sbt-papers) | Working papers on SBT and the underlying epistemological architecture |
| [Substack](https://spectralbranding.substack.com) | Applied analysis articles |
| [SSRN Preprint](https://papers.ssrn.com) | Formal academic paper *(link pending)* |

## Author

**Dmitry Zharnikov** — dmitry@spectralbranding.com

## Citation

```bibtex
@misc{zharnikov2026sbt,
  title={Spectral Brand Theory: AI-Native Brand Analysis Toolkit},
  author={Zharnikov, Dmitry},
  year={2026},
  url={https://github.com/spectralbranding/sbt-framework}
}
```

## License

[MIT](LICENSE) — use freely with attribution.
