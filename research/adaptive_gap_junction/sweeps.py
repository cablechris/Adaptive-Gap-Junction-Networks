from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random

from .disorder import apply_disorder, apply_quenched_edge_removals
from .dynamics import step
from .initialization import initial_state
from .morphology import classify_macrostate
from .model import DisorderKind, DisorderSpec, PolarityFieldSpec, SimulationConfig
from .observables import ap_voltage_variance, consensus_fraction, final_abs_mean_voltage, polarity_contrast, spatial_variance
from .percolation import has_spanning_cluster
from .simulator import run_simulation


OUTPUT_DIR = Path("research/adaptive_gap_junction/results")


@dataclass(slots=True)
class RunSummary:
    lattice_size: int
    dilution_fraction: float
    bond_occupation: float
    replicate: int
    seed: int
    epsilon: float
    abs_mean_voltage: float
    polarity_contrast: float
    consensus_fraction: float
    spanning_cluster: bool


@dataclass(slots=True)
class SweepRow:
    lattice_size: int
    dilution_fraction: float
    mean_bond_occupation: float
    mean_abs_voltage: float
    mean_polarity_contrast: float
    mean_consensus_fraction: float
    spanning_probability: float
    disrupted_fraction: float


@dataclass(slots=True)
class RecoveryRunSummary:
    lesion_kind: str
    lattice_size: int
    dilution_fraction: float
    replicate: int
    seed: int
    lesion_steps: int
    recovery_steps: int
    lesion_size: int
    pre_lesion_polarity_contrast: float
    final_anterior_mean: float
    final_posterior_mean: float
    final_ap_differential: float
    post_recovery_polarity_contrast: float
    recovery_fidelity: float
    final_spatial_variance: float
    final_macrostate: str
    final_dh_propensity: float
    bond_occupation: float
    lesioned_spanning_cluster: bool


@dataclass(slots=True)
class RecoverySweepRow:
    lesion_kind: str
    lattice_size: int
    dilution_fraction: float
    mean_bond_occupation: float
    mean_recovery_fidelity: float
    mean_final_anterior_mean: float
    mean_final_posterior_mean: float
    mean_final_ap_differential: float
    mean_post_recovery_polarity_contrast: float
    mean_final_spatial_variance: float
    mean_final_dh_propensity: float
    lesioned_spanning_probability: float
    failed_recovery_fraction: float
    wt_fraction: float
    cryptic_fraction: float
    dh_fraction: float


def occupied_edges_from_dilution(config: SimulationConfig) -> tuple[dict[tuple[int, int], float], set[int]]:
    rng = random.Random(config.disorder.seed)
    voltages, _polarity_field, _polarity_target, conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
    _site_offsets, edge_scales = apply_disorder(config, voltages, conductances, rng)
    updated_conductances, _updated_neighbors = apply_quenched_edge_removals(conductances, neighbors, edge_scales)
    occupied_edges = {edge: 1.0 for edge in updated_conductances}
    return occupied_edges, active_nodes


def bond_occupation_fraction(config: SimulationConfig) -> float:
    occupied_edges, _active_nodes = occupied_edges_from_dilution(config)
    _voltages, _polarity_field, _polarity_target, conductances, _active, _sink, _neighbors = initial_state(config)
    total_edges = len(conductances)
    if total_edges == 0:
        return 0.0
    return len(occupied_edges) / total_edges


def build_sweep_config(
    lattice_size: int,
    dilution_fraction: float,
    replicate: int,
    base_conductance: float = 0.35,
    polarity_field_amplitude: float = 0.15,
    polarity_field_tau_h: float = 2_000.0,
    well_linear: float = 1.0,
    well_cubic: float = 1.0,
) -> SimulationConfig:
    seed = lattice_size * 10_000 + int(round(dilution_fraction * 1_000)) * 10 + replicate
    return SimulationConfig(
        lattice_size=lattice_size,
        tau_v=1.0,
        tau_g=100.0,
        base_conductance=base_conductance,
        well_linear=well_linear,
        well_cubic=well_cubic,
        steps=300,
        noise_amplitude=0.02,
        polarity_field=PolarityFieldSpec(
            enabled=True,
            amplitude=polarity_field_amplitude,
            tau_h=polarity_field_tau_h,
        ),
        disorder=DisorderSpec(
            kind=DisorderKind.DILUTION,
            distribution="bernoulli bond dilution with removal fraction f_b",
            strength=dilution_fraction,
            seed=seed,
        ),
    )


