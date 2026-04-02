from __future__ import annotations
import npk_eutro
from npk_eutro.contracts import ClaimPayload
from npk_eutro.foundation import run_foundation, screen_claim
def test_version(): assert npk_eutro.__version__=='0.1.0'
def test_screening(): assert 'eutrophication_denial' in screen_claim(ClaimPayload('',claimed_fertilizer_never_causes_algae=True)).flags
def test_run(): assert run_foundation().health is not None
