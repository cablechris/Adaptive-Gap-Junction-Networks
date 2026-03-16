from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import math
import random

from .model import DisorderKind, LesionKind, SimulationConfig


@dataclass(slots=True)
class SimulationState:
    voltages: list[float]
    conductances: dict[tuple[int, int], float]
    active_nodes: set[int]
    sink_nodes: set[int]
    neighbors: dict[int, tuple[int, ...]]


def _edge_key(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def lattice_index(row: int, col: int, size: int) -> int:
    return row * size + col


def build_square_neighbors(size: int) -> dict[int, tuple[int, ...]]:
    neighbors: dict[int, tuple[int, ...]] = {}
    for row in range(size):
        for col in range(size):
            site = lattice_index(row, col, size)
            local: list[int] = []
            if row > 0:
                local.append(lattice_index(row - 1, col, size))
            if row + 1 < size:
                local.append(lattice_index(row + 1, col, size))
            if col > 0:
                local.append(lattice_index(row, col - 1, size))
            if col + 1 < size:
                local.append(lattice_index(row, col + 1, size))
            neighbors[site] = tuple(local)
    return neighbors


def initial_state(config: SimulationConfig) -> SimulationState:
    node_count = config.lattice_size * config.lattice_size
    neighbors = build_square_neighbors(config.lattice_size)
    active_nodes = set(range(node_count))
    sink_nodes: set[int] = set()

    if config.lesion.kind == LesionKind.SINK:
        sink_nodes = set(config.lesion.nodes)
    elif config.lesion.kind == LesionKind.TOPOLOGICAL_CUT:
        active_nodes.difference_update(config.lesion.nodes)

    severed = {_edge_key(i, j) for i, j in config.lesion.edges}
    conductances: dict[tuple[int, int], float] = {}
    updated_neighbors: dict[int, tuple[int, ...]] = {}

    for site, raw_neighbors in neighbors.items():
        filtered: list[int] = []
        for other in raw_neighbors:
            edge = _edge_key(site, other)
            removed_by_cut = (
                config.lesion.kind == LesionKind.TOPOLOGICAL_CUT
                and (site not in active_nodes or other not in active_nodes)
            )
            severed_edge = config.lesion.kind == LesionKind.EDGE_SEVER and edge in severed
            if removed_by_cut or severed_edge:
                continue
            filtered.append(other)
            if edge not in conductances:
                conductances[edge] = config.base_conductance
        updated_neighbors[site] = tuple(filtered)

    voltages = [0.0 for _ in range(node_count)]
    return SimulationState(
        voltages=voltages,
        conductances=conductances,
        active_nodes=active_nodes,
        sink_nodes=sink_nodes,
        neighbors=updated_neighbors,
    )


def double_well_force(v: float, linear: float, cubic: float) -> float:
    return linear * v - cubic * (v ** 3)


def plasticity_drive(delta_v: float, adaptation_strength: float, mismatch_target: float, mismatch_slope: float) -> float:
    mismatch = abs(delta_v) - mismatch_target
    return -adaptation_strength * mismatch_slope * mismatch


def apply_disorder(config: SimulationConfig, state: SimulationState, rng: random.Random) -> tuple[list[float], dict[tuple[int, int], float]]:
    site_offsets = [0.0 for _ in state.voltages]
    edge_scales = {edge: 1.0 for edge in state.conductances}
    spec = config.disorder
    if spec.kind == DisorderKind.NONE or spec.strength == 0.0:
        return site_offsets, edge_scales
    for site in range(len(site_offsets)):
        if spec.kind in (DisorderKind.SITE, DisorderKind.RANDOM_FIELD):
            site_offsets[site] = rng.gauss(0.0, spec.strength)
    for edge in list(edge_scales):
        if spec.kind in (DisorderKind.BOND, DisorderKind.RANDOM_BOND):
            edge_scales[edge] = max(0.0, 1.0 + rng.gauss(0.0, spec.strength))
        if spec.kind == DisorderKind.DILUTION and rng.random() < spec.strength:
            edge_scales[edge] = 0.0
    return site_offsets, edge_scales


def iter_edges(neighbors: dict[int, tuple[int, ...]]) -> Iterable[tuple[int, int]]:
    seen: set[tuple[int, int]] = set()
    for site, adjacent in neighbors.items():
        for other in adjacent:
            edge = _edge_key(site, other)
            if edge in seen:
                continue
            seen.add(edge)
            yield edge


def step(config: SimulationConfig, state: SimulationState, site_offsets: list[float], edge_scales: dict[tuple[int, int], float], rng: random.Random) -> None:
    next_voltages = list(state.voltages)
    dt = config.dt
    sqrt_dt = math.sqrt(dt)

    for site, voltage in enumerate(state.voltages):
        if site not in state.active_nodes:
            next_voltages[site] = 0.0
            continue
        if site in state.sink_nodes:
            next_voltages[site] = config.lesion.clamp_voltage
            continue

        coupling = 0.0
        for other in state.neighbors[site]:
            edge = _edge_key(site, other)
            g_ij = state.conductances.get(edge, 0.0) * edge_scales.get(edge, 1.0)
            coupling += g_ij * (state.voltages[other] - voltage)

        drift = (
            double_well_force(voltage, config.well_linear, config.well_cubic)
            + coupling
            + config.stimulation_amplitude
            - config.injury_amplitude
            + site_offsets[site]
        ) / config.tau_v
        noise = config.noise_amplitude * rng.gauss(0.0, 1.0) * sqrt_dt
        next_voltages[site] = voltage + dt * drift + noise

    for i, j in iter_edges(state.neighbors):
        delta_v = next_voltages[i] - next_voltages[j]
        edge = _edge_key(i, j)
        drive = plasticity_drive(
            delta_v=delta_v,
            adaptation_strength=config.plasticity.adaptation_strength,
            mismatch_target=config.plasticity.mismatch_target,
            mismatch_slope=config.plasticity.mismatch_slope,
        )
        g_ij = state.conductances[edge]
        g_dot = (drive - config.plasticity.decay_rate * g_ij) / config.tau_g
        state.conductances[edge] = max(0.0, g_ij + dt * g_dot)

    state.voltages[:] = next_voltages


def run_simulation(config: SimulationConfig) -> list[SimulationState]:
    rng = random.Random(config.disorder.seed)
    state = initial_state(config)
    site_offsets, edge_scales = apply_disorder(config, state, rng)
    history: list[SimulationState] = []
    for _ in range(config.steps):
        step(config, state, site_offsets, edge_scales, rng)
        history.append(
            SimulationState(
                voltages=list(state.voltages),
                conductances=dict(state.conductances),
                active_nodes=set(state.active_nodes),
                sink_nodes=set(state.sink_nodes),
                neighbors=dict(state.neighbors),
            )
        )
    return history
