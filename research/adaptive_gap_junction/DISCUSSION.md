# Discussion

## What We Set Out To Test

This project asked whether adaptive gap-junction network dynamics admit a
controlled Lyapunov description and, if so, whether that description supports a
genuine inference-like correspondence rather than a loose analogy.

## Main Findings

The symmetric no-drive base model does admit a Lyapunov-like functional. In the
fixed-conductance sector, the voltage dynamics are gradient descent on an
explicit energy built from the on-site double-well potential and the
graph-Laplacian coupling term.

That functional does not stabilize target morphology. Its minima favor spatially
homogeneous voltage states, so the core obstruction is not the absence of
gradient structure. The obstruction is that the system descends toward the wrong
attractor.

Pattern maintenance requires explicit non-equilibrium drive. A linearized AP-mode
analysis shows that sustaining an anterior-posterior gradient requires a spatially
structured drive term that offsets Laplacian smoothing. This is consistent with
the empirical Phase 1 result that bond dilution increases AP differential by
weakening diffusive smoothing.

Field-off persistence is not yet evidence of metastability. The estimated
homogenization timescale is much longer than the recovery window used in the
simulations, so short-term persistence after drive removal is currently explained
by slow relaxation rather than by a demonstrated cryptic attractor.

## Inference Correspondence

We then tested the strongest version of the inference claim by writing down an
explicit coarse-grained generative model on the current morphology feature map.

The key structural result is dimensional: the feature Jacobian has rank at most
4, while the voltage dynamics live in an `L^2`-dimensional state space. Exact
correspondence would require the generative gradient to span the full drift, so
this is already a hard obstruction to exact inference equivalence for the current
model class.

We measured the local comparison directly at clean driven operating points by
comparing the deterministic voltage drift against the pulled-back coarse
generative gradient. Alignment was weak and the captured drift variance was low,
so the explicit surrogate supports only heuristic similarity, not exact or local
reduced equivalence.

## Interpretation

The positive result is not that the system implements inference. The positive
result is that we can now state precisely why that stronger claim fails in the
tested regime:

- gradient structure exists
- it optimizes homogenization rather than morphology
- exact correspondence is dimensionally obstructed
- the tested reduced surrogate does not recover strong local drift alignment

## Scope Limits

These conclusions apply to the current symmetric base model and the present
coarse morphology surrogate. They do not rule out all future correspondence
claims in modified models. In particular, a reduced or asymptotic correspondence
could still emerge if adaptation changes the effective landscape, if the drive is
treated as part of the objective in a controlled way, or if a more faithful
macrostate representation is introduced.

## Bottom Line

The current adaptive gap-junction model supports a clean Lyapunov analysis, but
that analysis points away from an inference interpretation rather than toward
one. The strongest honest summary is:

```text
gradient structure exists, but it optimizes the wrong thing.
```
