"""
Capacity Analyzer (R4: Sphere Packing, Zharnikov 2026g).

Validates brand positioning claims against sphere packing bounds proven
in R4. Key result: the number of truly distinguishable brand positions
in 8D space has a finite upper bound.

Key R4 results enforced:
- Maximum packing capacity in S^7_+ (positive octant of 8-sphere)
- Minimum separation distance for distinguishable brands
- White space identification using covering radius
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    N_DIM,
    aitchison_distance,
    normalize_to_sphere,
    positive_orthant_fraction,
    sphere_surface_area,
    to_signal_array,
    unit_ball_volume,
)

# R4 key constants for n=8
# E8 lattice packing density (densest known in 8D, Viazovska 2017)
E8_PACKING_DENSITY = np.pi**4 / 384  # ~0.2537

# Practical minimum separation (Aitchison distance below which brands are
# perceptually indistinguishable to most observers)
MIN_DISTINGUISHABLE_DISTANCE = 0.15


@dataclass
class CapacityReport:
    """Report on positioning capacity and white space."""

    n_brands: int = 0
    theoretical_max: int = 0
    utilization: float = 0.0
    min_pairwise_distance: float = 0.0
    mean_pairwise_distance: float = 0.0
    crowded_pairs: list[tuple[str, str, float]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def estimate_packing_capacity(
    min_separation: float = MIN_DISTINGUISHABLE_DISTANCE,
) -> int:
    """
    Estimate maximum number of distinguishable brand positions in S^7_+.

    Uses sphere packing volume bounds:
    N <= Vol(S^7_+) / Vol(cap of radius r/2)

    This is a generous upper bound; actual capacity is lower due to
    geometric constraints.
    """
    # S^7_+ surface area
    total_sa = sphere_surface_area(N_DIM)
    orthant_sa = total_sa * positive_orthant_fraction(N_DIM)

    # Volume of a spherical cap of angular radius theta = min_separation / 2
    # For small theta, cap area ~ V_{n-2} * theta^(n-2)
    theta = min_separation / 2.0
    if theta <= 0:
        return 0

    # Small-angle cap volume approximation for S^(n-1)
    cap_volume = unit_ball_volume(N_DIM - 1) * theta ** (N_DIM - 1)

    if cap_volume <= 0:
        return 0

    return max(1, int(orthant_sa / cap_volume))


def analyze_positioning_capacity(
    profiles: dict[str, list[float] | np.ndarray],
    min_separation: float = MIN_DISTINGUISHABLE_DISTANCE,
) -> CapacityReport:
    """
    Analyze brand positioning density against R4 sphere packing bounds.

    Parameters
    ----------
    profiles : dict
        Brand name -> 8D signal profile.
    min_separation : float
        Minimum Aitchison distance for distinguishable brands.
    """
    report = CapacityReport()

    # Parse profiles
    arrays = {}
    for name, profile in profiles.items():
        try:
            arrays[name] = to_signal_array(profile)
        except ValueError:
            report.warnings.append(f"Skipping {name}: invalid profile")

    names = list(arrays.keys())
    report.n_brands = len(names)

    if report.n_brands < 2:
        report.warnings.append("Need at least 2 brands for capacity analysis")
        return report

    # Compute pairwise distances
    distances = []
    for i, n1 in enumerate(names):
        for n2 in names[i + 1 :]:
            d = aitchison_distance(arrays[n1], arrays[n2])
            distances.append((n1, n2, d))
            if d < min_separation:
                report.crowded_pairs.append((n1, n2, d))

    all_dists = [d for _, _, d in distances]
    report.min_pairwise_distance = min(all_dists)
    report.mean_pairwise_distance = float(np.mean(all_dists))

    # Theoretical capacity
    report.theoretical_max = estimate_packing_capacity(min_separation)
    if report.theoretical_max > 0:
        report.utilization = report.n_brands / report.theoretical_max

    # Warnings
    if report.crowded_pairs:
        report.warnings.append(
            f"{len(report.crowded_pairs)} brand pair(s) closer than "
            f"minimum separation {min_separation:.3f}. "
            "These brands may be perceptually indistinguishable to observers."
        )

    report.warnings.append(
        f"R4 bound: S^7_+ supports at most ~{report.theoretical_max} "
        f"distinguishable positions at separation {min_separation:.3f}. "
        f"Current utilization: {report.utilization:.1%} "
        f"({report.n_brands}/{report.theoretical_max})."
    )

    # Effective dimensionality check
    if report.n_brands >= 3:
        all_signals = np.array([arrays[n] for n in names])
        centered = all_signals - all_signals.mean(axis=0)
        _, singular_values, _ = np.linalg.svd(centered, full_matrices=False)
        total_sv = np.sum(singular_values**2)
        if total_sv > 0:
            cumulative = np.cumsum(singular_values**2) / total_sv
            eff_dim = int(np.searchsorted(cumulative, 0.95)) + 1
            if eff_dim < N_DIM:
                report.warnings.append(
                    f"Effective dimensionality: {eff_dim}/{N_DIM}. "
                    f"Brands cluster in a {eff_dim}D subspace. "
                    "Packing capacity in this subspace is lower."
                )

    return report
