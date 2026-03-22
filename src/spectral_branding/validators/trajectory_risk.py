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


# Velocity thresholds
# Per-period change below this (absolute value) is classified as "stable".
# On a 1-10 signal scale, 0.5 per period is ~5% shift.
VELOCITY_STABLE_THRESHOLD = 0.5


@dataclass
class VelocityReport:
    """Per-dimension velocity analysis for a brand profile.

    Operationalizes the discrete approximation to the continuous-time
    drift vector mu(X_t, t) defined in R6 Section 4.3.
    """

    velocity: dict[str, float] = field(default_factory=dict)
    direction: dict[str, str] = field(default_factory=dict)
    acceleration: dict[str, float | None] = field(default_factory=dict)
    periods_to_absorption: dict[str, float | None] = field(default_factory=dict)
    n_snapshots: int = 0
    period_label: str = "period"
    confidence_level: float = 0.90
    velocity_lower: dict[str, float] = field(
        default_factory=dict
    )  # lower conformal bound
    velocity_upper: dict[str, float] = field(
        default_factory=dict
    )  # upper conformal bound
    absorption_range: dict[str, tuple[float, float] | None] = field(
        default_factory=dict
    )  # (optimistic, pessimistic) periods


def _conformal_quantile(residuals: np.ndarray, alpha: float = 0.10) -> float:
    """Compute conformal prediction quantile from calibration residuals.

    Split conformal prediction (Vovk et al., 2005): distribution-free
    coverage guarantee P(true in interval) >= 1 - alpha.
    """
    n = len(residuals)
    scores = np.abs(residuals)
    level = min(np.ceil((1 - alpha) * (n + 1)) / n, 1.0)
    return float(np.quantile(scores, level))


def compute_velocity(
    current_signals: list[float] | np.ndarray,
    historical_signals: list[list[float] | np.ndarray],
    period_label: str = "period",
    confidence_level: float = 0.90,
) -> VelocityReport:
    """
    Compute per-dimension velocity from a time series of signal profiles.

    Parameters
    ----------
    current_signals : array-like
        Current 8D signal profile (most recent snapshot).
    historical_signals : list
        Previous signal profiles ordered oldest-to-newest.
        At least 1 historical snapshot required.
    period_label : str
        Label for the time unit (e.g. "quarter", "month", "year").
    confidence_level : float
        Nominal coverage for conformal prediction intervals (default 0.90).
        Requires n_snapshots >= 4 to produce bands.

    Returns
    -------
    VelocityReport
        Per-dimension velocity (signed rate of change per period),
        direction labels, acceleration (if 3+ snapshots),
        linear time-to-absorption estimates, and conformal prediction
        bands (if n_snapshots >= 4).
    """
    current = to_signal_array(current_signals)
    history = [to_signal_array(s) for s in historical_signals]
    all_snapshots = history + [current]
    n = len(all_snapshots)

    alpha = 1.0 - confidence_level
    report = VelocityReport(
        n_snapshots=n,
        period_label=period_label,
        confidence_level=confidence_level,
    )

    for i, dim_name in enumerate(DIMENSIONS):
        values = [snap[i] for snap in all_snapshots]
        diffs = np.diff(values)

        # Velocity: mean rate of change per period
        v = float(np.mean(diffs))
        report.velocity[dim_name] = v

        # Direction classification
        if abs(v) < VELOCITY_STABLE_THRESHOLD:
            report.direction[dim_name] = "stable"
        elif v > 0:
            report.direction[dim_name] = "rising"
        else:
            report.direction[dim_name] = "falling"

        # Acceleration: requires 3+ snapshots (2+ diffs)
        if len(diffs) >= 2:
            # Change in velocity between consecutive intervals
            accel = float(diffs[-1] - diffs[0]) / (len(diffs) - 1)
            report.acceleration[dim_name] = accel
        else:
            report.acceleration[dim_name] = None

        # Time-to-absorption estimate (linear extrapolation)
        if v < -VELOCITY_STABLE_THRESHOLD and current[i] > ABSORPTION_THRESHOLD:
            periods = (current[i] - ABSORPTION_THRESHOLD) / abs(v)
            report.periods_to_absorption[dim_name] = float(periods)
        else:
            report.periods_to_absorption[dim_name] = None

        # Conformal prediction bands — require n >= 4 (at least 3 residuals)
        # diffs has length n-1; running means need at least 2 diffs to produce
        # a residual (first running mean uses 1 diff, residual from 2nd onward).
        # With n >= 4 we have len(diffs) >= 3 and can form >= 2 residuals.
        if n >= 4:
            # Residuals: diff_k minus running mean of diffs up to step k
            residuals = []
            for k in range(1, len(diffs)):
                running_mean = float(np.mean(diffs[:k]))
                residuals.append(diffs[k] - running_mean)
            residuals_arr = np.array(residuals)
            q = _conformal_quantile(residuals_arr, alpha=alpha)
            report.velocity_lower[dim_name] = v - q
            report.velocity_upper[dim_name] = v + q

            # Absorption range: only when even optimistic bound is declining
            if report.velocity_upper[dim_name] < -VELOCITY_STABLE_THRESHOLD:
                v_lower = report.velocity_lower[dim_name]
                v_upper = report.velocity_upper[dim_name]
                cur_val = float(current[i])
                if cur_val > ABSORPTION_THRESHOLD:
                    pessimistic = (cur_val - ABSORPTION_THRESHOLD) / abs(v_lower)
                    optimistic = (cur_val - ABSORPTION_THRESHOLD) / abs(v_upper)
                    report.absorption_range[dim_name] = (
                        float(optimistic),
                        float(pessimistic),
                    )
                else:
                    report.absorption_range[dim_name] = None
            else:
                report.absorption_range[dim_name] = None

    return report


@dataclass
class TrajectoryReport:
    """Report on trajectory risk for a brand profile."""

    absorption_risk: dict[str, float] = field(default_factory=dict)
    high_risk_dimensions: list[str] = field(default_factory=list)
    overall_risk: str = "low"  # low, moderate, high, critical
    mixing_time_bound: float = MIXING_TIME_LOWER_BOUND
    warnings: list[str] = field(default_factory=list)
    non_ergodic_flag: bool = True  # always true for SBT (R6 Theorem 1)
    velocity_report: VelocityReport | None = None


def analyze_trajectory_risk(
    signals: list[float] | np.ndarray,
    brand_name: str = "brand",
    historical_signals: list[list[float] | np.ndarray] | None = None,
    sigma_0: float = DEFAULT_SIGMA_0,
    period_label: str = "period",
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
    if historical_signals and len(historical_signals) >= 1:
        try:
            history = [to_signal_array(s) for s in historical_signals]

            # Compute per-dimension velocity
            report.velocity_report = compute_velocity(
                arr, historical_signals, period_label=period_label
            )

            # Check for monotonic decline toward boundary (requires 3+ points)
            if len(historical_signals) >= 2:
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

            # Add velocity warnings for dimensions approaching absorption
            vr = report.velocity_report
            for dim_name in DIMENSIONS:
                pta = vr.periods_to_absorption.get(dim_name)
                if pta is not None and pta < 5.0:
                    report.warnings.append(
                        f"{brand_name}: {dim_name} declining at "
                        f"{vr.velocity[dim_name]:+.2f}/{vr.period_label}. "
                        f"Linear estimate: ~{pta:.1f} {vr.period_label}s "
                        f"to absorbing boundary. "
                        f"(R6: actual absorption is stochastic; "
                        f"this assumes constant velocity.)"
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
