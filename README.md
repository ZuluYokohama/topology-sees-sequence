# Topology Sees Sequence

**Kernel dimension of the kinematic sheaf is a step function of proline content in cyclic peptides.**

Middle-out SE(3) monodromy pipeline · Hard domain reduction · AfCycDesign grounding

## Core claim

When proline is treated as a genuine dimensional reduction of the local configuration space (φ constrained, only ψ free), the kernel dimension of the discrete kinematic monodromy map becomes sequence-dependent:

```
#Pro (N=5)   0  1  2  3  4  5
ker dim      4  3  2  1  0  0
```

Topology is therefore **not** sequence-blind. Scalar stiffness only rescales the metric (positive spectrum). Dimensional reduction moves the topological count itself.

## Middle-out pipeline

```
Slice 0  Topological core      sequence → domain → ker / obstruction
Slice 1  Local metric          residue stiffness / preferred basins
Slice 2  Kinematic connection  SE(3) Jacobian + spectrum + residual
Slice 3  Progressive closure   residual trajectory under rising constraint
```

The topological coordinate is computed first and never discarded. This is the dimensionalization path that end-to-end generative abstraction collapses.

Entry point: `middle_out_pipeline.py`

## Real-data grounding

- 10k+ hallucinated cyclic scaffolds from [AfCycDesign](https://huggingface.co/datasets/RosettaCommons/AfCycDesign)
- Obstruction distribution peaks at 0–2; extreme obstruction (≥4) is rare (~1.5%) and Pro-rich
- Consistent with design pipelines avoiding the topologically tight regime

## Key results (controlled model)

| Descriptor | Spearman vs strain proxy |
|------------|--------------------------|
| Raw #Pro | ~0.80 |
| Kernel dimension | ~0.80 |
| Hybrid (4−ker + λ) | ~0.81 |

## Repository layout

```
middle_out_pipeline.py          # executable middle-out stack
kinematic_*.py                  # SE(3) connection + variable-rank
variable_rank_sheaf.py          # abelian variable-rank demonstration
sequence_topological_fingerprint.py
calibration_*.py
spectral_fingerprint.py
FULL_DRAFT_topology_sees_sequence.md
COHERENT_ALIGNMENT.md
CODE_REVIEW.md
fig*.png / fig*.pdf             # core figures (see releases or local artifacts)
```

## Reproducibility

Python 3.10+, NumPy, SciPy, Matplotlib. Optional: `datasets`, `biopython`, `huggingface_hub` for AfCycDesign pulls.

```bash
python middle_out_pipeline.py
python sequence_topological_fingerprint.py
python make_figures.py
```

## Citation / status

Research draft, 4 August 2026. Supersedes earlier abelian equal-rank treatments that concluded topology is sequence-blind.

## License

Research code — use with attribution. Not a production design tool.
