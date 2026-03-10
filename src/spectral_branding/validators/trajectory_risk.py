"""
Trajectory Risk Analyzer (R6: Diffusion Dynamics, Zharnikov 2026j).

Validates brand perception trajectories against non-ergodic dynamics
proven in R6. Key result: brand perception evolves as a stochastic
process on S^7_+ with absorbing boundaries -- sufficiently negative
conviction is irreversible.

Key R6 results enforced:
- Absorption risk: min coordinate analysis (low values -> absorbing boundary)
- Non-ergodicity: time averages != ensemble averages
- Mixing time bounds on the perception manifold
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    DIMENSIONS,
    N_DIM,
    to_signal_array,
)

# R6 constants
# Minimum signal value before absorption risk becomes critical.
# On S^7_+, the absorbing boundary is where any coordinate -> 0.
# NOTE: R6 models absorption at coordinate = 0 (the Dirichlet boundary).
# This threshold is a practical engineering threshold that flags risk *before*
# reaching the mathematical absorbing boundary, giving practitioners time to act.
ABSORPTION_THRESHOLD = 2.0  # signal values below this are at risk

# Mixing time lower bound for diffusion on S^7_+ (R6 Theorem 3).
# R6 derives: tau_mix >= 2 / (lambda_gap * sigma_0^2)
# where lambda_gap = lambda_{D,2} - lambda_{D,1} = 160 - 112 = 48
# (Dirichlet spectral gap on S^7_+) and sigma_0 is the diffusion coefficient.
SPECTRAL_GAP = 48  # Dirichlet spectral gap from R6 Theorem 3
DEFAULT_SIGMA_0 = 0.1  # default diffusion coefficient


def _mixing_time_lower_bound(sigma_0: float = DEFAULT_SIGMA_0) -> float:
    """Compute mixing time lower bound per R6 Theorem 3.

    tau_mix >= 2 / (lambda_gap * sigma_0^2)
    """
    return 2.0 / (SPECTRAL_GAP * sigma_0**2)


MIXING_TIME_LOWER_BOUND = _mixing_time_lower_bound(DEFAULT_SIGMA_0)


@dataclass
class TrajectoryReport:
    """Report on trajectory risk for a brand profile."""

    absorption_risk: dict[str, float] = field(default_factory=dict)
    high_risk_dimensions: list[str] = field(default_factory=list)
    overall_risk: str = "low"  # low, moderate, high, critical
    mixing_time_bound: float = MIXING_TIME_LOWER_BOUND
    warnings: list[str] = field(default_factory=list)
    non_ergodic_flag: bool = True  # always true for SBT (R6 Theorem 1)


def analyze_trajectory_risk(
    signals: list[float] | np.ndarray,
    brand_name: str = "brand",
    historical_signals: list[list[float] | np.ndarray] | None = None,
    sigma_0: float = DEFAULT_SIGMA_0,
) -> TrajectoryReport:
    """
    Analyze absorption risk and trajectory dynamics for a brand profile.

    Parameters
    ----------
    signals : array-like
        Current 8D signal profile.
    brand_name : str
        Brand name for reporting.
    historical_signals : list, optional
        Previous signal profiles (time series) for trajectory analysis.
    sigma_0 : float
        Diffusion coefficient for mixing time bound (R6 Theorem 3).
        Default 0.1; lower values yield longer mixing times.
    """
    report = TrajectoryReport(mixing_time_bound=_mixing_time_lower_bound(sigma_0))

    try:
        arr = to_signal_array(signals)
    except ValueError as e:
        report.warnings.append(f"Invalid profile: {e}")
        report.overall_risk = "unknown"
        return report

    # Absorption risk per dimension
    # On S^7_+, each coordinate approaching 0 means approaching the absorbing
    # boundary. R6 proves this is irreversible once crossed.
    for i, dim_name in enumerate(DIMENSIONS):
        if arr[i] <= 0:
            risk = 1.0
        elif arr[i] < ABSORPTION_THRESHOLD:
            risk = 1.0 - (arr[i] / ABSORPTION_THRESHOLD)
        else:
            risk = 0.0
        report.absorption_risk[dim_name] = float(risk)
        if risk > 0.3:
            report.high_risk_dimensions.append(dim_name)

    # Overall risk classification
    max_risk = max(report.absorption_risk.values()) if report.absorption_risk else 0
    n_high = len(report.high_risk_dimensions)
    if max_risk >= 0.8 or n_high >= 3:
        report.overall_risk = "critical"
    elif max_risk >= 0.5 or n_high >= 2:
        report.overall_risk = "high"
    elif max_risk >= 0.3 or n_high >= 1:
        report.overall_risk = "moderate"
    else:
        report.overall_risk = "low"

    # Warnings based on risk level
    if report.overall_risk in ("critical", "high"):
        dims_str = ", ".join(report.high_risk_dimensions)
        report.warnings.append(
            f"{brand_name}: {report.overall_risk.upper()} absorption risk on "
            f"[{dims_str}]. R6 Theorem 4: once a dimension reaches the "
            "absorbing boundary, recovery is impossible. "
            "Prioritize reinforcement on these dimensions."
        )

    # Trajectory analysis if historical data available
    if historical_signals and len(historical_signals) >= 2:
        try:
            history = [to_signal_array(s) for s in historical_signals]
            # Check for monotonic decline toward boundary
            for i, dim_name in enumerate(DIMENSIONS):
                values = [h[i] for h in history] + [arr[i]]
                if len(values) >= 3:
                    diffs = np.diff(values)
                    if np.all(diffs < 0) and arr[i] < ABSORPTION_THRESHOLD * 1.5:
                        report.warnings.append(
                            f"{brand_name}: {dim_name} shows monotonic decline "
                            f"({values[0]:.1f} -> {arr[i]:.1f}). "
                            "Trajectory heading toward absorbing boundary."
                        )
        except (ValueError, IndexError):
            report.warnings.append("Historical data parsing failed")

    # Non-ergodicity reminder
    report.warnings.append(
        f"R6: Brand perception on S^7_+ is non-ergodic. "
        f"Time averages != ensemble averages. Brand health (ensemble) and "
        f"brand power (time average) are mathematically independent. "
        f"Mixing time lower bound: {report.mixing_time_bound:.1f} time units."
    )

    return report
