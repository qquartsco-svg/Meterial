from __future__ import annotations
import potash_kcl
from potash_kcl.contracts import ClaimPayload
from potash_kcl.foundation import run_foundation, screen_claim
def test_version(): assert potash_kcl.__version__=='0.1.0'
def test_screening(): assert 'potash_abundance_myth' in screen_claim(ClaimPayload('',claimed_trivial_ocean_kcl_without_energy=True)).flags
def test_run(): assert run_foundation().health is not None
