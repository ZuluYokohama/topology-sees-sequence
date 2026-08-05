# Prediction 2 — Experiment Protocol

## Goal

Test whether **reference-connection strain** `E_ref` (or its rotational residual θ_ref) predicts a **backbone-specific** energy or experimental cyclization difficulty.

## Why not Rosetta total / Bishop-on-closed

- Rosetta total fails the positive control against rama deviation (ρ ≈ 0.1).
- Bishop holonomy on deposited closed coordinates is a different object from reference θ (ρ ≈ 0 vs E_ref, n=450).

## Instrument: E_ref

```python
from derive import strain
r = strain(sequence)  # E, theta_deg, gap
```

Preferred geometry: Ala/X ≈ (−63°, −43°), Gly ≈ (−82°, 8°), Pro ≈ (−65°, 145°), ω = π (trans).  
Optional: cis-Pro (ω = 0) reduces poly-Pro E dramatically (∼325 → ∼38) — report both.

## Tier A — cheapest computational (preferred next)

### A1. Rosetta rama + omega terms only

For each designed structure:
1. Extract `rama` and `omega` score terms (not total).
2. Correlate with E_ref and θ_ref (Spearman, within-N and pooled).
3. Positive control: rama term vs geometric rama deviation must be strong.

**Pass criterion:** Spearman(E_ref, rama_term) significantly > 0 after within-N residualization, and positive control holds.

### A2. Cyclized − linear backbone ΔE

1. Take sequence S, build linear extended or AF-linear model.
2. Cyclize with same FF (or restrain termini) and relax backbone-only if possible.
3. ΔE = E_cyclic − E_linear (backbone terms).
4. Correlate ΔE with E_ref.

**Pass criterion:** positive Spearman, stable across N bins.

## Tier B — experimental

### B1. Effective molarity / cyclization yield

Plot log(yield) or effective molarity vs E_ref (or θ_ref²/N).  
Compare slope to Jacobson–Stockmayer reference (entropy-dominated 1/N scaling).

**Pass criterion:** residual variance after N-scaling still tracks sequence-level E_ref.

## Tier C — controls (required alongside A/B)

1. **Shuffle sequences** preserving N: destroy sequence→E_ref link; correlation with energy must collapse.
2. **Within-N only:** report per-N Spearman so N-confounding cannot fake a hit.
3. **cis-Pro sensitivity:** recompute E_ref with ω=0 for Pro; if conclusions flip, report both.

## Current baselines (do not treat as P2)

| Observation | n | ρ |
|-------------|---|---|
| E_ref vs Rosetta total | 450 | −0.10 |
| E_ref vs Bishop E | 450 | 0.00 |
| E_ref vs empirical NLL/residue | 131 | +0.36 |
| E_ref vs frac_gly | 450 | +0.37 |
| E_ref vs frac_pro (within-N mean) | 450 | +0.06 |

## Decision rule

- **Support:** Tier A or B pass + controls.
- **Fail:** Tier A with valid positive control shows null/negative after within-N residualization.
- **Untested:** anything that only uses Rosetta total or Bishop-on-closed.
