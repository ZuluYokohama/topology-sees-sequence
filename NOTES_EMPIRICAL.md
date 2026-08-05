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

Per-residue empirical unusualness falls mildly with N; reference strain correlates positively with per-residue NLL at modest strength. Caveat: density is from the designed set itself, not a physical rama potential.

## Experimental CCDC (no sequences in CIF parse)

Bishop θ still: RH12_1 ≈ 0°, RH7 enantiomer pair ±83°, RAR13 four chains 132–137°.

## Still needed for P2

- Rosetta rama / omega terms only
- Or E(cyclized) − E(linear) under any backbone-capable FF
- Or experimental cyclization yields
