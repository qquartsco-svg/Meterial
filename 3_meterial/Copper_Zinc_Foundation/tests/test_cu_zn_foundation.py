from __future__ import annotations
import cu_zn
from cu_zn.contracts import CuZnClaimPayload
from cu_zn.foundation import assess_conductivity, run_cu_zn_foundation, screen_cu_zn_claim

def test_version(): assert cu_zn.__version__=='0.1.0'
def test_conductivity(): assert assess_conductivity(0.9).conductivity_ms_m > assess_conductivity(0.6).conductivity_ms_m
def test_screening(): assert 'conductivity_myth' in screen_cu_zn_claim(CuZnClaimPayload('',claimed_perfect_conductivity=True)).flags
def test_run(): assert run_cu_zn_foundation().health is not None
