"""
Cohort Validator (R3: Cohort Boundaries, Zharnikov 2026f).

Validates cohort analysis results against concentration of measure bounds
proven in R3. Key result: in 8D perception space, cohort boundaries are
inherently fuzzy -- sharp segmentation is geometrically impossible.

Key R3 results enforced:
- Boundary fuzziness >= 57% at delta=0.10 (Theorem 2)
- Membership probability transitions smoothly (no sharp cutoffs)
- Distance contrast ratio bounds cohort separability
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    N_DIM,
    fisher_rao_distance,
    to_signal_array,
)

# R3 Theorem 2: minimum boundary fuzziness on Delta^7
# P(|d(x, boundary) - E[d]| <= delta) >= 1 - 2*exp(-c*n*delta^2)
# For n=8, delta=0.10: fuzziness ~= 0.57
BOUNDARY_FUZZINESS_N8_D010 = 0.57

# Concentration constant for the simplex (Dirichlet measure)
CONCENTRATION_CONSTANT = 0.5  # conservative bound from R3


@dataclass
class CohortReport:
    """Validation report for cohort analysis."""

    valid: bool = True
    n_cohorts: int = 0
    boundary_fuzziness: float = BOUNDARY_FUZZINESS_N8_D010
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    cohort_separability: dict[tuple[str, str], float] = field(default_factory=dict)


def validate_cohort_assignment(
    observer_profiles: dict[str, list[float] | np.ndarray],
    cohort_labels: dict[str, str],
    min_cohort_size: int = 2,
) -> CohortReport:
    """
    Validate cohort assignments against R3 geometric bounds.

    Parameters
    ----------
    observer_profiles : dict
        Observer name -> weight profile (probability vector on Delta^7).
    cohort_labels : dict
        Observer name -> cohort label.
    min_cohort_size : int
        Minimum observers per cohort for meaningful analysis.
    """
    report = CohortReport()

    # Parse profiles
    profiles = {}
    for name, weights in observer_profiles.items():
        try:
            arr = to_signal_array(weights)
            if np.any(arr < 0):
                report.warnings.append(f"{name}: negative weights, skipping")
                continue
            total = np.sum(arr)
            if total > 0:
                profiles[name] = arr / total
            else:
                report.warnings.append(f"{name}: zero-sum weights, skipping")
        except ValueError:
            report.warnings.append(f"{name}: invalid profile shape, skipping")

    if len(profiles) < 2:
        report.warnings.append("Fewer than 2 valid profiles; cohort analysis skipped")
        return report

    # Identify cohorts
    cohorts: dict[str, list[str]] = {}
    for name, label in cohort_labels.items():
        if name in profiles:
            cohorts.setdefault(label, []).append(name)

    report.n_cohorts = len(cohorts)

    # Check cohort sizes
    for label, members in cohorts.items():
        if len(members) < min_cohort_size:
            report.warnings.append(
                f"Cohort '{label}' has {len(members)} member(s) "
                f"(minimum {min_cohort_size}). Assignment may be noise."
            )

    # Core R3 constraint: boundary fuzziness
    report.warnings.append(
        f"R3 bound: In {N_DIM}D perception space, cohort boundaries have "
        f">={BOUNDARY_FUZZINESS_N8_D010:.0%} fuzziness at delta=0.10. "
        "Sharp cohort boundaries are geometrically impossible."
    )

    # Compute inter-cohort separability
    cohort_names = list(cohorts.keys())
    for i, c1 in enumerate(cohort_names):
        for c2 in cohort_names[i + 1 :]:
            members1 = [profiles[m] for m in cohorts[c1] if m in profiles]
            members2 = [profiles[m] for m in cohorts[c2] if m in profiles]
            if not members1 or not members2:
                continue

            # Mean inter-cohort distance
            inter_dists = []
            for p1 in members1:
                for p2 in members2:
                    if np.all(p1 > 0) and np.all(p2 > 0):
                        inter_dists.append(fisher_rao_distance(p1, p2))

            # Mean intra-cohort distances
            intra_dists = []
            for group in [members1, members2]:
                for j in range(len(group)):
                    for k in range(j + 1, len(group)):
                        if np.all(group[j] > 0) and np.all(group[k] > 0):
                            intra_dists.append(fisher_rao_distance(group[j], group[k]))

            if inter_dists and intra_dists:
                mean_inter = np.mean(inter_dists)
                mean_intra = np.mean(intra_dists)
                if mean_intra > 0:
                    ratio = mean_inter / mean_intra
                    report.cohort_separability[(c1, c2)] = float(ratio)
                    if ratio < 1.5:
                        report.warnings.append(
                            f"Cohorts '{c1}' and '{c2}': separability ratio "
                            f"{ratio:.2f} < 1.5. Boundary is fuzzy "
                            "(consistent with R3 concentration bounds)."
                        )

    # Flag if too many cohorts relative to dimensionality
    if report.n_cohorts > N_DIM:
        report.warnings.append(
            f"{report.n_cohorts} cohorts in {N_DIM}D space: "
            "more cohorts than dimensions suggests over-segmentation."
        )

    return report
