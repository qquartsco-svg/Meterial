"""Oxygen_Foundation v0.1.0 — O₂ production, LOX, oxidiser safety, screening."""

__version__ = "0.1.0"

from .contracts import (
    HealthVerdict,
    O2Properties,
    OxygenClaimPayload,
    OxygenFoundationReport,
    OxygenHealthReport,
    OxygenScreeningReport,
    ProductionMethod,
    StorageMethod,
    Verdict,
)
from .foundation import collect_concept_layers, compute_health, run_oxygen_foundation

__all__ = [
    "__version__",
    "HealthVerdict",
    "O2Properties",
    "OxygenClaimPayload",
    "OxygenFoundationReport",
    "OxygenHealthReport",
    "OxygenScreeningReport",
    "ProductionMethod",
    "StorageMethod",
    "Verdict",
    "collect_concept_layers",
    "compute_health",
    "run_oxygen_foundation",
]
