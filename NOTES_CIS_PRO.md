# cis-Pro sensitivity of reference strain

Exact inputs for the poly-Pro comparison (`derive.strain`, N=12):

| Case | Sequence | omega_mode | Per-residue ω | E_ref (approx) |
|------|----------|------------|---------------|----------------|
| all-trans | `P`×12 | `trans` | ω=π for all 12 residues | ≈ 325 |
| cis-Pro | `P`×12 | `cis_pro` | ω=0 for all Pro (here all 12) | ≈ 38 |

Reproduce:

```bash
python -c "from derive import strain; print(strain('P'*12)); print(strain('P'*12, omega_mode='cis_pro'))"
```

Other sequences change less under `cis_pro`. Conclusions that lean on poly-Pro extremity must report both ω conventions.

On the AF-designed n=450 set, frac_gly **correlates with** E_ref more than frac_pro (Spearman ρ +0.37 vs +0.17 pooled; within-N Pro mean ρ only +0.06). Association language only — no pre-selection / predictive claim without the generator’s selection criterion.
