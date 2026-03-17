from __future__ import annotations

from .morphology import classify_macrostate
from .model import DisorderKind, DisorderSpec, LesionKind, LesionSpec, SimulationConfig
from .simulator import run_simulation


def build_baseline_config() -> SimulationConfig:
    return SimulationConfig(
        lattice_size=16,
        tau_v=1.0,
        tau_g=100.0,
        steps=250,
        disorder=DisorderSpec(
            kind=DisorderKind.DILUTION,
            distribution="bernoulli bond dilution with removal fraction f_b",
            strength=0.1,
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
    macrostate = classify_macrostate(final_state.voltages, config)
    print(f"steps={config.steps}")
    print(f"epsilon={config.epsilon:.4f}")
    print(f"active_nodes={len(final_state.active_nodes)}")
    print(f"sink_nodes={len(final_state.sink_nodes)}")
    print(f"mean_voltage={mean_voltage:.6f}")
    print(f"macrostate={macrostate.macrostate}")
    print(f"dh_propensity={macrostate.features.dh_propensity:.3f}")


if __name__ == "__main__":
    main()
