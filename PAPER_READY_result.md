# Topology Sees Sequence in the Kinematic Sheaf of Cyclic Peptides

## Paper-ready core statement

We model a cyclic peptide backbone as a discrete kinematic connection with values in SE(3). The differential of the monodromy map,

$$d\mu:\mathbb{R}^{d}\to\mathfrak{se}(3)\simeq\mathbb{R}^{6},$$

has kernel equal to the space of infinitesimal closed motions. This kernel is the geometric analogue of the harmonic space of a cellular sheaf.

When every residue is assigned a two-dimensional domain the kernel dimension is the familiar $2N-6$. Once proline is treated as a genuine dimensional reduction (φ constrained, only ψ free) the domain dimension itself becomes sequence-dependent. For cyclic pentapeptides the measured kernel dimension falls in exact steps with proline count:

$$
\begin{array}{c|cccccc}
\#\mathrm{Pro} & 0 & 1 & 2 & 3 & 4 & 5 \\
\hline
\dim\ker d\mu & 4 & 3 & 2 & 1 & 0 & 0
\end{array}
$$

Topology is therefore not blind to sequence. Scalar stiffness changes (metric overlays) leave the kernel dimension invariant and only rescale the positive spectrum; dimensional reduction of the local configuration space moves the topological count itself.

The same construction recovers the earlier abelian results as the special case in which the structure group is reduced from SE(3) to an abelian 2-torus of dihedral angles and all stalks are forced to equal rank. The kinematic sheaf with hard domain reduction is the geometric refinement that restores sequence dependence to the topology while remaining faithful to rigid-body closure.

### Separation of sequence effects

- **Topological** — kernel dimension is a step function of the number of dimension-reducing residues.
- **Metric** — positive eigenvalues of the kinematic Laplacian respond smoothly to both proline and glycine content.

### Scope and status

Results are for the linearised kinematic connection of cyclic pentapeptides. Hard domain reduction (removal of the proline φ coordinate) is the only overlay found that moves kernel dimension; pure metric stiffening and geometry re-optimisation under soft penalties affect only the spectrum. Full numerical confirmation across multiple sequence families is contained in the accompanying code.
