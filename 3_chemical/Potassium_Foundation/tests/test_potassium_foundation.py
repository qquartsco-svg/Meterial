from __future__ import annotations
import potassium
from potassium.contracts import PotassiumClaimPayload
from potassium.foundation import assess_electrolyte, run_potassium_foundation, screen_potassium_claim

def test_version(): assert potassium.__version__=='0.1.0'
def test_electrolyte(): assert assess_electrolyte(4.2).risk_level=='low'
def test_screening(): assert 'electrolyte_denial' in screen_potassium_claim(PotassiumClaimPayload('',claimed_no_hyperkalemia_risk=True)).flags
def test_run(): assert run_potassium_foundation().health is not None
