"""
Resource Allocation Validator (R7: Spectral Resource Allocation, Zharnikov 2026k).

Validates resource allocation analyses against optimal allocation theorems
and alignment gap bounds proven in R7. Key results enforced:

- Optimal allocation proportional to cohort weights / cost (Theorem 1)
- Alignment gap >= Fisher-Rao lower bound (Theorem 2)
- Multi-cohort efficiency bounded by Fisher-Rao ball radius (Theorem 3)
- Cost-minimizing metamers satisfy hyperplane constraint (Theorem 4)
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    N_DIM,
    fisher_rao_distance,
    hellinger_distance,
    normalize_to_simplex,
    to_signal_array,
)

# R7 Theorem 3: Fisher-Rao ball radius for given efficiency loss
# For epsilon=0.10 (10% loss), max radius ~0.32 on Delta^7
MULTI_COHORT_RADIUS_EPS010 = 0.32

# For epsilon=0.30 (30% loss), max radius ~pi/4
MULTI_COHORT_RADIUS_EPS030 = np.pi / 4.0

# Default cost parameters (uniform quadratic: alpha_i = 1.0 for all i)
DEFAULT_COST_PARAMS = np.ones(N_DIM)

# Default shadow price (budget scaling factor)
DEFAULT_LAMBDA = 1.0

# Tolerance for numerical comparisons
NUMERICAL_TOL = 1e-8


def herfindahl_index(w: np.ndarray) -> float:
    """
    Herfindahl concentration index: H(w) = sum(w_i^2).

    Higher H means more concentrated weights (fewer dimensions matter).
    From R7 Proposition 1: higher H -> higher optimal value.
    """
    return float(np.sum(w**2))


@dataclass
class AllocationReport:
    """Validation report for resource allocation analysis."""

    valid: bool = True
    alignment_gap: float = 0.0
    alignment_gap_lower_bound: float = 0.0
    multi_cohort_feasible: bool = True
    multi_cohort_diameter: float = 0.0
    efficiency_loss_bound: float = 0.0
    herfindahl_founder: float = 0.0
    herfindahl_cohort: float = 0.0
    blind_spot_dimensions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def compute_optimal_allocation(
    cohort_weights: np.ndarray,
    cost_params: np.ndarray | None = None,
    shadow_price: float = DEFAULT_LAMBDA,
) -> np.ndarray:
    """
    Compute optimal signal portfolio for a single cohort (Theorem 1).

    s_i*(c) = w_i(c) / (lambda * alpha_i)

    Parameters
    ----------
    cohort_weights : array
        Cohort weight profile on Delta^7.
    cost_params : array, optional
        Per-dimension cost parameters alpha_i. Defaults to uniform.
    shadow_price : float
        Budget shadow price lambda.

    Returns
    -------
    Optimal signal portfolio s*.
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS
    return cohort_weights / (shadow_price * cost_params)


def compute_alignment_gap(
    founder_weights: np.ndarray,
    cohort_weights: np.ndarray,
    cost_params: np.ndarray | None = None,
    shadow_price: float = DEFAULT_LAMBDA,
) -> float:
    """
    Compute alignment gap A(f,c) under quadratic costs (Proposition 2).

    A(f,c) = V(s*_f, f) - V(s*_f, c)
           = (1 / (2 * lambda * alpha_bar)) * ||w(f) - w(c)||_2^2

    under uniform costs. For non-uniform costs, computes directly from
    value function difference.
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS

    s_founder = compute_optimal_allocation(founder_weights, cost_params, shadow_price)
    v_founder_for_founder = float(np.dot(founder_weights, s_founder))
    v_founder_for_cohort = float(np.dot(cohort_weights, s_founder))
    return v_founder_for_founder - v_founder_for_cohort


def compute_alignment_gap_lower_bound(
    founder_weights: np.ndarray,
    cohort_weights: np.ndarray,
    cost_params: np.ndarray | None = None,
    shadow_price: float = DEFAULT_LAMBDA,
) -> float:
    """
    Theorem 2 lower bound: A(f,c) >= H(f,c)^2 / (2 * lambda * alpha_bar).

    Uses Hellinger distance on the probability simplex.
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS
    alpha_bar = float(np.mean(cost_params))
    h = hellinger_distance(founder_weights, cohort_weights)
    return h**2 / (2.0 * shadow_price * alpha_bar)


