from __future__ import annotations

import random
import unittest

from .model import DisorderKind, DisorderSpec, LesionKind, LesionSpec, SimulationConfig
from .run_baseline import build_baseline_config
from .simulator import apply_disorder, initial_state, run_simulation


class AdaptiveGapJunctionTests(unittest.TestCase):
    def test_baseline_config_uses_empirical_epsilon_scale(self) -> None:
        config = build_baseline_config()
        self.assertGreaterEqual(config.epsilon, 1e-3)
        self.assertLessEqual(config.epsilon, 1e-2)

    def test_sink_lesion_is_not_a_topological_cut(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            lesion=LesionSpec(kind=LesionKind.SINK, nodes=(5,), clamp_voltage=-1.0),
        )
        state = initial_state(config)
        self.assertIn(5, state.active_nodes)
        self.assertIn(5, state.sink_nodes)
        self.assertTrue(state.neighbors[5])

    def test_topological_cut_removes_node_from_active_graph(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            lesion=LesionSpec(kind=LesionKind.TOPOLOGICAL_CUT, nodes=(5,)),
        )
        state = initial_state(config)
        self.assertNotIn(5, state.active_nodes)
        for adjacent in state.neighbors.values():
            self.assertNotIn(5, adjacent)

    def test_bond_dilution_zeroes_edges_without_removing_nodes(self) -> None:
        config = SimulationConfig(
            lattice_size=4,
            disorder=DisorderSpec(
                kind=DisorderKind.DILUTION,
                distribution="bernoulli bond dilution",
                strength=1.0,
                seed=3,
            ),
        )
        state = initial_state(config)
        active_before = set(state.active_nodes)
        _site_offsets, edge_scales = apply_disorder(config, state, random.Random(config.disorder.seed))
        self.assertEqual(active_before, state.active_nodes)
        self.assertTrue(edge_scales)
        self.assertTrue(all(scale == 0.0 for scale in edge_scales.values()))

    def test_baseline_run_returns_finite_voltage_data(self) -> None:
        history = run_simulation(build_baseline_config())
        self.assertTrue(history)
        final_state = history[-1]
        self.assertEqual(len(final_state.voltages), 16 * 16)
        self.assertTrue(all(isinstance(voltage, float) for voltage in final_state.voltages))


if __name__ == "__main__":
    unittest.main()
