# Corrections relative to the original abelian preprint

1. **slice0 / combinatorial obstruction**  
   `obst = n_Pro` is an algebraic identity under hard domain reduction, not a free topological invariant of the backbone.

2. **Bishop holonomy on deposited coordinates**  
   Under the paper’s *reference Ramachandran connection* (or any flat connection forced to close by domain reduction), a deposited closed conformation has **trivial sheaf θ** by construction. That does **not** mean every connection on a closed CA trace has trivial holonomy: `bishop_holonomy` on final CA coordinates generally returns a **nonzero** Bishop phase (Gauss–Bonnet / writhe object). Measuring Bishop θ on final traces therefore does **not** recover the paper’s sheaf θ. Empirically Spearman ρ(E_ref, Bishop E) ≈ 0 on n=450 designed scaffolds (summary in `STATUS_P1_P2.md` / `NOTES_EMPIRICAL.md`; full n=450 manifest+workflow not checked into this branch — treat as descriptive until the correlation artifact is regenerated).

3. **SE(3) frame monodromy ≠ Bishop**  
   Numerical comparison on secondary-structure prototypes and random chains shows large disagreements (often >50°). Three different holonomies: sheaf SO(2), SE(3) Rot(μ), Bishop.

4. **Reference connection**  
   The geometrically correct obstruction is the residual screw of the product of residue transforms with every residue at its preferred Ramachandran geometry (`derive.py`). Least-norm dihedral correction yields sequence-dependent strain (poly-Pro ≫ poly-Ala).

5. **Rosetta total score**  
   Does not track backbone strain (positive control failed). Cannot be used to falsify or confirm P2.

6. **ψ ≈ φ closure locus**  
   Stands as pure geometry: 182 uniform rise≈0 solutions for N=5–16, 100% with |ψ−φ|<15°.

7. **P2 status**  
   Untested against a valid strain-specific observable (rama/omega terms, cyclized−linear ΔE, or experimental yields).
