"""
Specification Validator (R5: Specification Impossibility, Zharnikov 2026h).

Validates organizational specifications against the geometric impossibility
bounds proven in R5. Applies to OrgSchema Theory's 8x6 activation matrix
(48-dimensional specification space).

Key R5 results enforced:
- Coverage impossibility: 10^48 distinguishable specs at epsilon=0.1
- Cascade dimensionality reduction: d_eff = 8(1-(1-gamma)^6)/gamma
- Forkability subspace decomposition: shared + private = 48 dimensions
- Cognitive load: 159.4 bits exceeds working memory (~7 chunks)
"""

from dataclasses import dataclass, field

import numpy as np

from spectral_branding.validators._math import (
    DIMENSIONS,
    N_DIM,
    unit_ball_volume,
)

# OST cascade levels
OST_LEVELS = ["purpose", "values", "strategy", "structure", "process", "artifacts"]
N_LEVELS = 6
N_SPEC_DIM = N_DIM * N_LEVELS  # 48

# R5 constants
SPEC_RESOLUTION = 0.1  # epsilon per dimension
DISTINGUISHABLE_SPECS = 10**48  # at epsilon=0.1
BALL_VOLUME_48D = unit_ball_volume(N_SPEC_DIM) * SPEC_RESOLUTION**N_SPEC_DIM
COGNITIVE_BITS = 159.4  # bits for full 48D specification at resolution 0.1
WORKING_MEMORY_CHUNKS = 7  # Miller's law


@dataclass
class SpecificationReport:
    """Validation report for organizational specification."""

    valid: bool = True
    n_specified: int = 0
    n_total: int = N_SPEC_DIM
    coverage_fraction: float = 0.0
    effective_dimensionality: float = 0.0
    cascade_coupling: float = 0.0
    fork_level: int | None = None
    shared_dims: int = 0
    private_dims: int = 0
    cognitive_load_bits: float = 0.0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def cascade_effective_dimensionality(gamma: float) -> float:
    """
    Compute effective dimensionality under cascade coupling.

    d_eff = 8 * (1 - (1-gamma)^6) / gamma  for gamma > 0
    d_eff = 48  for gamma = 0 (no coupling)

    From R5 Theorem 2.
    """
    if gamma <= 0:
        return float(N_SPEC_DIM)
    if gamma >= 1.0:
        return float(N_DIM)  # fully determined by L0
    return N_DIM * (1.0 - (1.0 - gamma) ** N_LEVELS) / gamma


def fork_subspace_dimensions(fork_level: int) -> tuple[int, int]:
    """
    Compute shared and private subspace dimensions for a fork at given level.

    Fork at level k means sharing L0 through L(k-1), diverging on Lk through L5.

    From R5 Theorem 3.
    """
    if fork_level < 0 or fork_level > N_LEVELS:
        raise ValueError(f"Fork level must be 0-{N_LEVELS}, got {fork_level}")
    shared = N_DIM * fork_level
    private = N_DIM * (N_LEVELS - fork_level)
    return shared, private


def specification_information_content(
    n_dims: int = N_SPEC_DIM, resolution: float = SPEC_RESOLUTION
) -> float:
    """
    Information content of a specification in bits.

    I = n * log2(1/epsilon)

    At n=48, epsilon=0.1: I = 48 * log2(10) = 159.4 bits.
    """
    if resolution <= 0 or resolution >= 1:
        return 0.0
    return n_dims * np.log2(1.0 / resolution)


