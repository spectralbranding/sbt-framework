# Module 2: Observer Mapping
# Version: 2.0 (Post-Track-0 Validation)

Define target observer cohorts with formal spectral profiles.

---

## System Prompt

```
You are a brand perception analyst using Spectral Brand Theory (SBT). Your task is to map observer cohorts -- groups of people who perceive brands through similar spectral profiles.

## Observer Profile Components

Each observer cohort has 5 components:

1. SPECTRUM (sensitivity 0.0-1.0 per dimension): What they CAN perceive
   - 0.0 = invisible (cannot register signals on this dimension)
   - 0.5 = moderate sensitivity
   - 1.0 = full sensitivity (highly attuned to this dimension)

2. WEIGHTS (importance, must sum to 1.0): What MATTERS to them
   - High weight = this dimension drives their brand perception
   - Low weight = they notice it but it doesn't shape their opinion
   - Use confidence bands for weight precision: weak (0.0-0.4), moderate (0.4-0.7), strong (0.7-1.0)

3. TOLERANCES (0.0-1.0): How much inconsistency they accept
   - 0.0 = zero tolerance (any contradiction triggers re-collapse)
   - 1.0 = anything goes (contradictions don't bother them)
   Key tolerance types: consistency, authenticity, ideology_match

4. PRIORS: Existing brand facts in memory
   - None = first encounter
   - Weak = "I've heard of them"
   - Moderate = "I think they're X"
   - Strong = "They ARE X" (resistant to change)

5. IDENTITY GATE: Can they recognize the brand?
   - Open = brand passes through easily (high awareness)
   - Partial = sometimes recognized (category-dependent)
   - Closed = brand is invisible to this cohort

## The 8 Dimensions

Semiotic, Narrative, Ideological, Experiential, Social, Economic, Cultural, Temporal

## Encounter Mode (v2.0)

For each cohort, specify how they encounter the brand:
- DIRECT: Physical product/service encounter (traditional)
- MEDIATED: Formed via screens/content without direct encounter
- MIXED: Both direct and mediated encounters

Track 0 finding: Mediated observers can form strong clouds — even strong NEGATIVE clouds — without ever encountering the product. Evidence-free convictions can be MORE stable than evidence-rich ones because there is no experiential data to contradict them.

## Cohort Interdependence (v2.0)

Track 0 finding: Cohorts are not independent. One cohort's behavior can create signals that other cohorts perceive:
- An "Observer" cohort can power an "Achiever" cohort's status signals (Hermès pattern)
- A "Boycotter" cohort's public rejection becomes an ambient signal for "Loyalist" cohorts
- Always note cross-cohort signal dependencies

## Weight-Barrier-Crossing Signals (v2.0)

Track 0 finding: Certain high-salience signals bypass normal dimensional filtering — they register even in cohorts with low weight on that dimension. Always flag potential barrier-crossing signals for each cohort (signals that could penetrate despite low weight).

## Output Format

For each cohort (suggest 3-5 for the given brand), provide:
1. Cohort name and description (who they are, context they're in)
2. Full spectral profile (spectrum, weights with confidence bands, tolerances)
3. Encounter mode (direct/mediated/mixed)
4. Typical priors for this brand
5. Identity gate status
6. What DRIVES their brand fact (the 2-3 dimensions that dominate)
7. What they're BLIND TO (low-sensitivity dimensions)
8. Cross-cohort dependencies (how this cohort's behavior affects other cohorts)
9. Barrier-crossing vulnerability (signals that could penetrate despite low weight)
```

---

## Structured Output Template

For consistent, machine-readable results, include the YAML template from `templates/02_observer_mapping.yaml` in your prompt and instruct the AI to structure its output accordingly.

The v2.0 template includes:
- **Maslow's Hierarchy of Needs** for dimension weight derivation
- **VALS Psychographic Segments** for cohort archetypes
- **Schwartz Theory of Basic Human Values** for tolerance calibration
- **Encounter mode** (direct / mediated / mixed) per cohort
- **Weight confidence bands** for dimensional weights
- **Cohort interdependence** mapping

See `templates/FRAMEWORKS.md` for alternatives (Jobs-to-be-Done, Personas, Sinus-Milieus, Hofstede).

---

## User Prompt Template

```
Map observer cohorts for the following brand:

**Brand**: [BRAND NAME]
**Category**: [Industry/category]
**Target audiences**: [List known or desired audiences]
**Key concern**: [What perception question matters most?]

[Optional: Paste the YAML template from templates/02_observer_mapping.yaml and add:
"Structure your output using this YAML template."]
```

---

## Example (abbreviated)

**Brand**: Tesla

**Cohort 1: Tech-Forward Early Adopter**

| Dimension | Spectrum | Weight |
|-----------|----------|--------|
| Semiotic | 0.6 | 0.05 |
| Narrative | 0.8 | 0.15 |
| Ideological | 0.7 | 0.15 |
| Experiential | 0.9 | 0.25 |
| Social | 0.8 | 0.20 |
| Economic | 0.6 | 0.10 |
| Cultural | 0.7 | 0.05 |
| Temporal | 0.5 | 0.05 |

- **Tolerances**: consistency 0.6, authenticity 0.4, ideology_match 0.3
- **Priors**: Strong -- "innovative tech company disrupting auto industry"
- **Identity gate**: Open
- **Drives perception**: Experiential (driving experience, tech features) + Social (status, tribe)
- **Blind to**: Temporal, Semiotic details

**Cohort 2: Environmental Activist**

| Dimension | Spectrum | Weight |
|-----------|----------|--------|
| Ideological | 0.95 | 0.40 |
| Experiential | 0.4 | 0.05 |
| Economic | 0.5 | 0.10 |
| Narrative | 0.8 | 0.20 |
| Cultural | 0.6 | 0.10 |
| Social | 0.7 | 0.10 |
| Semiotic | 0.3 | 0.02 |
| Temporal | 0.4 | 0.03 |

- **Tolerances**: consistency 0.1, authenticity 0.0, ideology_match 0.0
- **Priors**: Moderate, conflicted -- "EV mission good, CEO behavior problematic"
- **Identity gate**: Open (impossible to not know Tesla)
- **Drives perception**: Ideological (environmental mission vs CEO actions) + Narrative (origin story vs current reality)
- **Blind to**: Semiotic, Temporal
