# Lyapunov Structure and Obstruction Note

## Purpose

This note fixes the deterministic base-case system for Phase 2 and records the first analytic conclusion carried forward from Phase 1:

- a Lyapunov-like functional exists for the symmetric no-drive base case
- its descent favors homogeneous voltage states
- the obstruction to an inference-style correspondence is not the absence of gradient structure, but the mismatch between the functional's attractor and the target AP morphology

## Base-Case System

We analyze the deterministic lattice model with:

- nearest-neighbor square-lattice graph
- symmetric adaptive couplings `G_ij = G_ji >= 0`
- no stochastic forcing
- no lesion current, injury current, or disorder offsets
- no external polarity-maintaining drive `h_i`

Write the voltage dynamics as

```text
tau_V dV_i/dt = f(V_i) + sum_{j ~ i} G_ij (V_j - V_i)
```

with on-site force

```text
f(V) = a V - b V^3 = - dU/dV,
U(V) = -a V^2 / 2 + b V^4 / 4.
```

For the base adaptive rule used in Phase 1,

```text
tau_G dG_ij/dt = Phi(Delta_ij) - lambda_G G_ij,
Delta_ij = V_i - V_j.
```

The two sign choices tested empirically were

```text
Phi(Delta_ij) = -alpha |Delta_ij|
Phi(Delta_ij) = +alpha |Delta_ij|.
```

The Laplacian contribution is

```text
(L_G V)_i = sum_{j ~ i} G_ij (V_i - V_j),
```

so the voltage equation is equivalently

```text
tau_V dV_i/dt = - dU/dV_i - (L_G V)_i.
```

## Candidate Functional

For fixed symmetric `G`, the natural functional is

```text
L[V ; G] = sum_i U(V_i) + (1/2) sum_{(i,j)} G_ij (V_i - V_j)^2.
```

Here `(i, j)` denotes each undirected occupied edge counted once. Equivalently, if one sums over ordered pairs `(i, j)` and `(j, i)`, the same coupling energy is written with coefficient `1/4`.

Its voltage gradient is

```text
dL/dV_i = dU/dV_i + sum_{j ~ i} G_ij (V_i - V_j),
```

which gives

```text
tau_V dV_i/dt = - dL/dV_i.
```

Therefore, for frozen symmetric `G`,

```text
dL/dt = sum_i (dL/dV_i) dV_i/dt
      = -(1/tau_V) sum_i (dL/dV_i)^2
      <= 0.
```

This is the cleanest exact gradient statement available from the present model.

## Homogeneous-State Preference

The coupling term satisfies

```text
(1/2) sum_{(i,j)} G_ij (V_i - V_j)^2 >= 0
```

with equality if and only if `V_i = V_j` on every occupied connected edge. On each connected component, the coupling energy is thus minimized by spatially homogeneous voltages.

This is the core Phase 1 carry-forward result:

- symmetric diffusive coupling is a graph-Laplacian smoothing operator
- increasing bond dilution weakens that smoothing
- AP differential therefore increases as dilution removes smoothing edges
- this trend does not depend on the sign of `Phi` as long as the coupling remains symmetric and diffusive

So the functional descends toward homogeneous states, not toward the target AP morphology.

## What Changes When `G` Adapts

If `G_ij` evolves, then the fixed-`G` proof above is no longer the whole story. For the extended candidate

```text
L[V, G] = sum_i U(V_i) + (1/2) sum_{(i,j)} G_ij (V_i - V_j)^2 + R(G),
```

the `V` sector still contributes a negative-definite term,

```text
-(1/tau_V) sum_i (dL/dV_i)^2,
```

but the `G` sector produces extra terms involving

```text
(1/2) (V_i - V_j)^2 dG_ij/dt + (dR/dG_ij) dG_ij/dt.
```

For the present Phase 2 starting point, the decisive analytic fact is already visible before choosing `R(G)`:

