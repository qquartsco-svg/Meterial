from __future__ import annotations

from .circularity import assess_circularity
from .contracts import (
    CarbonCompositeReadinessReport,
    CarbonMaterialCandidate,
    CircularityReport,
    CompositeProcessConfig,
    MaterialPerformanceReport,
    ProcessPerformanceReport,
    ProductSpec,
)
from .material import assess_material_performance
from .observer import assess_readiness
from .process import assess_process


def run_composite_assessment(
    material: CarbonMaterialCandidate,
    process: CompositeProcessConfig,
    spec: ProductSpec,
) -> tuple[CarbonCompositeReadinessReport, MaterialPerformanceReport, ProcessPerformanceReport, CircularityReport]:
    material_report = assess_material_performance(material, spec)
    process_report = assess_process(process)
    circularity_report = assess_circularity(material, process)
    readiness = assess_readiness(material_report, process_report, circularity_report)
    return readiness, material_report, process_report, circularity_report

