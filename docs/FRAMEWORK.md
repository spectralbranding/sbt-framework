# Spectral Branding Framework

**Version**: 2.3 (Mathematical Foundations)
**Status**: Draft
**Last Updated**: 2026-03-09
**Related**: `GLOSSARY.md`

---

## Overview

This document applies the atom-cloud-fact epistemological pattern from the alibi project to branding theory. A brand is modeled as a stellar object: composed of brand-atom signals across multiple dimensions, perceived differently by observers with different spectral sensitivities and positions. There is no single brand perception that applies universally across all observers — each cohort assembles structurally different brand meaning from the same signal environment. The brand's signal architecture (what it emits across eight dimensions) can be characterized at the brand level; brand meaning exists only in the minds of those who perceive it.

The framework provides both a critique of traditional branding theory and a practical architecture for AI-era brand management.

A note on terminology: 'Spectral Brand Theory' is the proper name of this work (as published on Zenodo). The term 'theory' follows a common convention in academic frameworks and reflects the theoretical ambition of the work. SBT is currently best characterized as an analytical framework: a formally specified set of constructs and mechanisms that generates testable hypotheses about brand perception. It becomes a theory in the scientific sense — with predictive power and empirical validation — as the hypotheses in Part 7 are tested.

---

## Part 1: The Epistemic Pattern

The alibi project implements a three-stage pipeline that models the progression from observation to knowledge. This pattern is domain-agnostic.

```mermaid
graph TD
    subgraph "Stage 1: Observation"
        D1[Document A] -->|extract| A1[Atom: VENDOR]
        D1 -->|extract| A2[Atom: ITEM]
        D1 -->|extract| A3[Atom: AMOUNT]
        D1 -->|extract| A4[Atom: DATETIME]
        D2[Document B] -->|extract| A5[Atom: VENDOR]
        D2 -->|extract| A6[Atom: AMOUNT]
        D2 -->|extract| A7[Atom: DATETIME]
    end

    subgraph "Stage 2: Hypothesis"
        A1 & A2 & A3 & A4 -->|bundle| B1[Bundle: BASKET]
        A5 & A6 & A7 -->|bundle| B2[Bundle: STATEMENT_LINE]
        B1 & B2 -->|score > 0.5| C1[Cloud: Probabilistic Cluster]
    end

    subgraph "Stage 3: Knowledge"
        C1 -->|collapse| F1[Fact: Confirmed Purchase]
    end

    style D1 fill:#e8f4fd,stroke:#333
    style D2 fill:#e8f4fd,stroke:#333
    style C1 fill:#fff3cd,stroke:#333
    style F1 fill:#d4edda,stroke:#333
```

Seven architectural principles make this work:

| # | Principle | Alibi Implementation | Domain-Agnostic Form |
|---|-----------|---------------------|---------------------|
| 1 | Dimensional typing | 6 atom types (VENDOR, ITEM, PAYMENT, DATETIME, AMOUNT, TAX) | Observations belong to typed dimensions |
| 2 | Source-bound observation | Atoms belong to exactly one document | No observation claims to see from two places |
| 3 | Hard identity gate | Vendor gate prevents false clustering | Core identity match is a precondition for clustering |
| 4 | Asymmetric tolerances | receipt+statement: 5d, invoice+payment: 60d | Context determines what "close enough" means |
| 5 | Weighted multi-dimensional scoring | vendor 0.30, amount 0.40, date 0.20, items 0.50 bonus | Not all dimensions are equal |
| 6 | Re-collapse on new evidence | Facts rebuilt from scratch, never patched | Truth is recalculated from surviving evidence set (signals that have not decayed + crystallized priors) |
| 7 | Epistemic separation | Atoms != Clouds != Facts | Observations != Hypotheses != Knowledge |

*Note on the analogy's limits: the alibi architecture is structural, not literal. Financial atoms (VENDOR, AMOUNT, DATETIME) are discrete, structured, and objectively verifiable. Brand signals are interpretive, continuous, and overlapping. The epistemic architecture — observations → hypotheses → knowledge — transfers across domains; the data precision does not. Brand 'atoms' are more accurately described as typed signal contributions than as discrete measurable units.*

---

## Part 2: The Stellar Object Mapping

A brand is a stellar object. The same constellation of stars appears different from every point in the universe, and to every creature with a different range of spectral sensitivity.

```mermaid
graph LR
    subgraph "The Brand<br/>(stellar object)"
        S1((Semiotic))
        S2((Narrative))
        S3((Ideological))
        S4((Experiential))
        S5((Social))
        S6((Economic))
        S7((Cultural))
        S8((Temporal))
    end

    subgraph "Observer A<br/>Gen-Z Consumer"
        direction TB
        OA[Spectrum: Social + Cultural<br/>Weight: Social 0.40, Cultural 0.30]
        FA[Brand Fact A:<br/>'Trendy tribe marker']
    end

    subgraph "Observer B<br/>B2B Buyer"
        direction TB
        OB[Spectrum: Economic + Experiential<br/>Weight: Economic 0.45, Exp 0.35]
        FB[Brand Fact B:<br/>'Reliable cost-efficient supplier']
    end

    subgraph "Observer C<br/>Cultural Critic"
        direction TB
        OC[Spectrum: Semiotic + Cultural<br/>Weight: Cultural 0.40, Semiotic 0.35]
        FC[Brand Fact C:<br/>'Derivative aesthetics, <br/>appropriative messaging']
    end

    S5 & S7 -.->|perceived| OA --> FA
    S6 & S4 -.->|perceived| OB --> FB
    S1 & S7 -.->|perceived| OC --> FC

    style S1 fill:#fce4ec,stroke:#333
    style S2 fill:#e8eaf6,stroke:#333
    style S3 fill:#e0f2f1,stroke:#333
    style S4 fill:#fff8e1,stroke:#333
    style S5 fill:#f3e5f5,stroke:#333
    style S6 fill:#e8f5e9,stroke:#333
    style S7 fill:#fbe9e7,stroke:#333
    style S8 fill:#e3f2fd,stroke:#333
```

| Stellar Concept | Brand Equivalent |
|----------------|-----------------|
| Stars (atoms) composing the object | Brand signals emitted across dimensions |
| Observer's position in the universe | Social/professional/cultural cohort |
| Observer's spectral sensitivity | Values, beliefs, cultural codes, literacy |
| Visible constellation from Earth | Brand-as-perceived by one cohort |
| Same stars seen from Andromeda | Same brand perceived by a different cohort |
| Infrared vs visible vs X-ray | Emotional vs rational vs social perception channels |
| The stellar object itself (all stars, all radiation) | The brand's signal architecture — objectively characterizable across all eight dimensions |

The critical insight: **there is no universal brand perception.** The brand's signal architecture — its eight-dimensional emission pattern — is objectively real and characterizable. What cannot exist in a single universal form is brand *meaning*: each observer cohort assembles structurally different brand meaning from the same signal environment, collapsing whichever atoms they can perceive through their particular spectrum into distinct brand facts.

*A note on the spectral metaphor's limits: in optics, a stellar object's spectrum is observer-independent — the star emits what it emits regardless of who measures it. Brand perception inverts this: the 'spectrum' is observer-specific. The metaphor is useful for visualizing multi-dimensionality and observer sensitivity differences, but breaks down precisely where it matters most — in SBT, the observer's spectral profile creates the perceived brand, not merely filters a fixed emission.*

---

## Part 3: Spectral Branding Architecture

### 3.1 Brand Atom Types (8 Dimensions)

```mermaid
graph TD
    subgraph "Brand Atom Dimensions"
        SEM[Semiotic<br/>logo, name, colors,<br/>sounds, typography]
        NAR[Narrative<br/>origin story, founder myth,<br/>key events, legends]
        IDE[Ideological<br/>values, ethics, purpose,<br/>promises, positions]
        EXP[Experiential<br/>touchpoints, service,<br/>product use, UX]
        SOC[Social<br/>community markers,<br/>tribal signals, status]
        ECO[Economic<br/>price positioning,<br/>premium/discount signals]
        CUL[Cultural<br/>aesthetic codes, references,<br/>zeitgeist, humor, taste]
        TMP[Temporal<br/>heritage, evolution,<br/>era associations]
    end

    SEM --- NAR --- IDE --- EXP
    SOC --- ECO --- CUL --- TMP

    style SEM fill:#fce4ec,stroke:#c62828
    style NAR fill:#e8eaf6,stroke:#283593
    style IDE fill:#e0f2f1,stroke:#004d40
    style EXP fill:#fff8e1,stroke:#f57f17
    style SOC fill:#f3e5f5,stroke:#6a1b9a
    style ECO fill:#e8f5e9,stroke:#2e7d32
    style CUL fill:#fbe9e7,stroke:#bf360c
    style TMP fill:#e3f2fd,stroke:#0d47a1
```