- the voltage part of the dynamics is gradient descent for fixed symmetric `G`
- the attractor selected by the Laplacian term is homogenization
- any adaptive extension must overcome that target mismatch, not create gradient structure from nothing

## Drive Threshold Framing

Phase 1 showed that AP pattern maintenance requires the non-equilibrium drive `h_i`. The threshold problem for Phase 2 is therefore:

```text
tau_V dV_i/dt = - dU/dV_i - (L_G V)_i + h_i.
```

To maintain a target AP gradient, `h_i` must compensate the Laplacian smoothing term at the relevant mode scale. The smallest sustaining drive should therefore scale with:

- typical occupied-edge conductance magnitude
- graph spectrum of the diluted Laplacian
- system size `L`
- dilution fraction through the occupied-edge set

### Linearized AP-Mode Estimate

Let the target morphology be projected onto the first AP mode of the free-boundary square lattice,

```text
V(x, y, t) ~= A(t) phi_1(x),
```

where `phi_1` varies along the AP axis and is constant along the transverse direction. For the intact square lattice with free boundaries, the first non-constant Laplacian eigenvalue is

```text
lambda_1(L) = 2 (1 - cos(pi / L)).
```

Under bond dilution, a mean-field effective Laplacian replaces `G` by `p G_bar`, where `p` is the occupied-edge fraction. Linearizing the on-site force near the origin gives

```text
f(V) ~= a V,
```

so the AP-mode amplitude obeys

```text
tau_V dA/dt ~= (a - p G_bar lambda_1(L)) A + h_1.
```

Therefore the projected drive needed to hold a target amplitude `A_*` is

```text
h_1^*(L, p, G_bar, A_*) = (p G_bar lambda_1(L) - a) A_*.
```

Interpreted as a minimum external sustaining drive,

```text
h_min = max(0, (p G_bar lambda_1(L) - a) A_*).
```

Here `a` is the linear coefficient of the on-site voltage force,

```text
f(V) = a V - b V^3,
```

or equivalently the negative curvature of the local potential at the origin. It is not the conductance decay rate `lambda_G`. The role of `a` in this threshold estimate is purely voltage-sector: it measures how strongly the local double-well dynamics amplify the AP mode near the linearization point. The role of `lambda_G` enters only once adaptive `G_ij` dynamics are restored in the joint `(V, G)` analysis.

This gives the right first-order trends:

- larger conductance requires larger sustaining drive
- larger bond occupation requires larger sustaining drive
- larger systems require smaller first-mode eigenvalue and therefore weaker AP-mode smoothing per unit conductance
- dilution lowers the drive needed to maintain the AP mode because it weakens Laplacian smoothing

This is a mean-field dilution approximation. Replacing the bond-diluted Laplacian by `p L_full` is exact only in an annealed disorder picture where occupied bonds fluctuate independently in time. The current simulations use quenched bond dilution: the occupied graph is fixed at initialization. Near the percolation threshold, the true first non-constant eigenvalue of the quenched graph drops faster than the linear `p` estimate because connectivity becomes filamentary and non-mean-field. So the formula above is a useful first approximation, but it should be expected to underestimate the required sustaining drive near `p_c`.

This is not yet the full nonlinear threshold. It is the controlled first approximation around the dominant AP mode and is the correct bridge from the Lyapunov argument to the simulation trends.

### Post-Drive Relaxation Timescale

After drive removal, the same AP-mode projection gives the Laplacian homogenization timescale

```text
tau_relax ~= tau_V / (p G_bar lambda_1(L)).
```

This estimate intentionally isolates the smoothing contribution. It is the right first diagnostic for field-suppression experiments:

- if `tau_relax` is much longer than the observation window, apparent pattern persistence is consistent with slow relaxation alone
- if `tau_relax` is much shorter than the observation window, then some additional stabilizing mechanism is required

For the current recovery-window scale used in the Phase 1 experiments,

```text
200 steps * dt = 200 * 0.02 = 4 tau_V,
```

