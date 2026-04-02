"""Fundamental physical constants used across chemistry layers."""

from __future__ import annotations

R_GAS_J_PER_MOL_K: float = 8.314462618  # universal gas constant [J/(mol·K)]
R_GAS_KJ_PER_MOL_K: float = R_GAS_J_PER_MOL_K / 1000.0

KB_J_PER_K: float = 1.380649e-23  # Boltzmann constant [J/K]
KB_EV_PER_K: float = 8.617333262e-5  # Boltzmann constant [eV/K]

FARADAY_C_PER_MOL: float = 96485.33212  # Faraday constant [C/mol]

AVOGADRO: float = 6.02214076e23  # Avogadro number [1/mol]

PLANCK_J_S: float = 6.62607015e-34  # Planck constant [J·s]

STANDARD_TEMPERATURE_K: float = 298.15  # 25 °C
STANDARD_PRESSURE_PA: float = 101325.0  # 1 atm

WATER_ELECTROLYSIS_E0_V: float = 1.229  # standard reversible potential for water splitting
