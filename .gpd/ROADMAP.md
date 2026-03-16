# Roadmap: Adaptive Gap-Junction Networks and the Physical Limits of Non-Equilibrium Morphological Inference

## Overview

This roadmap follows the supplied operator prompt directly plus the injected empirical constraints. It starts by making the stochastic lattice model explicit and executable with unperturbed `epsilon ~ 10^-2 to 10^-3`, a three-valued macrostate (`WT`, `Cryptic`, `DH`) or an explicit limitation note, and octanol-style bond dilution as the primary disorder test. It then determines whether any Lyapunov structure survives the adaptive dynamics, tests whether any generative-model correspondence is mathematically earned, replaces naive linear reachability with ensemble-based nonlinear diagnostics, prices any memory claim by entropy production, and ends with finite-size predictions and manuscript packaging.

## Contract Overview

| Contract Item | Advanced By Phase(s) | Status |
| --- | --- | --- |
| Controlled model specification with lesion taxonomy, empirical timescales, and macrostate handling | Phase 1 | Planned |
| Lyapunov or obstruction account with `epsilon` breakdown threshold | Phase 2 | Planned |
| Explicit generative-model correspondence classification | Phase 3 | Planned |
| Nonlinear reachability, basin, and information-decay comparison | Phase 4 | Planned |
| Dissipation-bounded memory account | Phase 5 | Planned |
| Finite-size threshold classification and bond-percolation comparison | Phase 6 | Planned |
| Manuscript, code, figures, and claim-status table | Phase 7 | Planned |

## Phases

- [ ] **Phase 1: Simulation Foundation** - Define and implement the full lattice model, lesion classes, disorder options, and baseline dynamical phenomenology.
- [ ] **Phase 2: Lyapunov Structure and Obstruction Terms** - Determine global, local, or reduced Lyapunov structure and quantify where it fails.
- [ ] **Phase 3: Generative Model and Inference Correspondence** - Define `P(m)` and `P(V|m)` explicitly and classify any valid correspondence.
- [ ] **Phase 4: Nonlinear Reachability and Information Propagation** - Compute empirical reachability, basin structure, perturbation propagation, and information decay.
- [ ] **Phase 5: Thermodynamic Cost** - Estimate entropy production from pathwise forward/reverse trajectory ensembles and bound memory claims.
- [ ] **Phase 6: Falsifiable Predictions and Phase Diagrams** - Produce threshold studies, finite-size comparisons, and stimulation/plasticity/disorder predictions.
- [ ] **Phase 7: Manuscript and Artifact Packaging** - Package the code, figures, manuscript, and summary table.

## Phase Details

### Phase 1: Simulation Foundation

**Goal:** Make the model executable without hidden assumptions and verify the baseline phenomenology under intact and lesioned conditions.
**Depends on:** Nothing
**Requirements:** [DERV-01, DERV-02, SIMU-01, SIMU-02, SIMU-03, VALD-02]
**Contract Coverage:**
- Advances: model definition, lesion taxonomy, disorder classification
- Deliverables: simulator module, lesion routines, baseline run summaries
- Anchor coverage: operator prompt, local GPD scaffold
- Forbidden proxies: zero-out-only lesions presented as cuts; unspecified disorder; implicit boundary conditions
**Success Criteria** (what must be TRUE):

1. The full model, all boundary conditions, and all lesion classes are defined in writing and code.
2. Nondimensional control parameters are documented and sweepable.
3. The unperturbed fast-slow regime is anchored to `epsilon ~ 10^-2 to 10^-3` rather than a stronger assumed separation.
4. The WT/Cryptic/DH macrostate handling is implemented or explicitly deferred as a manuscript limitation.
5. Intact and lesioned runs reproduce metastability, propagation, hysteresis, repair, or failure modes with saved metadata.
6. Sink lesions remain analytically and numerically distinct from topological edge removal.
   **Plans:** 3 plans

Plans:

- [ ] 01-01: Write the formal model specification, empirical timescale table, macrostate handling, and lesion taxonomy.
- [ ] 01-02: Implement lattice dynamics, graph surgery, bond-dilution disorder hooks, and stimulation/injury protocols.
- [ ] 01-03: Run baseline intact/perturbed/lesioned simulations and record phenomenology.

### Phase 2: Lyapunov Structure and Obstruction Terms

