from __future__ import annotations
import cr_ni_ss
from cr_ni_ss.contracts import ClaimPayload, Grade
from cr_ni_ss.foundation import assess_alloy, run_foundation, screen_claim
def test_version(): assert cr_ni_ss.__version__=='0.1.0'
def test_grade_risk(): assert assess_alloy(Grade.SS430).pitting_risk=='high'
def test_screening(): assert 'pitting_denial' in screen_claim(ClaimPayload('',claimed_no_pitting=True)).flags
def test_run(): assert run_foundation().health is not None
