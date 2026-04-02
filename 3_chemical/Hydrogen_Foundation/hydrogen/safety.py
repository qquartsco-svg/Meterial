"""L5 — Hydrogen safety.

Core question: *What can go wrong, and how do we prevent it?*

H₂ is the lightest, most diffusive gas.  It is flammable in a very wide
range (4–75 vol%) and has the lowest ignition energy of any common fuel.
On the positive side, it rises and disperses extremely fast in open air.
"""

from __future__ import annotations

from typing import List

from .constants import (
    H2_AUTOIGNITION_K,
    H2_FLAME_SPEED_M_PER_S,
    H2_LEL_VOL_PERCENT,
    H2_MIN_IGNITION_ENERGY_MJ,
    H2_UEL_VOL_PERCENT,
)
from .contracts import ConceptLayer, SafetyAssessment


def is_within_flammable_range(concentration_vol_percent: float) -> bool:
    """Check whether H₂ concentration lies between LEL and UEL."""
    return H2_LEL_VOL_PERCENT <= concentration_vol_percent <= H2_UEL_VOL_PERCENT


def required_ventilation_m3_per_s(
    leak_rate_g_per_s: float,
    target_vol_percent: float = 1.0,
) -> float:
    """Minimum ventilation airflow to dilute a leak below *target_vol_percent*.

    Based on ideal mixing at STP: Q = (ṁ / ρ_H₂) / (C_target / 100).
    """
    if target_vol_percent <= 0:
        raise ValueError("target_vol_percent must be > 0")
    rho_h2 = 0.0899  # kg/m³ at STP
    leak_m3_per_s = (leak_rate_g_per_s / 1000.0) / rho_h2
    return leak_m3_per_s / (target_vol_percent / 100.0)


def embrittlement_risk_level(
    material_tensile_strength_mpa: float,
    h2_partial_pressure_mpa: float,
) -> str:
    """Rough heuristic for hydrogen embrittlement risk.

    High-strength steels (>700 MPa) at high H₂ pressure are most susceptible.
    """
    if material_tensile_strength_mpa > 900 and h2_partial_pressure_mpa > 10:
        return "high"
    if material_tensile_strength_mpa > 600 or h2_partial_pressure_mpa > 30:
        return "moderate"
    return "low"


def explosion_overpressure_kpa(
    h2_mass_kg: float,
    confinement_volume_m3: float,
) -> float:
    """Extremely rough TNT-equivalent overpressure estimate.

    H₂ LHV ≈ 120 MJ/kg.  TNT equivalent ≈ 4.6 MJ/kg.
    This is a *screening-level* estimate only.
    """
    if confinement_volume_m3 <= 0:
        return 0.0
    tnt_eq_kg = h2_mass_kg * 120.0 / 4.6 * 0.1  # 10 % yield factor
    radius_m = confinement_volume_m3 ** (1.0 / 3.0)
    scaled_distance = radius_m / max(tnt_eq_kg ** (1.0 / 3.0), 0.001)
    if scaled_distance < 0.5:
        return 2000.0  # severe
    return max(100.0 / scaled_distance**2, 0.1)


def assess_safety(
    h2_concentration_vol_percent: float,
    leak_rate_g_per_s: float = 0.0,
    ventilation_m3_per_s: float = 0.0,
    material_tensile_mpa: float = 400.0,
    h2_partial_pressure_mpa: float = 35.0,
    h2_mass_kg: float = 5.0,
    confinement_volume_m3: float = 50.0,
) -> SafetyAssessment:
    """Composite safety assessment."""
    flammable = is_within_flammable_range(h2_concentration_vol_percent)
    req_vent = required_ventilation_m3_per_s(max(leak_rate_g_per_s, 0.001))
    vent_ok = ventilation_m3_per_s >= req_vent
    embr = embrittlement_risk_level(material_tensile_mpa, h2_partial_pressure_mpa)
    overpressure = explosion_overpressure_kpa(h2_mass_kg, confinement_volume_m3)

    risk = "acceptable"
    notes: List[str] = []
    if flammable:
        risk = "marginal"
        notes.append(f"Concentration {h2_concentration_vol_percent:.1f} % is within flammable range.")
    if not vent_ok and leak_rate_g_per_s > 0:
        risk = "marginal"
        notes.append(f"Ventilation insufficient: need ≥ {req_vent:.3f} m³/s.")
    if embr == "high":
        risk = "unacceptable"
        notes.append("High embrittlement risk — material selection review required.")
    if overpressure > 500:
        risk = "unacceptable"
        notes.append(f"Potential overpressure {overpressure:.0f} kPa — blast mitigation needed.")

    return SafetyAssessment(
        h2_concentration_vol_percent=h2_concentration_vol_percent,
        within_flammable_range=flammable,
        leak_rate_g_per_s=leak_rate_g_per_s,
        ventilation_adequate=vent_ok,
        embrittlement_risk=embr,
        explosion_overpressure_kpa=round(overpressure, 1),
        risk_level=risk,
        notes=notes,
    )


def safety_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="Flammability",
            description=(
                "LEL 4 %, UEL 75 % in air.  Extremely wide range.  "
                "Minimum ignition energy ~0.017 mJ — static discharge can suffice."
            ),
            key_equations=[
                "Flammable if LEL ≤ C ≤ UEL",
                "Q_vent = (ṁ/ρ) / (C_target/100)",
            ],
        ),
        ConceptLayer(
            name="Embrittlement",
            description=(
                "H atoms diffuse into metal lattice → reduced ductility, crack growth.  "
                "High-strength steels (> 700 MPa) are most susceptible.  "
                "Mitigation: material selection, coatings, lower pressure."
            ),
        ),
        ConceptLayer(
            name="Explosion / Deflagration",
            description=(
                "Confined H₂–air mixtures can transition from deflagration to detonation.  "
                "Flame speed ~3.5 m/s (stoichiometric, laminar).  "
                "Venting and leak detection are primary safeguards."
            ),
        ),
    ]
