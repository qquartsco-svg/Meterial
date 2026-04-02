"""Comprehensive tests for Meterial v0.2.1."""

from __future__ import annotations

import math
import pytest

from chemical_reaction.contracts import (
    ChemicalClaimPayload,
    ChemicalSpecies,
    ConceptLayer,
    ElectrochemicalCell,
    HealthVerdict,
    KineticState,
    Phase,
    Reaction,
    ReactionTerm,
    ThermodynamicState,
    Verdict,
)
from chemical_reaction.constants import (
    FARADAY_C_PER_MOL,
    R_GAS_J_PER_MOL_K,
    STANDARD_TEMPERATURE_K,
    WATER_ELECTROLYSIS_E0_V,
)

# ════════════════════════════════════════════════════════════════════════
# Fixtures — common species and reactions
# ════════════════════════════════════════════════════════════════════════

H2 = ChemicalSpecies("H2", 2.016, Phase.GAS)
O2 = ChemicalSpecies("O2", 32.0, Phase.GAS)
H2O_L = ChemicalSpecies("H2O", 18.015, Phase.LIQUID)
H2O_G = ChemicalSpecies("H2O", 18.015, Phase.GAS)
CO2 = ChemicalSpecies("CO2", 44.01, Phase.GAS)
CH4 = ChemicalSpecies("CH4", 16.04, Phase.GAS)
N2 = ChemicalSpecies("N2", 28.014, Phase.GAS)
Na_plus = ChemicalSpecies("Na", 22.99, Phase.AQUEOUS, charge=1)
Cl_minus = ChemicalSpecies("Cl", 35.45, Phase.AQUEOUS, charge=-1)

WATER_FORMATION = Reaction(
    reactants=(ReactionTerm(H2, 2.0), ReactionTerm(O2, 1.0)),
    products=(ReactionTerm(H2O_L, 2.0),),
    delta_h_kj_per_mol=-571.6,
    delta_s_j_per_mol_k=-326.8,
    activation_energy_kj_per_mol=75.0,
    label="2H2 + O2 → 2H2O(l)",
)

SABATIER = Reaction(
    reactants=(ReactionTerm(CO2, 1.0), ReactionTerm(H2, 4.0)),
    products=(ReactionTerm(CH4, 1.0), ReactionTerm(H2O_L, 2.0)),
    delta_h_kj_per_mol=-165.0,
    delta_s_j_per_mol_k=-172.0,
    label="CO2 + 4H2 → CH4 + 2H2O",
)


# ════════════════════════════════════════════════════════════════════════
# L0 — Contracts
# ════════════════════════════════════════════════════════════════════════

class TestContracts:
    def test_species_creation(self):
        assert H2.formula == "H2"
        assert H2.phase == Phase.GAS
        assert H2.charge == 0

    def test_species_with_charge(self):
        assert Na_plus.charge == 1
        assert Cl_minus.charge == -1

    def test_reaction_creation(self):
        assert len(WATER_FORMATION.reactants) == 2
        assert len(WATER_FORMATION.products) == 1
        assert WATER_FORMATION.delta_h_kj_per_mol == -571.6

    def test_thermodynamic_state(self):
        ts = ThermodynamicState(298.15, delta_g_kj_per_mol=-237.0, spontaneous=True)
        assert ts.spontaneous is True

    def test_kinetic_state(self):
        ks = KineticState(rate_constant_k=0.05, order=1.0, half_life_s=13.86)
        assert ks.order == 1.0

    def test_concept_layer(self):
        cl = ConceptLayer("test", "summary", "detail")
        assert cl.name == "test"

    def test_phases(self):
        assert Phase.GAS.value == "gas"
        assert Phase.AQUEOUS.value == "aqueous"

    def test_electrochemical_cell(self):
        cell = ElectrochemicalCell("Zn→Zn²⁺", "Cu²⁺→Cu", 1.10, 2)
        assert cell.n_electrons == 2


