"""Tests for OST specification validator (R5)."""

import numpy as np
import pytest

from spectral_branding.validators.specification_validator import (
    N_LEVELS,
    N_SPEC_DIM,
    cascade_effective_dimensionality,
    fork_subspace_dimensions,
    specification_information_content,
    validate_activation_matrix,
)


class TestCascadeDimensionality:
    def test_no_coupling(self):
        assert cascade_effective_dimensionality(0.0) == 48.0

    def test_full_coupling(self):
        assert cascade_effective_dimensionality(1.0) == 8.0

    def test_moderate_coupling(self):
        d_eff = cascade_effective_dimensionality(0.5)
        assert 15.0 < d_eff < 16.5  # ~15.8

    def test_monotonic_decrease(self):
        prev = cascade_effective_dimensionality(0.0)
        for gamma in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
            curr = cascade_effective_dimensionality(gamma)
            assert curr <= prev + 1e-10
            prev = curr


class TestForkSubspace:
    def test_no_fork(self):
        shared, private = fork_subspace_dimensions(0)
        assert shared == 0
        assert private == 48

    def test_full_fork(self):
        shared, private = fork_subspace_dimensions(6)
        assert shared == 48
        assert private == 0

    def test_franchise_fork(self):
        # Share L0-L2 (purpose, values, strategy), fork L3-L5
        shared, private = fork_subspace_dimensions(3)
        assert shared == 24
        assert private == 24

    def test_sum_is_48(self):
        for k in range(N_LEVELS + 1):
            shared, private = fork_subspace_dimensions(k)
            assert shared + private == N_SPEC_DIM

    def test_invalid_level(self):
        with pytest.raises(ValueError):
            fork_subspace_dimensions(7)
        with pytest.raises(ValueError):
            fork_subspace_dimensions(-1)


class TestInformationContent:
    def test_full_spec(self):
        bits = specification_information_content(48, 0.1)
        assert 159.0 < bits < 160.0  # ~159.4

    def test_reduced_spec(self):
        bits = specification_information_content(16, 0.1)
        assert bits < 159.4

    def test_zero_resolution(self):
        assert specification_information_content(48, 0.0) == 0.0

    def test_one_resolution(self):
        assert specification_information_content(48, 1.0) == 0.0


class TestActivationMatrixValidation:
    def test_valid_array_matrix(self):
        matrix = np.random.rand(8, 6)
        report = validate_activation_matrix(matrix, cascade_gamma=0.5)
        assert report.valid
        assert report.effective_dimensionality < 48

    def test_valid_dict_matrix(self):
        matrix = {
            "purpose": {"semiotic": 0.8, "narrative": 0.7},
            "values": {"ideological": 0.9},
        }
        report = validate_activation_matrix(matrix)
        assert report.valid

    def test_out_of_range_fails(self):
        matrix = np.ones((8, 6)) * 1.5
        report = validate_activation_matrix(matrix)
        assert not report.valid
        assert any("outside [0,1]" in e for e in report.errors)

    def test_coverage_warning(self):
        matrix = np.random.rand(8, 6)
        report = validate_activation_matrix(matrix)
        assert any("R5 Theorem 1" in w for w in report.warnings)

    def test_cascade_warning(self):
        matrix = np.random.rand(8, 6)
        report = validate_activation_matrix(matrix, cascade_gamma=0.5)
        assert any("R5 Theorem 2" in w for w in report.warnings)

    def test_fork_warning(self):
        matrix = np.random.rand(8, 6)
        report = validate_activation_matrix(matrix, fork_at=3)
        assert any("R5 Theorem 3" in w for w in report.warnings)
        assert report.shared_dims == 24
        assert report.private_dims == 24

    def test_sparsity_warning(self):
        matrix = np.zeros((8, 6))
        matrix[0, 0] = 0.5  # only 1/48 specified
        report = validate_activation_matrix(matrix)
        assert any("sparse" in w for w in report.warnings)

    def test_transposed_matrix(self):
        matrix = np.random.rand(6, 8)  # 6x8 instead of 8x6
        report = validate_activation_matrix(matrix)
        assert report.valid  # should auto-transpose

    def test_wrong_shape_fails(self):
        matrix = np.random.rand(5, 5)
        report = validate_activation_matrix(matrix)
        assert not report.valid

    def test_cascade_consistency_check(self):
        # Create matrix with high deviation between adjacent levels
        matrix = np.zeros((8, 6))
        matrix[:, 0] = 0.9  # L0 all high
        matrix[:, 1] = 0.1  # L1 all low (inconsistent with high gamma)
        report = validate_activation_matrix(matrix, cascade_gamma=0.8)
        assert any("Cascade inconsistency" in w for w in report.warnings)

    def test_cognitive_load_warning(self):
        matrix = np.random.rand(8, 6)
        report = validate_activation_matrix(matrix, cascade_gamma=0.0)
        assert any("Cognitive load" in w for w in report.warnings)
