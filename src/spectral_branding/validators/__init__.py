"""
Math-hardened validators for SBT/OST LLM pipeline.

Each validator enforces proven mathematical bounds from the R1-R7 research
papers as runtime constraints on LLM-generated brand/organizational analyses.

SBT validators: metric (R1), metamerism (R2), cohort (R3), capacity (R4),
                trajectory (R6), resource allocation (R7)
OST validators: specification (R5)
"""

from spectral_branding.validators.resource_allocation_validator import (
    validate_resource_allocation,
)
from spectral_branding.validators.specification_validator import (
    validate_activation_matrix,
)
from spectral_branding.validators.validate import validate_analysis

__all__ = [
    "validate_analysis",
    "validate_activation_matrix",
    "validate_resource_allocation",
]