def summarize_run(config: SimulationConfig, replicate: int) -> RunSummary:
    history = run_simulation(config)
    final_state = history[-1]
    occupied_edges, active_nodes = occupied_edges_from_dilution(config)
    return RunSummary(
        lattice_size=config.lattice_size,
        dilution_fraction=config.disorder.strength,
        bond_occupation=bond_occupation_fraction(config),
        replicate=replicate,
        seed=config.disorder.seed,
        epsilon=config.epsilon,
        abs_mean_voltage=final_abs_mean_voltage(final_state.voltages),
        polarity_contrast=polarity_contrast(
            final_state.voltages,
            lattice_size=config.lattice_size,
            axis=config.polarity_axis,
        ),
        consensus_fraction=consensus_fraction(final_state.voltages),
        spanning_cluster=has_spanning_cluster(config.lattice_size, occupied_edges, active_nodes),
    )


def aggregate_rows(rows: list[RunSummary], undiluted_reference: float) -> SweepRow:
    count = len(rows)
    disrupted = [row for row in rows if abs(row.polarity_contrast) <= 0.5 * undiluted_reference]
    return SweepRow(
        lattice_size=rows[0].lattice_size,
        dilution_fraction=rows[0].dilution_fraction,
        mean_bond_occupation=sum(row.bond_occupation for row in rows) / count,
        mean_abs_voltage=sum(row.abs_mean_voltage for row in rows) / count,
        mean_polarity_contrast=sum(row.polarity_contrast for row in rows) / count,
        mean_consensus_fraction=sum(row.consensus_fraction for row in rows) / count,
        spanning_probability=sum(1.0 for row in rows if row.spanning_cluster) / count,
        disrupted_fraction=len(disrupted) / count,
    )


def estimate_threshold(rows: list[SweepRow], field_name: str, crossing_value: float) -> float | None:
    for row in sorted(rows, key=lambda item: item.dilution_fraction):
        value = getattr(row, field_name)
        if value >= crossing_value:
            return 1.0 - row.dilution_fraction
    return None


def estimate_spanning_threshold(rows: list[SweepRow], crossing_value: float = 0.5) -> float | None:
    threshold: float | None = None
    for row in sorted(rows, key=lambda item: item.dilution_fraction):
        if row.spanning_probability >= crossing_value:
            threshold = 1.0 - row.dilution_fraction
    return threshold


def run_bond_dilution_sweep(
    lattice_sizes: tuple[int, ...] = (16, 32, 64),
    dilution_grid: tuple[float, ...] = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7),
    replicates: int = 6,
) -> dict[str, object]:
    all_runs: list[RunSummary] = []
    all_rows: list[SweepRow] = []
    notes = [
        "Operational polarity-disruption metric: abs(polarity contrast) falls below 50% of the undiluted polarity contrast for the same lattice size.",
        "This sweep still uses a voltage-based surrogate rather than an explicit WT/Cryptic/DH classifier.",
        "Initial condition is a stable anterior/posterior voltage pattern rather than the unstable V=0 barrier state.",
        "Bond-dilution comparison target for octanol-style blockade: 2D square-lattice bond percolation p_c ~ 0.5.",
    ]

    for lattice_size in lattice_sizes:
        baseline_config = build_sweep_config(lattice_size=lattice_size, dilution_fraction=0.0, replicate=0)
        baseline_summary = summarize_run(baseline_config, replicate=0)
        undiluted_reference = max(abs(baseline_summary.polarity_contrast), 1e-9)
        size_rows: list[SweepRow] = []

        for dilution_fraction in dilution_grid:
            run_summaries: list[RunSummary] = []
            for replicate in range(replicates):
                config = build_sweep_config(lattice_size=lattice_size, dilution_fraction=dilution_fraction, replicate=replicate)
                summary = summarize_run(config, replicate=replicate)
                run_summaries.append(summary)
                all_runs.append(summary)
            aggregated = aggregate_rows(run_summaries, undiluted_reference=undiluted_reference)
            size_rows.append(aggregated)
            all_rows.append(aggregated)

        disruption_threshold = estimate_threshold(size_rows, field_name="disrupted_fraction", crossing_value=0.5)
        spanning_threshold = estimate_spanning_threshold(size_rows, crossing_value=0.5)
        notes.append(f"L={lattice_size}: estimated polarity threshold p~{disruption_threshold} and spanning threshold p~{spanning_threshold}.")

    return {
        "metadata": {
            "lattice_sizes": list(lattice_sizes),
            "dilution_grid": list(dilution_grid),
            "replicates": replicates,
            "percolation_target_pc": 0.5,
            "notes": notes,
        },
        "rows": [asdict(row) for row in all_rows],
        "runs": [asdict(run) for run in all_runs],
    }


