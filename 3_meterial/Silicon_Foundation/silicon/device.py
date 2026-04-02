from __future__ import annotations

from typing import List

from .contracts import ConceptLayer, DeviceAssessment, DomainMode


def assess_pv_device() -> DeviceAssessment:
    return DeviceAssessment(
        domain=DomainMode.PHOTOVOLTAIC,
        efficiency_fraction=0.22,
        defect_density_cm2=1e5,
        thermal_margin_c=40.0,
        notes=["Commercial Si PV range; temperature coefficient matters in field output."],
    )


def assess_logic_device() -> DeviceAssessment:
    return DeviceAssessment(
        domain=DomainMode.SEMICONDUCTOR,
        efficiency_fraction=0.60,
        defect_density_cm2=5e4,
        thermal_margin_c=25.0,
        notes=["Logic yield and thermal budget constrain effective performance/watt."],
    )


def device_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(name="Yield-Defect Coupling", description="Defect density drives yield and cost; thermal margins shape reliability."),
    ]