and for representative parameters `G_bar = 0.2 ... 1.0`, `p ~= 0.5`, `L = 16`, and `lambda_1(16) ~= 0.0384`,

```text
tau_relax ~= 1 / (0.5 * G_bar * 0.0384) ~= 52 ... 260.
```

So persistence over a `4 tau_V` recovery window is consistent with slow homogenization and does not by itself establish a metastable field-off cryptic attractor.

## Task 3 Baseline Ordering

The symmetry-breaking analysis should proceed in this order:

1. Static `h_i`, fixed `G_ij`
2. Static `h_i`, adaptive `G_ij`
3. `h_i -> 0` during recovery

The cleanest exact baseline is the fixed-`G` driven system with effective functional

```text
L_eff[V] = sum_i U(V_i) + (1/2) sum_{(i,j)} G_ij (V_i - V_j)^2 - sum_i h_i V_i.
```

The tilt term `- sum_i h_i V_i` breaks the symmetry of the undriven homogeneous landscape and selects the AP mode once its amplitude exceeds the smoothing threshold. This is the simplest controlled case in which the target of descent is no longer homogeneous.

### Case 1: Fixed `G`, Static `h`

Using the unordered-edge convention above, stationarity of `L_eff` gives

```text
dU/dV_i + sum_{j ~ i} G_ij (V_i - V_j) = h_i.
```

Since the dynamical on-site force is

```text
f_dyn(V) = - dU/dV = a V - b V^3,
```

the same fixed-point equation can be written as

```text
-f_dyn(V_i) + sum_{j ~ i} G_ij (V_i - V_j) = h_i.
```

Linearizing near the midpoint `V_i ~= 0` gives

```text
dU/dV_i ~= -a V_i,
```

so the linear-response fixed point satisfies

```text
(-a I + G_bar L) V_* = h,
V_* = (-a I + G_bar L)^(-1) h.
```

This is the Case 1 baseline implemented in `research/adaptive_gap_junction/analysis.py`.

Two caveats matter:

1. `(-a I + G_bar L)` is the linearized stationarity operator around the midpoint of the double well. Its invertibility is the correct first response calculation for the AP mode, but it does not by itself prove that the full quartic `L_eff` has a unique global minimum.
2. The condition

```text
a > G_bar lambda_max(L)
```

puts the linearized operator in the negative-definite regime used by this approximation. For the square-lattice graph, `lambda_max(L)` is bounded by `4` and approaches `8` only in periodic or higher-degree conventions. In the current free-boundary nearest-neighbor lattice, using the exact graph Laplacian is better than substituting a bulk value by hand.

Given a chosen AP-shaped drive vector `h`, the linearized AP differential is then

```text
A_* = <h, V_*> / ||h||^2
    = <h, (-a I + G_bar L)^(-1) h> / ||h||^2.
```

For a pure first AP-mode drive, this reduces to the scalar gain law

```text
A_* ~ h_0 / (a - G_bar lambda_1(L))
```

within the present sign convention for the response operator. This is the clean reference point that later cases modify through conductance adaptation and drive removal.

## Correspondence Obstruction

The inference-style correspondence fails in the symmetric no-drive base case for a precise reason:

1. A gradient structure exists at least in the frozen-`G` voltage sector.
2. Its descent direction suppresses spatial variation.
3. The target morphology is spatially structured.
4. Therefore the mismatch is between the functional's minimizers and the desired morphology, not between the dynamics and gradient descent itself.

This is the obstruction to carry into later phases:

```text
existing functional attractor != target morphology.
```

## Symmetry Breaking Needed For A Correspondence

To make a morphology-seeking correspondence plausible, the model must break the symmetric homogenizing target in at least one controlled way:

- asymmetric or non-reciprocal `G_ij`
- spatially inhomogeneous sustaining drive `h_i`
- a plasticity rule not reducible to symmetric diffusive smoothing driven only by `|Delta V|`

These are the Phase 2 comparison cases, not assumptions for the base proof.