def write_bond_dilution_sweep(output_path: Path | None = None) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = output_path or OUTPUT_DIR / "bond_dilution_sweep.json"
    payload = run_bond_dilution_sweep()
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return target


def default_sink_patch(lattice_size: int, width: int = 2) -> tuple[int, ...]:
    center = lattice_size // 2
    half_width = max(1, width // 2)
    patch: list[int] = []
    row_start = max(0, center - half_width)
    row_stop = min(lattice_size, row_start + width)
    col_start = max(0, center - half_width)
    col_stop = min(lattice_size, col_start + width)
    for row in range(row_start, row_stop):
        for col in range(col_start, col_stop):
            patch.append(row * lattice_size + col)
    return tuple(patch)


def default_midline_edge_cut(lattice_size: int, axis: str = "x") -> tuple[tuple[int, int], ...]:
    edges: list[tuple[int, int]] = []
    if axis == "x":
        left_col = max(0, lattice_size // 2 - 1)
        right_col = min(lattice_size - 1, left_col + 1)
        for row in range(lattice_size):
            left = row * lattice_size + left_col
            right = row * lattice_size + right_col
            edges.append((left, right))
        return tuple(edges)

    top_row = max(0, lattice_size // 2 - 1)
    bottom_row = min(lattice_size - 1, top_row + 1)
    for col in range(lattice_size):
        top = top_row * lattice_size + col
        bottom = bottom_row * lattice_size + col
        edges.append((top, bottom))
    return tuple(edges)


def remove_edges_from_graph(
    conductances: dict[tuple[int, int], float],
    neighbors: dict[int, tuple[int, ...]],
    severed_edges: set[tuple[int, int]],
) -> tuple[dict[tuple[int, int], float], dict[int, tuple[int, ...]]]:
    updated_conductances = {
        edge: value for edge, value in conductances.items() if edge not in severed_edges
    }
    updated_neighbors: dict[int, tuple[int, ...]] = {}
    for node, adjacent in neighbors.items():
        updated_neighbors[node] = tuple(
            other for other in adjacent if (min(node, other), max(node, other)) not in severed_edges
        )
    return updated_conductances, updated_neighbors


def add_localized_current(
    site_offsets: list[float],
    nodes: tuple[int, ...],
    amplitude: float,
) -> list[float]:
    updated_offsets = list(site_offsets)
    for node in nodes:
        updated_offsets[node] += amplitude
    return updated_offsets


def suppress_local_polarity_target(
    polarity_target: list[float],
    nodes: tuple[int, ...],
) -> list[float]:
    updated_target = list(polarity_target)
    for node in nodes:
        updated_target[node] = 0.0
    return updated_target


def run_sink_recovery_protocol(
    config: SimulationConfig,
    lesion_nodes: tuple[int, ...],
    clamp_voltage: float = -1.0,
    lesion_steps: int = 40,
    recovery_steps: int = 120,
    lesion_current: float = 0.0,
    suppress_field_during_recovery: bool = False,
) -> RecoveryRunSummary:
    rng = random.Random(config.disorder.seed)
    voltages, polarity_field, polarity_target, conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
    site_offsets, edge_scales = apply_disorder(config, voltages, conductances, rng)
    conductances, neighbors = apply_quenched_edge_removals(conductances, neighbors, edge_scales)
    occupied_edges, active_for_span = occupied_edges_from_dilution(config)

    pre_lesion = polarity_contrast(voltages, lattice_size=config.lattice_size, axis=config.polarity_axis)
    lesion_site_offsets = add_localized_current(site_offsets, lesion_nodes, lesion_current)
    lesion_polarity_target = suppress_local_polarity_target(polarity_target, lesion_nodes)
    recovery_polarity_target = lesion_polarity_target if suppress_field_during_recovery else polarity_target

    for _ in range(lesion_steps):
        lesion_sink_nodes = set(lesion_nodes)
        voltages, polarity_field, conductances = step(
            config=config,
            voltages=voltages,
            polarity_field=polarity_field,
            polarity_target=lesion_polarity_target,
            conductances=conductances,
            active_nodes=active_nodes,
            sink_nodes=lesion_sink_nodes,
            neighbors=neighbors,
            site_offsets=lesion_site_offsets,
            edge_scales=edge_scales,
            rng=rng,
        )
        for node in lesion_nodes:
            voltages[node] = clamp_voltage

    for _ in range(recovery_steps):
        voltages, polarity_field, conductances = step(
            config=config,
            voltages=voltages,
            polarity_field=polarity_field,
            polarity_target=recovery_polarity_target,
            conductances=conductances,
            active_nodes=active_nodes,
            sink_nodes=set(),
            neighbors=neighbors,
            site_offsets=site_offsets,
            edge_scales=edge_scales,
            rng=rng,
        )

    post_recovery = polarity_contrast(voltages, lattice_size=config.lattice_size, axis=config.polarity_axis)
    anterior_mean, posterior_mean, ap_differential, _ap_variance = ap_voltage_variance(
        voltages,
        lattice_size=config.lattice_size,
        axis=config.polarity_axis,
    )
    baseline_scale = max(abs(pre_lesion), 1e-9)
    recovery_fidelity = abs(post_recovery) / baseline_scale
    morphology = classify_macrostate(voltages, config)
    return RecoveryRunSummary(
        lesion_kind="sink",
        lattice_size=config.lattice_size,
        dilution_fraction=config.disorder.strength,
        replicate=int(str(config.disorder.seed)[-1]) if str(config.disorder.seed)[-1].isdigit() else 0,
        seed=config.disorder.seed,
        lesion_steps=lesion_steps,
        recovery_steps=recovery_steps,
        lesion_size=len(lesion_nodes),
        pre_lesion_polarity_contrast=pre_lesion,
        final_anterior_mean=anterior_mean,
        final_posterior_mean=posterior_mean,
        final_ap_differential=ap_differential,
        post_recovery_polarity_contrast=post_recovery,
        recovery_fidelity=recovery_fidelity,
        final_spatial_variance=spatial_variance(voltages),
        final_macrostate=morphology.macrostate,
        final_dh_propensity=morphology.features.dh_propensity,
        bond_occupation=bond_occupation_fraction(config),
        lesioned_spanning_cluster=has_spanning_cluster(config.lattice_size, occupied_edges, active_for_span),
    )


def aggregate_recovery_rows(rows: list[RecoveryRunSummary]) -> RecoverySweepRow:
    count = len(rows)
    failures = [row for row in rows if row.recovery_fidelity < 0.5]
    wt_rows = [row for row in rows if row.final_macrostate == "wt"]
    cryptic_rows = [row for row in rows if row.final_macrostate == "cryptic"]
    dh_rows = [row for row in rows if row.final_macrostate == "dh"]
    return RecoverySweepRow(
        lesion_kind=rows[0].lesion_kind,
        lattice_size=rows[0].lattice_size,
        dilution_fraction=rows[0].dilution_fraction,
        mean_bond_occupation=sum(row.bond_occupation for row in rows) / count,
        mean_recovery_fidelity=sum(row.recovery_fidelity for row in rows) / count,
        mean_final_anterior_mean=sum(row.final_anterior_mean for row in rows) / count,
        mean_final_posterior_mean=sum(row.final_posterior_mean for row in rows) / count,
        mean_final_ap_differential=sum(row.final_ap_differential for row in rows) / count,
        mean_post_recovery_polarity_contrast=sum(row.post_recovery_polarity_contrast for row in rows) / count,
        mean_final_spatial_variance=sum(row.final_spatial_variance for row in rows) / count,
        mean_final_dh_propensity=sum(row.final_dh_propensity for row in rows) / count,
        lesioned_spanning_probability=sum(1.0 for row in rows if row.lesioned_spanning_cluster) / count,
        failed_recovery_fraction=len(failures) / count,
        wt_fraction=len(wt_rows) / count,
        cryptic_fraction=len(cryptic_rows) / count,
        dh_fraction=len(dh_rows) / count,
    )


def run_sink_recovery_sweep(
    lattice_sizes: tuple[int, ...] = (16,),
    dilution_grid: tuple[float, ...] = (0.0, 0.3, 0.5, 0.6),
    replicates: int = 2,
    lesion_steps: int = 40,
    recovery_steps: int = 120,
    lesion_patch_width: int = 2,
    lesion_current: float = 0.0,
    base_conductance: float = 0.35,
    polarity_field_amplitude: float = 0.15,
    polarity_field_tau_h: float = 2_000.0,
    well_linear: float = 1.0,
    well_cubic: float = 1.0,
    suppress_field_during_recovery: bool = False,
) -> dict[str, object]:
    all_runs: list[RecoveryRunSummary] = []
    all_rows: list[RecoverySweepRow] = []
    notes = [
        "Recovery protocol: temporary sink lesion, then release and measure post-lesion polarity contrast.",
        "Failure criterion: recovery fidelity < 0.5 relative to the pre-lesion polarity contrast.",
        f"Localized lesion-phase current amplitude: {lesion_current}.",
        f"Base conductance: {base_conductance}.",
        f"Polarity-field amplitude h_0: {polarity_field_amplitude}.",
        f"Polarity-field timescale tau_h: {polarity_field_tau_h}.",
        f"Well linear coefficient: {well_linear}.",
        f"Well cubic coefficient: {well_cubic}.",
        f"Polarity field suppressed during recovery: {suppress_field_during_recovery}.",
        "Recorded cryptic reference point: edge-sever, L=16, h_0=0.02, tau_h=100, base_conductance=0.2, well_linear=0.4 gave mean_final_dh_propensity ~ 0.263-0.265 with cryptic_fraction = 1.0 across tested dilutions.",
        "Final morphology is reported as a coarse-grained WT/Cryptic/DH surrogate based on posterior depolarization propensity.",
    ]
    for lattice_size in lattice_sizes:
        lesion_nodes = default_sink_patch(lattice_size, width=lesion_patch_width)
        for dilution_fraction in dilution_grid:
            summaries: list[RecoveryRunSummary] = []
            for replicate in range(replicates):
                config = build_sweep_config(
                    lattice_size=lattice_size,
                    dilution_fraction=dilution_fraction,
                    replicate=replicate,
                    base_conductance=base_conductance,
                    polarity_field_amplitude=polarity_field_amplitude,
                    polarity_field_tau_h=polarity_field_tau_h,
                    well_linear=well_linear,
                    well_cubic=well_cubic,
                )
                summary = run_sink_recovery_protocol(
                    config=config,
                    lesion_nodes=lesion_nodes,
                    lesion_steps=lesion_steps,
                    recovery_steps=recovery_steps,
                    lesion_current=lesion_current,
                    suppress_field_during_recovery=suppress_field_during_recovery,
                )
                summaries.append(summary)
                all_runs.append(summary)
            all_rows.append(aggregate_recovery_rows(summaries))
    return {
        "metadata": {
            "lesion_kind": "sink",
            "lattice_sizes": list(lattice_sizes),
            "dilution_grid": list(dilution_grid),
            "replicates": replicates,
            "lesion_steps": lesion_steps,
            "recovery_steps": recovery_steps,
            "lesion_patch_width": lesion_patch_width,
            "lesion_current": lesion_current,
            "base_conductance": base_conductance,
            "polarity_field_amplitude": polarity_field_amplitude,
            "polarity_field_tau_h": polarity_field_tau_h,
            "well_linear": well_linear,
            "well_cubic": well_cubic,
            "suppress_field_during_recovery": suppress_field_during_recovery,
            "lesion_nodes": list(default_sink_patch(lattice_sizes[0], width=lesion_patch_width)) if lattice_sizes else [],
            "notes": notes,
        },
        "rows": [asdict(row) for row in all_rows],
        "runs": [asdict(run) for run in all_runs],
    }


def run_edge_sever_recovery_protocol(
    config: SimulationConfig,
    lesion_edges: tuple[tuple[int, int], ...],
    lesion_steps: int = 40,
    recovery_steps: int = 120,
    lesion_current: float = 0.0,
    suppress_field_during_recovery: bool = False,
) -> RecoveryRunSummary:
    rng = random.Random(config.disorder.seed)
    voltages, polarity_field, polarity_target, conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
    site_offsets, edge_scales = apply_disorder(config, voltages, conductances, rng)
    conductances, neighbors = apply_quenched_edge_removals(conductances, neighbors, edge_scales)
    occupied_edges, active_for_span = occupied_edges_from_dilution(config)

    severed_edges = {
        (min(i, j), max(i, j))
        for i, j in lesion_edges
        if (min(i, j), max(i, j)) in conductances
    }
    lesioned_occupied_edges, _ = remove_edges_from_graph(occupied_edges, neighbors, severed_edges)
    saved_edges = {edge: conductances[edge] for edge in severed_edges}
    lesioned_conductances, lesioned_neighbors = remove_edges_from_graph(conductances, neighbors, severed_edges)
    lesion_nodes = tuple(sorted({node for edge in lesion_edges for node in edge}))

    pre_lesion = polarity_contrast(voltages, lattice_size=config.lattice_size, axis=config.polarity_axis)
    lesion_site_offsets = add_localized_current(site_offsets, lesion_nodes, lesion_current)
    lesion_polarity_target = suppress_local_polarity_target(polarity_target, lesion_nodes)
    recovery_polarity_target = lesion_polarity_target if suppress_field_during_recovery else polarity_target

    for _ in range(lesion_steps):
        voltages, polarity_field, lesioned_conductances = step(
            config=config,
            voltages=voltages,
            polarity_field=polarity_field,
            polarity_target=lesion_polarity_target,
            conductances=lesioned_conductances,
            active_nodes=active_nodes,
            sink_nodes=set(),
            neighbors=lesioned_neighbors,
            site_offsets=lesion_site_offsets,
            edge_scales=edge_scales,
            rng=rng,
        )

    restored_conductances = dict(lesioned_conductances)
    restored_conductances.update(saved_edges)
    for _ in range(recovery_steps):
        voltages, polarity_field, restored_conductances = step(
            config=config,
            voltages=voltages,
            polarity_field=polarity_field,
            polarity_target=recovery_polarity_target,
            conductances=restored_conductances,
            active_nodes=active_nodes,
            sink_nodes=set(),
            neighbors=neighbors,
            site_offsets=site_offsets,
            edge_scales=edge_scales,
            rng=rng,
        )

    post_recovery = polarity_contrast(voltages, lattice_size=config.lattice_size, axis=config.polarity_axis)
    anterior_mean, posterior_mean, ap_differential, _ap_variance = ap_voltage_variance(
        voltages,
        lattice_size=config.lattice_size,
        axis=config.polarity_axis,
    )
    baseline_scale = max(abs(pre_lesion), 1e-9)
    recovery_fidelity = abs(post_recovery) / baseline_scale
    morphology = classify_macrostate(voltages, config)
    return RecoveryRunSummary(
        lesion_kind="edge_sever",
        lattice_size=config.lattice_size,
        dilution_fraction=config.disorder.strength,
        replicate=int(str(config.disorder.seed)[-1]) if str(config.disorder.seed)[-1].isdigit() else 0,
        seed=config.disorder.seed,
        lesion_steps=lesion_steps,
        recovery_steps=recovery_steps,
        lesion_size=len(lesion_edges),
        pre_lesion_polarity_contrast=pre_lesion,
        final_anterior_mean=anterior_mean,
        final_posterior_mean=posterior_mean,
        final_ap_differential=ap_differential,
        post_recovery_polarity_contrast=post_recovery,
        recovery_fidelity=recovery_fidelity,
        final_spatial_variance=spatial_variance(voltages),
        final_macrostate=morphology.macrostate,
        final_dh_propensity=morphology.features.dh_propensity,
        bond_occupation=bond_occupation_fraction(config),
        lesioned_spanning_cluster=has_spanning_cluster(
            config.lattice_size,
            lesioned_occupied_edges,
            active_for_span,
        ),
    )


def run_edge_sever_recovery_sweep(
    lattice_sizes: tuple[int, ...] = (16,),
    dilution_grid: tuple[float, ...] = (0.0, 0.3, 0.5, 0.6),
    replicates: int = 2,
    lesion_steps: int = 40,
    recovery_steps: int = 120,
    lesion_current: float = 0.0,
    base_conductance: float = 0.35,
    polarity_field_amplitude: float = 0.15,
    polarity_field_tau_h: float = 2_000.0,
    well_linear: float = 1.0,
    well_cubic: float = 1.0,
    suppress_field_during_recovery: bool = False,
) -> dict[str, object]:
    all_runs: list[RecoveryRunSummary] = []
    all_rows: list[RecoverySweepRow] = []
    notes = [
        "Recovery protocol: temporary midline edge sever, then graph restoration and post-lesion polarity-contrast measurement.",
        "Failure criterion: recovery fidelity < 0.5 relative to the pre-lesion polarity contrast.",
        f"Localized lesion-phase current amplitude: {lesion_current}.",
        f"Base conductance: {base_conductance}.",
        f"Polarity-field amplitude h_0: {polarity_field_amplitude}.",
        f"Polarity-field timescale tau_h: {polarity_field_tau_h}.",
        f"Well linear coefficient: {well_linear}.",
        f"Well cubic coefficient: {well_cubic}.",
        f"Polarity field suppressed during recovery: {suppress_field_during_recovery}.",
        "Recorded cryptic reference point: edge-sever, L=16, h_0=0.02, tau_h=100, base_conductance=0.2, well_linear=0.4 gave mean_final_dh_propensity ~ 0.263-0.265 with cryptic_fraction = 1.0 across tested dilutions.",
        "Lesioned spanning probability is evaluated on the bond-diluted graph after temporary edge severing, not on the intact diluted graph.",
        "Final morphology is reported as a coarse-grained WT/Cryptic/DH surrogate based on posterior depolarization propensity.",
    ]
    lesion_edges_by_size = {
        lattice_size: default_midline_edge_cut(lattice_size)
        for lattice_size in lattice_sizes
    }
    for lattice_size in lattice_sizes:
        lesion_edges = lesion_edges_by_size[lattice_size]
        for dilution_fraction in dilution_grid:
            summaries: list[RecoveryRunSummary] = []
            for replicate in range(replicates):
                config = build_sweep_config(
                    lattice_size=lattice_size,
                    dilution_fraction=dilution_fraction,
                    replicate=replicate,
                    base_conductance=base_conductance,
                    polarity_field_amplitude=polarity_field_amplitude,
                    polarity_field_tau_h=polarity_field_tau_h,
                    well_linear=well_linear,
                    well_cubic=well_cubic,
                )
                summary = run_edge_sever_recovery_protocol(
                    config=config,
                    lesion_edges=lesion_edges,
                    lesion_steps=lesion_steps,
                    recovery_steps=recovery_steps,
                    lesion_current=lesion_current,
                    suppress_field_during_recovery=suppress_field_during_recovery,
                )
                summaries.append(summary)
                all_runs.append(summary)
            all_rows.append(aggregate_recovery_rows(summaries))
    return {
        "metadata": {
            "lesion_kind": "edge_sever",
            "lattice_sizes": list(lattice_sizes),
            "dilution_grid": list(dilution_grid),
            "replicates": replicates,
            "lesion_steps": lesion_steps,
            "recovery_steps": recovery_steps,
            "lesion_current": lesion_current,
            "base_conductance": base_conductance,
            "polarity_field_amplitude": polarity_field_amplitude,
            "polarity_field_tau_h": polarity_field_tau_h,
            "well_linear": well_linear,
            "well_cubic": well_cubic,
            "suppress_field_during_recovery": suppress_field_during_recovery,
            "lesion_edges": {
                str(size): [list(edge) for edge in lesion_edges]
                for size, lesion_edges in lesion_edges_by_size.items()
            },
            "notes": notes,
        },
        "rows": [asdict(row) for row in all_rows],
        "runs": [asdict(run) for run in all_runs],
    }
