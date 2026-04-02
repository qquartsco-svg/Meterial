"""Silicon_Foundation v0.1.0 — refining, device yield, thermal realism, screening."""

__version__ = "0.1.0"

from .contracts import (
    DeviceAssessment,
    DomainMode,
    HealthVerdict,
    RefiningAssessment,
    RefiningMethod,
    SiProperties,
    SiliconClaimPayload,
    SiliconFoundationReport,
    SiliconHealthReport,
    SiliconScreeningReport,
    Verdict,
)
from .foundation import collect_concept_layers, compute_health, run_silicon_foundation

__all__ = [
    "__version__",
    "DeviceAssessment",
    "DomainMode",
    "HealthVerdict",
    "RefiningAssessment",
    "RefiningMethod",
    "SiProperties",
    "SiliconClaimPayload",
    "SiliconFoundationReport",
    "SiliconHealthReport",
    "SiliconScreeningReport",
    "Verdict",
    "collect_concept_layers",
    "compute_health",
    "run_silicon_foundation",
]
