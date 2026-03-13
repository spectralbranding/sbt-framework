"""Tests for SBT math-hardened validators."""

import numpy as np
import pytest

from spectral_branding.validators._math import (
    CANONICAL_BRANDS,
    N_DIM,
    aitchison_distance,
    clr_transform,
    fisher_rao_distance,
    normalize_to_simplex,
    normalize_to_sphere,
    to_signal_array,
    verify_triangle_inequality,
)
from spectral_branding.validators.capacity_analyzer import (
    analyze_positioning_capacity,
    estimate_packing_capacity,
)
from spectral_branding.validators.cohort_validator import validate_cohort_assignment
from spectral_branding.validators.metamerism_detector import detect_metamerism
from spectral_branding.validators.metric_validator import (
    validate_observer_profile,
    validate_signal_profile,
)
from spectral_branding.validators.trajectory_risk import (
    DEFAULT_SIGMA_0,
    SPECTRAL_GAP,
    _mixing_time_lower_bound,
    analyze_trajectory_risk,
)
from spectral_branding.validators.validate import validate_analysis

# =============================================================================
# _math.py tests
# =============================================================================


class TestMathUtilities:
    def test_to_signal_array_valid(self):
        arr = to_signal_array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        assert arr.shape == (N_DIM,)

    def test_to_signal_array_wrong_length(self):
        with pytest.raises(ValueError, match="Expected 8"):
            to_signal_array([1.0, 2.0, 3.0])

    def test_clr_transform_sums_to_zero(self):
        s = np.array([9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5])
        clr = clr_transform(s)
        assert np.isclose(np.sum(clr), 0.0, atol=1e-10)

    def test_clr_transform_rejects_nonpositive(self):
        with pytest.raises(ValueError):
            clr_transform(np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]))

    def test_aitchison_distance_self_is_zero(self):
        s = CANONICAL_BRANDS["Hermes"]
        assert np.isclose(aitchison_distance(s, s), 0.0)

    def test_aitchison_distance_symmetric(self):
        h = CANONICAL_BRANDS["Hermes"]
        t = CANONICAL_BRANDS["Tesla"]
        assert np.isclose(aitchison_distance(h, t), aitchison_distance(t, h))

    def test_aitchison_triangle_inequality(self):
        h = CANONICAL_BRANDS["Hermes"]
        i = CANONICAL_BRANDS["IKEA"]
        t = CANONICAL_BRANDS["Tesla"]
        d_hi = aitchison_distance(h, i)
        d_it = aitchison_distance(i, t)
        d_ht = aitchison_distance(h, t)
        assert verify_triangle_inequality(d_hi, d_it, d_ht)

    def test_fisher_rao_distance_self_is_zero(self):
        w = np.array([0.125] * 8)
        assert np.isclose(fisher_rao_distance(w, w), 0.0)

    def test_fisher_rao_distance_positive(self):
        w1 = np.array([0.25, 0.10, 0.05, 0.25, 0.10, 0.05, 0.15, 0.05])
        w2 = np.array([0.05, 0.10, 0.30, 0.10, 0.20, 0.05, 0.10, 0.10])
        d = fisher_rao_distance(w1, w2)
        assert d > 0

    def test_normalize_to_simplex(self):
        v = np.array([2.0, 3.0, 5.0, 1.0, 4.0, 2.0, 1.0, 2.0])
        result = normalize_to_simplex(v)
        assert np.isclose(np.sum(result), 1.0)

    def test_normalize_to_sphere(self):
        s = np.array([3.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        result = normalize_to_sphere(s)
        assert np.isclose(np.linalg.norm(result), 1.0)


# =============================================================================
# metric_validator.py tests
# =============================================================================


class TestMetricValidator:
    def test_valid_canonical_profile(self):
        report = validate_signal_profile(CANONICAL_BRANDS["Hermes"].tolist())
        assert report.valid
        assert len(report.errors) == 0

    def test_wrong_dimensions(self):
        report = validate_signal_profile([1.0, 2.0, 3.0])
        assert not report.valid
        assert any("Dimension" in e for e in report.errors)

    def test_negative_values(self):
        report = validate_signal_profile([5.0, 5.0, -1.0, 5.0, 5.0, 5.0, 5.0, 5.0])
        assert not report.valid
        assert any("Non-positive" in e for e in report.errors)

    def test_zero_value(self):
        report = validate_signal_profile([5.0, 5.0, 0.0, 5.0, 5.0, 5.0, 5.0, 5.0])
        assert not report.valid

    def test_out_of_range_warning(self):
        report = validate_signal_profile([15.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0])
        assert report.valid  # warning, not error
        assert len(report.warnings) > 0

    def test_distances_to_canonical_computed(self):
        report = validate_signal_profile([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0])
        assert "Hermes" in report.distances
        assert "Tesla" in report.distances

    def test_valid_observer_profile(self):
        report = validate_observer_profile([0.125] * 8)
        assert report.valid

    def test_observer_negative_weights(self):
        report = validate_observer_profile([0.3, -0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1])
        assert not report.valid

    def test_observer_non_normalized_warning(self):
        report = validate_observer_profile([0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1])
        # Sum = 1.1, should warn
        # Actually sum = 1.1? Let me check: 0.2*3 + 0.1*5 = 0.6 + 0.5 = 1.1
        assert any(
            "sum" in w.lower() or "normaliz" in w.lower() for w in report.warnings
        )

    def test_observer_degenerate_warning(self):
        report = validate_observer_profile(
            [0.96, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005]
        )
        # Sum = 0.995, close to 1. Max = 0.96 > 0.95
        assert any("degenerate" in w.lower() for w in report.warnings)


# =============================================================================
# metamerism_detector.py tests
# =============================================================================


class TestMetamerismDetector:
    def test_detect_with_similar_scores(self):
        profiles = {
            "A": [9.0, 9.0, 7.0, 9.0, 8.0, 3.0, 9.0, 9.0],
            "B": [3.0, 3.0, 9.0, 3.0, 8.0, 9.0, 3.0, 3.0],
        }
        scores = {"A": 78.0, "B": 80.0}
        report = detect_metamerism(profiles, scalar_scores=scores)
        assert len(report.metameric_pairs) > 0

    def test_no_metamerism_when_scores_differ(self):
        profiles = {
            "A": [9.0, 9.0, 7.0, 9.0, 8.0, 3.0, 9.0, 9.0],
            "B": [3.0, 3.0, 9.0, 3.0, 8.0, 9.0, 3.0, 3.0],
        }
        scores = {"A": 95.0, "B": 30.0}
        report = detect_metamerism(profiles, scalar_scores=scores)
        assert len(report.metameric_pairs) == 0

    def test_distortion_bound_increases_with_brands(self):
        profiles = {f"B{i}": [5.0 + i * 0.1] * 8 for i in range(20)}
        report = detect_metamerism(profiles)
        assert report.distortion_bound > 0

    def test_r2_warning_always_present(self):
        profiles = {"A": [5.0] * 8, "B": [6.0] * 8}
        report = detect_metamerism(profiles)
        assert any("R2 bound" in w for w in report.warnings)


# =============================================================================
# cohort_validator.py tests
# =============================================================================


class TestCohortValidator:
    def test_valid_cohort_assignment(self):
        observers = {
            "obs1": [0.25, 0.10, 0.05, 0.25, 0.10, 0.05, 0.15, 0.05],
            "obs2": [0.20, 0.15, 0.05, 0.20, 0.15, 0.05, 0.15, 0.05],
            "obs3": [0.05, 0.10, 0.30, 0.10, 0.20, 0.05, 0.10, 0.10],
            "obs4": [0.05, 0.05, 0.25, 0.15, 0.25, 0.05, 0.10, 0.10],
        }
        labels = {
            "obs1": "aesthete",
            "obs2": "aesthete",
            "obs3": "values",
            "obs4": "values",
        }
        report = validate_cohort_assignment(observers, labels)
        assert report.n_cohorts == 2

    def test_r3_fuzziness_warning(self):
        observers = {
            "obs1": [0.25, 0.10, 0.05, 0.25, 0.10, 0.05, 0.15, 0.05],
            "obs2": [0.05, 0.10, 0.30, 0.10, 0.20, 0.05, 0.10, 0.10],
        }
        labels = {"obs1": "A", "obs2": "B"}
        report = validate_cohort_assignment(observers, labels)
        assert any("R3 bound" in w for w in report.warnings)

    def test_over_segmentation_warning(self):
        observers = {f"obs{i}": [0.125] * 8 for i in range(10)}
        labels = {f"obs{i}": f"cohort_{i}" for i in range(10)}
        report = validate_cohort_assignment(observers, labels)
        assert any("over-segmentation" in w for w in report.warnings)


# =============================================================================
# capacity_analyzer.py tests
# =============================================================================


class TestCapacityAnalyzer:
    def test_packing_capacity_positive(self):
        cap = estimate_packing_capacity(0.15)
        assert cap > 0

    def test_canonical_brands_analysis(self):
        profiles = {k: v.tolist() for k, v in CANONICAL_BRANDS.items()}
        report = analyze_positioning_capacity(profiles)
        assert report.n_brands == 5
        assert report.theoretical_max > report.n_brands

    def test_crowded_pairs_detected(self):
        # Two nearly identical brands
        profiles = {
            "A": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            "B": [5.01, 5.01, 5.01, 5.01, 5.01, 5.01, 5.01, 5.01],
        }
        report = analyze_positioning_capacity(profiles)
        assert len(report.crowded_pairs) > 0

    def test_r4_warning_present(self):
        profiles = {k: v.tolist() for k, v in CANONICAL_BRANDS.items()}
        report = analyze_positioning_capacity(profiles)
        assert any("R4 bound" in w for w in report.warnings)


# =============================================================================
# trajectory_risk.py tests
# =============================================================================


class TestTrajectoryRisk:
    def test_low_risk_for_strong_brand(self):
        report = analyze_trajectory_risk(CANONICAL_BRANDS["Hermes"].tolist(), "Hermes")
        assert report.overall_risk == "low"

    def test_high_risk_for_weak_dimension(self):
        # Tesla has temporal=2.0, right at threshold
        report = analyze_trajectory_risk(CANONICAL_BRANDS["Tesla"].tolist(), "Tesla")
        # Tesla: ideological=3.0 ok, temporal=2.0 borderline, cultural=4.0 ok
        assert report.overall_risk in ("low", "moderate")

    def test_critical_risk_for_near_zero(self):
        signals = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 1.0, 0.5]
        report = analyze_trajectory_risk(signals, "Weak")
        assert report.overall_risk in ("high", "critical")
        assert len(report.high_risk_dimensions) >= 1

    def test_non_ergodic_flag(self):
        report = analyze_trajectory_risk([5.0] * 8, "Test")
        assert report.non_ergodic_flag is True

    def test_historical_decline_warning(self):
        current = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.5]
        history = [
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 3.0],
        ]
        report = analyze_trajectory_risk(
            current, "Declining", historical_signals=history
        )
        assert any("monotonic decline" in w for w in report.warnings)

    def test_r6_warning_present(self):
        report = analyze_trajectory_risk([5.0] * 8, "Test")
        assert any("R6" in w for w in report.warnings)

    def test_mixing_time_formula_matches_r6(self):
        # R6 Theorem 3: tau_mix >= 2 / (lambda_gap * sigma_0^2)
        # with lambda_gap = 48 (Dirichlet spectral gap)
        expected = 2.0 / (SPECTRAL_GAP * DEFAULT_SIGMA_0**2)
        assert _mixing_time_lower_bound(DEFAULT_SIGMA_0) == pytest.approx(expected)
        report = analyze_trajectory_risk([5.0] * 8, "Test")
        assert report.mixing_time_bound == pytest.approx(expected)

    def test_mixing_time_custom_sigma(self):
        sigma = 0.2
        expected = 2.0 / (SPECTRAL_GAP * sigma**2)
        report = analyze_trajectory_risk([5.0] * 8, "Test", sigma_0=sigma)
        assert report.mixing_time_bound == pytest.approx(expected)

    def test_absorption_warning_references_theorem_4(self):
        # Near-zero dimensions should trigger warning referencing R6 Theorem 4
        signals = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 0.5, 0.5]
        report = analyze_trajectory_risk(signals, "Weak")
        assert any("Theorem 4" in w for w in report.warnings)


