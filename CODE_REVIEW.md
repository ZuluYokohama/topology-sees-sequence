# Code & Domain Review

Cross-domain review of the full session package (geometry, topology, numerics, data, process).

## 1. Geometry / kinematics

**Strengths**
- SE(3) residue transforms with standard bond lengths/angles are explicit and reproducible.
- Monodromy residual (so(3) log + translation) is the correct linearised obstruction.
- Hard domain reduction for proline is implemented consistently (φ frozen at −65°).

**Risks / limits**
- Idealised bond geometry; real PDBs deviate → absolute residuals are not zero even for good designs.
- ω fixed at π (trans peptide); cis-Pro and non-standard geometry not modelled.
- Linearisation is local; finite closure can still exist when ker is reduced but non-zero.

**Verdict**: Geometrically sound for the claimed scope (linearised kinematic connection).

## 2. Topology / sheaf

**Strengths**
- Clear separation: metric overlays leave ker invariant; dimensional reduction moves ker.
- Step function for N=5 is numerically exact under hard domain reduction.
- Euler / Betti language is used carefully (ker of dμ as geometric harmonic space).

**Risks**
- "Topology sees sequence" is true under the modelling choice of variable-rank stalks. Equal-rank theories remain sequence-blind by construction — that is not a bug in those theories, it is their hypothesis.
- Variable-rank is discrete (rank 1 vs 2). Soft rank was shown not to move ker.

**Verdict**: Claim is correctly scoped and demonstrated.

## 3. Numerics

**Strengths**
- Pure NumPy/SciPy; no hidden dependencies for core results.
- SVD / eigvalsh thresholds documented; kernel counts stable under re-optimisation.
- Middle-out pipeline returns consistent signals across the Pro ladder.

**Risks**
- Finite-difference Jacobians (eps ~1e-6) are adequate for N≤16 but not highly accurate for very stiff directions.
- Optimisation (L-BFGS-B) can miss global closure minima; multiple random starts mitigate but do not eliminate this.
- Batch V&V on AfCycDesign used reduced trial counts for speed; residual=0 on long chains is expected (domain still large).

**Verdict**: Sufficient for the reported claims; not a high-precision production solver.

## 4. Data / external grounding

**Strengths**
- AfCycDesign sequence-level obstruction distribution is reproducible via Hugging Face `datasets`.
- Real PDB dihedrals and frame residuals extracted with BioPython.
- Qualitative mapping to known macrocycles (Gramicidin S, SFTI-1, etc.) is coherent.

**Risks**
- Sequence-level obstruction ≠ atomic residual on filtered designs (signal optimised away post-filter). This is documented, not hidden.
- Experimental split of AfCycDesign is tiny; claims rest primarily on hallucinated scaffolds.
- No experimental cyclisation yields yet — ranking power is model-internal.

**Verdict**: Honest grounding. External predictive validation remains open.

## 5. Process / abstraction

**Strengths**
- Middle-out principle is explicit and implemented: topology first, never discarded.
- Correct diagnosis that end-to-end generative pipelines evaluate the wrong slice (final filtered endpoints).
- Coherent alignment document ties theory, pipeline, and data.

**Risks**
- Pipeline slices 1–3 are still minimal; collective modes / persistence / side chains not yet layered.
- No live coupling to a design optimiser (Rosetta, AF, etc.).

**Verdict**: Process architecture is the right direction; depth of outward slices can grow.

## 6. Software hygiene

- Scripts are self-contained; some duplication of geometry primitives across files (acceptable for research snapshots).
- No tests/CI yet.
- Large binary figures should be LFS or linked if the repo grows.
- No secrets or private operator data included.

## Overall

The package is coherent, the central geometric claim is demonstrated, and the limits are stated. Suitable as a research repository and draft foundation. Not yet a calibrated predictor of experimental cyclisation yields.
