# Research State

## Project Reference

See: `.gpd/PROJECT.md` (updated 2026-03-16)

**Machine-readable scoping contract:** `.gpd/state.json` field `project_contract`

**Core research question:** For adaptive gap-junction networks with bistable fast voltage dynamics and slow coupling plasticity, what mathematically controlled regime, if any, supports Lyapunov-like reduction, morphology-conditioned information retention, and falsifiable repair thresholds before nonconservative flux, disorder, topology change, or fast-slow breakdown destroy that description?
**Current focus:** Phase 1: Simulation Foundation

## Current Position

**Current Phase:** 01
**Current Phase Name:** Simulation Foundation
**Total Phases:** 7
**Current Plan:** 1
**Total Plans in Phase:** 3
**Status:** Ready to plan
**Last Activity:** 2026-03-16
**Last Activity Description:** Bootstrapped the GPD project and injected empirical constraints on timescales, macrostate structure, and bond-dilution disorder.

**Progress:** [----------] 0%

## Active Calculations

- None yet - phase planning and implementation have not started.

## Intermediate Results

- None yet - no derivations or simulation outputs have been produced.

## Open Questions

- Which plasticity rule `Phi(Delta V, s_ij, xi_ij)` should be the base-case choice for balancing local biophysical plausibility with analytical tractability?
- Which low-dimensional feature map `phi(V)` is expressive enough for Phase 3 without being reverse-engineered to fit a desired objective and while separating WT, Cryptic, and DH?
- What reduced-order domain is acceptable for quasipotential or transition-path calculations if the full lattice is too expensive?

## Performance Metrics

| Label | Duration | Tasks | Files |
| --- | --- | --- | --- |
| bootstrap | - | 1 | 8 |

## Accumulated Context

### Decisions

Full log: `.gpd/DECISIONS.md`

**Recent high-impact:**
- [Phase 0]: Use the supplied operator prompt as the governing scoping contract and preserve it verbatim in `.gpd/intake/`.
- [Phase 0]: Keep the project literature-agnostic until explicit benchmark references are loaded rather than inventing anchors.

### Active Approximations

| Approximation | Validity Range | Controlling Parameter | Current Value | Status |
| --- | --- | --- | --- | --- |
| Fast-slow reduction | unperturbed `epsilon ~ 10^-3 to 10^-2`; breakdown tested upward | `epsilon = tau_V / tau_G` | `10^-3 to 10^-2` baseline | Pending validation |
| Reduced-order basin analysis | Small patch or coarse reduction only if justified | reduced state dimension | not set | Pending validation |

**Convention Lock:**

- Metric signature: not set
- Fourier convention: response/MI conventions to be set in Phase 1 if needed
- Natural units: lattice units with nondimensional groups
- Gauge choice: not set
- Regularization scheme: not set
- Renormalization scheme: not set
- Coordinate system: 2D square lattice with nearest-neighbor graph
- Spin basis: binary polarity macrostate when needed
- State normalization: probability distributions normalized to one
- Coupling convention: symmetric base case `G_ij = G_ji`
- Index positioning: sites `i, j`; edges `(i, j)`; lattice size `L`; time index implicit
- Time ordering: forward and time-reversed path ensembles for thermodynamic estimators
- Commutation convention: not set
- Levi-Civita sign: not set
- Generator normalization: not set
- Covariant derivative sign: not set
- Gamma matrix convention: not set
- Creation/annihilation order: not set

### Propagated Uncertainties

| Quantity | Current Value | Uncertainty | Last Updated (Phase) | Method |
| --- | --- | --- | --- | --- |
| none | - | - | - | - |

### Pending Todos

None yet.

### Blockers/Concerns

- No explicit external literature anchors or benchmark datasets have been added yet.
- The project has not yet chosen the base-case plasticity rule or voltage potential family.
- The project must either support a three-state WT/Cryptic/DH macrostate or state binary reduction as an explicit limitation.
- Octanol-like disorder must be modeled as bond dilution and compared with `p_c ~ 0.5`.
- Basin-geometry estimation on large lattices may require a justified reduced model.

## Session Continuity

**Last session:** 2026-03-16
**Stopped at:** Project bootstrap complete; Phase 1 ready to plan
**Resume file:** `.gpd/ROADMAP.md`