# ════════════════════════════════════════════════════════════════════════
# L1 — Species & Bonds
# ════════════════════════════════════════════════════════════════════════

class TestSpeciesAndBonds:
    def test_parse_formula_h2o(self):
        from chemical_reaction.species_and_bonds import parse_formula
        atoms = parse_formula("H2O")
        assert atoms["H"] == 2.0
        assert atoms["O"] == 1.0

    def test_parse_formula_co2(self):
        from chemical_reaction.species_and_bonds import parse_formula
        atoms = parse_formula("CO2")
        assert atoms["C"] == 1.0
        assert atoms["O"] == 2.0

    def test_mass_balance_water_formation(self):
        from chemical_reaction.species_and_bonds import verify_mass_balance
        assert verify_mass_balance(WATER_FORMATION) is True

    def test_mass_balance_broken(self):
        from chemical_reaction.species_and_bonds import verify_mass_balance
        bad = Reaction(
            reactants=(ReactionTerm(H2, 1.0),),
            products=(ReactionTerm(H2O_L, 1.0),),
        )
        assert verify_mass_balance(bad) is False

    def test_charge_balance_neutral(self):
        from chemical_reaction.species_and_bonds import verify_charge_balance
        assert verify_charge_balance(WATER_FORMATION) is True

    def test_bond_energy_known(self):
        from chemical_reaction.species_and_bonds import bond_energy_kj_per_mol
        assert bond_energy_kj_per_mol("H-H") == 436.0

    def test_bond_energy_unknown_raises(self):
        from chemical_reaction.species_and_bonds import bond_energy_kj_per_mol
        with pytest.raises(KeyError):
            bond_energy_kj_per_mol("X-Y")

    def test_estimate_delta_h_from_bonds(self):
        from chemical_reaction.species_and_bonds import estimate_delta_h_from_bonds
        dh = estimate_delta_h_from_bonds({"H-H": 1.0}, {"H-H": 1.0})
        assert abs(dh) < 1e-9


# ════════════════════════════════════════════════════════════════════════
# L2 — Thermodynamics
# ════════════════════════════════════════════════════════════════════════

class TestThermodynamics:
    def test_gibbs_exergonic(self):
        from chemical_reaction.thermodynamics import gibbs_free_energy
        dg = gibbs_free_energy(-100.0, 50.0, 298.15)
        assert dg < 0

    def test_gibbs_endergonic(self):
        from chemical_reaction.thermodynamics import gibbs_free_energy
        dg = gibbs_free_energy(100.0, -50.0, 298.15)
        assert dg > 0

    def test_is_spontaneous(self):
        from chemical_reaction.thermodynamics import is_spontaneous
        assert is_spontaneous(-10.0) is True
        assert is_spontaneous(10.0) is False

    def test_assess_thermodynamic_state(self):
        from chemical_reaction.thermodynamics import assess_thermodynamic_state
        ts = assess_thermodynamic_state(-571.6, -326.8, 298.15)
        assert ts.spontaneous is True
        assert ts.delta_g_kj_per_mol is not None
        assert ts.delta_g_kj_per_mol < 0

    def test_entropy_sign_heuristic_positive(self):
        from chemical_reaction.thermodynamics import entropy_sign_heuristic
        decompose = Reaction(
            reactants=(ReactionTerm(H2O_L, 2.0),),
            products=(ReactionTerm(H2, 2.0), ReactionTerm(O2, 1.0)),
        )
        assert entropy_sign_heuristic(decompose) == "likely_positive"

    def test_entropy_sign_heuristic_negative(self):
        from chemical_reaction.thermodynamics import entropy_sign_heuristic
        assert entropy_sign_heuristic(WATER_FORMATION) == "likely_negative"

    def test_temperature_crossover(self):
        from chemical_reaction.thermodynamics import temperature_crossover
        t = temperature_crossover(100.0, 200.0)
        assert t is not None
        assert abs(t - 500.0) < 1.0

    def test_temperature_crossover_none(self):
        from chemical_reaction.thermodynamics import temperature_crossover
        assert temperature_crossover(100.0, 0.0) is None

    def test_water_formation_gibbs(self):
        from chemical_reaction.thermodynamics import gibbs_free_energy
        dg = gibbs_free_energy(-571.6, -326.8, 298.15)
        assert -480 < dg < -450

    def test_concept_layers(self):
        from chemical_reaction.thermodynamics import thermodynamic_concept_layers
        layers = thermodynamic_concept_layers()
        assert len(layers) >= 3


