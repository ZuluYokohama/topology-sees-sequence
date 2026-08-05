# Topology / Holonomy of Cyclic Peptides

Research code for geometric obstruction in cyclic peptide backbones.

## Corrected core claims (Aug 2026)

1. **Reference-connection strain** — the residual SE(3) screw of the product of residue transforms with every residue at preferred Ramachandran geometry — is the geometrically right obstruction object (`derive.py`). It is strongly sequence-dependent (poly-Pro ≫ poly-Ala).

2. **Bishop holonomy** of the deposited CA curve is a real, reproducible geometric invariant (transport ↔ Gauss–Bonnet to 1e−15) but is **not** the sheaf θ of the abelian paper and is empirically independent of reference strain on AF-designed closed scaffolds (ρ ≈ 0, n=450).

3. **ψ ≈ φ closure locus** — pure geometry: 182 uniform rise≈0 solutions for N=5–16, 100% with |ψ−φ| < 15°.

4. **Combinatorial proline count** is not a free topological invariant.

5. **Rosetta total score** does not track backbone strain; P2 against it is invalid.

See `STATUS_P1_P2.md` and `CORRECTIONS.md`.

## Quick start

```bash
pip install numpy scipy
python derive.py          # reference strain on poly-A / sequence variants
python run_p1.py          # Bishop on experimental CCDC CIFs (needs network)
python middle_out_pipeline.py   # earlier kinematic stack (model object)
```

## Empirical notes

| Test | Result |
|------|--------|
| E_ref vs Bishop E (n=450) | ρ ≈ 0 |
| E_ref vs Rosetta total | ρ ≈ −0.10 |
| Empirical rama NLL/residue vs N (n=131) | ρ ≈ −0.62 (mild dilution of *unusualness*) |
| E_ref vs NLL/residue | ρ ≈ +0.36 |

P2 remains **untested** against a true backbone energy (rama/omega terms or cyclized−linear ΔE).

## Layout

- `derive.py` — reference-connection strain
- `holonomy_extract.py` / `run_p1.py` — Bishop measurement
- `middle_out_pipeline.py` — SE(3) kinematic slices
- `STATUS_P1_P2.md` / `CORRECTIONS.md` — status and corrections log
- `CODE_REVIEW.md` — multi-domain review

## License

Research code — use with attribution.
