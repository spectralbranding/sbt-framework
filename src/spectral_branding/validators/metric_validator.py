"""
Metric Validator (R1: Formal Metric, Zharnikov 2026d).

Validates that LLM-generated brand profiles satisfy the geometric
constraints proven in R1:
- Signal values are strictly positive (required for Aitchison geometry)
- Observer weights form valid probability vectors (simplex constraint)
- Pairwise distances satisfy triangle inequality
- Distance magnitudes are plausible given known brand distances
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    CANONICAL_BRANDS,
    N_DIM,
    SIGNAL_MAX,
    SIGNAL_MIN,
    aitchison_distance,
    clr_transform,
    fisher_rao_distance,
    normalize_to_simplex,
    to_signal_array,
    verify_triangle_inequality,
)


@dataclass
class MetricReport:
    """Validation report for metric constraints."""

    valid: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    distances: dict[str, float] = field(default_factory=dict)


def validate_signal_profile(signals: list[float] | np.ndarray) -> MetricReport:
    """
    Validate a brand signal profile against R1 metric constraints.

    Checks:
    1. Exactly 8 dimensions
    2. All values strictly positive (Aitchison geometry requires s_i > 0)
    3. Values within plausible range [1, 10]
    4. CLR transform is computable
    5. Distances to canonical brands are computable and satisfy triangle inequality
    """
    report = MetricReport()

    # Check dimensionality
    try:
        arr = to_signal_array(signals)
    except ValueError as e:
        report.valid = False
        report.errors.append(f"Dimension error: {e}")
        return report

    # Check strict positivity (required for log in CLR transform)
    if np.any(arr <= 0):
        zero_dims = [i for i, v in enumerate(arr) if v <= 0]
        report.valid = False
        report.errors.append(
            f"Non-positive values at dimensions {zero_dims}. "
            "Aitchison geometry requires all s_i > 0 (R1 Sec. 4)."
        )
        return report

    # Check plausible range
    if np.any(arr < SIGNAL_MIN) or np.any(arr > SIGNAL_MAX):
        out_of_range = [
            (i, float(arr[i]))
            for i in range(N_DIM)
            if arr[i] < SIGNAL_MIN or arr[i] > SIGNAL_MAX
        ]
        report.warnings.append(
            f"Values outside [{SIGNAL_MIN}, {SIGNAL_MAX}] range: {out_of_range}"
        )

    # Verify CLR transform works
    try:
        clr = clr_transform(arr)
        if not np.isclose(np.sum(clr), 0.0, atol=1e-10):
            report.errors.append("CLR transform sum != 0 (internal error)")
            report.valid = False
    except ValueError as e:
        report.valid = False
        report.errors.append(f"CLR transform failed: {e}")
        return report

    # Compute distances to canonical brands
    for name, canonical in CANONICAL_BRANDS.items():
        d = aitchison_distance(arr, canonical)
        report.distances[name] = d

    # Verify triangle inequality among canonical + new brand
    all_brands = list(CANONICAL_BRANDS.values()) + [arr]
    n = len(all_brands)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                d_ij = aitchison_distance(all_brands[i], all_brands[j])
                d_jk = aitchison_distance(all_brands[j], all_brands[k])
                d_ik = aitchison_distance(all_brands[i], all_brands[k])
                if not verify_triangle_inequality(d_ij, d_jk, d_ik):
                    report.valid = False
                    report.errors.append(
                        f"Triangle inequality violation for brands {i},{j},{k}"
                    )

    # Plausibility check: extreme distances are suspicious
    max_canonical_dist = max(
        aitchison_distance(a, b)
        for a in CANONICAL_BRANDS.values()
        for b in CANONICAL_BRANDS.values()
    )
    for name, d in report.distances.items():
        if d > 3.0 * max_canonical_dist:
            report.warnings.append(
                f"Distance to {name} ({d:.3f}) is >3x the max canonical "
                f"distance ({max_canonical_dist:.3f}). Profile may be extreme."
            )

    return report


def validate_observer_profile(weights: list[float] | np.ndarray) -> MetricReport:
    """
    Validate an observer spectral profile against R1 simplex constraints.

    Checks:
    1. Exactly 8 dimensions
    2. All values non-negative
    3. Values sum to 1 (probability simplex)
    4. No single dimension dominates excessively (>0.95)
    """
    report = MetricReport()

    try:
        arr = to_signal_array(weights)
    except ValueError as e:
        report.valid = False
        report.errors.append(f"Dimension error: {e}")
        return report

    if np.any(arr < 0):
        report.valid = False
        report.errors.append(
            "Observer weights must be non-negative (probability simplex)."
        )
        return report

    if not np.isclose(np.sum(arr), 1.0, atol=1e-6):
        report.warnings.append(
            f"Weights sum to {np.sum(arr):.6f}, not 1.0. Normalizing."
        )
        arr = normalize_to_simplex(arr)

    # Check for degenerate concentration
    if np.max(arr) > 0.95:
        dominant = int(np.argmax(arr))
        report.warnings.append(
            f"Weight {arr[dominant]:.3f} on dimension {dominant} "
            f"is near-degenerate. Fisher-Rao distance may be unreliable."
        )

    # Check for zero weights (Fisher-Rao requires w_i > 0)
    if np.any(arr == 0):
        zero_dims = [i for i, v in enumerate(arr) if v == 0]
        report.warnings.append(
            f"Zero weights at dimensions {zero_dims}. "
            "Fisher-Rao distance requires w_i > 0 (R1 Sec. 5). "
            "Observer is blind to these dimensions."
        )

    return report