| Dimension | Examples | Alibi Analog |
|-----------|----------|-------------|
| **Semiotic** | Logo, name, colors, sounds, typography, packaging | VENDOR (identification signals) |
| **Narrative** | Origin story, founder myth, key events, brand legends | DATETIME (temporal anchors) |
| **Ideological** | Stated values, ethical positions, purpose, promises | -- (new dimension) |
| **Experiential** | Touchpoints, service moments, product use, UX | ITEM (the actual "stuff") |
| **Social** | Community markers, tribal signals, status codes | PAYMENT (social exchange currency) |
| **Economic** | Price positioning, value signals, premium/discount | AMOUNT (monetary meaning) |
| **Cultural** | Aesthetic codes, references, zeitgeist, humor | TAX (cultural overhead) |
| **Temporal** | Heritage, evolution moments, era associations | DATETIME (when things happened) |

*Ordering note: dimensions in this document follow the conceptual order used throughout the articles and analytical content (semiotic → narrative → ideological → experiential → social → economic → cultural → temporal). This order groups dimensions by their epistemological role in the perception pipeline. The website and visual identity system uses a different ordering based on physical wavelength sequence of the visible spectrum (semiotic/violet → narrative/indigo → temporal/blue → ideological/teal → economic/green → experiential/amber → cultural/orange → social/red). Both orderings are valid; the conceptual order is canonical for analytical and theoretical purposes.*

### 3.2 Brand Bundles (Encounter Types)

Each brand encounter produces a typed bundle, analogous to how each document type produces a different bundle in alibi.

| Bundle Type | Channel | Typical Atoms |
|-------------|---------|---------------|
| **CAMPAIGN** | Advertising | semiotic + narrative + cultural + economic |
| **ENCOUNTER** | Store/service visit | experiential + semiotic + social + economic |
| **USAGE** | Product consumption | experiential + economic + temporal |
| **TESTIMONY** | Word-of-mouth / review | narrative + social + ideological |
| **EMPLOYMENT** | Working at the brand | cultural + ideological + social + economic |
| **INVESTMENT** | Financial relationship | economic + narrative + temporal |
| **NEWS** | Media coverage | narrative + cultural + social + ideological |

### 3.3 Observer Model

This is the missing piece in classical branding. In alibi, the system is the sole observer with fixed weights. In branding, **observers are heterogeneous** -- each assembles a different brand from the same atoms.

```mermaid
graph TD
    subgraph "Observer Profile"
        SP[Spectrum<br/>which dimensions<br/>they CAN perceive]
        WE[Weights<br/>which dimensions<br/>MATTER to them]
        TH[Tolerances<br/>how much variance<br/>they accept]
        PR[Priors<br/>existing brand<br/>facts in memory]
        IG[Identity Gate<br/>can they recognize<br/>the brand at all?]
    end

    SP --> WE --> TH --> PR --> IG

    IG -->|pass| CF[Cloud Formation]
    IG -->|fail| NO[No Perception<br/>atoms are noise]

    CF -->|threshold met| COL[Collapse to Fact]
    CF -->|below threshold| FORM[Forming<br/>awareness without opinion]

    COL --> PART[Partial Fact<br/>'I think they are X']
    COL --> CONF[Confirmed Fact<br/>'They ARE X']

    style SP fill:#e8eaf6,stroke:#333
    style WE fill:#e8eaf6,stroke:#333
    style TH fill:#e8eaf6,stroke:#333
    style PR fill:#e8eaf6,stroke:#333
    style IG fill:#fff3cd,stroke:#333
    style FORM fill:#fff3cd,stroke:#333
    style PART fill:#ffe0b2,stroke:#333
    style CONF fill:#d4edda,stroke:#333
    style NO fill:#ffcdd2,stroke:#333
```

Example observer profiles:

| Cohort | High-Sensitivity Dims | Primary Weights | Tolerance |
|--------|----------------------|----------------|-----------|
| Gen-Z consumer | social, cultural, semiotic | social: 0.40, cultural: 0.30 | Low for ideological inconsistency |
| B2B buyer | economic, experiential, temporal | economic: 0.40, experiential: 0.35 | High for cultural (irrelevant to them) |
| Brand employee | ideological, cultural, social | ideological: 0.35, cultural: 0.30 | Zero for ideological contradiction |
| Investor | economic, narrative, temporal | economic: 0.45, narrative: 0.30 | High for experiential (not their concern) |
| Cultural critic | semiotic, cultural, narrative | cultural: 0.40, semiotic: 0.35 | Zero for cultural inauthenticity |

**Estimating dimensional weights**: In current practice, weights are estimated through structured expert judgment informed by available behavioral data: stated purchase drivers, revealed preferences, complaint/praise patterns, and cohort characteristics. These estimates should be treated as hypotheses requiring validation rather than measurements. A validated approach would use conjoint analysis (presenting trade-offs between dimensional attributes to reveal implicit weighting) or MaxDiff scaling (identifying which dimensions are most/least important). All weight assignments in SBT case studies are expert estimates with ±0.10-0.15 uncertainty range.

**Identifying observer cohorts**: Cohorts are clusters in spectral-profile space — groups of observers whose dimensional weight profiles are similar enough to produce structurally similar perception clouds. Discovery process: (1) Start with existing segmentation — map known demographic/psychographic segments to likely spectral profiles; (2) Identify signal-responsive groups — which audiences react distinctly to the same brand signal? Distinct reactions imply distinct weight profiles; (3) Use behavioral evidence — purchase patterns, advocacy behavior, complaint types, and content consumption patterns reveal dimensional priorities; (4) Validate with LLM analysis — run the framework's observer mapping module to generate candidate cohort profiles for expert review. The resulting cohorts are hypotheses to be validated against consumer research.

### 3.4 Cloud Formation and Fact Collapse

Brand perception follows the same epistemic pipeline as financial facts:

*A note on terminology: 'cloud' and 'collapse' invoke quantum mechanics to suggest indeterminacy before crystallization, not as a mathematical claim. Brand perception does not obey quantum mechanics. The terms are used for their intuitive resonance: an uncertain impression (cloud) that resolves into a definite belief (collapse).*

```mermaid
stateDiagram-v2
    [*] --> Unaware: No atoms received

    Unaware --> Noise: Atoms arrive,<br/>identity gate FAILS
    Unaware --> Forming: Atoms arrive,<br/>identity gate PASSES

    Noise --> [*]: Atoms discarded

    Forming --> Forming: More atoms cluster
    Forming --> Partial: Threshold met,<br/>weak corroboration
    Forming --> Confirmed: Threshold met,<br/>strong corroboration

    Partial --> Confirmed: More evidence accumulates
    Partial --> ReCollapse: Contradicting atoms arrive
    Confirmed --> ReCollapse: Scandal / rebrand / new evidence

    ReCollapse --> Forming: Insufficient evidence after rebuild
    ReCollapse --> Partial: Moderate evidence after rebuild
    ReCollapse --> Confirmed: Strong evidence after rebuild
    ReCollapse --> Unaware: All evidence contradicted

    note right of Forming
        "I've heard of them."
        No opinion formed yet.
    end note

    note right of Partial
        "I think they're X."
        Subject to re-collapse.
    end note

    note right of Confirmed
        "They ARE X."
        Resistant to contradicting atoms.
    end note

    note right of ReCollapse
        Conviction recalculated from
        surviving evidence + crystallized priors.
        Triggered by threshold contradiction.
    end note
```

**The Brand Identity Gate** functions like alibi's vendor gate: the observer must first *recognize* these atoms as belonging to the same entity. Logo, name, visual identity serve this function. Without passing the gate, atoms don't cluster -- they are noise.

**Scoring is observer-specific**: unlike alibi's fixed weights, brand cloud formation uses the observer's own weight profile. A Gen-Z consumer clusters by social + cultural. A B2B buyer clusters by economic + experiential. *The same atoms produce different clouds.*

**Re-collapse**: a brand scandal, product failure, or brilliant campaign introduces atoms that contradict existing evidence past a threshold, triggering re-collapse. Re-collapse recalculates conviction from the surviving evidence set plus any crystallized priors. Priors act as weighted anchors — they persist through re-collapse but can be overridden by sufficiently strong contradicting evidence. This is recalculation from the current evidence base, not recalculation from a blank slate. The distinction from incremental updating is that re-collapse is triggered by a threshold event (sufficient contradicting evidence) rather than happening continuously. This explains why some brands recover from scandals (new positive atoms outweigh negative in re-collapse) and some don't (negative atoms dominate, priors reversed).

**Single-bundle collapse**: one devastating news article collapses directly into a fact with no corroboration needed -- same as a standalone receipt in alibi.

**Collapse threshold specification**: Collapse for observer k occurs when accumulated cloud confidence reaches that observer's threshold:

```
Collapse(k) occurs when:
  cloud_confidence(k) ≥ threshold(k)

  where:
  - cloud_confidence = Σ(perceived_signal_weights × dimensional_weights)
    normalized by maximum possible score
  - threshold(k) is observer-specific, inversely related to tolerance
    (low-tolerance observers require higher confidence before collapse)
  - priors from previous collapses lower the threshold for consistent evidence
    and raise it for contradicting evidence
```

The threshold parameters remain illustrative — exact calibration requires empirical measurement of real observer responses. What the specification establishes is the form: collapse is a function of accumulated weighted evidence relative to an observer-specific threshold shaped by tolerance and priors.

### 3.5 Signal Dissemination: Pre-Encounter Mechanics

