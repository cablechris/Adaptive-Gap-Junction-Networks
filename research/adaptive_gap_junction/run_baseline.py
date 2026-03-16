from __future__ import annotations

from .model import DisorderKind, DisorderSpec, LesionKind, LesionSpec, SimulationConfig
from .simulator import run_simulation


def build_baseline_config() -> SimulationConfig:
    return SimulationConfig(
        lattice_size=16,
        steps=250,
        disorder=DisorderSpec(
            kind=DisorderKind.RANDOM_FIELD,
            distribution="gaussian(mean=0,std=W)",
            strength=0.03,
            seed=7,
        ),
        lesion=LesionSpec(
            kind=LesionKind.SINK,
            nodes=(120, 121, 136, 137),
            clamp_voltage=-1.0,
        ),
    )


def main() -> None:
    config = build_baseline_config()
    history = run_simulation(config)
    final_state = history[-1]
    mean_voltage = sum(final_state.voltages) / len(final_state.voltages)
    print(f"steps={config.steps}")
    print(f"epsilon={config.epsilon:.4f}")
    print(f"active_nodes={len(final_state.active_nodes)}")
    print(f"sink_nodes={len(final_state.sink_nodes)}")
    print(f"mean_voltage={mean_voltage:.6f}")


if __name__ == "__main__":
    main()
