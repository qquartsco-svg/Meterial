from __future__ import annotations
import carbon_element
from carbon_element.contracts import ClaimPayload
from carbon_element.foundation import run_foundation, screen_claim
def test_version(): assert carbon_element.__version__=='0.1.0'
def test_screening(): assert 'co2_element_conflation' in screen_claim(ClaimPayload('',claimed_co2_is_elemental_carbon=True)).flags
def test_run(): assert run_foundation().health is not None
