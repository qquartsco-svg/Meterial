from __future__ import annotations

import lithium
from lithium.battery import assess_battery_chemistry
from lithium.contracts import BatteryChemistry, LithiumClaimPayload
from lithium.extraction import assess_brine_extraction, assess_hard_rock_extraction
from lithium.foundation import collect_concept_layers, compute_health, run_lithium_foundation
from lithium.properties import lithium_property_card
from lithium.screening import screen_lithium_claim


def test_version():
    assert lithium.__version__ == "0.1.0"


def test_property_card():
    c = lithium_property_card()
    assert c.molar_mass_g_per_mol > 6.0


def test_extraction_models():
    b = assess_brine_extraction()
    h = assess_hard_rock_extraction()
    assert b.water_intensity_l_per_kg_lce > h.water_intensity_l_per_kg_lce


def test_battery_lfp():
    r = assess_battery_chemistry(BatteryChemistry.LFP)
    assert r.cycle_life_80pct > 2000


def test_battery_nmc():
    r = assess_battery_chemistry(BatteryChemistry.NMC)
    assert r.specific_energy_wh_per_kg > 200


def test_screening_flags():
    r = screen_lithium_claim(LithiumClaimPayload("", claimed_zero_degradation=True))
    assert "degradation_denial" in r.flags


def test_collect_layers():
    assert len(collect_concept_layers()) >= 5


def test_compute_health():
    h = compute_health()
    assert h.composite_omega > 0.0


def test_run_foundation():
    r = run_lithium_foundation()
    assert r.extraction is not None and r.battery is not None and r.health is not None
