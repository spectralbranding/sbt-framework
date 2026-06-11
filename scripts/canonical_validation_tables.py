"""Companion computation script for the sbt-framework MethodsX article, Section 3.

Reproduces the quantitative validation results: the pairwise Aitchison-distance matrix
for the five canonical brand profiles, Fisher-Rao distances among representative observer
cohorts, a worked alignment-gap example, and an error-injection failure case.

Run:  cd /path/to/sbt-framework && uv run python <this script>
Deterministic: the five canonical profiles are fixed constants in the toolkit; the
representative cohorts/founder are fixed below. No randomness.
"""
import itertools
import numpy as np
from spectral_branding.validators._math import (
    CANONICAL_BRANDS, aitchison_distance, fisher_rao_distance, normalize_to_simplex,
)
from spectral_branding.validators.validate import validate_analysis

np.set_printoptions(precision=4, suppress=True)
names = list(CANONICAL_BRANDS.keys())

print("=" * 64)
print("A. Pairwise Aitchison distance matrix (5 canonical brands, 10 pairs)")
print("=" * 64)
print(f"{'':12}" + "".join(f"{n:>11}" for n in names))
for a in names:
    row = "".join(f"{aitchison_distance(CANONICAL_BRANDS[a], CANONICAL_BRANDS[b]):>11.4f}" for b in names)
    print(f"{a:12}{row}")
print("\nPairwise list:")
for a, b in itertools.combinations(names, 2):
    print(f"  {a:10}-{b:10}: {aitchison_distance(CANONICAL_BRANDS[a], CANONICAL_BRANDS[b]):.4f}")

print("\n" + "=" * 64)
print("B. Representative observer cohorts (weights on Delta^7) + Fisher-Rao")
print("=" * 64)
# Fixed representative cohorts (8 weights, sum to 1; S-N-I-E-So-Ec-C-T order)
cohorts = {
    "value_seeker":  [0.08, 0.07, 0.05, 0.12, 0.10, 0.40, 0.10, 0.08],
    "status_seeker": [0.22, 0.10, 0.06, 0.14, 0.28, 0.05, 0.10, 0.05],
    "ethics_seeker": [0.06, 0.14, 0.34, 0.08, 0.10, 0.05, 0.18, 0.05],
}
for k, v in cohorts.items():
    assert abs(sum(v) - 1.0) < 1e-9, f"{k} not on simplex"
print(f"{'':16}" + "".join(f"{n:>15}" for n in cohorts))
for a in cohorts:
    row = "".join(f"{fisher_rao_distance(np.array(cohorts[a]), np.array(cohorts[b])):>15.4f}" for b in cohorts)
    print(f"{a:16}{row}")

print("\n" + "=" * 64)
print("C. Worked alignment-gap example (founder vs cohorts; brand = Patagonia)")
print("=" * 64)
founder = [0.06, 0.14, 0.34, 0.08, 0.10, 0.05, 0.18, 0.05]  # founder mirrors ethics_seeker
analysis = {
    "brand_profiles": {"Patagonia": list(CANONICAL_BRANDS["Patagonia"])},
    "observer_profiles": cohorts,
    "cohort_labels": {k: f"cohort_{i}" for i, k in enumerate(cohorts)},
    "founder_weights": founder,
}
res = validate_analysis(analysis)
if res.allocation is not None:
    al = res.allocation
    print(f"  Alignment gap (founder vs cohort set): {al.alignment_gap:.4f}")
    print(f"  Efficiency loss: {al.efficiency_loss:.4f}")
    print(f"  Multi-cohort feasible: {al.multi_cohort_feasible}")
    print(f"  Blind-spot dimensions: {al.blind_spot_dimensions}")
    cd = getattr(al, "cohort_diameter", None)
    if cd is not None:
        print(f"  Cohort Fisher-Rao diameter: {cd:.4f}")
print("\n  Distances from Patagonia to canonical anchors (metric validator):")
if res.metric is not None:
    for n, d in sorted(res.metric.distances.items(), key=lambda x: x[1]):
        print(f"    {n:12}: {d:.4f}")

print("\n" + "=" * 64)
print("D. Error-injection failure case (non-positive signal value)")
print("=" * 64)
bad = {"brand_profiles": {"BadBrand": [0.0, 7.0, 8.0, 7.5, 9.0, 6.0, 8.0, 6.5]}}
bad_res = validate_analysis(bad)
print(f"  valid: {bad_res.valid}")
for e in bad_res.all_errors:
    print(f"  ERROR: {e}")