**Goal:** Establish whether a Lyapunov description exists and isolate the terms that obstruct it.
**Depends on:** Phase 1
**Requirements:** [DERV-03, DERV-04, ANLY-01, VALD-01, VALD-06]
**Contract Coverage:**
- Advances: controlled asymptotics and failure analysis
- Deliverables: derivation note, reduced-functional note, obstruction-term table
- Anchor coverage: explicit operator-prompt constraints about `epsilon`, term dropping, forcing, and symmetry
- Forbidden proxies: local stability claims generalized globally; neglected terms omitted from reporting
**Success Criteria** (what must be TRUE):

1. The status of global Lyapunov existence is stated precisely: yes, no, or only under bracketed assumptions.
2. Any local or reduced result includes the operating point, the required assumptions, and the leading correction terms.
3. A breakdown threshold in `epsilon` or forcing amplitude is reported for every reduced description.
4. Every dropped term is named and its magnitude quantified over the studied regime.
   **Plans:** 3 plans

Plans:

- [ ] 02-01: Analyze the deterministic symmetric-`G` system for exact or obstructed gradient structure.
- [ ] 02-02: Derive local and `epsilon -> 0` reduced functionals with explicit corrections.
- [ ] 02-03: Compare reduced predictions with direct simulation near the predicted breakdown regime.

### Phase 3: Generative Model and Inference Correspondence

**Goal:** Determine whether the adaptive dynamics minimize any explicitly defined variational objective and classify the correspondence honestly.
**Depends on:** Phase 2
**Requirements:** [DERV-05, VALD-03]
**Contract Coverage:**
- Advances: explicit `P(m)` and `P(V|m)` rather than analogy by vocabulary
- Deliverables: generative-model note and correspondence-classification table
- Anchor coverage: operator-prompt ban on premature inference language
- Forbidden proxies: engineered post hoc matching presented as exact correspondence
**Success Criteria** (what must be TRUE):

1. `P(m)` is explicit and justified for the chosen macrostate.
2. `P(V|m)` is explicit on a stated coarse feature map `phi(V)`.
3. The resulting objective is written down and compared against the adaptive dynamics.
4. If the full WT/Cryptic/DH macrostate is not implemented, the binary reduction is stated explicitly as a scope limitation.
5. The result is classified as exact equivalence, local reduced equivalence, asymptotic analogy, universality-class correspondence, or heuristic similarity.
   **Plans:** 2 plans

Plans:

- [ ] 03-01: Define the macrostate prior and coarse-grained likelihood family.
- [ ] 03-02: Compare the resulting objective with the adaptive dynamics and classify the correspondence.

### Phase 4: Nonlinear Reachability and Information Propagation

**Goal:** Replace linearized reachability surrogates with ensemble-defined nonlinear diagnostics and compare them with basin and information measures.
**Depends on:** Phase 3
**Requirements:** [SIMU-04, SIMU-05, SIMU-06, ANLY-02, VALD-04]
**Contract Coverage:**
- Advances: reachability, basin geometry, and information decay under common control sweeps
- Deliverables: ensemble metadata, reachability maps, basin/quasipotential figures, MI decay plots
- Anchor coverage: operator-prompt constraints on ensembles, FTLEs, and reduced-order caveats
- Forbidden proxies: unspecified perturbation ensembles; FTLEs used as basin boundaries
**Success Criteria** (what must be TRUE):

1. Ensemble A and Ensemble B are reported numerically and reproduced in saved run metadata.
2. An empirical nonlinear reachability metric is computed from trajectory data.
3. Basin structure is estimated with quasipotential, minimum-action, or transition-path statistics.
4. At least one mutual-information observable yields an empirical decay length.
5. The project states whether reachability, basin structure, and information decay align or diverge.
   **Plans:** 3 plans

Plans:

- [ ] 04-01: Define Ensemble A and Ensemble B, then compute empirical reachability.
- [ ] 04-02: Estimate basin geometry on the lattice or a justified reduced patch.
- [ ] 04-03: Measure information propagation and compare its decay with reachability and basin observables.

### Phase 5: Thermodynamic Cost