The perception pipeline (§3.4) begins when atoms reach an observer. But atoms must first travel from emission to the observer's environment. The **Signal Dissemination Layer** models this pre-encounter phase.

```mermaid
graph TB
    subgraph "Emission"
        E[Brand emits atoms]
        A[Ambient atoms generated]
        S[Synthetic atoms generated]
    end

    subgraph "Dissemination"
        CH[Channels<br/>bandwidth, reach, fidelity]
        SF[Signal Fields<br/>spatiotemporal atom sets]
        EE[Encounter Events<br/>attention ∩ atoms]
    end

    subgraph "Perception (existing)"
        IG[Identity Gate]
        SP[Spectrum Filter]
        WA[Weight Assignment]
        CF[Cloud Formation]
        CO[Collapse]
    end

    E --> CH
    A --> CH
    S --> CH
    CH --> SF
    SF --> EE
    EE --> IG
    IG --> SP --> WA --> CF --> CO

    CO -->|Signal Amplification| CH
```

**Key concepts**:

- **Signal field**: the set of brand atoms present in a given spatiotemporal environment. A brand's signal field in Berlin differs from its field in Tokyo. Not all emitted atoms populate all fields.
- **Channel**: the medium through which atoms travel from emission to signal field. Properties: bandwidth (capacity), reach (how many fields), fidelity (dimensional preservation), selectivity (cohort targeting). Channels are distinct from encounter modes (direct/mediated) -- a channel delivers atoms to the environment; encounter mode describes how the observer processes them.
- **Encounter event**: the moment atoms intersect an observer's attention. Governed by field density, observer receptivity (need-state activation + curiosity threshold), and algorithmic mediation.
- **Observer receptivity**: a pre-perception property combining need-state activation (Rossiter & Percy's "Category Need") and curiosity threshold. Low receptivity means atoms exist in the field but are never processed.
- **Gate friction**: the number of encounter events required to transition an observer's identity gate from Closed to Open. Reduced by distinctive brand assets (Romaniuk & Sharp), signal salience, and repeated mere exposure (Zajonc 1968).
- **Signal amplification**: Confirmed observers become secondary emitters, creating new ambient atoms in new signal fields -- a feedback loop from perception back to dissemination.
- **First-atom effect**: the first brand atom encountered creates the initial prior schema, disproportionately shaping all subsequent perception (anchoring, primacy effect).

**Dissemination states** (per observer × brand, preceding the perception state machine):

| State | Description | Transition trigger |
|---|---|---|
| Absent | No brand atoms in observer's signal field | Channel delivers atoms → Present |
| Present | Atoms in field, no encounter event | Attention intersects atoms → Encountered |
| Encountered | At least one encounter event has occurred | Enters perception pipeline (identity gate) |

This resolves the relationship between SBT and acquisition-focused frameworks: Sharp's "mental availability" = field density × gate friction⁻¹ × spectral profile accessibility. Sharp's "physical availability" = channel coverage across observer environments. Schwartz's "Unaware" = SBT's Absent state. Customer acquisition = the product of transition rates across dissemination and perception states.

New hypotheses H6-H10 address gate friction variance, first-atom primacy, amplification asymmetry, channel-dimension coupling, and field density thresholds.

### 3.6 Geometric Structure of the Perception Space

The constructs in §3.1-3.5 describe the architecture of brand perception qualitatively. This section formalizes the mathematical spaces in which those constructs live, providing the rigorous metric foundation that makes SBT's claims about brand distance, observer similarity, cohort boundaries, and perception dynamics formally precise rather than metaphorical.

**Why geometry matters for brand theory**: Brand perception involves comparison (which brand is "closer" to my ideal?), classification (which observer cohort do I belong to?), and dynamics (how does my perception change over time?). Each of these operations requires a notion of distance. Without a formal metric, "brand distance" is a metaphor. With one, it becomes a computable quantity with provable properties.

#### 3.6.1 The Brand Signal Space

Brand emission profiles (§3.1) are vectors in $\mathbb{R}^8_+$: eight non-negative signal strengths, one per dimension (semiotic, narrative, ideological, experiential, social, economic, cultural, temporal).

Raw Euclidean distance is inappropriate for brand comparison because perception is proportional, not additive (per the Weber-Fechner law: a change from 0.1 to 0.2 is perceptually equivalent to a change from 0.5 to 1.0). The appropriate metric is the **Aitchison distance**, which operates on log-ratios of signal components:

$$d_B(S_A, S_B) = \sqrt{\sum_{i=1}^{8} \left( \log \frac{S_{A,i}}{g(S_A)} - \log \frac{S_{B,i}}{g(S_B)} \right)^2}$$

where $g(S) = (\prod_i S_i)^{1/8}$ is the geometric mean. This metric is scale-invariant (doubling all signals does not change distances) and subcompositionally coherent (comparing brands on a subset of dimensions is consistent with the full comparison). Geodesics in this space are straight lines in log-ratio coordinates, meaning that brand evolution (rebranding trajectories) follows paths that preserve signal ratios rather than absolute values.

For normalized brand profiles (signal strengths scaled to unit norm), the natural space is $S^7_+$: the positive octant of the 7-sphere. This octant comprises only $1/2^8 = 1/256$ of the full sphere surface, reflecting the constraint that brand signals are non-negative. The compression of available brand space has a direct strategic implication: differentiation is harder than naive 8-dimensional counting suggests.

#### 3.6.2 The Observer Weight Space

Observer weight profiles (§3.3) are probability vectors on the 7-simplex $\Delta^7$: eight non-negative weights summing to 1.0, representing the relative importance each observer assigns to the eight dimensions.

The appropriate metric for $\Delta^7$ is the **Fisher-Rao distance**:

$$d_O(w^{(1)}, w^{(2)}) = 2 \arccos \left( \sum_{i=1}^{8} \sqrt{w_i^{(1)} w_i^{(2)}} \right)$$

This metric is uniquely invariant under sufficient-statistic transformations (Cencov's theorem, 1972), making it the canonical distance measure on probability spaces. A key perceptual property: the Fisher-Rao metric is highly sensitive to changes in small weights. An observer who shifts from 0.01 to 0.02 on the ideological dimension (barely noticing it vs. beginning to notice) traverses a larger geometric distance than an observer shifting from 0.25 to 0.26 on the same dimension. This matches the psychological reality that awakening to a previously ignored dimension is a larger perceptual shift than a marginal adjustment to an already-salient one.

Geodesics on $\Delta^7$ under Fisher-Rao "bulge" toward the simplex center (maximum entropy). Interpolating between two polarized observers yields a middle profile with higher entropy than a linear average would predict -- the geometric "compromise" between specialists is a generalist.

#### 3.6.3 The Combined Perception Space

Brand perception in SBT is observer-dependent: two observers may perceive the same brand pair as close or far apart, depending on their weight profiles. This is formalized as a **warped product manifold** $\Delta^7 \times_w \mathbb{R}^8$, where the observer weights "warp" the brand space metric:

$$D^2\big((w^{(1)}, S^{(1)}),\; (w^{(2)}, S^{(2)})\big) = d_O^2(w^{(1)}, w^{(2)}) + \sum_{k=1}^{8} \bar{w}_k \left( \text{clr}_k(S^{(1)}) - \text{clr}_k(S^{(2)}) \right)^2$$

where $\bar{w}_k = (w_k^{(1)} + w_k^{(2)})/2$ and $\text{clr}$ is the centered log-ratio transform.

This structure generalizes the INDSCAL model (Carroll & Chang 1970), which has been empirically validated in psychometric scaling studies: observers share a common brand space but apply individual dimension weights. The warped product formalization gives INDSCAL a rigorous differential-geometric foundation and extends it with a proper metric on the observer space itself.

The **observer-dependent pseudo-metric** on brand space alone:

$$d_w(S_A, S_B) = \left\| \sqrt{w} \circ (S_A - S_B) \right\|_2$$

may degenerate (equal zero for distinct brands) when the observer assigns zero weight to all dimensions where the brands differ. The kernel of this metric -- the set of brand pairs indistinguishable to observer $w$ -- formalizes "blind spots" in brand perception.

#### 3.6.4 Concentration of Measure and Cohort Geometry

At $n = 8$ dimensions, the observer simplex $\Delta^7$ already exhibits significant concentration of measure: the expected squared Euclidean distance between two uniformly random observer profiles is $E[\|X - Y\|^2] = 2n/((n+1)(n+2)) = 16/90 \approx 0.178$, and pairwise distances concentrate tightly around $\sqrt{0.178} \approx 0.42$.

This concentration has three consequences for SBT:

1. **Null model baseline**: Brand differentiation is "meaningful" only when observer-weighted distance exceeds the concentration radius. Many perceived brand differences may be noise rather than structural.

2. **Cohort boundary fuzziness**: For any partition of $\Delta^7$ into $k$ cohort regions, the fraction of observer profiles near a boundary grows with dimensionality. At $n = 8$, boundaries are already substantially fuzzy -- which is why Claude's 5-6 cohorts and Gemini's 3 cohorts (§5.11) represent valid clusterings at different granularity thresholds rather than contradictory results.

3. **Specialization advantage**: Most random observer profiles are "unbalanced" (concentrating weight on a few dimensions). A brand that tries to satisfy all 8 dimensions equally is geometrically further from the typical observer than a brand that specializes -- formalizing the D/A Goldilocks zone (§5.4) as a geometric rather than merely empirical pattern.

**Companion paper**: Zharnikov (2026d), "Brand Space Geometry: A Formal Metric for Multi-Dimensional Brand Perception."

**Computational enforcement**: The mathematical constraints defined in §3.6 and the companion papers (R1-R6) are computationally enforced by the validation module (`src/spectral_branding/validators/`). Every LLM-generated spectral profile is checked against metric constraints (positivity, triangle inequality), metamerism bounds (R2), cohort boundary fuzziness (R3), positioning capacity (R4), and trajectory absorption risk (R6). This ensures that the framework's mathematical foundations are active runtime constraints, not just theoretical properties.

---

## Part 4: AI-Era Spectral Branding

### 4.1 What AI Changes at Each Pipeline Stage

```mermaid
graph TB
    subgraph "Pre-AI Pipeline"
        E1[Brand emits atoms<br/>campaigns, products] --> O1[Human observers<br/>perceive directly]
        O1 --> C1[Organic cloud formation<br/>years to stabilize]
        C1 --> F1[Stable brand facts<br/>change slowly]
    end

    subgraph "AI-Era Pipeline"
        E2[Brand emits atoms<br/>at infinite scale,<br/>personalized per observer] --> AI[AI Mediation Layer<br/>algorithms filter,<br/>re-rank, re-context]
        AMB2[Synthetic atoms<br/>AI-generated reviews,<br/>deepfakes, LLM summaries] --> AI
        AI --> O2[Human observers<br/>see AI-curated atoms]
        AI --> SO[Synthetic observers<br/>procurement AI,<br/>recommendation engines]
        O2 --> C2[Platform-shaped clouds<br/>filter bubbles]
        SO --> C3[Algorithmic evaluation<br/>no gestalt needed]
        C2 --> F2[Volatile brand facts<br/>re-collapse in hours]
        C3 --> F3[Raw atom scoring<br/>no 'brand image'<br/>brands unnecessary]
    end

    style AI fill:#fff3cd,stroke:#333
    style AMB2 fill:#ffcdd2,stroke:#333
    style SO fill:#e1bee7,stroke:#333
    style F3 fill:#ffcdd2,stroke:#333
```

**Atom generation**: AI enables infinite atom generation at near-zero marginal cost. Personalized semiotic, narrative, experiential atoms for every individual observer. This breaks the "one campaign, many observers" model. Danger: atom inflation devalues each individual atom. More atoms does not mean stronger collapse -- it can mean more noise, weaker clustering.

**Observation**: AI observers (recommendation algorithms, search engines, social feeds) mediate between brand atoms and humans. They pre-filter, re-rank, and re-contextualize atoms before human perception. The brand emits atom X, but the algorithm presents atom X' to the human. The brand increasingly does not control what observers actually perceive.

**Cloud formation**: AI-mediated environments create filter bubbles -- artificial constraints on which atoms reach which observers. Brand clouds form differently on TikTok vs LinkedIn vs Amazon not because the brand emits different atoms, but because the platform's AI selects different atom subsets for presentation.

**Fact collapse**: AI accelerates re-collapse cycles. Pre-AI brand facts were stable for years. Now a single viral moment can force re-collapse for millions simultaneously. AI also enables **synthetic facts** -- AI-generated brand perceptions assembled from synthetic atoms (deepfakes, AI reviews). The forgery problem: if brand facts can be assembled from synthetic atoms, what does "brand truth" mean?

### 4.2 Spectral Brand Management System

An AI-era brand management system mirrors alibi's architecture directly:

```mermaid
graph TD
    subgraph "1. Brand Atom Registry"
        DA[Designed Atoms<br/>campaigns, products,<br/>communications]
        AA[Ambient Atoms<br/>reviews, mentions,<br/>competitor framing]
        DA & AA --> REG[(Atom Registry<br/>typed, timestamped,<br/>tagged by dimension)]
    end

    subgraph "2. Observer Cohort Models"
        REG --> OCM[Observer Profiles<br/>spectrum, weights,<br/>tolerances, priors]
    end

    subgraph "3. Cloud Monitor"
        OCM --> CM[Real-time tracking:<br/>which atoms clustering<br/>in which cohorts?]
        CM --> DIV{Cloud<br/>Divergence?}
        DIV -->|yes| ALERT[Coherence Alert:<br/>cohorts see<br/>different brands]
        DIV -->|no| OK[Healthy:<br/>controlled variance]
    end

    subgraph "4. Collapse Predictor"
        CM --> CP[AI Model:<br/>'If we emit atom set Y,<br/>cohort X will collapse<br/>into fact Z with prob P']
    end

    subgraph "5. Re-collapse Defense"
        CM --> RD[Monitor incoming atoms<br/>that could force<br/>unwanted re-collapse]
        RD --> PRE[Pre-position<br/>counter-atoms]
    end

    style REG fill:#e3f2fd,stroke:#333
    style OCM fill:#e8eaf6,stroke:#333
    style CM fill:#fff8e1,stroke:#333
    style CP fill:#e8f5e9,stroke:#333
    style RD fill:#fce4ec,stroke:#333
    style ALERT fill:#ffcdd2,stroke:#333
```

| System Component | Function | Alibi Analog |
|-----------------|----------|-------------|
| Brand Atom Registry | Track every emission + ambient signal, typed by dimension | Atom storage (documents -> atoms) |
| Observer Cohort Models | Define spectrum, weights, tolerances per cohort | Identity system (canonical entity registry) |
| Cloud Monitor | Track which atoms are clustering in which cohorts | Cloud formation (probabilistic clustering) |
| Collapse Predictor | Predict how new atoms will change facts per cohort | -- (new, AI-native capability) |
| Re-collapse Defense | Detect and buffer against unwanted re-collapse | Re-collapse on new evidence |

### 4.3 Brand as Executable Model

In the AI era, a brand is no longer a "platform document" or "brand book." It is an executable model:

- **Input**: observer profile + context
- **Processing**: atom selection + scoring + clustering
- **Output**: predicted brand fact (what this observer will believe)

Brand management becomes model management:

- **Training data**: all historical atoms + observer responses
- **Loss function**: divergence between intended collapse and actual collapse
- **Optimization**: adjusting atom emission policy to minimize loss

This is not speculative. Personalization engines, dynamic creative optimization, and AI-driven brand tracking are already converging toward this architecture. The spectral model provides the theoretical framework that unifies these operational tools.

### 4.4 When Do Brands Become Unnecessary?

**When will the atom-to-fact pipeline become unnecessary?**

Answer: when AI observers make all decisions without collapsing atoms into facts. If an AI procurement system evaluates a product on raw atoms (price, specs, reviews) without forming a "brand image," then branding is dead *for that observer*. But as long as human observers need cognitive shortcuts (gestalts, attractors) to navigate choice complexity, the collapse mechanism persists -- and therefore brands persist.

The real threat is not AI replacing brands, but **AI making observers so granular that no two observers collapse the same fact.** When every person has a unique brand fact, the concept of "a brand" (singular, shared) dissolves into N individual brand relationships. The brand as a collective phenomenon dies; the brand as a personal relationship lives.

---

### 4.5 Competitive Context Limitation and Extension

**Current scope**: the framework analyzes brands in isolation. Each SBT analysis models one brand's signal architecture and the observer cohorts that perceive it.

**The gap**: real brand health is co-determined by competitors. A brand's signal architecture produces different observer responses depending on what competitors are signaling simultaneously. Tesla's ambient signal contamination operates differently in a market with no direct EV competitor than in a market where multiple credible alternatives exist. The designed/ambient ratio has different strategic implications depending on whether competitors are high-D/A (controlled) or low-D/A (chaotic).

**The extension**: modeling competitive contexts in SBT would require adding a second signal environment to the observer model — the competitor's emission map — and analyzing how the two environments interact within the same observer's perceptual field. A dimension where Brand A dominates and Brand B is absent produces different conviction dynamics than a dimension where both brands are competing.

**Status**: competitive context modeling is a priority structural extension, not yet validated. The five-brand case studies were conducted in isolation. This is a named limitation of the current framework version.

---

## Part 5: Track 0 Exploratory Analysis — Nine Candidate Mechanisms (v2.0)

Track 0 applied the spectral framework to 5 brands (Hermès, IKEA, Patagonia, Tesla, Erewhon) across all 6 modules. The exploratory analysis identified 9 candidate mechanisms that extend the framework beyond its v1.0 specification. These represent analytical observations from five illustrative cases, not empirically validated findings.

### 5.1 Dark Signals: Structural Absence as Brand Dimension Modifier

**Discovery**: Hermès creates value through designed signal RESTRICTION, not amplification. The empty shelf, the wait list, the inability to buy — these are not failures of distribution but strategic acts of structural absence.

**Physics analog**: dark matter — invisible but gravitationally active. Cannot be observed directly but detected through effects on visible signals. Comprises the majority of brand power in scarcity brands.

**Three emission types** (replaces the binary designed/ambient model):

| Type | Mechanism | Signal Present? | Example |
|------|-----------|----------------|---------|
| **Positive** | Brand emits signal, atoms accumulate | Yes | Campaign, product launch |
| **Null** | Signal absent, unintentional | No (neglect) | Dormant dimension, forgotten brand |
| **Structural Absence** | Designed scarcity functions as signal | No (strategy) | Wait list, no discounts, geographic restriction |

**Formal specification**:

Standard cloud formation:
```
  Cloud = Σ(emitted_atoms × weights)
```

Cloud formation with structural absence — qualitative mechanism: Structural absence amplifies the perceived weight of present signals through contrast. The mechanism is not additive (absent signals do not contribute quantitative values to cloud formation) but multiplicative in perception: when some signals are withheld, the present signals carry more interpretive weight per unit of evidence. Concretely, an invitation to an exclusive event becomes more significant when 99% of requests are declined. The restriction creates the contrast that amplifies the signal. The scarcity multiplier is a conceptual amplification parameter — its formal quantification is on the research agenda.

**Dimensional constraints**: structural absence operates primarily on social (exclusivity), economic (no discounts), and experiential (geographic scarcity). It cannot operate on semiotic (no "absent logo") or narrative (absence of story is just absence).

**Scale-independent**: the mechanism works identically at $20 (Erewhon smoothie) and $15,000 (Hermès handbag).

**Prerequisites for structural absence**: the mechanism requires two conditions: (1) existing demand to restrict — the brand must have created desire before restricting access; (2) cultural context that makes restriction legible as intention rather than failure. Heritage is the most reliable source of this legitimizing context. However, equivalent context can be created by: cult community status (Erewhon, ~10 years), founder mythology, category-defining position, or strong ideological identity. The prerequisite is legitimizing context, of which heritage is one — but not the only — source.

### 5.2 Coherence Taxonomy: Five Types of Brand Architecture

**Dual-layer architecture note**: Humans perceive dots of different colour tones; AI reads the exact spectrum of light waves that compose each dot's lighting. SBT is built for both. The coherence type (ecosystem, signal, identity, experiential asymmetry, incoherent) is a structural classification in the L1 spectral profile — nominal, no ordering implied. The letter grade (A+ to C-) is an L2 rendered output: a projection of each type's typical disruption resilience mechanism onto a human-readable scale. Two brands with structurally different spectral profiles can project to the same grade — spectral metamerism. The grade tells you the resilience colour. For the full spectrum, consult the L1 spectral profile.

#### Worked Example — Tesla, Progressive Boycotter Cohort

**L1 Spectral Profile** (ground truth, machine-readable):

```
cohort: progressive_boycotter
dimensional_perception:
  ideological: {intensity: 4.5, weight: 0.55, valence: negative}
  social: {intensity: 3.8, weight: 0.25, valence: negative}
  cultural: {intensity: 3.2, weight: 0.17, valence: negative}
  experiential: {intensity: 4.2, weight: 0.03, valence: positive}
conviction: {direction: negative, confidence: 0.82, stability: absorbing}
gate_status: open (brand recognized, experiential gate closed)
```

**L2 Rendered Summary** (human-readable projection):

```
Brand: Tesla
Coherence type: Incoherent
Resilience grade: C-
Key risk: Amplifying — disruption widens existing divisions
Strategic note: Cannot communicate out of incoherence; structural fix required
```

The L2 tells you the colour (C-, amplifying fragility). The L1 tells you the spectrum (WHY it is C- for THIS cohort: ideological conviction at 0.55 weight with no experiential counter-evidence because the experiential gate is at 0.03).

**Theoretical derivation**: the five coherence types follow from the intersection of three structural properties that can be assessed independently of any specific brand:

| Cohort Interdependence | Ideological Centrality | Encounter Mode Variance | Coherence Type |
|---|---|---|---|
| High | Any | Low | Ecosystem |
| Low | Low | Low | Signal |
| Low | High | Low | Identity |
| Low | Low | High | Experiential Asymmetry |
| Low | Low | Low (contradictory signals) | Incoherent |

These five types represent the structurally distinct configurations of a multi-cohort brand within this three-property space. Additional types would require a fourth structural property not captured here.

**Discovery**: coherence is not a single variable from low to high. It has qualitative TYPES with structurally different resilience properties. A 7/10 Signal Coherence and a 7/10 Ecosystem Coherence would look identical on a traditional scorecard but have fundamentally different properties.

```mermaid
graph LR
    subgraph "Coherence Type Spectrum"
        EC[Ecosystem<br/>Hermès A+]
        SC[Signal<br/>IKEA A-]
        IC[Identity<br/>Patagonia B+]
        EA[Exp. Asymmetry<br/>Erewhon B-]
        IN[Incoherent<br/>Tesla C-]
    end

    EC --- SC --- IC --- EA --- IN

    style EC fill:#c8e6c9
    style SC fill:#e8f5e9
    style IC fill:#fff8e1
    style EA fill:#ffe0b2
    style IN fill:#ffcdd2
```

| Type | How Clouds Relate | Resilience Under Disruption | Brand Example |
|------|-------------------|---------------------------|---------------|
| **Ecosystem** | Different clouds reinforce through functional interdependence | Selective — absorbs by purification | Hermès |
| **Signal** | Consistent designed signals → consistent clouds | Uniform — transmits disruption evenly | IKEA |
| **Identity** | Ideological core filters cohort compatibility | Binary — divides along ideology | Patagonia |
| **Experiential Asymmetry** | Evidence gap between local and remote observers | Geographic — different impact by location | Erewhon |
| **Incoherent** | Contradictory signals → irreconcilable clouds | Amplifying — widens existing cracks | Tesla |

**Grade mapping function**: Each type maps to its grade via its disruption resilience mechanism. The function is `grade = f(resilience_mechanism, absorption_capacity)` — NOT `grade = f(coherence_quality)`. The taxonomy is nominal (five structural types, no inherent ordering). The grades are ordinal on a single variable: disruption resilience.

| Coherence Type | Resilience Mechanism | Grade | Rationale |
|---|---|---|---|
| Ecosystem | Selective absorption — unaffected cohorts stabilize the system | A+ | Disruption is metabolized selectively |
| Signal | Uniform transmission — disruption reaches all cohorts equally | A- | Strong but no selective defense |
| Identity | Binary rally/oppose — aligned cohorts strengthen under stress | B+ | Resilient within aligned cohort |
| Experiential Asymmetry | Geographic isolation — local and mediated cohorts disrupted independently | B- | Partial resilience only |
| Incoherent | Amplifying — disruptions widen existing cohort divisions | C- | Brand converts disruption into deeper fragmentation |

**Brand profile cards (L1 spectral / L2 rendered)**:

---
**HERMÈS — SPECTRAL PROFILE (L1)**
Coherence type:    Ecosystem
Signal arch:       Balanced, designed-dominant (D/A/S ~60/35/5)
Resilience mech:   Selective absorption — ecosystem metabolizes disruption
Dimensional peaks: Social (0.90), Economic (0.85), Experiential (0.80)
Structural asset:  Cohort interdependence — each cohort validates the others

**RENDERED SUMMARY (L2)**
Resilience grade:  A+
Key implication:   Ecosystem can sacrifice peripheral cohorts to purify the core

---
**IKEA — SPECTRAL PROFILE (L1)**
Coherence type:    Signal
Signal arch:       Designed-dominant (D/A/S ~70/25/5)
Resilience mech:   Uniform transmission — consistent signals, consistent response
Dimensional peaks: Experiential (0.85), Economic (0.85), Semiotic (0.75)
Structural asset:  Signal dominance — designed signals overwhelm ambient noise

**RENDERED SUMMARY (L2)**
Resilience grade:  A-
Key implication:   No selective defense — recovery requires system-wide correction

---
**PATAGONIA — SPECTRAL PROFILE (L1)**
Coherence type:    Identity
Signal arch:       Goldilocks zone, ideology-led (D/A/S ~55/40/5)
Resilience mech:   Binary division — aligned cohorts strengthen, others irrelevant
Dimensional peaks: Ideological (0.90), Cultural (0.75), Experiential (0.70)
Structural asset:  Ideological gravity — filters cohort compatibility at entry

**RENDERED SUMMARY (L2)**
Resilience grade:  B+
Key implication:   Do not moderate the ideology — it IS the architecture

---
**EREWHON — SPECTRAL PROFILE (L1)**
Coherence type:    Experiential Asymmetry
Signal arch:       Ambient-leaning (D/A/S ~25-40/55-70/5 — range reflects measurement uncertainty)
Resilience mech:   Geographic isolation — local vs mediated cohorts disrupted independently
Dimensional peaks: Social (0.90), Experiential (direct cohort: 0.80), Economic (0.75)
Structural risk:   Mediated cloud may never collapse to conviction — permanently partial

**RENDERED SUMMARY (L2)**
Resilience grade:  B-
Key implication:   Manage as two parallel brands: local and mediated

---
**TESLA — SPECTRAL PROFILE (L1)**
Coherence type:    Incoherent
Signal arch:       High-power, ambient-dominated (D/A/S ~30/65/5)
Resilience mech:   Amplifying — disruptions widen existing cohort divisions
Dimensional peaks: Experiential (0.90), Ideological (0.90), Economic (0.85)
Structural risk:   CEO-driven ambient contamination; absorbing negative cohorts;
                   ~65% of signal environment outside brand control

**RENDERED SUMMARY (L2)**
Resilience grade:  C-
Key implication:   Cannot communicate out of incoherence — structural fix required

---

**Spectral metamerism**: different L1 spectral profiles can project to the same L2 grade — as different spectra of light appear as the same colour to the human eye. A C- from Tesla (high-power, ambient-dominated, amplifying mechanism) and a C- from a hypothetical B2B brand with contradictory investor/customer messaging are the same grade but different spectra. The grade tells you the resilience colour. It cannot tell you whether you are looking at a single-wavelength laser or a broad-spectrum compound that happens to appear identical. When two brands receive the same coherence grade, or when a grade diagnosis feels insufficient, go to the L1 spectral profile. The grade is the compression. The profile is the ground truth.

### 5.3 Product-Anchored Cohort as Universal Resilience Asset

**Discovery**: confirmed across ALL 5 brands. In every disruption scenario, the cohort with highest experiential weight and evidence-based conviction provides the structural floor. Product-anchored cohorts absorb disruption better because their conviction is built on direct evidence, not ambient signals.

| Brand | Product Cohort | Experiential Weight | Disruption Behavior |
|-------|---------------|-------------------|-------------------|
| Hermès | Heritage Client | 0.30 | Reinforces ("art survives markets") |
| IKEA | Budget Family | 0.30 | Stabilizes ("products still work") |
| Patagonia | Outdoor Purist | 0.30 | Anchors ("gear is still excellent") |
| Tesla | Tech Loyalist | 0.35 | Sole firewall (only unconflicted dimension) |
| Erewhon | Wellness Devotee | 0.35 | Reinforces ("I know the product firsthand") |

### 5.4 Designed/Ambient Goldilocks Zone

**Exploratory hypothesis**: the five-brand comparison suggests a possible optimal designed/ambient signal ratio around 55-65% designed. This is an exploratory hypothesis requiring larger-sample validation.

| Brand | D/A/S Ratio (est.) | Coherence | Assessment |
|-------|-------------------|-----------|------------|
| IKEA | 70/25/5 | 7/10 | Slightly over-designed (lacks organic defenders) |
| Hermès | 60/35/5 | 8/10 | Goldilocks zone + ambient ALIGNMENT |
| Patagonia | 55/40/5 | 4/10 | Zone entry — but ideological split reduces coherence |
| Tesla | 30/65/5 | 2/10 | Critically under-designed (CEO ambient dominance) |
| Erewhon | ~25-40/55-70/5 | 4/10 | Ambient-dominated (brand doesn't control its narrative) |

*D = designed signals; A = ambient signals; S = synthetic/AI-generated and unclassified signals. Ratios are order-of-magnitude estimates (±10-15% uncertainty); a systematic signal audit would be required for precise measurement. Erewhon's wider range reflects divergent estimates across analyses.*

**Key qualifier**: the DIRECTION of ambient signals matters as much as the ratio. Hermès (60/35/5, aligned ambient) outperforms IKEA (70/25/5, passive ambient) because Hermès' ambient signals amplify designed signals rather than merely existing.

### 5.5 Temporal Compounding Pattern

**Analytical observation**: heritage depth appears to follow a non-linear pattern across the five brands. The temporal dimension is the only dimension that competitors cannot replicate and that no disruption can erase.

| Heritage Duration | Structural Role | Brand Example |
|-------------------|---------------|---------------|
| ~10 years | Negligible (currency, not heritage) | Erewhon |
| ~20 years | Supplementary (barely leveraged) | Tesla |
| ~50 years | Moderate (story exists but under-told) | Patagonia |
| ~80 years | Approaching threshold (significant but under-communicated) | IKEA |
| ~180+ years | Foundational architecture (heritage IS the operating system) | Hermès |

**Temporal modes**: heritage (compounds) vs currency (depreciates). Opposite risk profiles.

**Note**: these duration bands are approximate thresholds suggested by the five-brand comparison. They illustrate the mechanism's existence but are not empirically validated boundary conditions; a larger sample would likely refine the inflection points. The underlying mathematical form of the compounding relationship — whether logarithmic, exponential, or step-function — cannot be specified from five data points.

### 5.6 Mediated Cloud Formation

**Discovery**: clouds can form via screens without direct product encounter. The observer builds an impression from content, social media, and secondhand accounts — but this impression may never collapse to conviction. It exists in a permanent pre-conviction state.

- **Discovered**: Erewhon Digital Observer (cloud confidence 0.45, permanently forming)
- **Properties**: lower confidence, higher volatility, dual-coded (aspirational + incomplete)
- **Significance**: increasingly the DEFAULT mode for digital-native brand perception

### 5.7 Weight-Barrier-Crossing Signals

**Discovery**: certain signals bypass an observer's dimensional weight filtering. Not all weights are absolute.

- **Discovered**: IKEA case study — child labor scandal activates Budget Family despite 0.05 ideological weight
- **Mechanism**: signal migrates from primary dimension (ideological) to a dimension where the observer IS sensitive (experiential/safety)
- **Implication**: supply chain ethics is an experiential risk, not just an ideological one

### 5.8 Negative Cloud Resilience

**Discovery**: negative clouds STRENGTHEN during brand disruption. Evidence-free negative convictions are more stable than evidence-rich positive ones.

- **Discovered**: Tesla Boycotter (0.82 confidence, zero product experience)
- **Mechanism**: no experiential data to create cognitive dissonance. Brand crises CONFIRM the negative conviction rather than challenging it.
- **Paradox**: the observer with the LEAST evidence has the MOST stable conviction

### 5.9 Brand Health vs Brand Power Inversion

**Discovery**: brand health and brand power are independent variables. Traditional metrics conflate them.

| Brand | Traditional Power | Spectral Health | The Gap |
|-------|------------------|----------------|---------|
| Tesla | Highest (awareness, cultural impact) | Lowest (C-) | Maximum inversion |
| Hermès | Moderate (niche, exclusive) | Highest (A+) | Architecture > awareness |

**Implication**: the framework measures ARCHITECTURE, not AWARENESS. The confusion between brand power and brand health is the central error in traditional brand management.

### 5.10 Non-Ergodic Perception Dynamics

**Organizing analogy**: Peters' (2019) ergodicity economics provides an illuminating analogy for brand perception dynamics. In non-ergodic processes, the time average (what one agent experiences over time) diverges from the ensemble average (what many agents experience at one moment). Brand perception exhibits analogous dynamics: what any individual cohort experiences over time can diverge dramatically from what aggregate surveys capture at a single moment. We use this analogy as an organizing framework for understanding why brand health (time-dimension, cohort-specific) and brand power (ensemble dimension, aggregate) can be independent variables — not as a claim that brand perception obeys the specific mathematical properties Peters demonstrates for wealth processes.

**Theoretical basis**: Peters, O. (2019). The ergodicity problem in economics. *Nature Physics*, 15, 1216–1221. Peters demonstrates that for 300 years, economics has confused ensemble averages (across many agents at one moment) with time averages (one agent across time). In non-ergodic systems, these diverge. Brand perception exhibits analogous dynamics: signals compound multiplicatively, sequence matters, and negative conviction functions as a near-absorbing state. These are structural parallels to non-ergodic processes, not claims that brand perception obeys the specific mathematics of Peters' wealth model.

**What non-ergodicity explains in SBT**:

| SBT Discovery | Non-Ergodic Explanation |
|---------------|----------------------|
| Brand health != brand power (7.9) | Time average != ensemble average |
| Negative clouds strengthen under disruption (7.8) | Absorbing state — no reversal mechanism |
| Temporal compounding is non-linear (7.5) | Multiplicative path-dependent growth |
| Coherence type determines resilience (7.2) | Ergodicity profile determines which metrics are reliable |
| D/A ratio predicts controllability (7.4) | High D/A = more ergodic (controllable), low D/A = more non-ergodic (chaotic) |
| Evidence-free conviction > evidence-rich (7.8) | Non-ergodic trajectory without experiential friction |

**Proposed metric — Ergodicity Coefficient (epsilon)**:

```
epsilon(brand, dimension) in [0, 1]
epsilon = 1.0 -> ergodic: ensemble surveys reliable
epsilon -> 0.0 -> non-ergodic: must track cohort trajectories
```

The Ergodicity Coefficient is a proposed future metric that would quantify this divergence per dimension per brand. Its implementation requires longitudinal cohort panel data and is on the validation research agenda (Part 7, H4). It is not currently implemented or measured.

We note that Peters' ergodicity economics framework remains debated within economics (e.g., Doctor et al., 2020; Meder et al., 2021); our use is analogical rather than dependent on the resolution of that debate.

### 5.11 Cross-Model Pipeline Robustness

**Finding**: the analytical pipeline produces consistent structural diagnoses when executed by different LLMs (Claude Opus 4.6 and Gemini 3.1 Pro). This demonstrates prompt consistency and internal reproducibility — not empirical validity. Two LLMs trained on similar internet corpora about the same five well-documented brands producing similar outputs shows that the framework is specified precisely enough to constrain LLM analysis; it does not show that those outputs accurately represent real consumer perception processes.

**Cross-model replication** (all 5 brands × 6 modules):

| Brand | Claude Opus 4.6 | Gemini 3.1 Pro | Convergence |
|-------|----------------|----------------|-------------|
| Tesla | Incoherent, C- | Incoherent, C- | Identical |
| Hermès | Ecosystem, A+ | Ecosystem, A+ | Identical |
| Patagonia | Identity, B+ | Identity, B+ | Identical |
| IKEA | Signal, A- | Signal, A- | Identical |
| Erewhon | Exp. Asymmetry, B- | Exp. Asymmetry, B- | Identical |

5/5 brands: identical coherence type + identical grade. Both models independently derived structural absence (Hermès) and CEO ambient domination (Tesla) without these being named in prompts.

**Model-sensitive** (varies by LLM, does not affect structural diagnosis):
- Cohort granularity: Claude Opus 4.6 atomizes (5-6 cohorts), Gemini 3.1 Pro synthesizes (3 cohorts) — consistent across all 5 brands
- D/A ratio: within 10-15 percentage points (Gemini attributes slightly more to designed signals)
- Narrative style: Claude emphasizes paradoxes; Gemini is more operationally clinical

**Implication**: the framework acts as a structured lens that constrains LLM analysis toward consistent analytical conclusions regardless of which model holds the lens. Different models produce different *resolution* but the same *structure* — like telescopes of different apertures viewing the same constellation. Running the pipeline with multiple models is a recommended practice for maximum analytical depth and cross-checking of structural diagnoses.

---

## Part 6: Current Validation Status

### What the LLM-based analysis demonstrates

1. **Internal consistency**: the same structured prompts produce replicable outputs. The five-brand analysis can be reproduced exactly by any analyst using the same prompts — a prerequisite for a useful analytical tool.

2. **Illustrative power**: the framework produces non-obvious structural insights for well-known brands. Structural absence (Hermès), CEO ambient domination (Tesla), and mediated cloud formation (Erewhon) emerged from the analytical process without being seeded in prompts.

3. **Pedagogical utility**: the five brand analyses communicate the framework's mechanisms more clearly than abstract descriptions alone. The case studies are effective teaching material for the framework's concepts.

### What the LLM-based analysis does NOT demonstrate

1. **Empirical accuracy of observer weights**: the dimensional weights assigned to observer cohorts are expert estimates by the framework's author. They have not been validated against actual consumer data (surveys, conjoint analysis, MaxDiff). Two analysts with different intuitions about observer weights may produce different coherence diagnoses.

2. **Predictive validity**: no outcome has been tested against real consumer behavior. The framework has not predicted a brand event before it occurred and confirmed the prediction.

3. **Generalizability**: the five brands were selected because they are among the most analyzed brands in the world and because they illustrate structurally different architectures. This selection bias means the nine candidate mechanisms may not generalize to less-documented brands.

4. **What cross-model replication proves**: identical outputs from Claude and Gemini demonstrate prompt consistency, not theoretical validity. Both models were trained on similar internet corpora containing extensive analysis of these five brands. Agreement between models reflects shared training data and identical structured prompts — not independent confirmation of real consumer perceptions.

### What empirical validation would look like

1. **Dimensional validity study**: survey instruments measuring the importance of each of the 8 dimensions to real consumer cohorts. Do consumers weight semiotic, narrative, temporal, and other dimensions in ways consistent with the framework's expert estimates?

2. **Observer weight conjoint study**: conjoint analysis or MaxDiff methodology to replace expert-estimated dimensional weights with measured consumer preference weights.

3. **Conviction collapse longitudinal panel**: panel study tracking the same cohort through a brand crisis, measuring when and how perception clouds shift toward conviction (collapse) or dissolution.

4. **Cohort discovery research**: cluster analysis of real consumer spectral profiles to test whether the framework's proposed cohort structures emerge from actual consumer data or are imposed by the analytical process.

### Current epistemic status

SBT is a formally specified analytical framework with explicit constructs, mechanisms, and candidate hypotheses. The five-brand exploratory analysis demonstrates the framework's internal consistency and illustrative power. Empirical validation — required to confirm the framework's claims about real consumer perception processes — remains future work.

This is the standard intermediate stage for theoretical frameworks: formal specification → testable hypotheses → empirical validation. SBT is at stage two. The testable hypotheses are specified in Part 7 below.

### Sensitivity analysis of coherence type assignments

Sensitivity analysis tested the robustness of the five coherence type assignments under +/-0.10 perturbation of key cohort dimensional weights — the conservative end of the +/-0.10-0.15 estimation uncertainty acknowledged in Part 9.2. Five of five coherence types survive standard single-weight perturbation. Four of five (Tesla, Hermès, IKEA, Erewhon) are fully robust across all tested perturbation scenarios, including aggressive double perturbations. One brand (Patagonia) is conditionally robust: identity coherence holds under standard perturbation but approaches a type boundary under simultaneous ideological -0.10 and experiential +0.10 perturbation for values-aligned observers, at which point the diagnosis becomes ambiguous between identity and signal coherence. Six of seven key structural findings (asymmetric conviction resilience, CEO ambient domination, structural absence, ecosystem self-repair, signal consistency, experiential encounter mode gap) are fully robust. Patagonia's ideological gravitational center is conditionally robust and should carry a qualifier pending empirical weight validation. The overall robustness reflects the fact that coherence type diagnoses depend on structural relationships between cohorts and brand-level emission properties, not on exact weight values within individual cohorts. Empirical weight validation via MaxDiff survey (Part 9.1) is most urgent for Patagonia, where the diagnosis sits closest to a type boundary.

---

## Part 7: Testable Hypotheses

The following hypotheses are generated by the SBT framework and constitute the empirical research agenda required to validate SBT as a theory:

**H1 (D/A Goldilocks zone)**: Brands with 55-65% designed signals will show higher brand equity and disruption resilience than brands outside this range, controlling for category, age, and market position.
Testable via: Cross-sectional study of 50+ brands with empirically measured D/A ratios and brand equity scores.

**H2 (Asymmetric conviction resilience)**: Evidence-free negative brand convictions will show higher resistance to counter-evidence than evidence-rich positive convictions.
Testable via: Experiment — expose participants with no/high product experience to counter-attitudinal brand information; measure conviction change.

**H3 (Coherence type predicts disruption response)**: Ecosystem-coherent brands will show selective disruption absorption; incoherent brands will show disruption amplification.
Testable via: Longitudinal cohort tracking before/after documented brand crisis events; compare resilience profiles across coherence types.

**H4 (Non-ergodic gap)**: For incoherent brands, cross-sectional brand surveys will systematically overstate cohort-level resilience relative to longitudinal individual-level tracking.
Testable via: Paired study — compare snapshot survey scores to individual panel tracking data for the same brand across incoherent vs signal-coherent types.

**H5 (Structural absence prerequisite)**: Structural absence strategies generate positive scarcity signals only when brands have established existing demand and cultural context that makes restriction legible as intention.
Testable via: Experiment — manipulate scarcity for high vs low demand brands; measure perceived exclusivity vs perceived arrogance.

**H6 (Gate friction varies by cohort)**: Identity gate friction for a given brand will differ significantly across observer cohorts, with cohorts whose dominant dimensions match the brand's strongest emission dimensions showing lower gate friction.
Testable via: Exposure experiment — present brand cues to cohorts with different spectral profiles; measure recognition threshold (number of exposures to achieve recognition).

**H7 (First-atom primacy)**: The dimensional content of the first brand atom encountered will disproportionately determine the observer's initial spectral profile, persisting as a prior even after subsequent atoms provide evidence on other dimensions.
Testable via: Experiment — expose different groups to different "first atoms" (experiential vs. semiotic vs. ideological); measure resulting spectral profiles after equal total exposure.

**H8 (Amplification asymmetry)**: Confirmed observers with negative-valence brand facts will have higher amplification rates than those with positive-valence facts, creating faster field population for negative atoms.
Testable via: Track secondary emission behavior (reviews, social posts, word-of-mouth) for positive vs. negative Confirmed observers; measure volume and reach of emitted ambient atoms.

**H9 (Channel-dimension coupling)**: Specific channels show systematic dimensional bias in atom transmission — e.g., Instagram transmits semiotic + social at high fidelity but experiential at low fidelity; direct encounters transmit experiential at high fidelity but ideological at low fidelity.
Testable via: Compare spectral profiles of observers who encountered the same brand through different channels; measure dimensional variance attributable to channel.

**H10 (Field density threshold)**: There exists a minimum field density below which encounter probability drops to near-zero regardless of observer receptivity, and this threshold is higher for channels with low signal-to-noise ratio.
Testable via: Vary brand signal frequency in controlled environments; measure encounter rate as a function of field density and channel noise level.

## Part 8: Relationship to Existing Frameworks

SBT builds on and extends several established frameworks. The following comparisons locate SBT's contribution precisely.

**vs Keller Customer-Based Brand Equity (CBBE)**: Keller locates equity in the consumer's mind. SBT extends this by formalizing the consumer as a heterogeneous population (not a single model) and specifying the perception-to-conviction pipeline mechanically.

**vs Kapferer Brand Identity Prism**: Kapferer's six facets describe brand identity from the brand's perspective. SBT's eight dimensions describe perceptual channels through which observers filter brand signals — different structural purpose.

**vs Sharp (mental availability)**: Sharp addresses acquisition (passing the identity gate widely). SBT's Signal Dissemination Layer (§3.5) now formalizes the mapping: mental availability = field density × gate friction⁻¹ × spectral profile accessibility; physical availability = channel coverage across observer environments; Category Entry Points = need-state activators that raise observer receptivity; Distinctive Brand Assets = gate friction reducers. SBT extends Sharp by specifying what happens *after* mental availability is achieved — how different observers assemble different brand meanings from the same signals.

**vs Erdem & Swait (1998) brand signaling**: Erdem & Swait apply economic signaling theory to brand credibility as a unidimensional quality signal. SBT extends this to an eight-dimensional signal field where observers determine which signals are informative.

**vs Schmitt (1999) Experiential Marketing**: Schmitt's five strategic experiential modules (SENSE, FEEL, THINK, ACT, RELATE) decompose the experiential domain. SBT's Experiential dimension encompasses Schmitt's modules as sub-types; SBT's contribution is situating experiential signals within a multi-dimensional perception field where experiential evidence interacts with — and can be overridden by — ideological, social, and economic signals.

**vs Oswald (2012, 2015) Marketing Semiotics**: Oswald applies Peircean semiotics to brand strategy. SBT's Semiotic dimension operationalizes this — brand names, logos, and visual identity as signal types within a formal perception pipeline. SBT extends the semiotic approach by treating semiotic signals as one of eight perceptual channels rather than the primary analytical lens.

**vs Consumer Culture Theory (Arnould & Thompson)**: CCT theorizes consumers as active cultural authors — conceptually aligned with SBT's 'observer as active assembler.' SBT formalizes this active role as a parameterized spectral profile.

**vs Kapferer & Bastien anti-laws of luxury**: Kapferer & Bastien codified strategic restriction as a luxury management principle. SBT formalizes the mechanism: restriction functions as cross-dimensional signal generation (economic restriction → social signal). SBT's contribution is the tripartite emission taxonomy and the cross-dimensional mechanism, not the observation of strategic restriction itself.

**vs Brock (1968) Commodity Theory / Cialdini (2001) Scarcity Principle**: Commodity theory (Brock, 1968) and the scarcity principle (Cialdini, 2001; Lynn, 1991) establish that scarcity enhances perceived value. SBT's structural absence formalizes the mechanism: restriction on one dimension generates a cross-dimensional signal on another. The contribution is not the observation of scarcity effects (well-established) but the specification of the cross-dimensional generation mechanism and the two prerequisites (existing demand + legitimizing context).

**vs Krosnick & Petty (1995) Attitude Strength**: Attitude strength research (Krosnick & Petty, 1995; Petty & Krosnick, 1995) establishes that strong attitudes resist change. SBT's conviction collapse and asymmetric resilience mechanisms extend this by specifying the dimensional pathway: evidence-free convictions resist counter-evidence because the observer's spectral profile excludes the dimensions where counter-evidence exists (the experiential gate is closed).

---

## Part 9: Measurement Methodology

The following protocols provide practical paths from the SBT framework to real empirical measurement. These are starting-point designs; specific implementations will vary by budget, timeline, and brand context.

### 9.1 Dimensional Importance Survey

To measure how much each of the 8 dimensions matters to a target observer cohort, use a MaxDiff (Maximum Difference Scaling) survey:

1. Present respondents with sets of 4 brand attributes drawn from the 8 SBT dimensions
2. For each set, ask: which attribute matters MOST in forming your opinion of a brand? Which matters LEAST?
3. Analyze with multinomial logit model to produce importance scores for each dimension
4. Segment respondents by score similarity to identify cohort clusters

Minimum sample: 200 respondents per cohort of interest. The resulting importance scores directly populate dimensional weight profiles in the SBT observer model.

### 9.2 Observer Weight Estimation from Existing Data

When primary research is not available, estimate dimensional weights from secondary behavioral signals:

| Behavioral Signal | Dimension Implied | Weight Proxy Method |
|---|---|---|
| Purchase driver stated (survey) | Economic, Experiential | Relative frequency in stated reasons |
| Complaint topics (review analysis) | Highest-weight dimensions for that cohort | Topic frequency × sentiment intensity |
| Advocacy content (organic posts) | Which dimensions the advocate emphasizes | Content analysis → dimensional tagging |
| Churn reasons (exit survey) | Where the brand failed that cohort | Failure dimension = high weight |
| Event attendance patterns | Experiential, Social | Participation rate as weight proxy |

Weight estimates derived from behavioral signals carry ±0.10-0.15 uncertainty. Treat as hypotheses until validated with primary research.

### 9.3 D/A Ratio Estimation via Content Analysis

To measure the designed/ambient/synthetic ratio empirically:

1. Sample 200+ brand touchpoints from the past 12 months (social posts, earned media, reviews, news)
2. Code each touchpoint as: Designed (brand-controlled), Ambient (externally generated), Synthetic (AI-generated or algorithmic)
3. Weight by estimated reach (high-reach touchpoints count more)
4. Calculate weighted proportions

For ambient signals, separate by valence (positive/negative/neutral) — valence is often more diagnostic than volume.

### 9.4 Conviction Strength Proxies

Standard tracking metrics map approximately to SBT conviction states:

| Tracking Metric | SBT Construct | Mapping Notes |
|---|---|---|
| Unaided awareness | Identity gate permeability | Gate passed = aware; gate failed = aware of category, not brand |
| Brand consideration | Cloud formation stage | Considering = cloud forming or partial; not considering = unaware or contradicted |
| Net Promoter Score | Conviction direction + strength | Promoters = strong positive conviction; Detractors = strong negative conviction (often absorbing) |
| Brand loyalty / repeat purchase | Confirmed fact + crystallized prior | High loyalty = deep prior; switching = re-collapse occurred |
| Willingness to pay premium | Economic dimension weight | Higher WTP = higher economic weight in that cohort |

These mappings are approximate. SBT's constructs are more granular than standard tracking metrics. Use existing tracking data as orientation, not as ground truth for dimensional profiles.

### 9.5 Minimum Viable Research Design

Before trusting an SBT diagnosis for strategic decisions, the following minimum research investment is recommended:

1. **One MaxDiff survey** (n=300, split across 2-3 likely cohorts) to validate dimensional weights
2. **D/A ratio content analysis** (n=200 touchpoints) to validate the designed/ambient estimate
3. **Conviction depth interview** (n=10-15 per cohort) to validate the qualitative coherence diagnosis

Total investment: approximately 6-8 weeks of research, 2-3 analyst weeks. This produces a validated observer model rather than an expert-estimated one.

---

## Part 10: Mapping to Existing Brand Tracking

SBT introduces new constructs that complement existing tracking systems. The following translations allow practitioners to use existing tracking data as starting-point inputs for SBT analysis, and to interpret SBT outputs in the language of existing dashboards.

| Existing Metric | SBT Equivalent | Translation Notes |
|---|---|---|
| Brand awareness (unaided) | Identity gate permeability | Awareness = gate passed; non-awareness = gate failed or atoms below threshold |
| Brand consideration | Cloud formation stage | In consideration set = cloud forming (partial fact); not in set = unaware or contradicted |
| Brand preference | Cloud valence + conviction direction | Preferred = positive cloud forming toward collapse; rejected = negative cloud or absorbing state |
| Net Promoter Score | Conviction strength proxy | Promoters ≈ confirmed positive fact; Passives ≈ partial fact; Detractors ≈ strong negative conviction |
| Brand differentiation (Kantar) | Dimensional coverage | High differentiation = clear signal on at least one high-weight dimension for each cohort |
| Social listening sentiment | Ambient signal valence | Positive sentiment = ambient signal aligning with designed; negative = ambient contamination |
| Share of voice | D/A ratio approximation | Controlled SOV (owned + paid) ≈ designed signal volume proxy; earned SOV ≈ ambient signal proxy |
| Brand equity index | Coherence type + grade composite | High equity + low resilience = power-health inversion (see 7.9); track separately |
| Customer lifetime value by segment | Per-cohort conviction depth | High CLV cohort = confirmed fact + strong prior; segment by SBT cohort for structural insight |

**Important note**: these are approximate conceptual translations. SBT generates its own metrics (dimensional weight profiles, cloud confidence scores, D/A ratios, coherence types) that are more structurally specific than standard tracking outputs. The mapping above allows practitioners to orient SBT analysis within existing measurement infrastructure — not to replace existing tracking with SBT constructs directly.

**Recommended integration approach**: run SBT analysis in parallel with existing tracking for 2-3 quarters. Compare SBT diagnostic predictions (e.g., "this cohort's conviction is an absorbing negative state — NPS will not improve with messaging changes") against actual tracking movement. This generates the empirical track record that builds confidence in SBT structural diagnoses.

---

## References

**Source architecture**: `v2_architecture.md` -- Atom-Cloud-Fact pipeline
**Implementation**: `alibi/atoms/parser.py`, `alibi/clouds/formation.py`, `alibi/clouds/collapse.py`
**Identity system**: `alibi/identities/matching.py`
