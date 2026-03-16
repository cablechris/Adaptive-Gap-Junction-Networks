# Adaptive Gap-Junction Networks and the Physical Limits of Non-Equilibrium Morphological Inference

## What This Is

This project instantiates a GPD research workspace for a stochastic lattice model of adaptive gap-junction dynamics on a 2D tissue-like grid. The target deliverable is a simulation-backed and asymptotics-backed manuscript that determines when Lyapunov structure exists, when it fails, how nonlinear reachability and basin geometry behave under lesions and disorder, and whether any inference analogy is earned rather than relabeled post hoc.

## Core Research Question

For adaptive gap-junction networks with bistable fast voltage dynamics and slow coupling plasticity, what mathematically controlled regime, if any, supports Lyapunov-like reduction, morphology-conditioned information retention, and falsifiable repair thresholds before nonconservative flux, disorder, topology change, or fast-slow breakdown destroy that description?

## Scoping Contract Summary

### Contract Coverage

- Restricted Lyapunov regime: Derive or exclude a global or reduced Lyapunov functional, with explicit obstruction terms and a breakdown threshold in `epsilon = tau_V / tau_G`.
- Nonlinear repair geometry: Quantify empirical reachability, basin structure, and information decay under intact and lesioned topologies.
- Thermodynamic consistency: Bound any memory claim with measured entropy production from pathwise forward/reverse trajectory asymmetry.
- Acceptance signal: derivations with stated assumptions, topology-correct lesion code, reproducible phase diagrams, reachability/basin/MI/entropy figures, and a claim-status summary table.
- False progress to reject: post hoc relabeling of a fitted objective as inference, FTLE-only basin claims, linearized reachability as the primary metric, zeroed-node lesions treated as cuts, or any unquantified term dropping.

### User Guidance To Preserve

- **User-stated observables:** critical conductance threshold, hysteresis, repair fidelity, empirical decay length, quasipotential or transition-path basin structure, entropy production rate, and fast-slow breakdown near `epsilon -> 1`.
- **User-stated deliverables:** LaTeX manuscript, Python simulation/analysis codebase, figure suite, and a summary table with claim status, assumptions, disorder dependence, energetic cost, and falsifiability.
- **Must-have references / prior outputs:** the supplied operator prompt and the GPD workflow scaffold in this repository.
- **Stop / rethink conditions:** if a claimed equivalence requires engineered `P(m)` and `P(V|m)`, if disorder class is unspecified, if lesion handling is not topology-correct, if dissipation is unmeasured, or if reduced-function claims require uncontrolled term dropping.

### Scope Boundaries

**In scope**

- 2D square-lattice tissue model with nearest-neighbor coupling, optional quenched disorder, three lesion classes, stochastic forcing, slow adaptive conductances, and binary head-tail macrostate by default.
- Exact, local, asymptotic, and numerical analyses of Lyapunov structure, reachability, information flow, and entropy production.
- Finite-size studies at `L = 16, 32, 64` for threshold classification against connectivity/percolation observables.

**Out of scope**

- Biological wet-lab validation.
- Claims about cognition, belief, or free-energy minimization without an explicit generative model and demonstrated correspondence.
- Higher-dimensional tissues, long-range edges, or nonlocal biochemical transport beyond the base problem statement unless added later as a follow-up phase.

### Active Anchor Registry

- `prompt-operator-2026-03-16`: user-supplied GPD operator prompt
  - Why it matters: defines the non-negotiable modeling, derivation, and validation constraints
  - Carry forward: planning, execution, verification, writing
  - Required action: read, use, avoid
- `repo-gpd-main`: local `get-physics-done` checkout
  - Why it matters: provides the research-project scaffold, workflow, and artifact structure
  - Carry forward: planning, execution
  - Required action: use

### Carry-Forward Inputs

- Operator prompt preserved in `.gpd/intake/adaptive-gap-junction-operator-prompt.md`
- Empirical constraints: `tau_V ~ hours`, `tau_G ~ days-weeks`, `epsilon ~ 10^-2 to 10^-3`; macrostate `m in {WT, Cryptic, DH}`; octanol blockade treated as bond dilution with bond-percolation comparison
- No validated external literature anchors loaded yet

