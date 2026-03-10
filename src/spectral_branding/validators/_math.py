"""
Shared mathematical utilities for SBT validators.

Core functions derived from R1 (Zharnikov 2026d) formal metric definitions.
"""

import numpy as np
from scipy.special import gamma

# Canonical SBT dimensions (order matters)
DIMENSIONS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]
N_DIM = 8

# Canonical brand profiles (from SBT framework v2.3)
CANONICAL_BRANDS = {
    "Hermes": np.array([9.5, 9.0, 7.0, 9.0, 8.5, 3.0, 9.0, 9.5]),
    "IKEA": np.array([8.0, 7.5, 6.0, 7.0, 5.0, 9.0, 7.5, 6.0]),
    "Patagonia": np.array([6.0, 9.0, 9.5, 7.5, 8.0, 5.0, 7.0, 6.5]),
    "Erewhon": np.array([7.0, 6.5, 5.0, 9.0, 8.5, 3.5, 7.5, 2.5]),
    "Tesla": np.array([7.5, 8.5, 3.0, 6.0, 7.0, 6.0, 4.0, 2.0]),
}

# Signal value bounds (SBT uses 1-10 scale)
SIGNAL_MIN = 1.0
SIGNAL_MAX = 10.0


def to_signal_array(values: list[float] | np.ndarray) -> np.ndarray:
    """Convert a list of signal values to a numpy array, validating shape."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.shape != (N_DIM,):
        raise ValueError(f"Expected {N_DIM} dimensions, got {arr.shape}")
    return arr


def clr_transform(s: np.ndarray) -> np.ndarray:
    """
    Centered log-ratio transform: clr(s)_i = log(s_i / g(s)).

    Maps R^n_+ to a hyperplane in R^n where components sum to zero.
    From R1 Section 4 (Aitchison geometry).
    """
    if np.any(s <= 0):
        raise ValueError("All signal components must be strictly positive")
    log_s = np.log(s)
    return log_s - np.mean(log_s)


def aitchison_distance(s1: np.ndarray, s2: np.ndarray) -> float:
    """
    Aitchison distance: d_A(s1, s2) = ||clr(s1) - clr(s2)||_2.

    Scale-invariant metric on brand signal space (R1 Theorem 1).
    """
    return float(np.linalg.norm(clr_transform(s1) - clr_transform(s2)))


def fisher_rao_distance(w1: np.ndarray, w2: np.ndarray) -> float:
    """
    Fisher-Rao geodesic distance on the probability simplex.

    d_FR(w1, w2) = 2 * arccos(sum(sqrt(w1_i * w2_i)))

    Unique up to scaling by Cencov's theorem (R1 Section 5).
    """
    bc = np.clip(np.sum(np.sqrt(w1 * w2)), -1.0, 1.0)
    return 2.0 * float(np.arccos(bc))


def normalize_to_simplex(v: np.ndarray) -> np.ndarray:
    """Normalize a positive vector to the probability simplex."""
    total = np.sum(v)
    if total <= 0:
        raise ValueError("Cannot normalize: sum is non-positive")
    return v / total


def normalize_to_sphere(s: np.ndarray) -> np.ndarray:
    """Normalize a positive vector to the unit sphere S^(n-1)_+."""
    norm = np.linalg.norm(s)
    if norm == 0:
        raise ValueError("Cannot normalize zero vector to sphere")
    return s / norm


def unit_ball_volume(n: int) -> float:
    """Volume of the n-dimensional unit ball: pi^(n/2) / Gamma(n/2 + 1)."""
    return np.pi ** (n / 2.0) / gamma(n / 2.0 + 1.0)


def sphere_surface_area(n: int) -> float:
    """Surface area of S^(n-1): 2 * pi^(n/2) / Gamma(n/2)."""
    return 2.0 * np.pi ** (n / 2.0) / gamma(n / 2.0)


def positive_orthant_fraction(n: int) -> float:
    """Fraction of S^(n-1) in the positive orthant: 1/2^n."""
    return 1.0 / (2**n)


def verify_triangle_inequality(
    d_ab: float, d_bc: float, d_ac: float, tol: float = 1e-10
) -> bool:
    """Check if three distances satisfy the triangle inequality."""
    return (
        d_ab <= d_bc + d_ac + tol
        and d_bc <= d_ab + d_ac + tol
        and d_ac <= d_ab + d_bc + tol
    )
