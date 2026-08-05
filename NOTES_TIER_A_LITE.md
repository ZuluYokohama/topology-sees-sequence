# Tier A-lite: geometric backbone torsional energy

No Rosetta. Pure geometry:

```
E_bb = Σ_i [ (kφ+kψ) * dist²(to nearest rama basin) + kω * dist²(ω, {0,±π}) ]
```

Run on 131 local AF PDBs with extracted dihedrals.

## Results

| Pair | Spearman ρ |
|------|------------|
| E_ref vs E_bb_mean | +0.17 (borderline vs shuffle) |
| E_ref vs E_bb_sum | −0.37 |
| **Within-N mean** (E_ref, E_bb_mean) | **+0.07** |
| E_bb_mean vs #Pro | +0.67 |

Shuffle 95% for pooled E_ref vs E_bb_mean: [−0.17, +0.17]. True +0.17 sits on the edge.

## Reading

Post-design / post-relaxation structures do **not** clearly retain reference-connection strain in observed backbone torsions after within-N residualization. That is expected if generators and relaxers compress backbone strain.

This is **not** a fail of P2 against a true force-field rama term or cyclized−linear ΔE — those remain the Tier A targets in `P2_PROTOCOL.md`.

It **does** show that a geometry-only score on deposited designed coordinates is a weak instrument for E_ref, parallel to why Bishop-on-closed was the wrong object.

## Implication

The informative comparison is **pre-relaxation** or **sequence-only** (E_ref) vs an energy that still sees backbone strain (Rosetta rama term on unrelaxed poses, or explicit cyclic vs linear). Deposited AF scaffolds are the wrong slice for that test — same lesson as the holonomy category error, now for energy.
