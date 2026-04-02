"""Domain mapping — Hydrogen transport / mobility.

Key topics:
  - FCEV (Fuel Cell Electric Vehicle)
  - Heavy-duty transport (trucks, buses, trains, ships)
  - H₂ refuelling infrastructure
"""

from __future__ import annotations

from typing import List

from .contracts import ConceptLayer


def fcev_range_km(
    tank_h2_kg: float = 5.6,
    fuel_cell_efficiency: float = 0.50,
    vehicle_energy_kwh_per_100km: float = 20.0,
) -> float:
    """Approximate FCEV range.

    range = (m_H₂ × LHV × η_fc) / (energy_per_100km / 100)
    """
    from .constants import H2_LHV_KWH_PER_KG

    usable_kwh = tank_h2_kg * H2_LHV_KWH_PER_KG * fuel_cell_efficiency
    if vehicle_energy_kwh_per_100km <= 0:
        return 0.0
    return usable_kwh / (vehicle_energy_kwh_per_100km / 100.0)


def refuelling_time_min(
    tank_size_kg: float = 5.6,
    dispenser_rate_kg_per_min: float = 1.8,
) -> float:
    """Time to fill a 700-bar tank at a refuelling station."""
    if dispenser_rate_kg_per_min <= 0:
        return float("inf")
    return tank_size_kg / dispenser_rate_kg_per_min


def h2_cost_per_100km(
    h2_price_usd_per_kg: float = 10.0,
    fuel_cell_efficiency: float = 0.50,
    vehicle_energy_kwh_per_100km: float = 20.0,
) -> float:
    """Fuel cost per 100 km for an FCEV."""
    from .constants import H2_LHV_KWH_PER_KG

    kwh_per_kg_usable = H2_LHV_KWH_PER_KG * fuel_cell_efficiency
    if kwh_per_kg_usable <= 0:
        return float("inf")
    kg_per_100km = vehicle_energy_kwh_per_100km / kwh_per_kg_usable
    return kg_per_100km * h2_price_usd_per_kg


def transport_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="FCEV (Fuel Cell Electric Vehicle)",
            description=(
                "Toyota Mirai, Hyundai NEXO — 5–6 kg H₂ at 700 bar, ~500 km range.  "
                "Refuelling in 3–5 minutes vs 30+ min BEV DC-fast charging.  "
                "Infrastructure is the bottleneck, not the vehicle."
            ),
            key_equations=["range = m_H₂ × LHV × η_fc / (E/100km)"],
        ),
        ConceptLayer(
            name="Heavy-Duty / Marine / Rail",
            description=(
                "Strongest near-term use case for hydrogen mobility.  "
                "Heavy trucks, trains (Coradia iLint), and ferries cannot easily electrify "
                "due to battery weight/energy density constraints."
            ),
        ),
    ]
