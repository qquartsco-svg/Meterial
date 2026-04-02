from __future__ import annotations
import sulfur
from sulfur.contracts import SulfurClaimPayload
from sulfur.foundation import assess_li_s_battery, run_sulfur_foundation, screen_sulfur_claim

def test_version(): assert sulfur.__version__=='0.1.0'
def test_lis_profile(): assert assess_li_s_battery().specific_energy_wh_kg > 300
def test_screening(): assert 'so2_denial' in screen_sulfur_claim(SulfurClaimPayload('',claimed_zero_so2_pollution=True)).flags
def test_run(): assert run_sulfur_foundation().health is not None
