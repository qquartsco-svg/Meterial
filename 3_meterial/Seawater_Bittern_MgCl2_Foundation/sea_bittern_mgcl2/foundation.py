from typing import List, Optional

from .contracts import *


def assess_concentrate() -> ConcentrateAssessment:
    return ConcentrateAssessment(
        'Solar ponds and multi-effect stages concentrate halides; late bittern enriches Mg/Ca/SO4 tails.',
        'MgCl2·6H2O and bischofite paths compete with carnallite/K carnallite families in some deposits.',
        [
            'Read after Potassium_Chloride_Brine_Foundation; seawater grammar overlaps Iodine_Bromine_Foundation.',
        ],
    )


def assess_disposal() -> DisposalAssessment:
    return DisposalAssessment(
        'RO concentrate and salt-works discharge need dilution, mixing zones, or solidification strategies.',
        'Hygroscopic MgCl2 loads accelerate steel corrosion; dust and runoff chemistry differ from NaCl-only tales.',
        ['Policy narratives of "infinite dilution" ignore density plumes and benthic stress.'],
    )


def screen_claim(p: ClaimPayload) -> ScreeningReport:
    flags: List[str] = []
    reasons: List[str] = []
    omega = 0.64
    if p.claimed_bittern_mg_without_energy:
        flags.append('bittern_energy_denial')
        omega -= 0.3
        reasons.append(
            'Concentrating Mg from seawater or reject brines is evaporation, membrane, or thermal work—not free.'
        )
    if p.claimed_seawater_mg_instant_pure:
        flags.append('reject_brine_fantasy')
        omega -= 0.26
        reasons.append('Mg products still carry halide/sulfate matrices; purification and waste streams are real.')
    v = (
        Verdict.POSITIVE
        if omega >= 0.65 and not flags
        else (
            Verdict.NEUTRAL
            if omega >= 0.45
            else (Verdict.CAUTIOUS if omega >= 0.25 else Verdict.NEGATIVE)
        )
    )
    if not reasons:
        reasons.append('No specific issues detected.')
    return ScreeningReport(v, round(max(omega, 0), 3), flags, reasons)


def collect_layers() -> List[ConceptLayer]:
    return [
        ConceptLayer('Bittern ladder', 'NaCl harvest leaves Mg-dominant liquors with distinct handling.'),
        ConceptLayer('Desalination coupling', 'Permeate fresh water and reject brine are joint products.'),
    ]


def compute_health(
    sup=0.55, proc=0.54, qual=0.52, env=0.48, econ=0.53
) -> HealthReport:
    axes = [sup, proc, qual, env, econ]
    c = round(sum(axes) / len(axes), 3)
    v = (
        HealthVerdict.HEALTHY
        if c >= 0.7 and min(axes) >= 0.4
        else (
            HealthVerdict.STABLE
            if c >= 0.5
            else (HealthVerdict.FRAGILE if c >= 0.3 else HealthVerdict.CRITICAL)
        )
    )
    return HealthReport(sup, proc, qual, env, econ, c, v)


def run_foundation(claim: Optional[ClaimPayload] = None) -> FoundationReport:
    conc = assess_concentrate()
    disp = assess_disposal()
    sc = screen_claim(claim) if claim else None
    h = compute_health()
    return FoundationReport(conc, disp, sc, h, collect_layers())
