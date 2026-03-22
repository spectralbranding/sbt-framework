"""
Main orchestrator for SBT/OST math-hardened validation.

Runs all validators on an LLM-generated brand/organizational analysis
and produces a consolidated report with warnings, bounds, and flags.

SBT validators (R1-R4, R6-R7): brand profiles, observer profiles, cohorts, allocation
OST validators (R5): organizational activation matrices, cascade, forkability
"""

from dataclasses import dataclass, field
from typing import Any

from spectral_branding.validators.capacity_analyzer import (
    CapacityReport,
    analyze_positioning_capacity,
)
from spectral_branding.validators.cohort_validator import (
    CohortReport,
    validate_cohort_assignment,
)
from spectral_branding.validators.metamerism_detector import (
    MetamerismReport,
    detect_metamerism,
)
from spectral_branding.validators.metric_validator import (
    MetricReport,
    validate_observer_profile,
    validate_signal_profile,
)
from spectral_branding.validators.specification_validator import (
    SpecificationReport,
    validate_activation_matrix,
)
from spectral_branding.validators.resource_allocation_validator import (
    AllocationReport,
    validate_resource_allocation,
)
from spectral_branding.validators.trajectory_risk import (
    TrajectoryReport,
    VelocityReport,  # noqa: F401
    analyze_trajectory_risk,
    compute_velocity,  # noqa: F401
)


@dataclass
class ValidationResult:
    """Consolidated validation result from all validators."""

    valid: bool = True
    metric: MetricReport | None = None
    metamerism: MetamerismReport | None = None
    cohort: CohortReport | None = None
    capacity: CapacityReport | None = None
    specification: SpecificationReport | None = None
    allocation: AllocationReport | None = None
    trajectories: dict[str, TrajectoryReport] = field(default_factory=dict)
    all_warnings: list[str] = field(default_factory=list)
    all_errors: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """Human-readable validation summary."""
        lines = ["=== SBT/OST Math Validation Report ==="]

        if self.all_errors:
            lines.append(f"\nERRORS ({len(self.all_errors)}):")
            for e in self.all_errors:
                lines.append(f"  [!] {e}")

        if self.all_warnings:
            lines.append(f"\nWARNINGS ({len(self.all_warnings)}):")
            for w in self.all_warnings:
                lines.append(f"  [~] {w}")

        if self.metric and self.metric.distances:
            lines.append("\nDistances to canonical brands:")
            for name, d in sorted(self.metric.distances.items(), key=lambda x: x[1]):
                lines.append(f"  {name}: {d:.4f}")

        if self.capacity:
            lines.append(
                f"\nPositioning capacity: {self.capacity.n_brands}"
                f"/{self.capacity.theoretical_max} "
                f"({self.capacity.utilization:.1%})"
            )

        if self.allocation:
            lines.append(
                f"\nAlignment gap: {self.allocation.alignment_gap:.4f}"
                f" (efficiency loss: {self.allocation.efficiency_loss:.4f})"
            )
            if self.allocation.blind_spot_dimensions:
                lines.append(
                    f"  Blind spots: {', '.join(self.allocation.blind_spot_dimensions)}"
                )
            if not self.allocation.multi_cohort_feasible:
                lines.append("  Multi-cohort: INFEASIBLE (consider sub-brands)")

        for tname, treport in self.trajectories.items():
            if treport.velocity_report is not None:
                vr = treport.velocity_report
                pct = int(vr.confidence_level * 100)
                lines.append(f"\nVelocity ({tname}):")
                for dim in vr.velocity:
                    vel = vr.velocity[dim]
                    dirn = vr.direction[dim]
                    pta = vr.periods_to_absorption.get(dim)
                    line = f"  {dim}: {vel:+.2f}/{vr.period_label} ({dirn})"
                    # Conformal bands (present when n_snapshots >= 4)
                    if dim in vr.velocity_lower and dim in vr.velocity_upper:
                        lo = vr.velocity_lower[dim]
                        hi = vr.velocity_upper[dim]
                        line += f" [{pct}% CI: {lo:+.2f} to {hi:+.2f}]"
                    ar = vr.absorption_range.get(dim)
                    if ar is not None:
                        opt, pess = ar
                        line += (
                            f" — absorption in ~{opt:.1f}-{pess:.1f}"
                            f" {vr.period_label}s"
                        )
                    elif pta is not None:
                        line += f" — absorption in ~{pta:.1f} {vr.period_label}s"
                    lines.append(line)

        if self.specification:
            lines.append(
                f"\nSpecification: {self.specification.n_specified}"
                f"/{self.specification.n_total} dimensions specified, "
                f"d_eff={self.specification.effective_dimensionality:.1f}"
            )

        status = "PASS" if self.valid else "FAIL"
        lines.append(f"\nOverall: {status}")
        return "\n".join(lines)


