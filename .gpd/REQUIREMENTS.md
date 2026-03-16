# Requirements: Adaptive Gap-Junction Networks and the Physical Limits of Non-Equilibrium Morphological Inference

**Defined:** 2026-03-16
**Core Research Question:** For adaptive gap-junction networks with bistable fast voltage dynamics and slow coupling plasticity, what mathematically controlled regime, if any, supports Lyapunov-like reduction, morphology-conditioned information retention, and falsifiable repair thresholds before nonconservative flux, disorder, topology change, or fast-slow breakdown destroy that description?

## Primary Requirements

### Derivations

- [ ] **DERV-01**: Nondimensionalize the model and define the controlling parameters `epsilon`, coupling strength, noise-to-barrier ratio, injury amplitude, disorder strength, topology disruption fraction, stimulation amplitude, and adaptation strength, with unperturbed `epsilon` anchored to `10^-2` to `10^-3`.
- [ ] **DERV-02**: Specify the fast voltage dynamics, slow conductance dynamics, boundary conditions, disorder classes, and three lesion classes with topology-correct updates.
- [ ] **DERV-03**: Determine whether a global Lyapunov functional exists for deterministic symmetric-`G` dynamics, and if not isolate the obstruction terms.
- [ ] **DERV-04**: Derive any local metastable Lyapunov structure and any reduced `epsilon -> 0` functional with leading correction terms and an explicit validity threshold.
- [ ] **DERV-05**: Define `P(m)` and `P(V|m)` explicitly on a coarse-grained feature map `phi(V)` before any inference correspondence claim is made.
- [ ] **DERV-07**: Either extend the voltage/macrostate description to support `m in {WT, Cryptic, DH}` with DH as an absorbing non-equilibrium attractor, or state binary `m` as an explicit scope limitation.
- [ ] **DERV-06**: Derive the pathwise entropy-production estimator from forward and time-reversed trajectory ensembles and state its discretization assumptions.

### Simulations

- [ ] **SIMU-01**: Implement the 2D lattice simulator for intact tissue, weak perturbations, and all three lesion classes: sink, edge-sever, and topological cut.
- [ ] **SIMU-02**: Implement optional quenched disorder with explicit class labels and stated distributions before use, treating octanol-mediated blockade specifically as bond dilution.
- [ ] **SIMU-03**: Verify metastable patterns, hysteresis, propagation, repair, and failure modes across a documented parameter range.
- [ ] **SIMU-04**: Run ensemble-based empirical reachability studies with fully specified Ensemble A and Ensemble B parameters.
- [ ] **SIMU-05**: Estimate basin geometry with quasipotential, minimum-action, or transition-path statistics on either the full lattice or a justified reduced patch.
- [ ] **SIMU-06**: Measure at least one mutual-information observable and extract an empirical decay length under coupling, disorder, and plasticity sweeps.
- [ ] **SIMU-07**: Estimate entropy production rate from trajectory data and assess its sampling-interval sensitivity.
- [ ] **SIMU-08**: Perform finite-size checks at `L = 16, 32, 64` for conductance-threshold and connectivity/percolation comparisons.

### Analysis

- [ ] **ANLY-01**: Quantify all neglected terms whenever a reduced functional is claimed and report their magnitude over the simulated regime.
- [ ] **ANLY-02**: Test explicitly whether empirical reachability, basin structure, and information decay track one another or diverge.
- [ ] **ANLY-03**: Classify every disorder term by class and test whether it is relevant to the observed transition.
- [ ] **ANLY-04**: Compare plasticity-driven recovery against static-bias-driven recovery using common fidelity and reachability metrics.
- [ ] **ANLY-05**: Determine whether the critical conductance threshold is sharp or crossover-like and whether it coincides with, is dressed by, or is distinct from percolation structure.
- [ ] **ANLY-07**: Test whether the polarity-disruption threshold under bond dilution coincides with the 2D square-lattice bond-percolation critical point `p_c ~ 0.5`.
- [ ] **ANLY-06**: Determine whether strong stimulation compresses timescales toward `epsilon ~ 1` and qualitatively changes repair dynamics.