# ════════════════════════════════════════════════════════════════════════
# L3 — Kinetics
# ════════════════════════════════════════════════════════════════════════

class TestKinetics:
    def test_arrhenius_basic(self):
        from chemical_reaction.kinetics import arrhenius_rate_constant
        k = arrhenius_rate_constant(1e13, 75.0, 298.15)
        assert k > 0

    def test_arrhenius_higher_temp_faster(self):
        from chemical_reaction.kinetics import arrhenius_rate_constant
        k1 = arrhenius_rate_constant(1e13, 75.0, 298.15)
        k2 = arrhenius_rate_constant(1e13, 75.0, 398.15)
        assert k2 > k1

    def test_arrhenius_lower_ea_faster(self):
        from chemical_reaction.kinetics import arrhenius_rate_constant
        k_high = arrhenius_rate_constant(1e13, 100.0, 298.15)
        k_low = arrhenius_rate_constant(1e13, 50.0, 298.15)
        assert k_low > k_high

    def test_half_life_first_order(self):
        from chemical_reaction.kinetics import half_life
        hl = half_life(0.1, 1.0)
        assert abs(hl - math.log(2) / 0.1) < 1e-9

    def test_half_life_zero_order(self):
        from chemical_reaction.kinetics import half_life
        hl = half_life(0.5, 0.0, initial_conc=10.0)
        assert abs(hl - 10.0) < 1e-9

    def test_half_life_second_order(self):
        from chemical_reaction.kinetics import half_life
        hl = half_life(0.1, 2.0, initial_conc=1.0)
        assert abs(hl - 10.0) < 1e-9

    def test_rate_law(self):
        from chemical_reaction.kinetics import rate_law
        r = rate_law(0.5, [2.0], [1.0])
        assert abs(r - 1.0) < 1e-9

    def test_rate_law_second_order(self):
        from chemical_reaction.kinetics import rate_law
        r = rate_law(0.1, [2.0, 3.0], [1.0, 1.0])
        assert abs(r - 0.6) < 1e-9

    def test_catalyst_ea_reduction(self):
        from chemical_reaction.kinetics import catalyst_ea_reduction
        red = catalyst_ea_reduction(100.0, 60.0)
        assert abs(red - 0.4) < 1e-9

    def test_temperature_rate_ratio(self):
        from chemical_reaction.kinetics import temperature_rate_ratio
        ratio = temperature_rate_ratio(50.0, 298.15, 308.15)
        assert ratio > 1.0

    def test_assess_kinetic_state(self):
        from chemical_reaction.kinetics import assess_kinetic_state
        ks = assess_kinetic_state(1e13, 75.0, 298.15)
        assert ks.rate_constant_k > 0
        assert ks.half_life_s is not None


# ════════════════════════════════════════════════════════════════════════
# L4 — Equilibrium
# ════════════════════════════════════════════════════════════════════════

