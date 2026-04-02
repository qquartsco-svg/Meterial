from __future__ import annotations
import mcn
from mcn.contracts import Chemistry, MCNClaimPayload
from mcn.foundation import assess_cathode, run_mcn_foundation, screen_mcn_claim

def test_version(): assert mcn.__version__=='0.1.0'
def test_ni_energy_tradeoff(): assert assess_cathode(Chemistry.NMC811).specific_energy_wh_kg > assess_cathode(Chemistry.NMC111).specific_energy_wh_kg
def test_screening(): assert 'supply_denial' in screen_mcn_claim(MCNClaimPayload('',claimed_no_supply_risk=True)).flags
def test_run(): assert run_mcn_foundation().health is not None
