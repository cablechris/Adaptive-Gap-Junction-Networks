# GPD Operator Prompt

## Adaptive Gap-Junction Networks and the Physical Limits of Non-Equilibrium Morphological Inference

### Preserved User Prompt

PREFLIGHT CONSTRAINTS

- No global gradient assumption. Do not assume the joint `(V, G)` dynamics are globally gradient. Prove it, disprove it, or bracket the regime where it holds.
- No free inference claim. Do not use "variational free energy", "belief", or "inference" until `P(m)` and `P(V|m)` have been explicitly defined. If the generative model was engineered to match the Lyapunov structure post hoc, say so. That is relabeling, not correspondence.
- No free timescale separation. Treat `epsilon = tau_V / tau_G` as a primary asymptotic parameter with a finite validity domain. Derive the breakdown threshold explicitly.
- No free disorder. Every disorder term must be classified (site / bond / random-field / random-bond / dilution), assigned a stated distribution, and tested for relevance to the observed transition.
- No zero-out lesions. Ablation = topological removal + Laplacian update + Neumann boundary conditions on survivors. Zeroing `V_i` without graph surgery is a sink, not a cut. Treat them separately throughout.
- No linear Gramian as primary reachability metric. `U(V)` is nonlinear and bistable. Use ensemble-based empirical reachability with a fully specified ensemble: initial-condition distribution, perturbation amplitude, duration, horizon `T`, trajectory count, and attractor conditioning.
- No free FTLEs as basin boundaries. FTLEs are local sensitivity indicators only. Basin structure requires quasipotential estimates, minimum-action paths, or transition-path statistics.
- No free memory. Every claimed morphological memory or coupling-encoded constraint must carry an explicit dissipation estimate. Use pathwise KL divergence between forward and time-reversed trajectories as the entropy-production estimator.
- Label every result. Each conclusion must be labeled as one of: exact derivation / local result / asymptotic result / numerical result / interpretive claim. Do not generalize a local result.
- Negative results are acceptable. A clean proof of nonexistence or obstruction is a full success criterion.
- No hidden term dropping. If a Lyapunov-like functional is obtained only after neglecting terms, list those terms explicitly and quantify their magnitude over the simulated parameter range.

MODEL

- Geometry: 2D square lattice, `N` cells, nearest-neighbor coupling, optional quenched disorder with specified distribution before use.
- Fast dynamics (Layer A): `tau_V Vdot_i = -dU(V_i)/dV_i + sum_{j in N(i)} G_ij (V_j - V_i) + I_i^ext + eta_i(t)`.
- `U(V)`: double-well or excitable potential. No global linearization.
- `eta_i(t)`: Gaussian white noise with stated amplitude `D`.
- `I_i^ext`: injury, stimulation, or chemo-mechanical input.
- Slow dynamics (Layer B): `tau_G Gdot_ij = Phi(V_i - V_j, s_ij, xi_ij) - lambda_G G_ij`.
- `Phi`: local plasticity rule, specified explicitly.
- Base case: `G_ij = G_ji` (symmetric).
- Morphological macrostate (Layer C): default binary head-tail polarity.

PHASES

1. Phase 1 - Simulation Foundation
2. Phase 2 - Lyapunov Structure and Obstruction Terms
3. Phase 3 - Generative Model and Inference Correspondence
4. Phase 4 - Nonlinear Reachability and Information Propagation
5. Phase 5 - Thermodynamic Cost
6. Phase 6 - Falsifiable Predictions and Phase Diagrams

OUTPUTS

- LaTeX manuscript
- Python codebase
- Figures
- Summary table

SUCCESS CRITERIA

- Restricted regime with valid Lyapunov-like functional
- Sharp asymptotic account of when and why that structure fails
- Nonlinear, reproducibly defined replacement for the naive cognitive light cone
- Disorder-aware account of whether repair threshold is distinct from percolation structure
- Thermodynamically consistent account of tissue-scale error correction
- Robust falsifiable predictions about thresholds, hysteresis, topology-sensitive repair, or stimulation-induced fast-slow breakdown
- A clean negative result, mathematically sharp, is a full success

Do not complete the analogy unless the equations earn it.

### Injected Empirical Constraints

- `tau_V ~ hours`, `tau_G ~ days-weeks`, so unperturbed `epsilon = tau_V / tau_G ~ 10^-2 to 10^-3`. Do not assume faster separation.
- Morphological macrostate `m` is three-valued: `WT`, `Cryptic`, `DH`. `DH` is a stable non-equilibrium attractor, not a transient. Both `Cryptic` and `DH` reset to `WT` via hyperpolarization. Either extend `U(V)` to three wells or declare binary `m` an explicit scope limitation in the manuscript.
- Octanol-mediated gap-junction blockade is bond dilution, not uniform conductance scaling. Test whether the polarity-disruption threshold coincides with the 2D square-lattice bond-percolation critical point `p_c ≈ 0.5`.
