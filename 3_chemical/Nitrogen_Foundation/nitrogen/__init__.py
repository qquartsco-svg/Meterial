"""Nitrogen_Foundation v0.1.0 — N₂ separation, Haber cartoon, LN₂, screening."""

__version__ = "0.1.0"

from .contracts import (
    HealthVerdict,
    NitrogenClaimPayload,
    NitrogenFoundationReport,
    NitrogenHealthReport,
    NitrogenScreeningReport,
    N2Properties,
    SeparationMethod,
    StorageMethod,
    Verdict,
)
from .foundation import collect_concept_layers, compute_health, run_nitrogen_foundation

__all__ = [
    "__version__",
    "HealthVerdict",
    "NitrogenClaimPayload",
    "NitrogenFoundationReport",
    "NitrogenHealthReport",
    "NitrogenScreeningReport",
    "N2Properties",
    "SeparationMethod",
    "StorageMethod",
    "Verdict",
    "collect_concept_layers",
    "compute_health",
    "run_nitrogen_foundation",
]
