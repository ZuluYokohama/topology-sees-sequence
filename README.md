# Topology / Holonomy of Cyclic Peptides

Research code for geometric obstruction in cyclic peptide backbones.

## Corrected core claims (Aug 2026)

1. **Reference-connection strain** — the residual SE(3) screw of the product of residue transforms with every residue at preferred Ramachandran geometry — is the geometrically right obstruction object (`derive.py`). It is strongly sequence-dependent (poly-Pro ≫ poly-Ala).

2. **Bishop holonomy** of the deposited CA curve is a real, reproducible geometric invariant (transport ↔ Gauss–Bonnet to 1e−15) but is **not** the sheaf θ of the abelian paper. On AF-designed closed scaffolds it shows approximately zero Spearman correlation with reference strain (ρ ≈ 0, n=450) — descriptive association, not a claim of statistical independence under a pre-registered null.

3. **ψ ≈ φ closure locus** — pure geometry: 182 uniform rise≈0 solutions for N=5–16, 100% with |ψ−φ| < 15°.

4. **Combinatorial proline count** is not a free topological invariant.

5. **Rosetta total score** does not track backbone strain; P2 against it is invalid.

See `STATUS_P1_P2.md`, `CORRECTIONS.md`, `CORRECTION_NOTE.md`, and `NOTES_EMPIRICAL.md`.

**Operating call (post-merge):** use **E_ref as a sequence prior** — do not force P2 on deposited AF structures. See `NOTES_EREF_PRIOR.md`.

## Quick start

```bash
pip install numpy scipy
python derive.py          # reference strain on poly-A / sequence variants
python middle_out_v2.py   # slice 0 = E_ref (not n_Pro)
python run_p1.py          # Bishop on experimental CCDC CIFs (needs network)
python scripts/eref_prior.py   # sequence prior: exp vs hall vs random (needs data/*.csv)
```

## Empirical notes

| Test | Result |
|------|--------|
| E_ref vs Bishop E (n=450) | ρ ≈ 0 |
| E_ref vs Rosetta total | ρ ≈ −0.10 |
| Empirical rama NLL/residue vs N (n=131) | ρ ≈ −0.62 (length association; see NOTES_EMPIRICAL) |
| E_ref vs NLL/residue | ρ ≈ +0.36 (descriptive; density fit on same set) |

P2 is **parked** until a backbone-visible energy (rama/omega terms, cyclized−linear ΔE) or literature yields exist. Do not chase deposited AF totals. Details: `P2_PROTOCOL.md`, `NOTES_EREF_PRIOR.md`.

## Layout

- `derive.py` — reference-connection strain (`omega_mode='trans'|'cis_pro'`)
- `holonomy_extract.py` / `run_p1.py` — Bishop measurement
- `middle_out_pipeline.py` — SE(3) kinematic slices
- `STATUS_P1_P2.md` / `CORRECTIONS.md` — status and corrections log
- `NOTES_EMPIRICAL.md` / `NOTES_CIS_PRO.md` / `NOTES_TIER_A_LITE.md` — empirical notes
- `NOTES_EREF_PRIOR.md` — E_ref as sequence prior (designed vs exp vs random); P2 parked
- `P2_PROTOCOL.md` — pre-registered P2 (deferred until backbone-visible energy or yields)
- `CODE_REVIEW.md` — multi-domain review

## License

Research code — use with attribution.
