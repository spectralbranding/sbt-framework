"""Tests for Module 7 prompt generation with dimension_order parameter.

Covers:
  - canonical mode: standard S-N-I-E-So-Ec-C-T order
  - latin_square mode: 8 distinct orderings, each dimension in each position exactly once
  - random mode: same seed produces same order; different seeds produce different orders
  - prompt template reflects the reordered dimensions
  - backward compatibility: default is canonical
  - error handling for invalid inputs
"""

import pytest

from spectral_branding.prompt_generator import (
    CANONICAL_DIMENSIONS,
    LATIN_SQUARE,
    generate_prism_b_prompt,
    get_dimension_order,
    reset_latin_square_counter,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

CANONICAL_ORDER = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]


# ---------------------------------------------------------------------------
# canonical mode
# ---------------------------------------------------------------------------


class TestCanonicalMode:
    def test_canonical_returns_standard_order(self):
        """canonical mode must return the S-N-I-E-So-Ec-C-T sequence."""
        dims = get_dimension_order("canonical")
        assert dims == CANONICAL_ORDER

    def test_canonical_is_default(self):
        """Calling with no arguments must equal canonical."""
        assert get_dimension_order() == get_dimension_order("canonical")

    def test_canonical_is_defensive_copy(self):
        """Mutating the returned list must not affect the module constant."""
        dims = get_dimension_order("canonical")
        dims[0] = "MUTATED"
        assert CANONICAL_DIMENSIONS[0] == "semiotic"

    def test_canonical_length(self):
        assert len(get_dimension_order("canonical")) == 8

    def test_canonical_contains_all_dimensions(self):
        dims = get_dimension_order("canonical")
        assert set(dims) == set(CANONICAL_ORDER)


# ---------------------------------------------------------------------------
# latin_square mode
# ---------------------------------------------------------------------------


class TestLatinSquareMode:
    def setup_method(self):
        """Reset counter before each test to ensure isolation."""
        reset_latin_square_counter()

    def test_latin_square_produces_8_distinct_orderings(self):
        """Requesting rows 0-7 must yield 8 distinct permutations."""
        orderings = [
            get_dimension_order("latin_square", latin_square_row=i) for i in range(8)
        ]
        # All must be distinct
        as_tuples = [tuple(o) for o in orderings]
        assert len(set(as_tuples)) == 8

    def test_latin_square_each_dim_in_each_position_exactly_once(self):
        """Each dimension must appear in every column position exactly once."""
        orderings = [
            get_dimension_order("latin_square", latin_square_row=i) for i in range(8)
        ]
        for col in range(8):
            dims_at_col = [orderings[row][col] for row in range(8)]
            assert sorted(dims_at_col) == sorted(
                CANONICAL_ORDER
            ), f"Column {col} does not contain each dimension exactly once: {dims_at_col}"

    def test_latin_square_each_ordering_is_permutation(self):
        """Every row must be a permutation of the canonical set."""
        for i in range(8):
            row = get_dimension_order("latin_square", latin_square_row=i)
            assert sorted(row) == sorted(CANONICAL_ORDER)
            assert len(row) == 8

    def test_latin_square_row_0_is_canonical(self):
        """Row 0 of the Latin square is the canonical order."""
        assert (
            get_dimension_order("latin_square", latin_square_row=0) == CANONICAL_ORDER
        )

    def test_latin_square_auto_advance_cycles(self):
        """Auto-advance counter must cycle through all 8 rows."""
        reset_latin_square_counter()
        orderings = [get_dimension_order("latin_square") for _ in range(8)]
        as_tuples = [tuple(o) for o in orderings]
        assert len(set(as_tuples)) == 8

    def test_latin_square_auto_advance_wraps_at_8(self):
        """After 8 calls the auto-advance counter wraps to row 0."""
        reset_latin_square_counter()
        first_pass = [tuple(get_dimension_order("latin_square")) for _ in range(8)]
        second_pass = [tuple(get_dimension_order("latin_square")) for _ in range(8)]
        assert first_pass == second_pass

    def test_latin_square_explicit_row_does_not_advance_counter(self):
        """Passing latin_square_row= explicitly must not advance the auto counter."""
        reset_latin_square_counter()
        # Two calls with explicit row 0 — counter should still be 0
        get_dimension_order("latin_square", latin_square_row=0)
        get_dimension_order("latin_square", latin_square_row=0)
        # Now auto-advance should still start at row 0
        auto = get_dimension_order("latin_square")
        assert auto == CANONICAL_ORDER

    def test_latin_square_row_out_of_range_raises(self):
        with pytest.raises(ValueError, match="latin_square_row"):
            get_dimension_order("latin_square", latin_square_row=8)

    def test_latin_square_negative_row_raises(self):
        with pytest.raises(ValueError, match="latin_square_row"):
            get_dimension_order("latin_square", latin_square_row=-1)

    def test_latin_square_constant_matches_computed_rows(self):
        """LATIN_SQUARE module constant must match get_dimension_order output."""
        for i, expected in enumerate(LATIN_SQUARE):
            assert get_dimension_order("latin_square", latin_square_row=i) == expected


