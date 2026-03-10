"""
Metamerism Detector (R2: Spectral Metamerism, Zharnikov 2026e).

Detects when brand profiles that appear similar under one metric are
structurally different in the full 8D space. R2 proves that compressing
8D profiles to scalar scores must lose information (JL lemma lower bound:
>152% distortion for 10+ points).

Key R2 results enforced:
- Any single-number score conflates structurally different brands
- Minimum distortion bound: epsilon >= 1.52 for n=10 points in R^8
- Null space dimension >= 7 for any scalar projection
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    N_DIM,
    aitchison_distance,
    clr_transform,
    to_signal_array,
)

# R2 Theorem 1: JL distortion lower bound
# For n points in R^d projected to R^k, epsilon >= sqrt(d / (k * ln(n))) - 1
# For d=8, k=1, n=10: epsilon >= sqrt(8 / ln(10)) - 1 ~= 1.52
JL_DISTORTION_BOUND_N10 = 1.52
NULL_SPACE_DIM_SCALAR = N_DIM - 1  # 7 dimensions lost in scalar projection


@dataclass
class MetamerismReport:
    """Report on metameric risk for a set of brand profiles."""

    metameric_pairs: list[tuple[str, str, float]] = field(default_factory=list)
    scalar_collapse_risk: float = 0.0
    information_loss_dims: int = NULL_SPACE_DIM_SCALAR
    warnings: list[str] = field(default_factory=list)
    distortion_bound: float = JL_DISTORTION_BOUND_N10


def detect_metamerism(
    profiles: dict[str, list[float] | np.ndarray],
    scalar_scores: dict[str, float] | None = None,
    score_tolerance: float = 5.0,
    distance_threshold: float = 0.3,
) -> MetamerismReport:
    """
    Detect metameric pairs: brands with similar scalar scores but different
    spectral profiles.

    Parameters
    ----------
    profiles : dict
        Brand name -> 8D signal profile mapping.
    scalar_scores : dict, optional
        Brand name -> single-number score (e.g., NPS, brand health).
        If provided, checks for score-similar but structurally-different pairs.
    score_tolerance : float
        Maximum score difference to consider "similar" (default: 5 points).
    distance_threshold : float
        Minimum Aitchison distance to consider "structurally different".
    """
    report = MetamerismReport()

    # Convert all profiles
    arrays = {}
    for name, profile in profiles.items():
        try:
            arrays[name] = to_signal_array(profile)
        except ValueError:
            report.warnings.append(f"Skipping {name}: invalid profile shape")

    names = list(arrays.keys())

    # Update distortion bound for actual number of brands
    n_brands = len(names)
    if n_brands >= 2:
        ln_n = np.log(max(n_brands, 2))
        ratio = N_DIM / (1.0 * ln_n)  # k=1 for scalar projection
        if ratio > 1:
            report.distortion_bound = np.sqrt(ratio) - 1.0
        else:
            report.distortion_bound = 0.0

    # If scalar scores provided, detect score-metameric pairs
    if scalar_scores is not None:
        for i, n1 in enumerate(names):
            for n2 in names[i + 1 :]:
                if n1 not in scalar_scores or n2 not in scalar_scores:
                    continue
                score_diff = abs(scalar_scores[n1] - scalar_scores[n2])
                if score_diff <= score_tolerance:
                    d_aitchison = aitchison_distance(arrays[n1], arrays[n2])
                    if d_aitchison >= distance_threshold:
                        report.metameric_pairs.append((n1, n2, d_aitchison))

    # Always compute structural diversity (how spread out are the profiles?)
    if len(names) >= 2:
        all_clr = np.array([clr_transform(arrays[n]) for n in names])
        # Variance along each CLR dimension
        variances = np.var(all_clr, axis=0)
        # How many dimensions carry substantial variance?
        total_var = np.sum(variances)
        if total_var > 0:
            sorted_var = np.sort(variances)[::-1]
            cumulative = np.cumsum(sorted_var) / total_var
            # Number of dimensions needed for 90% of variance
            dims_90 = int(np.searchsorted(cumulative, 0.9)) + 1
            if dims_90 <= 2:
                report.warnings.append(
                    f"Only {dims_90} dimensions carry 90% of variance. "
                    "Scalar collapse risk is lower but still loses structure."
                )
            report.scalar_collapse_risk = 1.0 - (1.0 / max(dims_90, 1))

    # Core R2 warning: always flag scalar reduction
    if len(names) >= 2:
        report.warnings.append(
            f"R2 bound: projecting {N_DIM}D profiles to a scalar loses "
            f"{NULL_SPACE_DIM_SCALAR} dimensions. Minimum distortion for "
            f"{n_brands} brands: {report.distortion_bound:.0%} "
            f"(Larsen-Nelson 2017 tight bound)."
        )

    if report.metameric_pairs:
        report.warnings.append(
            f"Found {len(report.metameric_pairs)} metameric pair(s): "
            "brands with similar scores but different spectral structure."
        )

    return report