class TestEquilibrium:
    def test_equilibrium_constant_favorable(self):
        from chemical_reaction.equilibrium import equilibrium_constant
        k = equilibrium_constant(-50.0, 298.15)
        assert k > 1.0

    def test_equilibrium_constant_unfavorable(self):
        from chemical_reaction.equilibrium import equilibrium_constant
        k = equilibrium_constant(50.0, 298.15)
        assert k < 1.0

    def test_reaction_quotient(self):
        from chemical_reaction.equilibrium import reaction_quotient
        q = reaction_quotient([(2.0, 1.0)], [(1.0, 1.0)])
        assert abs(q - 2.0) < 1e-9

    def test_le_chatelier_forward(self):
        from chemical_reaction.equilibrium import le_chatelier_shift
        assert le_chatelier_shift(0.1, 10.0) == "forward"

    def test_le_chatelier_backward(self):
        from chemical_reaction.equilibrium import le_chatelier_shift
        assert le_chatelier_shift(100.0, 10.0) == "backward"

    def test_le_chatelier_equilibrium(self):
        from chemical_reaction.equilibrium import le_chatelier_shift
        assert le_chatelier_shift(10.0, 10.0) == "at_equilibrium"

    def test_van_t_hoff(self):
        from chemical_reaction.equilibrium import van_t_hoff_k_at_new_temp
        k2 = van_t_hoff_k_at_new_temp(1.0, -100.0, 298.15, 398.15)
        assert k2 < 1.0  # exothermic: K decreases with T

    def test_gibbs_from_k(self):
        from chemical_reaction.equilibrium import gibbs_from_k
        dg = gibbs_from_k(1.0, 298.15)
        assert abs(dg) < 1e-9


# ════════════════════════════════════════════════════════════════════════
# L5 — Electrochemistry
# ════════════════════════════════════════════════════════════════════════

class TestElectrochemistry:
    def test_nernst_standard(self):
        from chemical_reaction.electrochemistry import nernst_potential
        e = nernst_potential(1.10, 2, 1.0, 298.15)
        assert abs(e - 1.10) < 1e-6

    def test_nernst_non_standard(self):
        from chemical_reaction.electrochemistry import nernst_potential
        e = nernst_potential(1.10, 2, 0.01, 298.15)
        assert e > 1.10

    def test_cell_voltage(self):
        from chemical_reaction.electrochemistry import cell_voltage
        v = cell_voltage(0.34, -0.76)
        assert abs(v - 1.10) < 1e-9

    def test_faraday_mass(self):
        from chemical_reaction.electrochemistry import faraday_mass_g
        m = faraday_mass_g(10.0, 3600.0, 63.55, 2)
        assert m > 0

    def test_faraday_mol(self):
        from chemical_reaction.electrochemistry import faraday_mol
        mol = faraday_mol(FARADAY_C_PER_MOL, 1.0, 1)
        assert abs(mol - 1.0) < 1e-6

    def test_butler_volmer_zero_eta(self):
        from chemical_reaction.electrochemistry import butler_volmer_current_density
        j = butler_volmer_current_density(0.01, 0.5, 0.5, 0.0)
        assert abs(j) < 1e-12

    def test_butler_volmer_anodic(self):
        from chemical_reaction.electrochemistry import butler_volmer_current_density
        j = butler_volmer_current_density(0.01, 0.5, 0.5, 0.1)
        assert j > 0

    def test_water_electrolysis_minimum_voltage(self):
        from chemical_reaction.electrochemistry import water_electrolysis_minimum_voltage
        v = water_electrolysis_minimum_voltage(298.15)
        assert abs(v - WATER_ELECTROLYSIS_E0_V) < 0.01

    def test_electrolysis_efficiency(self):
        from chemical_reaction.electrochemistry import electrolysis_efficiency
        eff = electrolysis_efficiency(1.23, 1.80)
        assert 0.6 < eff < 0.7

    def test_concept_layers(self):
        from chemical_reaction.electrochemistry import electrochemistry_concept_layers
        layers = electrochemistry_concept_layers()
        assert len(layers) >= 4


# ════════════════════════════════════════════════════════════════════════
# L6 — Screening
# ════════════════════════════════════════════════════════════════════════

