# E_ref as sequence prior (not P2 on deposited AF)

**Date:** 5 August 2026  
**Context:** PR #1 merged. Geometry done. Deposited AF / total-score P2 parked.

## Call

Treat **E_ref** as a **sequence-level prior** (slice 0). Do not force Prediction 2 on already-closed, already-relaxed coordinates. More PDBs will not fix that category error.

## Cohorts

| Cohort | Source | n | How scored |
|--------|--------|---|------------|
| Experimental | `afcycpep_data_experimental.csv` (HF AfCycDesign) | 8 | all sequences |
| Hallucinated sample | `afcycpep_data_hallucinated.csv` | 400 | ≤40 per N∈[7,16], seed 0 |
| Random (hall-matched N) | uniform 20 AA | 400 | same N multiset as hall sample |
| Random (exp-matched N) | uniform 20 AA | 400 | 50 draws per experimental N |

Instrument: `derive.strain(seq)` default `omega_mode='trans'`. No coordinates, no force field.

Reproduce:

```bash
python scripts/eref_prior.py   # or re-run analysis that wrote data/eref_*.csv
```

Artifacts: `data/eref_prior_summary.csv`, `data/eref_experimental.csv`, `data/eref_hall_sample.csv`.

## Results (sequence only)

| Cohort | n | mean E | median | p10 | p90 | frac E>1 | frac E>5 | frac E>20 |
|--------|---|--------|--------|-----|-----|----------|----------|-----------|
| experimental | 8 | 1.726 | 1.635 | 1.07 | 2.62 | 87.5% | 0% | 0% |
| hallucinated sample | 400 | 1.637 | 1.346 | 0.77 | 2.92 | 71.3% | 0.8% | 0% |
| random (hall N) | 400 | 1.176 | 1.037 | 0.41 | 2.20 | 54.3% | 0.3% | 0% |
| random (exp N) | 400 | 1.196 | 1.050 | 0.41 | 2.12 | 55.8% | 0.5% | 0% |

### Within-N: hall mean − random mean

Every N in 7–16: **hall mean E_ref ≥ random mean** (largest gap at short rings N=7–9, Δ ≈ +0.9–1.1; shrinks toward ~+0.1 at N=16).

### Composition (why hall sits above random)

| Cohort | mean f_Pro | mean f_Gly |
|--------|------------|------------|
| hall | 0.110 | 0.101 |
| random | 0.046 | 0.056 |
| experimental | 0.156 | 0.131 |

Hall ρ(E_ref, f_Pro) ≈ 0.28; ρ(E_ref, f_Gly) ≈ 0.31. Random ρ(E_ref, f_Pro) ≈ 0.56 (composition drives more of random variance).

### Experimental table (all 8)

| ID | Sequence | N | E_ref |
|----|----------|---|-------|
| RH7_1 | WMPGRDP | 7 | 0.834 |
| RH13_1 | EYDAAGRLDPATG | 13 | 1.175 |
| RAR13_1 | TDPEDVLRGLPGA | 13 | 1.176 |
| RH8_1 | DPRDPWTG | 8 | 1.562 |
| RH12_1 | DIYYPEYNMRIG | 12 | 1.709 |
| RH11_1 | LPGTEWERMHG | 11 | 2.069 |
| RH9_1 | LAWIMPELG | 9 | 2.586 |
| RH10_1 | LPDPRWADLG | 10 | 2.698 |

## Interpretation (honest)

1. **E_ref is usable as a sequence prior** — no structure required; ranks are well-defined and extreme poly-Pro territory (E ≫ 20) is empty in both hall and experimental sets.
2. **“Generators avoid high E_ref” is not supported** on this sample. Hallucinated and experimental sequences sit **above** length-matched random AA in mean/median E_ref, largely with **elevated Pro/Gly fraction**, not with systematic selection against reference strain.
3. What *is* avoided is the **extreme tail** (poly-Pro-like E ~ 10²). That is a weak, composition-bounded claim — not a pass of P2.
4. **Do not** read these distributions as backbone energy evidence. They are geometric obstruction scores on sequences only.

## Parked

| Item | Status |
|------|--------|
| P2 vs Rosetta total / Bishop-on-closed / deposited AF E_bb | Invalid or exhausted slice |
| P2 vs rama/omega terms or cyclized−linear ΔE | Deferred until instrument exists |
| OpenMM/FF install in this sandbox | Not pursued for a weak ρ chase |
| Literature yields vs E_ref | Open later (Tier B) |

## Middle-out reminder

```
Slice 0  E_ref, θ_ref, gap     ← sequence prior (this note)
Slice 1  composition features  ← Pro/Gly features only
Slice 2  observed coordinates  ← never substitute for slice 0
Slice 3  backbone-only energy  ← P2 when available
```

## One-line

**Merge done; E_ref ranks sequences without coordinates; designed sets are not low-E_ref relative to random — they are composition-shifted and extreme-tail-light; true P2 stays parked.**
