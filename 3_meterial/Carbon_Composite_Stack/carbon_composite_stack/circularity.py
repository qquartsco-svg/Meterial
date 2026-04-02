from __future__ import annotations

from .contracts import CarbonMaterialCandidate, CircularityReport, CompositeProcessConfig


def assess_circularity(
    material: CarbonMaterialCandidate,
    process: CompositeProcessConfig,
) -> CircularityReport:
    recycle_score = max(0.0, min(1.0, material.recycle_content_ratio))
    scrap_penalty = max(0.0, min(1.0, process.scrap_rate))
    omega = max(0.0, min(1.0, 0.7 * recycle_score + 0.3 * (1.0 - scrap_penalty)))
    return CircularityReport(
        recycle_score=recycle_score,
        scrap_penalty=scrap_penalty,
        omega_circularity=omega,
    )

