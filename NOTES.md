# Notes on remaining local artifacts

The sandbox session also produced additional scripts and figures that are not all mirrored here due to push payload limits:

- `FULL_DRAFT_topology_sees_sequence.md` — complete short paper draft
- `kinematic_variable_rank.py`, `variable_rank_sheaf.py`, `sequence_topological_fingerprint.py`
- `spectral_fingerprint.py`, calibration scripts, hybrid feature tests
- Figures: fig1_kernel_step, fig2_real_peptides, fig3_afcycdesign_obstruction, fig4_obst_vs_N

These remain in the session artifacts directory and can be added in a follow-up commit from a local clone.

## Run the middle-out pipeline

```bash
pip install numpy scipy
python middle_out_pipeline.py
```

Expected: kernel dimension steps down with proline count; PPPPP shows non-zero residual.
