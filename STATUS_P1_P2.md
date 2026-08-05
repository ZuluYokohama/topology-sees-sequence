# Status: P1 / P2 after reference-connection correction
**5 August 2026**

## Conceptual corrections (locked)

1. **Bishop holonomy ≠ paper θ.** Three different holonomies (SO(2) sheaf, SE(3) Rot(μ), Bishop on CA). Equality is a theorem, not a definition. Numerically they diverge.

2. **Closed deposited structures have trivial holonomy by definition.** θ cannot be read off the observed conformation as the theory's obstruction. θ is the residual screw of the **reference connection** (every residue at preferred Ramachandran geometry).

3. **Combinatorial obst = n_Pro is an identity**, not a free topological invariant.

4. **Rosetta total score does not track backbone strain** (positive control failed). Nulls against Rosetta total cannot falsify backbone-strain theory.

## What stands

| Result | Evidence |
|--------|----------|
| Extraction machinery (Bishop, transport ↔ GB) | Agreement 1e−15; crystallographic copies to 5° |
| ψ≈φ closure locus | Geometry-only; 182 solutions N=5–16, 100% with \|ψ−φ\|<15° |
| Reference-connection residual = geometric obstruction | Derived; sequence-dependent (poly-P E≈325, poly-A E≈0.3) |
| Loop-closure Jacobian rank 6 on real designs | No kinematic singularities in sample |

## Empirical (n=450 hall_theta)

| Pair | Spearman ρ |
|------|------------|
| E_ref vs Bishop E_tot | 0.00 (null) |
| E_ref vs Rosetta total | −0.10 |
| ref θ vs Bishop θ | +0.03 |
| E_ref vs N | −0.31 |
| \|Bishop θ\| vs N | +0.31 |

## P2 status

**Untested** against a valid strain-specific observable.

Invalid instruments: Rosetta total, Bishop-on-closed as proxy for reference θ.

Valid next: Rosetta rama/omega terms; E(cyclized)−E(linear); experimental yields.
