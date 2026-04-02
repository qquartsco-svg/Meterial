from __future__ import annotations
import ft_liquids
from ft_liquids.contracts import ClaimPayload
from ft_liquids.foundation import run_foundation, screen_claim
def test_version(): assert ft_liquids.__version__=='0.1.0'
def test_screening(): assert 'selectivity_fantasy' in screen_claim(ClaimPayload('',claimed_only_diesel_no_light_ends=True)).flags
def test_run(): assert run_foundation().health is not None
