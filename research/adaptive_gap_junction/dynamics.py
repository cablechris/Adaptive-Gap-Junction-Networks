from __future__ import annotations

from collections.abc import Iterable
import math
import random

from .geometry import edge_key
from .model import SimulationConfig


def double_well_force(v: float, linear: float, cubic: float) -> float:
    return linear * v - cubic * (v ** 3)


def plasticity_drive(delta_v: float, adaptation_strength: float, mismatch_target: float, mismatch_slope: float) -> float:
    mismatch = abs(delta_v) - mismatch_target
    return adaptation_strength * mismatch_slope * mismatch


def iter_edges(neighbors: dict[int, tuple[int, ...]]) -> Iterable[tuple[int, int]]:
    seen: set[tuple[int, int]] = set()
    for site, adjacent in neighbors.items():
        for other in adjacent:
            edge = edge_key(site, other)
            if edge in seen:
                continue
            seen.add(edge)
            yield edge


def step(
    config: SimulationConfig,
    voltages: list[float],
    conductances: dict[tuple[int, int], float],
    active_nodes: set[int],
    sink_nodes: set[int],
    neighbors: dict[int, tuple[int, ...]],
    site_offsets: list[float],
    edge_scales: dict[tuple[int, int], float],
    rng: random.Random,
) -> tuple[list[float], dict[tuple[int, int], float]]:
    next_voltages = list(voltages)
    next_conductances = dict(conductances)
    dt = config.dt
    sqrt_dt = math.sqrt(dt)

    for site, voltage in enumerate(voltages):
        if site not in active_nodes:
            next_voltages[site] = 0.0
            continue
        if site in sink_nodes:
            next_voltages[site] = config.lesion.clamp_voltage
            continue

        coupling = 0.0
        for other in neighbors[site]:
            edge = edge_key(site, other)
            g_ij = next_conductances.get(edge, 0.0) * edge_scales.get(edge, 1.0)
            coupling += g_ij * (voltages[other] - voltage)

        drift = (
            double_well_force(voltage, config.well_linear, config.well_cubic)
            + coupling
            + config.stimulation_amplitude
            - config.injury_amplitude
            + site_offsets[site]
        ) / config.tau_v
        noise = config.noise_amplitude * rng.gauss(0.0, 1.0) * sqrt_dt
        next_voltages[site] = voltage + dt * drift + noise

    for i, j in iter_edges(neighbors):
        delta_v = next_voltages[i] - next_voltages[j]
        edge = edge_key(i, j)
        drive = plasticity_drive(
            delta_v=delta_v,
            adaptation_strength=config.plasticity.adaptation_strength,
            mismatch_target=config.plasticity.mismatch_target,
            mismatch_slope=config.plasticity.mismatch_slope,
        )
        g_ij = next_conductances[edge]
        g_dot = (drive - config.plasticity.decay_rate * g_ij) / config.tau_g
        next_conductances[edge] = max(0.0, g_ij + dt * g_dot)

    return next_voltages, next_conductances
