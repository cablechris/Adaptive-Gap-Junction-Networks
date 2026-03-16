from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class PotentialKind(StrEnum):
    DOUBLE_WELL = "double_well"


class DisorderKind(StrEnum):
    NONE = "none"
    SITE = "site"
    BOND = "bond"
    RANDOM_FIELD = "random_field"
    RANDOM_BOND = "random_bond"
    DILUTION = "dilution"


class LesionKind(StrEnum):
    NONE = "none"
    SINK = "sink"
    EDGE_SEVER = "edge_sever"
    TOPOLOGICAL_CUT = "topological_cut"


@dataclass(slots=True)
class DisorderSpec:
    kind: DisorderKind = DisorderKind.NONE
    distribution: str = "none"
    strength: float = 0.0
    seed: int = 0


@dataclass(slots=True)
class LesionSpec:
    kind: LesionKind = LesionKind.NONE
    nodes: tuple[int, ...] = ()
    edges: tuple[tuple[int, int], ...] = ()
    clamp_voltage: float = 0.0


@dataclass(slots=True)
class PlasticitySpec:
    adaptation_strength: float = 0.1
    mismatch_target: float = 0.0
    mismatch_slope: float = 1.0
    decay_rate: float = 0.05
    field_scale: float = 0.0


@dataclass(slots=True)
class SimulationConfig:
    lattice_size: int = 16
    tau_v: float = 1.0
    tau_g: float = 20.0
    potential_kind: PotentialKind = PotentialKind.DOUBLE_WELL
    well_linear: float = 1.0
    well_cubic: float = 1.0
    base_conductance: float = 0.35
    dt: float = 0.02
    steps: int = 200
    noise_amplitude: float = 0.02
    stimulation_amplitude: float = 0.0
    injury_amplitude: float = 0.0
    disorder: DisorderSpec = field(default_factory=DisorderSpec)
    lesion: LesionSpec = field(default_factory=LesionSpec)
    plasticity: PlasticitySpec = field(default_factory=PlasticitySpec)

    @property
    def epsilon(self) -> float:
        return self.tau_v / self.tau_g
