"""
Resource Allocation Validator (R7: Spectral Resource Allocation, Zharnikov 2026k).

Validates resource allocation analyses against optimal allocation theorems
and alignment gap bounds proven in R7. Key results enforced:

- Optimal allocation proportional to cohort weights / cost (Theorem 1)
- Alignment gap with Hellinger distance diagnostic (Theorem 2)
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

# Blind spot threshold: founder weight below this is considered near-zero.
# Cohort weight above BLIND_SPOT_COHORT_MIN on the same dimension triggers
# a blind spot warning. Threshold set to match practitioner expectations:
# a 2% allocation is effectively negligible for most budget structures.
BLIND_SPOT_FOUNDER_MAX = 0.02
BLIND_SPOT_COHORT_MIN = 0.05


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
    efficiency_loss: float = 0.0
    per_cohort_gaps: dict[str, float] = field(default_factory=dict)
    multi_cohort_feasible: bool = True
    multi_cohort_diameter: float = 0.0
    efficiency_loss_bound: float = 0.0
    herfindahl_founder: float = 0.0
    herfindahl_cohort: float = 0.0
    blind_spot_dimensions: list[str] = field(default_factory=list)
    data_quality: str = "unknown"
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

    Under uniform costs with alpha_i = alpha_bar:
        A(f,c) = (1 / (lambda * alpha_bar)) * (||w(f)||^2 - <w(f), w(c)>)

    Note: this is NOT symmetric. A(f,c) != A(c,f) in general.
    For the symmetric efficiency loss, use compute_efficiency_loss().
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS

    s_founder = compute_optimal_allocation(founder_weights, cost_params, shadow_price)
    v_founder_for_founder = float(np.dot(founder_weights, s_founder))
    v_founder_for_cohort = float(np.dot(cohort_weights, s_founder))
    return v_founder_for_founder - v_founder_for_cohort


def compute_efficiency_loss(
    founder_weights: np.ndarray,
    cohort_weights: np.ndarray,
    cost_params: np.ndarray | None = None,
    shadow_price: float = DEFAULT_LAMBDA,
) -> float:
    """
    Compute the cohort's efficiency loss from founder misallocation.

    L(f,c) = U(s*_c, c) - U(s*_f, c)

    where U(s, w) = w.s - (1/2) * s' * diag(alpha) * s is net value.

    Under uniform costs:
        L(f,c) = ||w(f) - w(c)||^2 / (2 * lambda * alpha_bar)

    This is symmetric, always non-negative, and measures how much value
    the cohort loses because the founder optimizes for their own weights.
    """
    if cost_params is None:
        cost_params = DEFAULT_COST_PARAMS
    alpha_bar = float(np.mean(cost_params))
    diff = founder_weights - cohort_weights
    return float(np.sum(diff**2)) / (2.0 * shadow_price * alpha_bar)


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


def _has_nan_or_inf(arr: np.ndarray) -> bool:
    """Check for NaN or Inf values."""
    return bool(np.any(np.isnan(arr)) or np.any(np.isinf(arr)))


def validate_resource_allocation(
    founder_weights: list[float] | np.ndarray,
    cohort_weights: dict[str, list[float] | np.ndarray],
    proposed_allocation: list[float] | np.ndarray | None = None,
    cost_params: list[float] | np.ndarray | None = None,
    shadow_price: float = DEFAULT_LAMBDA,
    efficiency_tolerance: float = 0.10,
    data_source: str = "unknown",
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
    data_source : str
        Origin of weight data: 'survey', 'financial_report',
        'behavioral', 'llm_estimate', or 'unknown'. When source is
        'llm_estimate' or 'unknown', a quality warning is emitted.
    """
    report = AllocationReport()
    report.data_quality = data_source

    # --- Data quality gate ---
    if data_source in ("llm_estimate", "unknown"):
        report.warnings.append(
            f"Data quality: weights source is '{data_source}'. "
            "Results are indicative only. Validate with MaxDiff survey "
            "or financial report analysis before making budget decisions."
        )

    # Parse and normalize founder weights
    try:
        fw = to_signal_array(founder_weights)
        if _has_nan_or_inf(fw):
            report.errors.append("Founder weights contain NaN or Inf values")
            report.valid = False
            return report
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
        if _has_nan_or_inf(cp):
            report.errors.append("Cost parameters contain NaN or Inf values")
            report.valid = False
            return report
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
            if _has_nan_or_inf(cw):
                report.warnings.append(f"Cohort '{name}': NaN or Inf values, skipping")
                continue
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
            if not _has_nan_or_inf(proposed):
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

    worst_gap = 0.0
    worst_bound = 0.0
    worst_cohort_h = 0.0

    for name, cw in parsed_cohorts.items():
        actual_gap = compute_alignment_gap(fw, cw, cp, shadow_price)
        eff_loss = compute_efficiency_loss(fw, cw, cp, shadow_price)
        lower_bound = compute_alignment_gap_lower_bound(fw, cw, cp, shadow_price)
        d_fr = fisher_rao_distance(fw, cw)

        report.per_cohort_gaps[name] = actual_gap

        if actual_gap > worst_gap:
            worst_gap = actual_gap
            worst_bound = lower_bound
            worst_cohort_h = herfindahl_index(cw)

        if eff_loss > report.efficiency_loss:
            report.efficiency_loss = eff_loss

        if actual_gap > 0.05:
            report.warnings.append(
                f"R7 Thm 2: Alignment gap with cohort '{name}' = {actual_gap:.4f} "
                f"(efficiency loss = {eff_loss:.4f}, "
                f"Fisher-Rao distance = {d_fr:.4f}). "
                "Founder is investing in wrong dimensions."
            )

    report.alignment_gap = worst_gap
    report.alignment_gap_lower_bound = worst_bound
    report.herfindahl_cohort = worst_cohort_h

    # --- Proposition 3: Blind spot detection ---
    from spectral_branding.validators._math import DIMENSIONS

    for name, cw in parsed_cohorts.items():
        for i in range(N_DIM):
            if fw[i] < BLIND_SPOT_FOUNDER_MAX and cw[i] > BLIND_SPOT_COHORT_MIN:
                dim_name = DIMENSIONS[i]
                if dim_name not in report.blind_spot_dimensions:
                    report.blind_spot_dimensions.append(dim_name)
                report.warnings.append(
                    f"R7 Prop 3: Founder blind spot on '{dim_name}' "
                    f"(founder weight = {fw[i]:.3f}, "
                    f"cohort '{name}' weight = {cw[i]:.2f}). "
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
