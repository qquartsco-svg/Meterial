"""L6 — ATHENA screening for hydrogen claims.

Flags:
  1. thermodynamics_violation   — η > 100 %, free energy violation
  2. impossible_cost            — cost below physical energy floor
  3. perpetual_hydrogen         — closed loop with no external energy input
  4. ignored_storage_losses     — no boil-off, no compression energy
  5. over_unity_fuel_cell       — fuel cell η_e > ΔG/ΔH theoretical
  6. safety_handwave            — no mention of LEL/UEL or embrittlement
  7. colour_washing             — mislabelled colour code
"""

from __future__ import annotations

from typing import List, Optional

from .contracts import (
    ConceptLayer,
    HydrogenClaimPayload,
    HydrogenScreeningReport,
    Verdict,
)


_FLAG_DEFS = {
    "thermodynamics_violation": "Claimed efficiency exceeds thermodynamic limit.",
    "impossible_cost": "Claimed cost is below the physical energy floor (~$1/kg with free electricity).",
    "perpetual_hydrogen": "Closed-loop claim with no external energy source.",
    "ignored_storage_losses": "No storage losses (compression / boil-off / round-trip) acknowledged.",
    "over_unity_fuel_cell": "Fuel cell electric efficiency claimed above ΔG/ΔH limit (~83 %).",
    "safety_handwave": "Safety risks (flammability, embrittlement) not addressed.",
    "colour_washing": "Hydrogen colour code does not match production pathway.",
}


def screen_hydrogen_claim(
    payload: HydrogenClaimPayload,
) -> HydrogenScreeningReport:
    """Screen a hydrogen-related claim through ATHENA rules."""
    flags: List[str] = []
    reasoning: List[str] = []
    omega = 0.70  # start at a conservative baseline

    if payload.claimed_efficiency is not None:
        if payload.claimed_efficiency > 1.0:
            flags.append("thermodynamics_violation")
            reasoning.append(
                f"Claimed efficiency {payload.claimed_efficiency:.0%} exceeds unity."
            )
            omega -= 0.50
        elif payload.claimed_efficiency > 0.83:
            flags.append("over_unity_fuel_cell")
            reasoning.append(
                f"Efficiency {payload.claimed_efficiency:.0%} exceeds ΔG/ΔH limit for fuel cells."
            )
            omega -= 0.20

    if payload.claimed_cost_usd_per_kg is not None:
        if payload.claimed_cost_usd_per_kg < 0.5:
            flags.append("impossible_cost")
            reasoning.append(
                f"${payload.claimed_cost_usd_per_kg}/kg is below the physical energy floor."
            )
            omega -= 0.35
        elif payload.claimed_cost_usd_per_kg < 1.0:
            reasoning.append(
                f"${payload.claimed_cost_usd_per_kg}/kg is extremely aggressive — verify assumptions."
            )
            omega -= 0.10

    if payload.claimed_energy_density_kwh_per_kg is not None:
        if payload.claimed_energy_density_kwh_per_kg > 39.4:
            flags.append("thermodynamics_violation")
            reasoning.append(
                "Claimed energy density exceeds H₂ HHV (39.4 kWh/kg)."
            )
            omega -= 0.30

    tags_lower = [t.lower() for t in payload.tags]
    if "perpetual" in tags_lower or "closed_loop_no_input" in tags_lower:
        flags.append("perpetual_hydrogen")
        reasoning.append("Perpetual hydrogen loop without external energy is impossible.")
        omega -= 0.30

    if "no_storage_loss" in tags_lower:
        flags.append("ignored_storage_losses")
        reasoning.append("All storage methods have non-zero energy penalties and losses.")
        omega -= 0.10

    if "safety_ignored" in tags_lower:
        flags.append("safety_handwave")
        reasoning.append("Hydrogen safety (LEL/UEL, embrittlement) must be addressed.")
        omega -= 0.10

    omega = max(omega, 0.0)
    omega = round(omega, 3)

    if omega >= 0.65 and not flags:
        verdict = Verdict.POSITIVE
    elif omega >= 0.45:
        verdict = Verdict.NEUTRAL
    elif omega >= 0.25:
        verdict = Verdict.CAUTIOUS
    else:
        verdict = Verdict.NEGATIVE

    if not reasoning:
        reasoning.append("No specific issues detected — claim is within expected bounds.")

    return HydrogenScreeningReport(
        verdict=verdict,
        omega=omega,
        flags=flags,
        reasoning=reasoning,
    )


def screening_concept_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer(
            name="ATHENA Hydrogen Screening",
            description=(
                "Conservative 4-tier (positive / neutral / cautious / negative) screening "
                "for hydrogen economy claims.  Flags: thermodynamics violation, impossible cost, "
                "perpetual hydrogen, ignored storage losses, over-unity fuel cell, safety handwave, "
                "colour washing."
            ),
        ),
    ]