class TestScreening:
    def test_positive_claim(self):
        from chemical_reaction.screening import screen_chemical_claim
        payload = ChemicalClaimPayload("Water electrolysis requires 1.23V")
        report = screen_chemical_claim(payload)
        assert report.verdict == Verdict.POSITIVE
        assert report.omega > 0.5

    def test_negative_mass_violation(self):
        from chemical_reaction.screening import screen_chemical_claim
        payload = ChemicalClaimPayload(
            "This reaction creates gold from lead with no energy input",
            violates_mass_conservation=True,
            violates_energy_conservation=True,
        )
        report = screen_chemical_claim(payload)
        assert report.verdict == Verdict.NEGATIVE

    def test_negative_over_unity(self):
        from chemical_reaction.screening import screen_chemical_claim
        payload = ChemicalClaimPayload(
            "This device produces more energy than consumed",
            claims_over_unity=True,
        )
        report = screen_chemical_claim(payload)
        assert report.verdict == Verdict.NEGATIVE

    def test_cautious_perpetual(self):
        from chemical_reaction.screening import screen_chemical_claim
        payload = ChemicalClaimPayload(
            "This reaction runs forever without fuel",
            claims_perpetual_reaction=True,
        )
        report = screen_chemical_claim(payload)
        assert report.verdict == Verdict.CAUTIOUS

    def test_neutral_soft_flag(self):
        from chemical_reaction.screening import screen_chemical_claim
        payload = ChemicalClaimPayload(
            "Reaction proceeds instantly without catalyst",
            ignores_activation_barrier=True,
        )
        report = screen_chemical_claim(payload)
        assert report.verdict == Verdict.NEUTRAL

    def test_multiple_flags_combined(self):
        from chemical_reaction.screening import screen_chemical_claim
        payload = ChemicalClaimPayload(
            "Infinite free energy from water",
            violates_energy_conservation=True,
            claims_over_unity=True,
            claims_perpetual_reaction=True,
        )
        report = screen_chemical_claim(payload)
        assert report.verdict == Verdict.NEGATIVE
        assert report.omega < 0.1

    def test_screening_concept_layers(self):
        from chemical_reaction.screening import screening_concept_layers
        layers = screening_concept_layers()
        assert len(layers) >= 5


# ════════════════════════════════════════════════════════════════════════
# Domain mappings
# ════════════════════════════════════════════════════════════════════════

class TestDomains:
    def test_battery_layers(self):
        from chemical_reaction.domain_battery import battery_domain_layers
        layers = battery_domain_layers()
        assert len(layers) >= 4
        names = [l.name for l in layers]
        assert "ocv_as_nernst" in names
        assert "arrhenius_resistance" in names

    def test_life_support_layers(self):
        from chemical_reaction.domain_life_support import life_support_domain_layers
        layers = life_support_domain_layers()
        assert len(layers) >= 4
        names = [l.name for l in layers]
        assert "water_electrolysis" in names
        assert "sabatier_co2_reduction" in names

    def test_materials_layers(self):
        from chemical_reaction.domain_materials import materials_domain_layers
        layers = materials_domain_layers()
        assert len(layers) >= 4
        names = [l.name for l in layers]
        assert "resin_cure_kinetics" in names
        assert "corrosion_electrochemistry" in names


# ════════════════════════════════════════════════════════════════════════
# Extension hooks
# ════════════════════════════════════════════════════════════════════════

class TestExtensionHooks:
    def test_roadmap_tags(self):
        from chemical_reaction.extension_hooks import extension_roadmap_tags
        tags = extension_roadmap_tags()
        assert len(tags) >= 10

    def test_bridge_notes(self):
        from chemical_reaction.extension_hooks import bridge_notes_for_sibling_engines
        bridges = bridge_notes_for_sibling_engines()
        assert "Battery_Dynamics_Engine" in bridges
        assert "TerraCore_Stack" in bridges
        assert "DIRECT" in bridges["Battery_Dynamics_Engine"]
        assert "CONCEPTUAL" in bridges["Token_Dynamics_Foundation"]


# ════════════════════════════════════════════════════════════════════════
# Foundation
# ════════════════════════════════════════════════════════════════════════

