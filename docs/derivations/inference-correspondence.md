# Inference Correspondence Note

## Purpose

This note starts Phase 3 from the completed Phase 2 baseline.

The central question is no longer whether the adaptive gap-junction system has
gradient structure. Phase 2 already isolated that point:

- a Lyapunov-like voltage functional exists for the symmetric fixed-`G` sector
- its descent target is homogenization, not the target AP morphology
- sustaining drive `h_i` can tilt the landscape toward a patterned state
- short field-off persistence is currently explained by slow Laplacian
  relaxation, not by a demonstrated metastable cryptic attractor

So the Phase 3 task is to classify, precisely, whether any explicit generative
model produces an exact correspondence, a reduced/local one, or only a
heuristic analogy.

## Objects To Define

We need three objects.

### 1. Macrostate Variable

Let

```text
m in {WT, Cryptic, DH}
```

be the morphology macrostate.

At present the code implements a coarse surrogate classifier based on posterior
depolarization propensity rather than a true three-well dynamical embedding.
That limitation must remain explicit throughout Phase 3.

### 2. Feature Map

Let

```text
phi(V)
```

be the coarse voltage feature map used by the generative model. The minimum
viable choice should be low-dimensional, explicit, and physically interpretable.

A natural starting point is

```text
phi(V) = (
    anterior_mean(V),
    posterior_mean(V),
    AP_differential(V),
    dh_propensity(V)
).
```

This matches the current codebase and avoids inventing hidden latent variables
 before they are justified.

### 3. Generative Family

We need an explicit prior and conditional family:

```text
P(m),
P(phi(V) | m).
```

The corresponding negative log objective is

```text
F_gen[V, m] = -log P(m) - log P(phi(V) | m).
```

If one marginalizes over `m`,

```text
F_marg[V] = -log sum_m P(m) P(phi(V) | m).
```

Any inference-style claim must compare the actual voltage dynamics against the
gradient of one of these explicitly defined objectives.

## Minimal Explicit Model

The smallest defensible Phase 3 model is:

```text
P(m = WT) = P(m = Cryptic) = P(m = DH) = 1/3
```

and a diagonal Gaussian likelihood on the current coarse feature map

```text
phi(V) = (
    anterior_mean,
    posterior_mean,
    AP_differential,
    dh_propensity
).
```

Choose macrostate target vectors

```text
mu_WT      = (V_A, V_P, V_A - V_P, 0)
mu_Cryptic = (V_A, (V_A + V_P)/2, (V_A - V_P)/2, 1/2)
mu_DH      = (V_A, V_A, 0, 1)
```

with diagonal width matrix `Sigma = diag(sigma_k^2)`. Then

```text
F_gen[V, m]
  = -log P(m)
  + (1/2) (phi(V) - mu_m)^T Sigma^(-1) (phi(V) - mu_m)
  + const.
```

This model is now implemented explicitly in
`research/adaptive_gap_junction/analysis.py`.

## Correspondence Test

The base deterministic driven voltage dynamics are

```text
tau_V dV_i/dt = - dL_eff/dV_i,
```

with

```text
L_eff[V]
  = sum_i U(V_i)
  + (1/2) sum_(i,j) G_ij (V_i - V_j)^2
  - sum_i h_i V_i.
```

An exact generative correspondence would require

```text
dV_i/dt = -M_ij(V) dF_gen/dV_j
```

for some positive mobility operator `M`, together with an explicit
identification of `m`, `phi(V)`, `P(m)`, and `P(phi(V)|m)`.

The immediate obstruction from Phase 2 is:

```text
argmin L_eff != target morphology
```

in the symmetric no-drive baseline.

This already rules out exact correspondence to a morphology-seeking inference
objective in that regime.

For the explicit Gaussian model above, the feature-space gradient has the form

```text
dF_gen/dV = J_phi(V)^T Sigma^(-1) (phi(V) - mu_m),
```

where `J_phi(V)` is the Jacobian of the coarse feature map. This makes the
current status especially clear:

- the objective is defined on a low-dimensional feature projection
- the actual lattice drift is defined site-by-site in full voltage space
- exact equality would require the full voltage drift to factor through the
  low-rank Jacobian of `phi`

That does not hold in the symmetric no-drive base case. So the explicit model
supports, at best, a reduced/local comparison rather than an exact dynamical
identification.

The Jacobian is now implemented explicitly for the current feature map in
`research/adaptive_gap_junction/analysis.py`. In the present surrogate model:

- `anterior_mean` and `posterior_mean` are linear site averages
- `AP_differential` is their difference
- `dh_propensity` is piecewise linear because the current code clamps it into
  `[0, 1]`