### Validations

- [ ] **VALD-01**: Distinguish exact, local, asymptotic, numerical, and interpretive outputs in all downstream summaries and manuscripts.
- [ ] **VALD-02**: Keep sink lesions analytically and numerically separate from edge-sever and topological-cut lesions throughout the project.
- [ ] **VALD-03**: Reject any inference-language claim unless the explicit generative model has been defined and the correspondence class has been stated.
- [ ] **VALD-04**: Reject FTLE-only basin claims and linear-Gramian-first reachability claims.
- [ ] **VALD-05**: Bound every memory or coupling-encoded-constraint claim by a measured dissipation number.
- [ ] **VALD-06**: Cross-check reduced descriptions against direct simulations near the reported breakdown threshold.

### Outputs

- [ ] **OUTP-01**: Produce a Python codebase with simulator, lesion routines, stimulation/disorder modules, reachability tooling, basin/quasipotential tooling, MI estimators, entropy-production estimator, and sweep scripts.
- [ ] **OUTP-02**: Produce a LaTeX manuscript covering model definition, asymptotics, obstruction terms, generative-model correspondence, disorder handling, entropy estimator, scope limits, and biological interpretation.
- [ ] **OUTP-03**: Produce figures for phase diagrams, hysteresis, lesion comparisons, disorder thresholds, reachability, basin/quasipotential structure, MI decay, entropy-versus-memory, and `epsilon` validity regimes.
- [ ] **OUTP-04**: Produce a summary table with columns `claim / mathematical status / assumptions / disorder dependence / energetic cost / biological interpretation / falsifiability`.

## Follow-up Requirements

### Extensions

- **EXTD-01**: Extend the model to longer-range coupling or irregular tissue graphs after the nearest-neighbor base case is verified.
- **EXTD-02**: Replace the binary macrostate with a richer morphology code once the base-case `m` is validated.
- **EXTD-03**: Calibrate model parameters against organism-specific experimental data.

## Out of Scope

| Topic | Reason |
| --- | --- |
| Wet-lab biological validation | Requires external experimental infrastructure and data |
| Claims about universal cognition or belief dynamics | Not justified unless the explicit generative-model correspondence is earned |
| Full-lattice exact quasipotentials for every large system size | Computationally unrealistic; reduced-order or sampled approximations are acceptable with stated limitations |

## Accuracy and Validation Criteria

| Requirement | Accuracy Target | Validation Method |
| --- | --- | --- |
| DERV-03 | Exact statement of assumptions and obstruction terms | Algebraic derivation plus limiting-case checks |
| DERV-04 | Leading `epsilon` corrections retained through first nontrivial order | Compare reduced predictions against direct simulation as `epsilon` increases |
| SIMU-03 | Reproducible metastability/hysteresis signatures across repeated runs | Seed-controlled replication and trajectory summary checks |
| SIMU-04 | Ensemble specification reported numerically in full | Audit against saved run metadata |
| SIMU-07 | Entropy estimate reported with `Delta t` sensitivity | Recompute on at least two sampling intervals |
| ANLY-05 | Threshold classification supported at `L = 16, 32, 64` | Finite-size comparison with connectivity and cluster-spanning statistics |
| VALD-05 | No memory claim without a dissipation number | Manual contract review plus figure/table evidence |

## Contract Coverage