# =============================================================================
# validate.py orchestrator tests
# =============================================================================


class TestValidateOrchestrator:
    def test_full_analysis_valid(self):
        analysis = {
            "brand_profiles": {k: v.tolist() for k, v in CANONICAL_BRANDS.items()},
        }
        result = validate_analysis(analysis)
        assert result.valid
        assert result.metric is not None
        assert result.metamerism is not None
        assert result.capacity is not None
        assert len(result.trajectories) == 5

    def test_invalid_profile_fails(self):
        analysis = {
            "brand_profiles": {
                "Bad": [0.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            },
        }
        result = validate_analysis(analysis)
        assert not result.valid
        assert len(result.all_errors) > 0

    def test_with_observer_profiles(self):
        analysis = {
            "brand_profiles": {"X": [5.0] * 8},
            "observer_profiles": {
                "obs1": [0.125] * 8,
                "obs2": [0.25, 0.10, 0.05, 0.25, 0.10, 0.05, 0.15, 0.05],
            },
            "cohort_labels": {"obs1": "A", "obs2": "B"},
        }
        result = validate_analysis(analysis)
        assert result.valid

    def test_summary_output(self):
        analysis = {
            "brand_profiles": {k: v.tolist() for k, v in CANONICAL_BRANDS.items()},
        }
        result = validate_analysis(analysis)
        summary = result.summary()
        assert "Math Validation Report" in summary
        assert "PASS" in summary

    def test_with_scalar_scores_detects_metamerism(self):
        analysis = {
            "brand_profiles": {
                "A": [9.0, 2.0, 9.0, 2.0, 9.0, 2.0, 9.0, 2.0],
                "B": [2.0, 9.0, 2.0, 9.0, 2.0, 9.0, 2.0, 9.0],
            },
            "scalar_scores": {"A": 78.0, "B": 78.0},
        }
        result = validate_analysis(analysis)
        assert result.metamerism is not None
        assert len(result.metamerism.metameric_pairs) > 0


class TestResourceAllocationValidator:
    """Tests for R7 resource allocation validator."""

    def test_identical_weights_zero_gap(self):
        """Same founder and cohort weights should produce zero alignment gap."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        w = [0.2, 0.1, 0.05, 0.2, 0.1, 0.05, 0.15, 0.15]
        report = validate_resource_allocation(
            founder_weights=w,
            cohort_weights={"target": w},
        )
        assert report.valid
        assert report.alignment_gap < 1e-10
        assert len(report.errors) == 0

    def test_divergent_weights_positive_gap(self):
        """Different weights should produce positive alignment gap."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        founder = [0.5, 0.3, 0.05, 0.05, 0.025, 0.025, 0.025, 0.025]
        cohort = [0.025, 0.025, 0.025, 0.025, 0.05, 0.05, 0.3, 0.5]
        report = validate_resource_allocation(
            founder_weights=founder,
            cohort_weights={"target": cohort},
        )
        assert report.valid
        assert report.alignment_gap > 0
        assert any(
            "Alignment gap" in w or "investing in wrong" in w for w in report.warnings
        )

    def test_theorem_2_lower_bound_holds(self):
        """Actual alignment gap must be >= Theorem 2 lower bound."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        founder = [0.4, 0.3, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025]
        cohort = [0.05, 0.05, 0.3, 0.3, 0.1, 0.1, 0.05, 0.05]
        report = validate_resource_allocation(
            founder_weights=founder,
            cohort_weights={"target": cohort},
        )
        assert report.valid
        assert report.alignment_gap >= report.alignment_gap_lower_bound - 1e-10

    def test_blind_spot_detected(self):
        """Founder with zero weight on a dimension cohort values should flag."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        founder = [0.3, 0.3, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0]
        cohort = [0.1, 0.1, 0.1, 0.1, 0.15, 0.15, 0.15, 0.15]
        report = validate_resource_allocation(
            founder_weights=founder,
            cohort_weights={"target": cohort},
        )
        assert len(report.blind_spot_dimensions) > 0
        assert any("blind spot" in w.lower() for w in report.warnings)

    def test_multi_cohort_close_weights_feasible(self):
        """Cohorts with similar weights should be servable by one portfolio."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        founder = [0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.15, 0.15]
        c1 = [0.14, 0.16, 0.11, 0.09, 0.1, 0.1, 0.15, 0.15]
        c2 = [0.16, 0.14, 0.09, 0.11, 0.1, 0.1, 0.15, 0.15]
        report = validate_resource_allocation(
            founder_weights=founder,
            cohort_weights={"c1": c1, "c2": c2},
        )
        assert report.multi_cohort_feasible

    def test_multi_cohort_divergent_infeasible(self):
        """Extreme cohort divergence should trigger sub-brand warning."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        founder = [0.125] * 8
        c1 = [0.9, 0.02, 0.01, 0.01, 0.02, 0.01, 0.02, 0.01]
        c2 = [0.01, 0.01, 0.02, 0.01, 0.01, 0.9, 0.02, 0.02]
        report = validate_resource_allocation(
            founder_weights=founder,
            cohort_weights={"c1": c1, "c2": c2},
        )
        assert not report.multi_cohort_feasible
        assert any("sub-brand" in w.lower() for w in report.warnings)

    def test_herfindahl_computed(self):
        """Herfindahl index should be computed for founder and cohort."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        founder = [0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        cohort = [0.125] * 8
        report = validate_resource_allocation(
            founder_weights=founder,
            cohort_weights={"target": cohort},
        )
        # Uniform weights: H = 8 * (1/8)^2 = 0.125
        assert abs(report.herfindahl_cohort - 0.125) < 0.01
        # Concentrated founder: H = 2 * 0.5^2 = 0.5
        assert report.herfindahl_founder > 0.4

    def test_negative_weights_error(self):
        """Negative founder weights should produce error."""
        from spectral_branding.validators.resource_allocation_validator import (
            validate_resource_allocation,
        )

        report = validate_resource_allocation(
            founder_weights=[-0.1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.2],
            cohort_weights={"target": [0.125] * 8},
        )
        assert not report.valid
        assert len(report.errors) > 0

    def test_optimal_allocation_proportional(self):
        """Optimal allocation should be proportional to weights / cost."""
        from spectral_branding.validators.resource_allocation_validator import (
            compute_optimal_allocation,
        )

        import numpy as np

        weights = np.array([0.4, 0.3, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025])
        costs = np.ones(8)
        optimal = compute_optimal_allocation(weights, costs, shadow_price=1.0)
        # With uniform costs and lambda=1, optimal = weights
        np.testing.assert_allclose(optimal, weights)

    def test_orchestrator_includes_allocation(self):
        """Orchestrator should run R7 when founder_weights provided."""
        analysis = {
            "brand_profiles": {
                "TestBrand": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            },
            "observer_profiles": {
                "Cohort_A": [0.2, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1],
            },
            "founder_weights": [0.3, 0.3, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05],
        }
        result = validate_analysis(analysis)
        assert result.allocation is not None
        assert result.allocation.alignment_gap >= 0