**Goal:** Quantify entropy production and tie any memory claim to measured dissipation.
**Depends on:** Phase 4
**Requirements:** [DERV-06, SIMU-07, VALD-05]
**Contract Coverage:**
- Advances: thermodynamically consistent memory/error-correction account
- Deliverables: entropy-production estimator, sensitivity note, entropy-versus-memory figure
- Anchor coverage: operator-prompt dissipation requirement
- Forbidden proxies: qualitative irreversibility claims with no pathwise KL estimate
**Success Criteria** (what must be TRUE):

1. Forward and reverse path ensembles are defined explicitly.
2. The discretized pathwise KL estimator is implemented with a stated `Delta t`.
3. Sensitivity to `Delta t` is measured and reported.
4. Any retained-memory claim is bounded by a dissipation number.
   **Plans:** 2 plans

Plans:

- [ ] 05-01: Define forward/reverse path ensembles and implement the entropy-production estimator.
- [ ] 05-02: Compare entropy production against memory/recovery observables and report the bound.

### Phase 6: Falsifiable Predictions and Phase Diagrams

**Goal:** Produce threshold classifications and experimentally falsifiable predictions across lesions, stimulation, noise, and plasticity.
**Depends on:** Phase 5
**Requirements:** [SIMU-08, ANLY-03, ANLY-04, ANLY-05, ANLY-06, OUTP-01]
**Contract Coverage:**
- Advances: repair-threshold classification, hysteresis predictions, plasticity-versus-bias comparison, fast-slow breakdown
- Deliverables: phase diagrams, finite-size threshold plots, prediction ledger
- Anchor coverage: operator-prompt prediction checklist and finite-size requirement
- Forbidden proxies: single-size threshold claims or percolation analogies without same-lattice connectivity observables
**Success Criteria** (what must be TRUE):

1. Critical conductance threshold behavior is classified using `L = 16, 32, 64`.
2. For octanol-style disorder, bond dilution is compared directly against the 2D square-lattice bond-percolation threshold `p_c ~ 0.5`.
3. Connectivity and cluster-spanning observables are compared directly against repair thresholds.
4. Hysteresis, plasticity blockade, stimulation compression, and disorder/noise effects are reported as explicit falsifiable predictions.
5. Each prediction lists observable, control parameter, scaling or transition expectation, finite-size classification, and falsification criterion.
   **Plans:** 3 plans

Plans:

- [ ] 06-01: Run finite-size bond-dilution threshold and connectivity/percolation comparisons.
- [ ] 06-02: Sweep plasticity, static bias, stimulation, and noise controls to extract falsifiable predictions.
- [ ] 06-03: Package the code modules and parameter-sweep scripts used for all reported results.

### Phase 7: Manuscript and Artifact Packaging

**Goal:** Produce the manuscript and final artifact set with explicit claim-status labeling.
**Depends on:** Phase 6
**Requirements:** [OUTP-02, OUTP-03, OUTP-04]
**Contract Coverage:**
- Advances: publication-ready packaging
- Deliverables: LaTeX manuscript, figure suite, summary table
- Anchor coverage: all prior derivations, code, and verification outputs
- Forbidden proxies: polished prose without claim-status traceability or energetic-cost accounting
**Success Criteria** (what must be TRUE):

1. The manuscript includes model, asymptotics, obstruction derivations, generative-model section, disorder handling, entropy estimator, and biological interpretation limits.
2. Figures cover the required phase diagrams, lesion comparisons, reachability, basin, MI, entropy, and `epsilon` validity regimes.
3. The summary table labels each claim by mathematical status, assumptions, disorder dependence, energetic cost, biological interpretation, and falsifiability.
   **Plans:** 2 plans

Plans:

- [ ] 07-01: Draft the manuscript and integrate the final figure set.
- [ ] 07-02: Build the claim-status summary table and reproducibility appendix.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7

| Phase | Plans Complete | Status | Completed |
| --- | --- | --- | --- |
| 1. Simulation Foundation | 0/3 | Ready to plan | - |
| 2. Lyapunov Structure and Obstruction Terms | 0/3 | Not started | - |
| 3. Generative Model and Inference Correspondence | 0/2 | Not started | - |
| 4. Nonlinear Reachability and Information Propagation | 0/3 | Not started | - |
| 5. Thermodynamic Cost | 0/2 | Not started | - |
| 6. Falsifiable Predictions and Phase Diagrams | 0/3 | Not started | - |
| 7. Manuscript and Artifact Packaging | 0/2 | Not started | - |
