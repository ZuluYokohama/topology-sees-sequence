# Empirical continuation notes

## Backbone-only NLL (empirical density from same designed set)

Built a 36×36 histogram over (φ,ψ) from 1551 residues in 131 local AF PDBs.
Scored each structure as sum of −log p under that density.

| Spearman | ρ |
|----------|---|
| E_ref vs nll_sum | −0.45 |
| E_ref vs nll_mean | **+0.36** |
| nll_mean vs N | **−0.62** |
| nll_sum vs N | +0.95 |

### How to read this (not independent strain evidence)

- These are **descriptive** associations on a design-compressed cohort. They are **not** independent evidence that E_ref is a physical strain observable.
- `nll_sum` is intrinsically length-dependent (ρ(nll_sum, N) = +0.95). Prefer per-residue `nll_mean`.
- ρ(nll_mean, N) = −0.62 is a **substantial** length association, not mild. Any E_ref ↔ nll_mean reading should be length-controlled (within-N or residualize on N) before interpretation.
- Density is fit from the **same** designed set (self-score). Leave-one-structure-out or an external rama density is required before claiming out-of-sample unusualness.
- Structure-level n = 131 for NLL tables; n = 450 for E_ref vs Bishop / Rosetta totals elsewhere.

## Experimental CCDC (no sequences in CIF parse)

Bishop θ still: RH12_1 ≈ 0°, RH7 enantiomer pair ±83°, RAR13 four chains 132–137°.
Reproduce with `python run_p1.py` (configured `IDS` only; atomic CIF download).

## Still needed for P2

- Rosetta rama / omega terms only (definitions in `P2_PROTOCOL.md`)
- Or E(cyclized) − E(linear) under the fixed A2 pipeline
- Or experimental cyclization yields under the fixed B1 response
