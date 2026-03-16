from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random

from .disorder import apply_disorder, apply_quenched_edge_removals
from .initialization import initial_state
from .model import DisorderKind, DisorderSpec, SimulationConfig
from .observables import consensus_fraction, final_abs_mean_voltage
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
    consensus_fraction: float
    spanning_cluster: bool


@dataclass(slots=True)
class SweepRow:
    lattice_size: int
    dilution_fraction: float
    mean_bond_occupation: float
    mean_abs_voltage: float
    mean_consensus_fraction: float
    spanning_probability: float
    disrupted_fraction: float


def occupied_edges_from_dilution(config: SimulationConfig) -> tuple[dict[tuple[int, int], float], set[int]]:
    rng = random.Random(config.disorder.seed)
    voltages, conductances, active_nodes, _sink_nodes, neighbors = initial_state(config)
    _site_offsets, edge_scales = apply_disorder(config, voltages, conductances, rng)
    updated_conductances, _updated_neighbors = apply_quenched_edge_removals(conductances, neighbors, edge_scales)
    occupied_edges = {edge: 1.0 for edge in updated_conductances}
    return occupied_edges, active_nodes


def bond_occupation_fraction(config: SimulationConfig) -> float:
    occupied_edges, _active_nodes = occupied_edges_from_dilution(config)
    _voltages, conductances, _active, _sink, _neighbors = initial_state(config)
    total_edges = len(conductances)
    if total_edges == 0:
        return 0.0
    return len(occupied_edges) / total_edges


def build_sweep_config(lattice_size: int, dilution_fraction: float, replicate: int) -> SimulationConfig:
    seed = lattice_size * 10_000 + int(round(dilution_fraction * 1_000)) * 10 + replicate
    return SimulationConfig(
        lattice_size=lattice_size,
        tau_v=1.0,
        tau_g=100.0,
        base_conductance=0.35,
        steps=300,
        noise_amplitude=0.02,
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
        consensus_fraction=consensus_fraction(final_state.voltages),
        spanning_cluster=has_spanning_cluster(config.lattice_size, occupied_edges, active_nodes),
    )


def aggregate_rows(rows: list[RunSummary], undiluted_reference: float) -> SweepRow:
    count = len(rows)
    disrupted = [row for row in rows if row.abs_mean_voltage <= 0.5 * undiluted_reference]
    return SweepRow(
        lattice_size=rows[0].lattice_size,
        dilution_fraction=rows[0].dilution_fraction,
        mean_bond_occupation=sum(row.bond_occupation for row in rows) / count,
        mean_abs_voltage=sum(row.abs_mean_voltage for row in rows) / count,
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
        "Operational polarity-disruption metric: abs(mean voltage) falls below 50% of the undiluted mean for the same lattice size.",
        "This sweep still uses a voltage-based surrogate rather than an explicit WT/Cryptic/DH classifier.",
        "Initial condition is a stable anterior/posterior voltage pattern rather than the unstable V=0 barrier state.",
        "Bond-dilution comparison target for octanol-style blockade: 2D square-lattice bond percolation p_c ~ 0.5.",
    ]

    for lattice_size in lattice_sizes:
        baseline_config = build_sweep_config(lattice_size=lattice_size, dilution_fraction=0.0, replicate=0)
        baseline_summary = summarize_run(baseline_config, replicate=0)
        undiluted_reference = max(baseline_summary.abs_mean_voltage, 1e-9)
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