def validate_resource_allocation(
    founder_weights: list[float] | np.ndarray,
    cohort_weights: dict[str, list[float] | np.ndarray],
    proposed_allocation: list[float] | np.ndarray | None = None,
    cost_params: list[float] | np.ndarray | None = None,
    shadow_price: float = DEFAULT_LAMBDA,
    efficiency_tolerance: float = 0.10,
) -> AllocationReport:
    """
    Validate resource allocation against R7 mathematical bounds.

    Parameters
    ----------
    founder_weights : array-like
        Founder's weight profile (8D, will be normalized to simplex).
    cohort_weights : dict
        Cohort name -> weight profile (8D, each normalized to simplex).
    proposed_allocation : array-like, optional
        Proposed signal portfolio to validate against optimum.
    cost_params : array-like, optional
        Per-dimension cost parameters. Defaults to uniform.
    shadow_price : float
        Budget shadow price.
    efficiency_tolerance : float
        Maximum acceptable efficiency loss for multi-cohort targeting.
    """
    report = AllocationReport()

    # Parse and normalize founder weights
    try:
        fw = to_signal_array(founder_weights)
        if np.any(fw < 0):
            report.errors.append("Founder weights contain negative values")
            report.valid = False
            return report
        if np.sum(fw) <= 0:
            report.errors.append("Founder weights sum to zero")
            report.valid = False
            return report
        fw = normalize_to_simplex(fw)
    except ValueError as e:
        report.errors.append(f"Invalid founder weights: {e}")
        report.valid = False
        return report

    # Parse cost parameters
    cp = DEFAULT_COST_PARAMS
    if cost_params is not None:
        cp = np.asarray(cost_params, dtype=np.float64)
        if cp.shape != (N_DIM,):
            report.errors.append(f"Cost params must have {N_DIM} dimensions")
            report.valid = False
            return report
        if np.any(cp <= 0):
            report.errors.append("Cost parameters must be strictly positive")
            report.valid = False
            return report

    # Parse cohort weights
    parsed_cohorts: dict[str, np.ndarray] = {}
    for name, weights in cohort_weights.items():
        try:
            cw = to_signal_array(weights)
            if np.any(cw < 0):
                report.warnings.append(f"Cohort '{name}': negative weights, skipping")
                continue
            if np.sum(cw) <= 0:
                report.warnings.append(f"Cohort '{name}': zero-sum weights, skipping")
                continue
            parsed_cohorts[name] = normalize_to_simplex(cw)
        except ValueError:
            report.warnings.append(f"Cohort '{name}': invalid shape, skipping")

    if not parsed_cohorts:
        report.errors.append("No valid cohort profiles provided")
        report.valid = False
        return report

    # --- Theorem 1: Optimal allocation check ---
    if proposed_allocation is not None:
        try:
            proposed = to_signal_array(proposed_allocation)
            # Check against each cohort's optimum
            for name, cw in parsed_cohorts.items():
                optimal = compute_optimal_allocation(cw, cp, shadow_price)
                deviation = float(np.linalg.norm(proposed - optimal))
                if deviation > 0.1 * float(np.linalg.norm(optimal)):
                    report.warnings.append(
                        f"R7 Thm 1: Proposed allocation deviates from "
                        f"cohort '{name}' optimum by {deviation:.4f} "
                        f"({deviation / max(float(np.linalg.norm(optimal)), NUMERICAL_TOL):.1%})"
                    )
        except ValueError:
            report.warnings.append("Proposed allocation: invalid shape, skipping check")

    # --- Theorem 2: Alignment gap analysis ---
    report.herfindahl_founder = herfindahl_index(fw)

    for name, cw in parsed_cohorts.items():
        actual_gap = compute_alignment_gap(fw, cw, cp, shadow_price)
        lower_bound = compute_alignment_gap_lower_bound(fw, cw, cp, shadow_price)
        d_fr = fisher_rao_distance(fw, cw)

        report.alignment_gap = actual_gap
        report.alignment_gap_lower_bound = lower_bound
        report.herfindahl_cohort = herfindahl_index(cw)

        # Verify Theorem 2 inequality (should always hold)
        if actual_gap < lower_bound - NUMERICAL_TOL:
            report.errors.append(
                f"R7 Thm 2 VIOLATED for cohort '{name}': "
                f"gap={actual_gap:.6f} < lower_bound={lower_bound:.6f}. "
                "This indicates a computation error."
            )
            report.valid = False

        if actual_gap > 0.05:
            report.warnings.append(
                f"R7 Thm 2: Alignment gap with cohort '{name}' = {actual_gap:.4f} "
                f"(Fisher-Rao distance = {d_fr:.4f}). "
                "Founder is investing in wrong dimensions."
            )

    # --- Proposition 3: Blind spot detection ---
    from spectral_branding.validators._math import DIMENSIONS

    for name, cw in parsed_cohorts.items():
        for i in range(N_DIM):
            if fw[i] < NUMERICAL_TOL and cw[i] > 0.05:
                report.blind_spot_dimensions.append(DIMENSIONS[i])
                report.warnings.append(
                    f"R7 Prop 3: Founder blind spot on '{DIMENSIONS[i]}' "
                    f"(founder weight ~0, cohort '{name}' weight = {cw[i]:.2f}). "
                    "Blind spots cause strictly larger alignment gaps "
                    "than distributed misallocation."
                )

    # --- Theorem 3: Multi-cohort feasibility ---
    if len(parsed_cohorts) >= 2:
        cohort_arrays = list(parsed_cohorts.values())
        max_dist = 0.0

        for i in range(len(cohort_arrays)):
            for j in range(i + 1, len(cohort_arrays)):
                if np.all(cohort_arrays[i] > 0) and np.all(cohort_arrays[j] > 0):
                    d = fisher_rao_distance(cohort_arrays[i], cohort_arrays[j])
                    if d > max_dist:
                        max_dist = d

        report.multi_cohort_diameter = max_dist

        # Compute radius threshold for given epsilon
        radius = np.arccos(np.clip(1.0 - efficiency_tolerance / 2.0, -1.0, 1.0))
        report.efficiency_loss_bound = efficiency_tolerance

        if max_dist > 2.0 * radius:
            report.multi_cohort_feasible = False
            report.warnings.append(
                f"R7 Thm 3: Cohort diameter {max_dist:.4f} exceeds "
                f"single-portfolio threshold {2.0 * radius:.4f} "
                f"for {efficiency_tolerance:.0%} efficiency loss. "
                "Consider sub-brands or separate portfolios."
            )
        else:
            report.warnings.append(
                f"R7 Thm 3: Cohort diameter {max_dist:.4f} within "
                f"single-portfolio threshold {2.0 * radius:.4f}. "
                f"Single brand can serve all cohorts within "
                f"{efficiency_tolerance:.0%} efficiency loss."
            )

    # --- Proposition 1: Concentration premium ---
    if report.herfindahl_founder > 0 and report.herfindahl_cohort > 0:
        if report.herfindahl_cohort > report.herfindahl_founder:
            report.warnings.append(
                f"R7 Prop 1: Cohort concentration (H={report.herfindahl_cohort:.3f}) "
                f"> founder concentration (H={report.herfindahl_founder:.3f}). "
                "Cohort's focused weights yield higher optimal value."
            )

    return report