def validate_analysis(analysis: dict[str, Any]) -> ValidationResult:
    """
    Validate an LLM-generated brand analysis against mathematical bounds.

    Expected analysis dict structure:
    {
        "brand_profiles": {
            "BrandName": [s1, s2, ..., s8],
            ...
        },
        "observer_profiles": {  # optional
            "ObserverName": [w1, w2, ..., w8],
            ...
        },
        "cohort_labels": {  # optional
            "ObserverName": "cohort_label",
            ...
        },
        "scalar_scores": {  # optional
            "BrandName": score,
            ...
        },
        "activation_matrix": ...,  # optional, 8x6 OST matrix
        "cascade_gamma": 0.5,  # optional, cascade coupling
        "fork_level": 3,  # optional, fork at level k
        "founder_weights": [w1, ..., w8],  # optional, R7 allocation
        "cost_params": [a1, ..., a8],  # optional, R7 cost parameters
        "historical_brand_profiles": {  # optional, R6 velocity tracking
            "BrandName": [[s1, ..., s8], [s1, ..., s8]],  # oldest to newest
        },
    }
    """
    result = ValidationResult()

    brand_profiles = analysis.get("brand_profiles", {})
    observer_profiles = analysis.get("observer_profiles", {})
    cohort_labels = analysis.get("cohort_labels", {})
    scalar_scores = analysis.get("scalar_scores", {})
    historical_brand_profiles = analysis.get("historical_brand_profiles", {})

    # 1. Metric validation (R1) -- validate each brand profile
    if brand_profiles:
        # Validate the first profile in detail (for single-brand analysis)
        first_name = next(iter(brand_profiles))
        result.metric = validate_signal_profile(brand_profiles[first_name])
        if not result.metric.valid:
            result.valid = False
            result.all_errors.extend(result.metric.errors)
        result.all_warnings.extend(result.metric.warnings)

        # Validate remaining profiles
        for name, profile in list(brand_profiles.items())[1:]:
            metric_report = validate_signal_profile(profile)
            if not metric_report.valid:
                result.valid = False
                result.all_errors.extend([f"{name}: {e}" for e in metric_report.errors])
            result.all_warnings.extend([f"{name}: {w}" for w in metric_report.warnings])

    # 2. Metamerism detection (R2)
    if len(brand_profiles) >= 2:
        result.metamerism = detect_metamerism(
            brand_profiles,
            scalar_scores=scalar_scores if scalar_scores else None,
        )
        result.all_warnings.extend(result.metamerism.warnings)

    # 3. Cohort validation (R3)
    if observer_profiles and cohort_labels:
        result.cohort = validate_cohort_assignment(observer_profiles, cohort_labels)
        if not result.cohort.valid:
            result.valid = False
            result.all_errors.extend(result.cohort.errors)
        result.all_warnings.extend(result.cohort.warnings)

    # 4. Capacity analysis (R4)
    if len(brand_profiles) >= 2:
        result.capacity = analyze_positioning_capacity(brand_profiles)
        result.all_warnings.extend(result.capacity.warnings)

    # 5. Trajectory risk (R6) -- per brand
    for name, profile in brand_profiles.items():
        history = historical_brand_profiles.get(name)
        traj_report = analyze_trajectory_risk(
            profile, brand_name=name, historical_signals=history
        )
        result.trajectories[name] = traj_report
        if traj_report.overall_risk in ("critical", "high"):
            result.all_warnings.extend(traj_report.warnings)
        # Only include non-ergodicity reminder once
        if name == next(iter(brand_profiles)):
            # Add the non-ergodic flag warning (last warning in the list)
            for w in traj_report.warnings:
                if w.startswith("R6: Brand perception"):
                    result.all_warnings.append(w)
                    break

    # 6. Specification validation (R5) -- OST activation matrix
    activation_matrix = analysis.get("activation_matrix")
    if activation_matrix is not None:
        cascade_gamma = analysis.get("cascade_gamma", 0.0)
        fork_level = analysis.get("fork_level")
        result.specification = validate_activation_matrix(
            activation_matrix,
            cascade_gamma=cascade_gamma,
            fork_at=fork_level,
        )
        if not result.specification.valid:
            result.valid = False
            result.all_errors.extend(result.specification.errors)
        result.all_warnings.extend(result.specification.warnings)

    # 7. Resource allocation validation (R7)
    founder_weights = analysis.get("founder_weights")
    if founder_weights is not None and observer_profiles:
        result.allocation = validate_resource_allocation(
            founder_weights=founder_weights,
            cohort_weights=observer_profiles,
            proposed_allocation=analysis.get("proposed_allocation"),
            cost_params=analysis.get("cost_params"),
        )
        if not result.allocation.valid:
            result.valid = False
            result.all_errors.extend(result.allocation.errors)
        result.all_warnings.extend(result.allocation.warnings)

    # Validate observer profiles (R1) if present
    for name, weights in observer_profiles.items():
        obs_report = validate_observer_profile(weights)
        if not obs_report.valid:
            result.all_errors.extend(
                [f"Observer {name}: {e}" for e in obs_report.errors]
            )
        result.all_warnings.extend(
            [f"Observer {name}: {w}" for w in obs_report.warnings]
        )

    return result
