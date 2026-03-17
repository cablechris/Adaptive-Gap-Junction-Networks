# Adaptive Gap-Junction Experiment Starter

This directory contains the tracked Phase 1 starter code for the adaptive gap-junction project bootstrapped under `.gpd/`.

Current scope:

- square-lattice geometry
- explicit lesion taxonomy: sink, edge-sever, topological cut
- explicit disorder taxonomy
- double-well fast voltage dynamics
- coarse-grained WT / Cryptic / DH morphology readout
- symmetric adaptive conductance dynamics
- stable anterior/posterior initialization near the two voltage wells
- Euler-Maruyama stepping for exploratory Phase 1 runs

This is not yet the full experiment. It is a foundation for Phase 1 implementation and later Phase 2-6 analysis.

Current runnable entry points:

- `python -m research.adaptive_gap_junction.run_baseline`
- `python -m research.adaptive_gap_junction.run_bond_dilution_sweep`
- `python -m research.adaptive_gap_junction.run_edge_sever_recovery_sweep`
- `python -m research.adaptive_gap_junction.run_sink_recovery_sweep`

The bond-dilution sweep currently uses an explicit surrogate for polarity disruption:

- order parameter: polarity contrast `mean(V_right) - mean(V_left)`
- disruption criterion: final `abs(polarity contrast)` falls below 50% of the undiluted baseline at the same `L`

This is a temporary operational definition until the WT / Cryptic / DH macrostate classifier is implemented.

Explicit limitation:

- WT / Cryptic / DH is currently implemented only as a coarse-grained posterior-depolarization surrogate, not as a true three-well or hybrid dynamical model.