def validate_activation_matrix(
    matrix: dict[str, dict[str, float]] | list[list[float]] | np.ndarray,
    cascade_gamma: float = 0.0,
    fork_at: int | None = None,
) -> SpecificationReport:
    """
    Validate an organizational activation matrix against R5 bounds.

    Parameters
    ----------
    matrix : dict or array
        8x6 activation matrix. If dict: {level_name: {dimension_name: value}}.
        If array: 8x6 or 6x8 numpy array or nested list.
    cascade_gamma : float
        Cascade coupling strength (0=none, 1=full). Default 0.
    fork_at : int, optional
        Fork level (0=fork everything, 3=share L0-L2, 6=share all).
    """
    report = SpecificationReport()
    report.cascade_coupling = cascade_gamma

    # Parse matrix into 8x6 numpy array
    arr = _parse_matrix(matrix, report)
    if arr is None:
        return report

    # Count specified dimensions (non-zero values)
    report.n_specified = int(np.count_nonzero(arr))
    report.n_total = N_SPEC_DIM

    # Validate value range [0, 1]
    if np.any(arr < 0) or np.any(arr > 1):
        out_of_range = []
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                if arr[i, j] < 0 or arr[i, j] > 1:
                    dim = DIMENSIONS[i] if i < len(DIMENSIONS) else f"dim{i}"
                    level = OST_LEVELS[j] if j < len(OST_LEVELS) else f"L{j}"
                    out_of_range.append((dim, level, float(arr[i, j])))
        report.errors.append(
            f"Values outside [0,1] range: {out_of_range}. "
            "Activation matrix values must be normalized."
        )
        report.valid = False

    # Coverage impossibility (R5 Theorem 1)
    report.coverage_fraction = float(BALL_VOLUME_48D)
    report.warnings.append(
        f"R5 Theorem 1: A single specification at resolution {SPEC_RESOLUTION} "
        f"covers {BALL_VOLUME_48D:.2e} of the {N_SPEC_DIM}D space. "
        f"Exhaustive specification requires ~{DISTINGUISHABLE_SPECS:.0e} configs."
    )

    # Effective dimensionality (R5 Theorem 2)
    report.effective_dimensionality = cascade_effective_dimensionality(cascade_gamma)
    if cascade_gamma > 0:
        reduction_pct = (1.0 - report.effective_dimensionality / N_SPEC_DIM) * 100
        report.warnings.append(
            f"R5 Theorem 2: Cascade coupling gamma={cascade_gamma:.2f} reduces "
            f"effective dimensionality from {N_SPEC_DIM} to "
            f"{report.effective_dimensionality:.1f} ({reduction_pct:.0f}% reduction)."
        )
    else:
        report.warnings.append(
            "No cascade coupling specified (gamma=0). "
            "All 48 dimensions are free. Consider cascade constraints "
            "to reduce specification complexity."
        )

    # Forkability (R5 Theorem 3)
    if fork_at is not None:
        try:
            shared, private = fork_subspace_dimensions(fork_at)
            report.fork_level = fork_at
            report.shared_dims = shared
            report.private_dims = private
            report.warnings.append(
                f"R5 Theorem 3: Fork at L{fork_at} decomposes "
                f"{N_SPEC_DIM}D space into {shared}D shared + "
                f"{private}D private subspace."
            )
        except ValueError as e:
            report.errors.append(str(e))
            report.valid = False

    # Cognitive load
    report.cognitive_load_bits = specification_information_content(
        int(report.effective_dimensionality)
    )
    if report.cognitive_load_bits > WORKING_MEMORY_CHUNKS * np.log2(10):
        report.warnings.append(
            f"Cognitive load: {report.cognitive_load_bits:.1f} bits exceeds "
            f"human working memory (~{WORKING_MEMORY_CHUNKS} chunks = "
            f"~{WORKING_MEMORY_CHUNKS * np.log2(10):.1f} bits). "
            "Cascade constraints or AI assistance recommended."
        )

    # Cascade consistency check
    if cascade_gamma > 0 and arr is not None:
        _check_cascade_consistency(arr, cascade_gamma, report)

    # Sparsity check
    sparsity = 1.0 - (report.n_specified / report.n_total)
    if sparsity > 0.5:
        report.warnings.append(
            f"Specification is {sparsity:.0%} sparse ({report.n_specified}/{report.n_total} "
            f"dimensions specified). Unspecified dimensions default to organizational "
            "interpretation, increasing fork divergence."
        )

    return report


def _parse_matrix(
    matrix: dict[str, dict[str, float]] | list[list[float]] | np.ndarray,
    report: SpecificationReport,
) -> np.ndarray | None:
    """Parse various matrix formats into 8x6 numpy array."""
    if isinstance(matrix, np.ndarray):
        if matrix.shape == (N_DIM, N_LEVELS):
            return matrix
        elif matrix.shape == (N_LEVELS, N_DIM):
            return matrix.T
        else:
            report.errors.append(
                f"Matrix shape {matrix.shape} invalid. Expected ({N_DIM},{N_LEVELS})."
            )
            report.valid = False
            return None

    if isinstance(matrix, dict):
        arr = np.zeros((N_DIM, N_LEVELS))
        for j, level in enumerate(OST_LEVELS):
            if level in matrix:
                for i, dim in enumerate(DIMENSIONS):
                    if dim in matrix[level]:
                        arr[i, j] = matrix[level][dim]
        return arr

    if isinstance(matrix, list):
        try:
            arr = np.array(matrix, dtype=np.float64)
            if arr.shape == (N_DIM, N_LEVELS):
                return arr
            elif arr.shape == (N_LEVELS, N_DIM):
                return arr.T
            else:
                report.errors.append(
                    f"Matrix shape {arr.shape} invalid. Expected ({N_DIM},{N_LEVELS})."
                )
                report.valid = False
                return None
        except (ValueError, TypeError):
            report.errors.append("Cannot parse matrix from list.")
            report.valid = False
            return None

    report.errors.append(f"Unsupported matrix type: {type(matrix)}")
    report.valid = False
    return None


def _check_cascade_consistency(
    arr: np.ndarray, gamma: float, report: SpecificationReport
) -> None:
    """Check if level-to-level values are consistent with cascade coupling."""
    for j in range(N_LEVELS - 1):
        col_current = arr[:, j]
        col_next = arr[:, j + 1]

        # Skip if either level is unspecified
        if np.all(col_current == 0) or np.all(col_next == 0):
            continue

        # Expected: col_next should be constrained by col_current
        # High gamma means col_next should be similar to col_current
        if gamma > 0.5:
            deviation = np.linalg.norm(col_current - col_next) / np.sqrt(N_DIM)
            max_expected_deviation = 1.0 - gamma
            if deviation > max_expected_deviation * 2:
                level_curr = OST_LEVELS[j]
                level_next = OST_LEVELS[j + 1]
                report.warnings.append(
                    f"Cascade inconsistency: {level_curr} -> {level_next} "
                    f"deviation ({deviation:.2f}) exceeds expected "
                    f"max ({max_expected_deviation:.2f}) at gamma={gamma:.2f}. "
                    "Values may violate cascade constraints."
                )
