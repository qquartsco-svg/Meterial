from __future__ import annotations
import ammonia_plant
from ammonia_plant.contracts import ClaimPayload
from ammonia_plant.foundation import run_foundation, screen_claim
def test_version(): assert ammonia_plant.__version__=='0.1.0'
def test_screening(): assert 'haber_energy_denial' in screen_claim(ClaimPayload('',claimed_zero_energy_ammonia=True)).flags
def test_run(): assert run_foundation().health is not None
