"""Phosphorus_Foundation v0.1.0 — extraction, ATP cycle, screening."""

__version__ = "0.1.0"

from .contracts import (
    DomainMode,
    ExtractionAssessment,
    ExtractionMethod,
    HealthVerdict,
    PProperties,
    PhosphorusClaimPayload,
    PhosphorusFoundationReport,
    PhosphorusHealthReport,
    PhosphorusScreeningReport,
    Verdict,
)
from .foundation import collect_concept_layers, compute_health, run_phosphorus_foundation

__all__ = [
    "__version__",
    "DomainMode",
    "ExtractionAssessment",
    "ExtractionMethod",
    "HealthVerdict",
    "PProperties",
    "PhosphorusClaimPayload",
    "PhosphorusFoundationReport",
    "PhosphorusHealthReport",
    "PhosphorusScreeningReport",
    "Verdict",
    "collect_concept_layers",
    "compute_health",
    "run_phosphorus_foundation",
]
