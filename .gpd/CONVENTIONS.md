# Conventions Ledger

**Project:** Adaptive Gap-Junction Networks and the Physical Limits of Non-Equilibrium Morphological Inference
**Created:** 2026-03-16
**Last updated:** 2026-03-16 (Phase 0)

> This file is append-only for convention entries. When a convention changes, add a new entry with the updated value and mark the old entry as superseded. Never delete entries.

---

## Statistical Mechanics

### Ensemble

| Field | Value |
| --- | --- |
| **Convention** | Non-equilibrium stochastic trajectory ensemble on a 2D square lattice; equilibrium language used only in explicitly reduced or limiting regimes |
| **Introduced** | Phase 0 |
| **Rationale** | The operator prompt is centered on driven, adaptive, non-equilibrium dynamics, so equilibrium assumptions must be explicit rather than default |
| **Dependencies** | Entropy-production estimator, pathwise KL divergence, basin statistics, interpretation of hysteresis and metastability |

### Unit System

| Field | Value |
| --- | --- |
| **Convention** | Lattice units with nondimensionalized time, voltage, and conductance variables; report all control parameters as explicit dimensionless groups |
| **Introduced** | Phase 0 |
| **Rationale** | The operator prompt requires nondimensionalization before Phase 1 output |
| **Dependencies** | Parameter sweeps, asymptotic reduction, manuscript tables, finite-size comparisons |

### Timescale Convention

| Field | Value |
| --- | --- |
| **Convention** | Fast voltage dynamics occur on hours, slow conductance adaptation on days to weeks, so unperturbed `epsilon = tau_V / tau_G ~ 10^-2 to 10^-3` |
| **Introduced** | Phase 0 |
| **Rationale** | Empirical constraint injected by the user; no stronger timescale separation should be assumed |
| **Dependencies** | Asymptotic reductions, stimulation-induced breakdown tests, parameter tables |

### Lattice Convention

| Field | Value |
| --- | --- |
| **Convention** | 2D square lattice of size `L x L` with nearest-neighbor edges; base case uses symmetric adaptive conductances `G_ij = G_ji` |
| **Introduced** | Phase 0 |
| **Rationale** | Matches the user-supplied model definition |
| **Dependencies** | Laplacian construction, lesion surgery, connectivity observables, finite-size scaling |
| **Test value** | Interior sites have degree 4 before lesions; boundaries depend on the chosen Phase 1 boundary condition |

### Order Parameter Convention

| Field | Value |
| --- | --- |
| **Convention** | Empirical macrostate is three-valued: `WT`, `Cryptic`, and `DH`; if a binary reduction is used anywhere, it must be declared as a scope limitation |
| **Introduced** | Phase 0 |
| **Rationale** | Injected empirical constraint supersedes the earlier binary default |
| **Dependencies** | `P(m)`, `P(V|m)`, polarity recovery metrics, summary-table interpretation |

### Disorder Convention

| Field | Value |
| --- | --- |
| **Convention** | Every disorder source must be labeled by class before use: site, bond, random-field, random-bond, or dilution, with an explicit distribution; octanol-mediated blockade is treated as bond dilution |
| **Introduced** | Phase 0 |
| **Rationale** | The operator prompt forbids unspecified disorder |
| **Dependencies** | Phase diagrams, relevance tests, percolation comparisons, manuscript claims |
| **Test value** | Bond-dilution threshold is compared against the 2D square-lattice bond-percolation point `p_c ~ 0.5` |

### Lesion Convention

| Field | Value |
| --- | --- |
| **Convention** | Sink lesions, edge-sever lesions, and topological cuts are distinct classes; topological cuts require graph surgery, Laplacian update, and Neumann survivor boundaries |
| **Introduced** | Phase 0 |
| **Rationale** | The operator prompt explicitly forbids conflating zeroed voltages with cuts |
| **Dependencies** | Simulator implementation, repair comparisons, interpretation of thresholds |
| **Test value** | Zeroing `V_i` without edge removal is treated as a sink, not a cut |

### Reachability Convention

| Field | Value |
| --- | --- |
| **Convention** | Primary reachability metric is empirical and ensemble-based; all reports must specify initial-condition distribution, perturbation amplitude, duration, horizon, trajectory count, and attractor conditioning |
| **Introduced** | Phase 0 |
| **Rationale** | The operator prompt forbids using a linear Gramian as the primary reachability metric |
| **Dependencies** | Phase 4 metrics, code interfaces, figure captions |

### Basin Convention

| Field | Value |
| --- | --- |
| **Convention** | FTLEs may be used only as local sensitivity indicators; basin claims require quasipotential estimates, minimum-action paths, or transition-path statistics |
| **Introduced** | Phase 0 |
| **Rationale** | Explicit operator-prompt guardrail |
| **Dependencies** | Basin figures, interpretation of morphological stability, validation checks |

### Thermodynamic Convention

| Field | Value |
| --- | --- |
| **Convention** | Memory, constraint retention, or error-correction claims require a reported entropy-production estimate from pathwise KL divergence between forward and reverse trajectories |
| **Introduced** | Phase 0 |
| **Rationale** | Explicit operator-prompt guardrail |
| **Dependencies** | Phase 5 analysis, summary table, manuscript claims |

### Result-Status Convention

| Field | Value |
| --- | --- |
| **Convention** | Every conclusion must be labeled as `exact derivation`, `local result`, `asymptotic result`, `numerical result`, or `interpretive claim` |
| **Introduced** | Phase 0 |
| **Rationale** | Prevents generalizing local or numerical results beyond their domain |
| **Dependencies** | All summary artifacts, manuscript wording, verification workflow |
