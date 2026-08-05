# Tier A-lite: geometric backbone torsional energy

No Rosetta. Pure geometry:

```text
E_bb = Σ_i [ kφ * angdist(φ_i, φ*_i)² + kψ * angdist(ψ_i, ψ*_i)²
             + kω * min_j angdist(ω_i, ω*_j)² ]
```

Definitions (match `derive.py` REF basins; angular distance is the signed wrap to (−π, π]):

- Nearest rama basin (φ*, ψ*): Gly → (−82°, 8°), Pro → (−65°, 145°), else → (−63°, −43°) — same as `derive.REF`.
- Distances are **separate** periodic angular distances on φ and on ψ (not a single 2D torus geodesic), weighted by kφ, kψ.
- ω targets {0, ±π}; `angdist(ω, target)` uses the same wrap; take the minimum over targets.
- Default coefficients used in the 131-structure run: kφ = kψ = 1, kω = 1 (unitless relative score).

Run on 131 local AF PDBs with extracted dihedrals (local cohort; structure IDs not checked into this branch — treat n=131 as the sample size label only until a manifest is committed).

## Results

| Pair | Spearman ρ |
|------|------------|
| E_ref vs E_bb_mean (pooled) | +0.17 (borderline vs shuffle) |
| E_ref vs E_bb_sum (pooled) | −0.37 (**length-confounded**; sum scales with N) |
| **Within-N mean** (E_ref, E_bb_mean) | **+0.07** |
| E_bb_mean vs #Pro | +0.67 |

Shuffle 95% interval for **pooled** E_ref vs E_bb_mean: [−0.17, +0.17]. Observed +0.17 sits on the edge of that pooled null; the within-N mean (+0.07) is the cleaner null comparison and does **not** clear a strong association.

## Reading

On this post-design / post-relaxation sample, deposited backbone torsions do **not** clearly retain reference-connection strain after within-N residualization. That is **consistent with** generators and relaxers compressing backbone strain (hypothesis — not established by pre/post-relaxation pairs here).

This is **not** a fail of P2 against a true force-field rama term or cyclized−linear ΔE — those remain the Tier A targets in `P2_PROTOCOL.md`.

It **does** show that a geometry-only score on deposited designed coordinates is a weak instrument for E_ref, parallel to why Bishop-on-closed was the wrong object.

## Implication

The informative comparison is **pre-relaxation** or **sequence-only** (E_ref) vs an energy that still sees backbone strain (Rosetta rama term on unrelaxed poses, or explicit cyclic vs linear). Deposited AF scaffolds are the wrong slice for that test — same lesson as the holonomy category error, now for energy.
