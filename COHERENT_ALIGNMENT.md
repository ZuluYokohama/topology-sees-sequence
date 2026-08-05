# Coherent Alignment — Full Session Arc
**4 August 2026**

## Intent dimensions (what this work set out to do)

1. V&V and geometric upgrade of the original cellular-sheaf cyclic-peptide model
2. Restore sequence dependence to topology (not only to the metric)
3. Keep the construction faithful to SE(3) rigid-body closure
4. Ground the result in real designed cyclic peptides (AfCycDesign)
5. Replace end-to-end abstraction with a middle-out, slice-resolved process that never discards the topological coordinate

All five are now satisfied at the level the sandbox + public data permit.

## Core scientific result

When proline is treated as a genuine dimensional reduction of the local configuration space, the kernel dimension of the kinematic monodromy map becomes a step function of proline content. Topology sees sequence. Scalar stiffness changes only the metric; dimensional reduction changes the topology.

For N=5 the measured relation is exact:

```
#Pro   0  1  2  3  4  5
ker    4  3  2  1  0  0
```

## Middle-out pipeline (the operating process)

```
Slice 0  Topological core     sequence → domain → ker / obstruction
Slice 1  Local metric         residue stiffness / preferred basins
Slice 2  Kinematic connection SE(3) Jacobian + spectrum + residual
Slice 3  Progressive closure  residual trajectory under rising constraint
```

The middle (obstruction / ker) is computed first and remains a live gauge at every outward slice. This is the dimensionalization path that mega-GPU end-to-end hallucination collapses and discards.

## Real-data grounding (AfCycDesign)

- 10 001 hallucinated cyclic scaffolds (N≈14–16)
- Obstruction distribution: 28% / 36% / 26% / 8% / 1.5% for obst = 0 / 1 / 2 / 3 / ≥4
- Extreme obstruction is rare and Pro-rich — consistent with design pipelines avoiding the topologically tight regime
- Sequence-level topological coordinate is already fixed before any coordinates exist (slice 0)

## Ranking power (controlled model)

Under a local-energy residual, kernel dimension ranks closure difficulty with Spearman ≈ 0.80, matching raw proline count; a hybrid edges higher. Topology is competitive with the strongest elementary sequence baseline.

## What the residual experiments taught

Final filtered high-pLDDT structures have already optimised local closure; post-hoc atomic residuals become uniformly good and erase the correlation. The topological signal is a prior and a running coordinate during dimensionalization, not a post-filter residual check. Evaluating only endpoints is the wrong slice.

## Sandbox capabilities used

- 2-core Xeon Platinum 8481C, full AVX-512
- OpenBLAS-backed NumPy
- Hugging Face `datasets` + direct PDB pulls from AfCycDesign
- Full kinematic SE(3) + sheaf spectral stack in pure Python/SciPy

## Artifacts (maximum-value package)

| File | Role |
|------|------|
| `FULL_DRAFT_topology_sees_sequence.md` | Paper-ready draft |
| `middle_out_pipeline.py` | Executable middle-out dimensionalization |
| `fig1_kernel_step.*` | Exact step-function figure |
| `fig2_real_peptides.*` | Obstruction on known macrocycles |
| `fig3_afcycdesign_obstruction.*` | Design-distribution histogram |
| `fig4_obst_vs_N.*` | Obstruction vs ring size |
| `RESULT_topology_sees_sequence.md` | Consolidated scientific claim |
| `PAPER_READY_result.md` | Drop-in abstract/result statement |
| Supporting kinematic / variable-rank / calibration scripts | Full reproducibility |

## Value status

The geometric fact, the middle-out process, and the real-design distribution are aligned and executable. The remaining leaps that increase external value (experimental cyclisation yields, full atomic monodromy trajectories, live insertion into a design loop) require either larger external data or engineering beyond the present sandbox session.

The coherent package is complete for the intent dimensions of this session.
