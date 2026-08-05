# Prediction 2 — Experiment Protocol

## Goal

Test whether **reference-connection strain** `E_ref` (or its rotational residual θ_ref) predicts a **backbone-specific** energy or experimental cyclization difficulty.

## Why not Rosetta total / Bishop-on-closed

- Rosetta total fails the positive control against rama deviation (ρ ≈ 0.1).
- Bishop holonomy on deposited closed coordinates is a different object from reference θ (ρ ≈ 0 vs E_ref, n=450).

## Instrument: E_ref

```python
from derive import strain
r = strain(sequence)                       # default omega_mode='trans' (ω=π all residues)
r = strain(sequence, omega_mode='cis_pro') # ω=0 for Pro, ω=π otherwise
# E, theta_deg, gap
```

Preferred geometry: Ala/X ≈ (−63°, −43°), Gly ≈ (−82°, 8°), Pro ≈ (−65°, 145°).  
Default ω = π (trans). Alternate path: `omega_mode='cis_pro'` (implemented in `derive.py`). Report both when poly-Pro drives conclusions (see `NOTES_CIS_PRO.md`).

## Statistical decision rules (fixed before Support/Fail)

| Rule | Definition |
|------|------------|
| Residualization | Within each N, residualize both variables on N (or use within-N Spearman only). Primary report is **within-N mean Spearman**. |
| α | 0.05 two-sided; report bootstrap 95% CI on Spearman (10 000 resamples, seed 0). |
| Effect size (pass floor) | Within-N mean \|ρ\| ≥ 0.30 **and** CI excludes 0. |
| Positive control floor | Same thresholds for rama_term vs geometric rama deviation. |
| Min per-N bin | n ≥ 15 structures per N for that N to enter the within-N mean. |
| Multiple testing | Two primary endpoints only (A1 or A2 or B1 — one chosen a priori); no other pairs claim “pass” without Bonferroni. |
| Shuffle control | 1000 sequence shuffles preserving N; observed ρ must exceed 97.5th percentile of null (two-sided 5%). |

Replace qualitative “strong / stable / tracks” with the table above.

## Tier A — cheapest computational (preferred next)

### A1. Rosetta rama + omega terms only

**Term definitions (fixed):**

- `rama_term` = sum of Rosetta `rama` score over all residues in the cyclic chain (no /N; termini included if present in the pose).
- `omega_term` = sum of Rosetta `omega` score over the same residues.
- Optional secondary: `rama_mean = rama_term / N`, `omega_mean = omega_term / N` (report but do not pass on means alone).

For each designed structure:
1. Extract `rama_term` and `omega_term` as defined above (not total).
2. Correlate with E_ref and θ_ref (Spearman, within-N and pooled).
3. Positive control: `rama_term` vs geometric rama deviation must pass the positive-control floor.

**Pass criterion:** within-N mean Spearman(E_ref, rama_term) meets effect-size floor **and** positive control holds **and** shuffle control holds.

### A2. Cyclized − linear backbone ΔE (fixed pipeline)

One pipeline only — no “or” branches at evaluation time:

1. **Linear model:** extended polypeptide of sequence S, ACE/NME caps, no disulfide.
2. **Cyclic model:** head-to-tail peptide bond on the same sequence; no side-chain cyclization.
3. **Force field / score:** Rosetta ref2015, score terms `rama`, `omega`, `cart_bonded` only (sum → E_bb).
4. **Relaxation:** CartesianMinimizeMover, backbone + χ free, 200 steps max; fail if score diverges or pose has chainbreak > 0.5 Å after minimize.
5. **ΔE** = E_bb(cyclic, post-relax) − E_bb(linear, post-relax). Failed relax → missing; do not impute.
6. Correlate ΔE with E_ref under the statistical rules above.

**Pass criterion:** within-N mean Spearman(E_ref, ΔE) meets effect-size floor + shuffle control.

## Tier B — experimental

### B1. Cyclization yield (single response)

**Response variable (fixed):** `log10(yield)` where yield is the fraction of cyclized product over starting linear precursor from a single HPLC assay, concentration 1 mM precursor, 25 °C, 24 h, mean of ≥3 technical replicates; values below LOQ censored at LOQ and flagged.

Do **not** swap in effective molarity under the same pass criterion without a new pre-registration (EM requires an explicit concentration model and is a different endpoint).

Plot `log10(yield)` vs E_ref (or θ_ref²/N). Compare residual after regressing out 1/N (Jacobson–Stockmayer-style) to sequence-level E_ref.

**Pass criterion:** residual Spearman(E_ref, log10(yield) | 1/N) meets effect-size floor + shuffle control.

## Tier C — controls (required alongside A/B)

1. **Shuffle sequences** preserving N: destroy sequence→E_ref link; correlation with energy must collapse (see statistical table).
2. **Within-N only:** report per-N Spearman so N-confounding cannot fake a hit.
3. **cis-Pro sensitivity:** recompute E_ref with `omega_mode='cis_pro'`; if conclusions flip, report both.

## Current baselines (do not treat as P2)

| Observation | n | ρ |
|-------------|---|---|
| E_ref vs Rosetta total | 450 | −0.10 |
| E_ref vs Bishop E | 450 | 0.00 |
| E_ref vs empirical NLL/residue | 131 | +0.36 |
| E_ref vs frac_gly | 450 | +0.37 |
| E_ref vs frac_pro (within-N mean) | 450 | +0.06 |

## Decision rule

- **Support:** Tier A or B pass + controls under the fixed statistical rules.
- **Fail:** Tier A with valid positive control shows null/negative after within-N residualization.
- **Untested:** anything that only uses Rosetta total or Bishop-on-closed.