| Requirement | Decisive Output / Deliverable | Anchor / Benchmark / Reference | Prior Inputs / Baselines | False Progress To Reject |
| --- | --- | --- | --- | --- |
| DERV-03 | Lyapunov/obstruction derivation note | `prompt-operator-2026-03-16` | Base model definition | Declaring gradient flow by symmetry intuition alone |
| DERV-05 | Explicit generative-model section | `prompt-operator-2026-03-16` | Coarse feature definition `phi(V)` | Using inference language before defining `P(m)` and `P(V|m)` |
| DERV-07 | Three-state macrostate definition or scope note | empirical macrostate constraint | Base model definition | Quietly collapsing WT/Cryptic/DH to binary with no manuscript warning |
| SIMU-01 | Lattice simulator and lesion module | `prompt-operator-2026-03-16` | Nondimensional model spec | Treating zeroed nodes as topological cuts |
| SIMU-02 | Disorder module with bond dilution | empirical octanol constraint | Lattice graph | Modeling octanol as uniform conductance scaling |
| SIMU-04 | Reachability report and saved ensemble metadata | `prompt-operator-2026-03-16` | Metastable operating points | Unspecified perturbation ensemble |
| SIMU-05 | Basin/quasipotential figure set | `prompt-operator-2026-03-16` | Reduced-order justification if needed | FTLE heatmaps presented as basin structure |
| SIMU-07 | Entropy-production analysis note | `prompt-operator-2026-03-16` | Forward/reverse path data | Memory claims with no dissipation estimate |
| ANLY-05 | Threshold/percolation comparison figure | `prompt-operator-2026-03-16` | Finite-size sweeps | Reporting a single-size crossover as a sharp transition |
| ANLY-07 | Bond-dilution universality-class comparison | empirical octanol constraint | Bond-dilution sweeps at `L = 16, 32, 64` | Claiming universality with no same-lattice `p_c ~ 0.5` comparison |
| OUTP-04 | Claim-status summary table | `prompt-operator-2026-03-16` | All prior phase outputs | Mixing interpretive claims with exact results |

## Traceability

| Requirement | Phase | Status |
| --- | --- | --- |
| DERV-01 | Phase 1: Simulation Foundation | Pending |
| DERV-02 | Phase 1: Simulation Foundation | Pending |
| SIMU-01 | Phase 1: Simulation Foundation | Pending |
| SIMU-02 | Phase 1: Simulation Foundation | Pending |
| SIMU-03 | Phase 1: Simulation Foundation | Pending |
| DERV-03 | Phase 2: Lyapunov Structure and Obstruction Terms | Pending |
| DERV-04 | Phase 2: Lyapunov Structure and Obstruction Terms | Pending |
| ANLY-01 | Phase 2: Lyapunov Structure and Obstruction Terms | Pending |
| DERV-05 | Phase 3: Generative Model and Inference Correspondence | Pending |
| DERV-07 | Phase 3: Generative Model and Inference Correspondence | Pending |
| VALD-03 | Phase 3: Generative Model and Inference Correspondence | Pending |
| SIMU-04 | Phase 4: Nonlinear Reachability and Information Propagation | Pending |
| SIMU-05 | Phase 4: Nonlinear Reachability and Information Propagation | Pending |
| SIMU-06 | Phase 4: Nonlinear Reachability and Information Propagation | Pending |
| ANLY-02 | Phase 4: Nonlinear Reachability and Information Propagation | Pending |
| DERV-06 | Phase 5: Thermodynamic Cost | Pending |
| SIMU-07 | Phase 5: Thermodynamic Cost | Pending |
| VALD-05 | Phase 5: Thermodynamic Cost | Pending |
| SIMU-08 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| ANLY-03 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| ANLY-04 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| ANLY-05 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| ANLY-07 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| ANLY-06 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| OUTP-01 | Phase 6: Falsifiable Predictions and Phase Diagrams | Pending |
| OUTP-02 | Phase 7: Manuscript and Artifact Packaging | Pending |
| OUTP-03 | Phase 7: Manuscript and Artifact Packaging | Pending |
| OUTP-04 | Phase 7: Manuscript and Artifact Packaging | Pending |

**Coverage:**

- Primary requirements: 26 total
- Mapped to phases: 26
- Unmapped: 0

---

_Requirements defined: 2026-03-16_
_Last updated: 2026-03-16 after project bootstrap_