### Skeptical Review

- **Weakest anchor:** no literature benchmark has been added yet for disorder thresholds, entropy-production estimators, or morphology observables.
- **Unvalidated assumptions:** a three-valued macrostate can be represented cleanly in the chosen coarse features or on-site potential; coarse-grained `phi(V)` features can capture the relevant morphology-conditioned observables; reduced-order quasipotential calculations retain the basin geometry of the full lattice.
- **Competing explanation:** observed recovery thresholds may be dressed connectivity or percolation phenomena rather than a distinct adaptive-repair transition.
- **Disconfirming observation:** empirical reachability, basin geometry, and information decay fail to co-vary, or any purported Lyapunov reduction breaks before the regime where the simulated repair effects occur.
- **False progress to reject:** visually smooth repair movies, stable-looking trajectories, or local FTLE patterns without quantified basin or dissipation evidence.

### Open Contract Questions

- Which specific plasticity rule `Phi(Delta V, s_ij, xi_ij)` best balances locality, symmetry, and analytical tractability for Phase 2?
- Which coarse-grained voltage features `phi(V)` produce the cleanest explicit `P(V|m)` for `m in {WT, Cryptic, DH}` in Phase 3 without being engineered merely to mirror a derived Lyapunov function?

## Research Questions

### Answered

(None yet - investigate to answer)

### Active

- [ ] Does the deterministic `(V, G)` system admit a global Lyapunov functional, a local metastable one, only an `epsilon -> 0` reduced one, or none of the above?
- [ ] What obstruction terms generate rotational flux in joint `(V, G)` space, and how large do they become over the target operating regime?
- [ ] Under which lesion classes, disorder families, and stimulation protocols do recovery thresholds align with or depart from connectivity/percolation structure, especially the 2D bond-percolation threshold?
- [ ] Does any explicit generative model yield exact equivalence, local reduced equivalence, asymptotic analogy, universality-class correspondence, or only heuristic similarity?
- [ ] What entropy-production cost accompanies coupling-encoded morphological memory or repair fidelity?

### Out of Scope

- Full biochemical pathway identification behind plasticity rules - requires a separate biological-modeling project.
- Experimental organism-specific calibration - needs external data not yet in the workspace.

## Research Context

### Physical System

A 2D square lattice of `N = L^2` cells with nearest-neighbor gap-junction couplings. Fast variables `V_i` evolve in a nonlinear on-site potential plus diffusive coupling, applied injury/stimulation fields, and stochastic noise. Slow edge variables `G_ij` adapt under a local plasticity rule and optional slow noise or injury fields, with symmetric `G_ij = G_ji` in the base case. The empirical macrostate is three-valued: WT, Cryptic, and DH, with DH treated as a stable non-equilibrium attractor and both Cryptic and DH resettable to WT by hyperpolarization.

### Theoretical Framework

Non-equilibrium statistical mechanics, stochastic dynamical systems, lattice simulation, metastability, large-deviation/transition-path analysis, nonlinear control/reachability, and stochastic thermodynamics.

### Key Parameters and Scales

| Parameter | Symbol | Regime | Notes |
| --- | --- | --- | --- |
| Fast-slow ratio | `epsilon = tau_V / tau_G` | unperturbed `10^-3` to `10^-2`; breakdown tested toward `epsilon ~ 1` | `tau_V ~ hours`, `tau_G ~ days-weeks`; no stronger separation assumed |
| Coupling strength scale | `g0` | weak to strong coupling | Distinct from adaptive `G_ij(t)` fluctuations |
| Noise-to-barrier ratio | `chi = D / Delta U` | sub- to super-activation | Controls metastability and switching |
| Adaptation strength | `alpha_Phi` | weak to strong | Determines feedback of voltage mismatch onto `G_ij` |
| Decay rate | `lambda_G` | positive | Slow conductance relaxation |
| Bond occupation / dilution | `p` or `1-f_b` | `0` to `1` | Primary octanol-disorder control; compare polarity disruption threshold against 2D square-lattice bond percolation `p_c ~ 0.5` |
| Disorder strength | `W` | zero to strong | Non-octanol disorder must still be labeled by disorder class and distribution |
| Injury amplitude | `A_inj` | zero to destructive | Includes sink lesions, stimulation, and field perturbations |
| Topology disruption fraction | `f_cut` | `0` to near percolation | Used for edge-sever and topological-cut lesions |
| Stimulation amplitude | `A_stim` | weak to strong | Used to test fast-slow breakdown |

