"""Hydrogen_Foundation v0.1.0 — 수소에 관한 모든 것.

수소의 물성, 생산, 저장, 연료전지, 안전, 스크리닝을 하나의 기초 레이어로.
"""

__version__ = "0.1.0"

from .contracts import (
    ColorCode,
    FuelCellType,
    H2Properties,
    HealthVerdict,
    HydrogenClaimPayload,
    HydrogenFoundationReport,
    HydrogenHealthReport,
    HydrogenScreeningReport,
    ProductionAssessment,
    ProductionMethod,
    SafetyAssessment,
    StorageAssessment,
    StorageMethod,
    Verdict,
)
from .foundation import (
    collect_concept_layers,
    compute_health,
    run_hydrogen_foundation,
)

__all__ = [
    "__version__",
    "ColorCode",
    "FuelCellType",
    "H2Properties",
    "HealthVerdict",
    "HydrogenClaimPayload",
    "HydrogenFoundationReport",
    "HydrogenHealthReport",
    "HydrogenScreeningReport",
    "ProductionAssessment",
    "ProductionMethod",
    "SafetyAssessment",
    "StorageAssessment",
    "StorageMethod",
    "Verdict",
    "collect_concept_layers",
    "compute_health",
    "run_hydrogen_foundation",
]