# ---------------------------------------------------------------------------
# random mode
# ---------------------------------------------------------------------------


class TestRandomMode:
    def test_random_same_seed_same_order(self):
        """Same seed must produce identical permutations across two calls."""
        d1 = get_dimension_order("random", seed=42)
        d2 = get_dimension_order("random", seed=42)
        assert d1 == d2

    def test_random_different_seeds_likely_differ(self):
        """Different seeds should produce different orderings (with very high probability)."""
        results = {tuple(get_dimension_order("random", seed=s)) for s in range(20)}
        # 8! = 40320 permutations; 20 distinct seeds should give >1 unique ordering
        assert len(results) > 1

    def test_random_is_permutation(self):
        """Random output must be a permutation of canonical dimensions."""
        dims = get_dimension_order("random", seed=99)
        assert sorted(dims) == sorted(CANONICAL_ORDER)
        assert len(dims) == 8

    def test_random_no_seed_is_non_deterministic(self):
        """Without a seed, repeated calls should (almost certainly) differ."""
        seen = {tuple(get_dimension_order("random")) for _ in range(50)}
        assert len(seen) > 1

    def test_random_defensive_copy(self):
        """Mutating returned list must not affect subsequent calls with same seed."""
        d1 = get_dimension_order("random", seed=7)
        d1[0] = "MUTATED"
        d2 = get_dimension_order("random", seed=7)
        assert d2[0] != "MUTATED"


# ---------------------------------------------------------------------------
# invalid mode
# ---------------------------------------------------------------------------


class TestInvalidMode:
    def test_invalid_mode_raises_value_error(self):
        with pytest.raises(ValueError, match="dimension_order"):
            get_dimension_order("alphabetical")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Prompt template reflects reordered dimensions
# ---------------------------------------------------------------------------


class TestPromptTemplateOrdering:
    def setup_method(self):
        reset_latin_square_counter()

    def test_canonical_prompt_contains_keys_in_order(self):
        """System prompt JSON template must list keys in canonical order."""
        result = generate_prism_b_prompt("Hermes", "canonical")
        system = result["system"]
        positions = [system.index(f'"{d}"') for d in CANONICAL_ORDER]
        assert positions == sorted(
            positions
        ), "Canonical dimension keys are not in canonical order in the prompt"

    def test_latin_square_prompt_reflects_row_order(self):
        """For each Latin square row, the prompt keys must follow that row's order."""
        for row_idx in range(8):
            result = generate_prism_b_prompt(
                "IKEA", "latin_square", latin_square_row=row_idx
            )
            system = result["system"]
            expected_order = LATIN_SQUARE[row_idx]
            positions = [system.index(f'"{d}"') for d in expected_order]
            assert positions == sorted(
                positions
            ), f"Row {row_idx}: dimension keys are not in expected order in the prompt"

    def test_random_prompt_reflects_shuffled_order(self):
        """Random prompt keys must follow the shuffled dimension order."""
        dims = get_dimension_order("random", seed=123)
        result = generate_prism_b_prompt("Tesla", "random", seed=123)
        system = result["system"]
        positions = [system.index(f'"{d}"') for d in dims]
        assert positions == sorted(
            positions
        ), "Random dimension keys are not in shuffled order in the prompt"

    def test_prompt_contains_brand_name(self):
        """User prompt must include the brand name."""
        result = generate_prism_b_prompt("Patagonia")
        assert "Patagonia" in result["user"]

    def test_prompt_returns_system_and_user_keys(self):
        """Return value must have 'system' and 'user' keys."""
        result = generate_prism_b_prompt("Erewhon")
        assert "system" in result
        assert "user" in result

    def test_prompt_all_8_dimensions_present(self):
        """All 8 dimension names must appear in the system prompt."""
        result = generate_prism_b_prompt("Hermes", "random", seed=0)
        system = result["system"]
        for dim in CANONICAL_ORDER:
            assert dim in system, f"Dimension '{dim}' missing from system prompt"

    def test_prompt_without_descriptions(self):
        """include_descriptions=False must produce a shorter prompt without dim descriptions."""
        with_desc = generate_prism_b_prompt("IKEA", include_descriptions=True)
        without_desc = generate_prism_b_prompt("IKEA", include_descriptions=False)
        assert len(with_desc["system"]) > len(without_desc["system"])
        # The description strings should not appear when disabled
        assert "Visual/auditory identity" not in without_desc["system"]

    def test_prompt_latin_square_auto_advance_reflects_ordering(self):
        """Auto-advance latin_square prompt must use the current counter row."""
        reset_latin_square_counter()
        # Row 0 = canonical
        result = generate_prism_b_prompt("Tesla", "latin_square")
        system = result["system"]
        expected_order = LATIN_SQUARE[0]
        positions = [system.index(f'"{d}"') for d in expected_order]
        assert positions == sorted(positions)
        # Row 1 = one-step rotation; next call should reflect that
        result2 = generate_prism_b_prompt("Tesla", "latin_square")
        system2 = result2["system"]
        expected_order2 = LATIN_SQUARE[1]
        positions2 = [system2.index(f'"{d}"') for d in expected_order2]
        assert positions2 == sorted(positions2)