class TestFoundation:
    def test_all_concept_layers(self):
        from chemical_reaction.foundation import all_concept_layers
        layers = all_concept_layers()
        assert len(layers) >= 25

    def test_foundation_no_reaction(self):
        from chemical_reaction.foundation import assess_chemical_foundation
        report = assess_chemical_foundation()
        assert report.layers_inspected >= 25
        assert 0.0 <= report.omega <= 1.0
        assert report.verdict in ("CONSISTENT", "PLAUSIBLE", "QUESTIONABLE", "IMPOSSIBLE")

    def test_foundation_water_formation(self):
        from chemical_reaction.foundation import assess_chemical_foundation
        report = assess_chemical_foundation(WATER_FORMATION, 298.15)
        assert report.verdict == "CONSISTENT"
        assert report.thermodynamic_feasibility != "not_assessed"
        assert report.omega > 0.5
        assert "ΔG" in " ".join(report.notes)

    def test_foundation_sabatier(self):
        from chemical_reaction.foundation import assess_chemical_foundation
        report = assess_chemical_foundation(SABATIER, 500.0)
        assert report.omega > 0.3

    def test_foundation_broken_reaction(self):
        from chemical_reaction.foundation import assess_chemical_foundation
        bad = Reaction(
            reactants=(ReactionTerm(H2, 1.0),),
            products=(ReactionTerm(H2O_L, 1.0),),
            delta_h_kj_per_mol=-100.0,
            delta_s_j_per_mol_k=-50.0,
        )
        report = assess_chemical_foundation(bad, 298.15)
        assert report.key_risk == "conservation_violation"

    def test_foundation_omega_cap(self):
        from chemical_reaction.foundation import assess_chemical_foundation
        report = assess_chemical_foundation(WATER_FORMATION, 298.15)
        assert report.omega <= 0.95


# ════════════════════════════════════════════════════════════════════════
# Health report
# ════════════════════════════════════════════════════════════════════════

class TestHealth:
    def test_health_report_creation(self):
        from chemical_reaction.contracts import ChemicalHealthReport, HealthVerdict
        hr = ChemicalHealthReport(
            omega_thermodynamic=0.8,
            omega_kinetic=0.7,
            omega_equilibrium=0.6,
            omega_conservation=1.0,
            omega_electrochemical=0.5,
            composite_omega=0.72,
            verdict=HealthVerdict.CONSISTENT,
        )
        assert hr.verdict == HealthVerdict.CONSISTENT
        assert hr.composite_omega == 0.72

    def test_health_verdicts(self):
        assert HealthVerdict.CONSISTENT.value == "CONSISTENT"
        assert HealthVerdict.IMPOSSIBLE.value == "IMPOSSIBLE"


# ════════════════════════════════════════════════════════════════════════
# Package integrity
# ════════════════════════════════════════════════════════════════════════

class TestPackageIntegrity:
    def test_version(self):
        from chemical_reaction import __version__
        assert __version__ == "0.2.1"

    def test_public_api_exports(self):
        import chemical_reaction
        assert hasattr(chemical_reaction, "assess_chemical_foundation")
        assert hasattr(chemical_reaction, "ChemicalSpecies")
        assert hasattr(chemical_reaction, "Reaction")
        assert hasattr(chemical_reaction, "Phase")
        assert hasattr(chemical_reaction, "Verdict")

    def test_constants_available(self):
        from chemical_reaction import R_GAS_J_PER_MOL_K, FARADAY_C_PER_MOL
        assert abs(R_GAS_J_PER_MOL_K - 8.314) < 0.01
        assert abs(FARADAY_C_PER_MOL - 96485.0) < 1.0

    def test_all_modules_importable(self):
        from chemical_reaction import species_and_bonds, thermodynamics, kinetics
        from chemical_reaction import equilibrium, electrochemistry, screening
        from chemical_reaction import domain_battery, domain_life_support, domain_materials
        from chemical_reaction import extension_hooks, foundation

    def test_version_file_matches(self):
        from pathlib import Path
        version_path = Path(__file__).resolve().parent.parent / "VERSION"
        assert version_path.read_text().strip() == "0.2.1"
