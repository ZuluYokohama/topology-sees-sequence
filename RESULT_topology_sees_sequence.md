# Topology Sees Sequence
## Kernel Dimension of the Kinematic Sheaf is a Step Function of Proline Content

**Result of the iterative geometric refinement cycle**  
4 August 2026

---

### Claim

When proline is treated as a genuine reduction in the dimension of the local configuration space (φ frozen, only ψ free), the dimension of the space of infinitesimal closed motions of a cyclic peptide becomes a direct function of proline count.

For a cyclic pentapeptide the measured relation is essentially exact:

| Number of Pro | Domain dim | rank(dμ) | Kernel dimension |
|---------------|------------|----------|------------------|
| 0             | 10         | 6        | **4**            |
| 1             | 9          | 6        | **3**            |
| 2             | 8          | 6        | **2**            |
| 3             | 7          | 6        | **1**            |
| 4             | 6          | 6        | **0**            |
| 5             | 5          | ≤5       | **0**            |

Each proline removes one dimension from the domain of the monodromy map.  
While the domain remains ≥6 the rank stays saturated at 6 and the kernel falls one-to-one with proline count.  
When the domain drops below 6 the rank is forced downward and the ring becomes over-constrained (residual remains large for all-proline).

**Topology is no longer blind to sequence.**

---

### Geometric setting

The backbone is modelled by the discrete kinematic connection whose residue transforms take values in SE(3).  
The monodromy map μ sends dihedral coordinates to the total rigid motion around the cycle.  
Its differential dμ : ℝ^{d} → se(3) ≅ ℝ⁶ has kernel equal to the infinitesimal closed motions (geometric harmonic sections of the kinematic sheaf).

Hard domain reduction assigns proline a 1-dimensional local domain.  
This is the only overlay found that moves the kernel dimension; pure metric stiffening, column scaling, and geometry re-optimisation under soft penalties change the positive spectrum but leave the kernel dimension invariant.

---

### Separation of effects

- **Topological content** — kernel dimension — is a step function of the number of dimension-reducing residues (Pro).  
- **Metric content** — positive eigenvalues of the kinematic Laplacian — continues to respond smoothly to both proline and glycine.

The two contributions are cleanly separated once the correct dimensional overlay is used.

---

### Relation to the abelian model

The earlier abelian sheaf (planar rotation θ on equal-rank dihedral stalks) correctly predicted that *scalar* stiffness leaves Betti numbers invariant.  
That statement remains true for pure metric changes.  
It does not survive once residues are allowed to carry different intrinsic dimensions.  
The kinematic construction with hard domain reduction is the geometric refinement that makes topology sequence-dependent while remaining faithful to SE(3) closure.

---

### Status

- Full numerical confirmation for N=5 across multiple sequence families.  
- Code: `kinematic_variable_rank.py`, `sequence_topological_fingerprint.py`.  
- The result is stable under re-optimisation of the closed geometry.

This is the consolidated scientific return of the cycle.