### Known Results

- The current workspace contains no validated project-specific derivations or simulations yet.
- The user prompt already rules out several common shortcuts: global-gradient assumptions, post hoc inference language, zero-out lesion surrogates, Gramian-first reachability, FTLE-as-basin claims, and memory claims without dissipation accounting.
- Empirical constraints to preserve: unperturbed `epsilon ~ 10^-2 to 10^-3`; macrostate `m` is three-valued (`WT`, `Cryptic`, `DH`); octanol-mediated blockade is bond dilution rather than uniform conductance scaling.

### What Is New

This project is designed to produce a disorder-aware, lesion-aware, thermodynamically consistent account of adaptive tissue-scale repair in a nonlinear stochastic lattice model, with explicit obstruction analysis for the cognitive/inference analogy rather than assuming it.

### Target Venue

Initial target: a theory/computation biophysics or non-equilibrium physics venue. Final journal choice should follow once the balance between derivation-heavy and simulation-heavy results is clearer.

### Computational Environment

Local Windows workstation in `C:\Users\cable\get-physics-done`. Simulation code, derivations, figures, and manuscript artifacts will be created inside this repository.

## Notation and Conventions

See `.gpd/CONVENTIONS.md` for all notation and sign conventions.

## Unit System

Lattice units with dimensionless time and voltage variables unless a later phase requires a physical-unit back-mapping. Report all nondimensional groups explicitly.

## Requirements

See `.gpd/REQUIREMENTS.md` for the detailed requirements specification.

## Key References

- Operator prompt anchor: `.gpd/intake/adaptive-gap-junction-operator-prompt.md`
- GPD workflow scaffold: `README.md`

## Constraints

- **Modeling**: No global linearization of `U(V)` and no uncontrolled global-gradient assumption - these would erase the core obstruction question.
- **Macrostate**: Either extend the model to support `m in {WT, Cryptic, DH}` explicitly, or state binary `m` as a scope limitation in the manuscript.
- **Disorder**: Octanol blockade must be treated as bond dilution, not uniform conductance scaling.
- **Verification**: Every conclusion must be labeled as `exact derivation`, `local result`, `asymptotic result`, `numerical result`, or `interpretive claim` - prevents scope inflation.
- **Lesions**: Topological lesions require graph surgery plus Laplacian update and Neumann survivor boundaries - zeroing `V_i` alone is a different lesion class.
- **Thermodynamics**: No memory or inference language without explicit dissipation or explicit generative-model definitions - prevents relabeling.
- **Reachability**: Ensemble specification is mandatory for every nonlinear reachability claim - no unspecified perturbation studies.

## Key Decisions

| Decision | Rationale | Outcome |
| --- | --- | --- |
| Base geometry is a 2D square lattice with nearest-neighbor edges | Matches the operator prompt and keeps asymptotics/sweeps tractable | Accepted |
| Default macrostate is binary head-tail polarity | User defined this as the default Layer C instantiation | Accepted |
| Empirical macrostate constraint overrides the binary default | WT, Cryptic, and DH must be represented explicitly or called out as a limitation | Accepted |
| Project starts without external literature anchors | Avoids inventing benchmarks before they are actually loaded and checked | Accepted |
| Claim labels are mandatory in all downstream artifacts | Required by the operator prompt | Accepted |

---

_Last updated: 2026-03-16 after project bootstrap_