So `J_phi(V)` has rank at most four, while the voltage dynamics live in an
`L^2`-dimensional state space. That rank mismatch is the structural reason the
current generative model can only support a reduced comparison.

## Current Classification

Given the present evidence, the correspondence status is:

```text
No exact correspondence in the symmetric no-drive base case.
```

Reason:

1. A gradient structure exists.
2. Its minimizers are homogeneous or smoothing-dominated.
3. The target inference objective would need minima aligned with WT/Cryptic/DH
   morphology.
4. Therefore the issue is target mismatch, not missing gradient structure.

This is stronger than saying "the analogy is unproven." It says the base system
already points at the wrong target.

For the current explicit Gaussian generative family, the honest classification
is:

```text
reduced heuristic model available; no exact correspondence established.
```

The model is useful because it makes the comparison falsifiable, not because it
has already succeeded.

## Local Comparison Test

The correct local test is now:

```text
drift(V) ?~ -M J_phi(V)^T Sigma^(-1) (phi(V) - mu_m)
```

near a driven AP operating point, for some positive scalar or low-complexity
mobility `M`.

If the two vectors align only weakly, the result remains heuristic.
If they align well in a narrow neighborhood of a driven operating point, the
status upgrades to local reduced correspondence.
If they align generically in voltage space, that would support a much stronger
claim, but the current rank argument already makes that unlikely.

## Measured Operating-Point Check

The comparison was evaluated at the cleanest Case 1 baseline:

- fixed symmetric `G`
- static AP drive
- undiluted lattice
- no disorder noise
- linearized driven operating point `V_* = (-a I + G L)^(-1) h`

Two AP-drive amplitudes were checked in this setting.

| Drive amplitude `h_0` | Cosine alignment of `drift(V_*)` with `-grad_V F_gen(V_*, WT)` | Drift variance captured by feature subspace `R^2` |
| --- | ---: | ---: |
| `0.02` | `0.298` | `0.090` |
| `0.15` | `0.368` | `0.137` |

Interpretation:

- cosine similarity stays below `0.5`
- captured drift variance stays low
- increasing the drive does not rescue the correspondence

So the explicit coarse generative model does not support a meaningful local
reduced correspondence at the tested AP operating points.

## What Would Rescue Correspondence

A nontrivial correspondence could still exist in one of the following weaker
senses.

### Local Reduced Correspondence

Near a driven AP operating point, the tilted functional

```text
L_eff[V]
```

may approximate a morphology-seeking objective after projecting onto a reduced
feature space.

This would be a local or reduced correspondence, not a global one.

### Asymptotic Correspondence

If slow adaptation modifies `G_ij` so that the reduced effective landscape
develops a stable AP-patterned minimum, then one may obtain an asymptotic
correspondence after eliminating fast variables or averaging over timescales.

This remains to be shown and is not currently established.

### Heuristic Similarity Only

If the explicit `P(m)` and `P(phi(V)|m)` can only be chosen after engineering
them to mimic the derived dynamics, then the result is heuristic similarity, not
an earned inference correspondence.

## Phase 3 Working Theorem

The correct starting theorem for Phase 3 is:

```text
The symmetric adaptive gap-junction base model does not realize an exact
inference correspondence in the no-drive regime, because its explicit Lyapunov
structure descends toward homogenization rather than toward the target
morphology manifold.
```

What remains open is whether a reduced, driven, or adaptation-renormalized
correspondence exists once the generative objects are written down explicitly.

Given the measured operating-point check above, the current status is sharper:
the tested reduced surrogate fails to recover strong local drift alignment even
in the clean fixed-`G` driven comparison where it has the best chance to work.

## Immediate Next Steps

1. Define the smallest explicit macrostate prior `P(m)`.
2. Differentiate the explicit coarse objective with respect to the voltage
   variables via `J_phi(V)^T`.
3. Compare that reduced gradient against the actual driven and undriven voltage
   drifts.
4. Determine whether the driven AP operating point supports a local reduced
   correspondence.
5. Keep exact, asymptotic, and heuristic classifications separate.

## Phase Boundary

Phase 2 is sufficiently complete to support Phase 3 because the key obstruction
has been identified sharply:

```text
gradient structure exists, but it optimizes the wrong thing.
```

Cases 2 and 3 from the Lyapunov note remain useful follow-on derivations, but
they are no longer blocking the core scientific question.

## Phase 3 Classification

The honest Phase 3 classification, using the operator-prompt categories, is:

```text
heuristic similarity only;
correspondence fails at the tested operating points.
```

The publishable positive statement is therefore the obstruction result:

```text
exact correspondence is dimensionally obstructed, and the current reduced
surrogate does not recover a strong local alignment with the actual adaptive
bioelectric drift.
```
