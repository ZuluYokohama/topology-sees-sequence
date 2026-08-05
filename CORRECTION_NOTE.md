# Correction Note: Holonomy and Strain in Cyclic Peptide Models

**Date:** 5 August 2026

## Abstract of the correction

Prior drafts identified the topological obstruction to ring closure with either (i) a combinatorial count of proline residues under hard domain reduction or (ii) the Bishop holonomy of the deposited CA trace. Both identifications are incorrect. The geometrically consistent obstruction is the residual screw of the **reference connection**: the product of residue SE(3) transforms evaluated at preferred Ramachandran geometry for each residue type. Least-norm correction of that residual defines a sequence-dependent strain E_ref.

## What was wrong

1. **Combinatorial obstruction.** Under the modeling choice that proline contributes one dihedral instead of two, the formula obst = (2N-6) - (2N-n_Pro-6) reduces identically to n_Pro. That is an algebraic identity, not an independent topological invariant of the backbone.

2. **Bishop holonomy on closed structures.** A closed conformation has trivial holonomy by definition. Measuring the parallel-transport defect of a normal around the deposited CA polygon recovers a real geometric quantity (equal to -2pi Wr mod 2pi; transport and Gauss-Bonnet agree to machine precision; crystallographic copies agree to ~5 degrees), but that quantity is not the sheaf-theoretic theta of the abelian model and is empirically independent of E_ref on 450 AF-designed scaffolds (Spearman rho approx 0).

3. **SE(3) frame monodromy vs Bishop.** Numerical comparison on secondary-structure prototypes and random chains shows large disagreements. Three distinct holonomies must not be conflated.

4. **Dependent variable for Prediction 2.** Rosetta total score does not track backbone strain. Null correlations against Rosetta total do not test the theory.

## What still stands

- Extraction machinery for Bishop holonomy (validated).
- psi approx phi uniform-closure locus from bond geometry alone (182 solutions for N = 5-16; 100% with |psi-phi| < 15 deg).
- Generic rank-6 loop-closure Jacobian on designed structures.
- Reference-connection strain as a well-defined, sequence-dependent geometric obstruction.

## Corrected Prediction 2

E_ref (or theta_ref) should be tested against a backbone-specific observable: Rosetta rama/omega terms, cyclized-linear backbone energy difference, or experimental cyclization yields — not against Rosetta total score or Bishop holonomy of the closed structure.

## One-sentence summary

The obstruction lives in the reference connection, not in a proline count and not in the holonomy of an already-closed chain.
